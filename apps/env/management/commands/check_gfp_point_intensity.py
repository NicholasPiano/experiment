'''


'''

#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

#local
from apps.cell.models import Cell
from apps.env.models import Experiment, Series

#util
import os
import re
import numpy as np
from scipy.misc import imsave
from scipy.ndimage.morphology import binary_dilation as dilate
import matplotlib.pyplot as plt

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    base_input_path = '/Volumes/transport/data/cp/centre-ij/tracks'
    base_output_path = '/Volumes/transport/data/cp/centre-ij/check-gfp-point'

    # make directory
    if not os.path.exists(base_output_path):
      os.mkdir(base_output_path)

    for e in Experiment.objects.all():

      # make directory
      if not os.path.exists(os.path.join(base_output_path, e.name)):
        os.mkdir(os.path.join(base_output_path, e.name))

      for s in e.series.all():

        # make directory
        if not os.path.exists(os.path.join(base_output_path, e.name, str(s.index))):
          os.mkdir(os.path.join(base_output_path, e.name, str(s.index)))

        # get image
        gfp = s.experiment.images.filter(series=s, channel=0)
        series_image = gfp.get(focus=0, timestep__index=0)
        series_image.load()

        # load tracks file
        cell_instances = []
        with open(os.path.join(base_input_path, e.name, str(s.index), 'tracks.xls')) as tracks_file:
          for line in tracks_file.readlines():
            if int('0' + line.split('\t')[0])>0:
              cell_instances.append(CellInstance(e.name, str(s.index), ' '.join(line.rstrip().split('\t'))))

        # loop through timesteps
        all_timestep_indices = [t.index for t in s.timesteps.order_by('index')]
        for t in s.timesteps.order_by('index'):
          print('%s %d %d'%(e.name, s.index, t.index))

          # cell instances at timestep
          ci = filter(lambda c: c.frame==all_timestep_indices.index(t.index)+1, cell_instances)

          # load images first
          gfp_t = gfp.filter(timestep=t)
          data = []
          dp_list = range(10,20)
          for g in gfp_t.order_by('focus'):
            g.load()

            for cell_instance in ci:
              # for each cell instance, mask the gfp stack at 0, 10, 20 pixels and find mean of mask at each z.
              row, column = cell_instance.row, cell_instance.column

              # plot mean gfp inside mask
              for dp in dp_list:
                line = [] # stores means from each level
                # make mask
                mask_gfp = g.array[row-dp:row+dp+1, column-dp:column+dp+1]

                # store
                data.append({'data':mask_gfp.mean(), 'c':cell_instance.id, 'dp':dp, 'f':g.focus})

          # plot data
          for cell_instance in filter(lambda x: x.id==1, ci):
            d_c = filter(lambda x: x['c']==cell_instance.id, data)
            for dp in dp_list:
              d_dp = filter(lambda x: x['dp']==dp, d_c)
              line = []
              for d in sorted(d_dp, key=lambda x: x['f']):
                line.append(d['data'])
              plt.plot(line, label='%d: %d'%(dp, np.argmax(line)))

            # save
            plt.legend()
            plot_path = os.path.join(base_output_path, e.name, str(s.index), 'point_c%d_t%s.tif'%(cell_instance.id, ('00' if int(t.index)<10 else ('0' if int(t.index)<100 else '')) + str(t.index)))
            plt.savefig(plot_path)
            plt.clf()

class CellInstance():
  def __init__(self, experiment, series, line):
    m = re.match(r'[0-9]+ (?P<id>[0-9]+) (?P<frame>[0-9]+) (?P<x>[0-9]+) (?P<y>[0-9]+) [-+]?[0-9]*\.?[0-9]+ [-+]?[0-9]*\.?[0-9]+ [0-9]+', line)
    self.experiment = experiment
    self.series = series
    self.id = int(m.group('id'))
    self.frame = int(m.group('frame'))
    self.row = int(m.group('y'))
    self.column = int(m.group('x'))
    self.z = None #set from gfp -> argmax from focus

  def __str__(self):
    return '[%s %s %d %d %d]' % (self.experiment, self.series, self.id, self.row, self.column)
