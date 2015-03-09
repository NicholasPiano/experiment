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
from skimage import filter as ft
from skimage import exposure

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    base_input_path = '/Volumes/transport/data/cp/centre-ij/tracks'
    base_output_path = '/Volumes/transport/data/cp/centre-ij/pmod-z'

    # make directory
    if not os.path.exists(base_output_path):
      os.mkdir(base_output_path)

    for e in Experiment.objects.filter(name='260714'):

      # make directory
      if not os.path.exists(os.path.join(base_output_path, e.name)):
        os.mkdir(os.path.join(base_output_path, e.name))

      for s in e.series.all():

        # make directory
        if not os.path.exists(os.path.join(base_output_path, e.name, str(s.index))):
          os.mkdir(os.path.join(base_output_path, e.name, str(s.index)))

        # get image
        bf = s.experiment.images.filter(series=s, channel=1)
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
        for t in s.timesteps.order_by('index').filter(index=113):
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

          # z positions of cells
          for cell_instance in ci:
            d_c = filter(lambda x: x['c']==cell_instance.id, data)
            argmax = []
            for dp in dp_list:
              d_dp = filter(lambda x: x['dp']==dp, d_c)
              line = []
              for d in sorted(d_dp, key=lambda x: x['f']):
                line.append(d['data'])
              argmax.append(np.argmax(line))
            cell_instance.z = int(np.mean(argmax))

          # divide z stack into chunks and group cells by chunk
          for c in range(int((gfp_t.count()+5)/5.0)):
            for cell_instance in ci:
              if cell_instance.c is None and cell_instance.z >= c*5 and cell_instance.z < (c+1)*5:
                cell_instance.c = c

          print([c.c for c in ci])

          if len(ci)!=0:
            for cl in np.unique([c.c for c in ci]): # for each unique level class
              # take 5 layers of bf and 10 layers of gfp
              # take bf max
              # take gfp sum
              # multiply

              bf_min, bf_max = cl*5, (cl+1)*5
              gfp_min, gfp_max = (0 if cl-2<0 else cl-2)*5, (cl+2)*5 if (cl+2)*5<gfp_t.count() else gfp_t.count()

              # make images
              bf_stack = bf.filter(timestep=t, focus__gte=bf_min, focus__lte=bf_max)
              gfp_stack = gfp_t.filter(focus__gte=gfp_min, focus__lte=gfp_max)

              bf_max_proj = np.zeros(series_image.array.shape)
              for b in bf_stack:
                b.load()
                bf_max_proj[bf_max_proj < b.array] = b.array[bf_max_proj < b.array]

              gfp_sum_proj = np.zeros(series_image.array.shape)
              for g in gfp_stack:
                g.load()
                gfp_sum_proj += g.array

              gfp_threshold = exposure.equalize_hist(gfp_sum_proj)
              gfp_threshold[gfp_sum_proj<gfp_sum_proj.mean()] = 0

              gfp_smooth = ft.gaussian_filter(gfp_threshold, sigma=5)

              # save output
              output_image = gfp_smooth * bf_max_proj
              sec_image_path = os.path.join(base_output_path, e.name, str(s.index), 'secondary_t%s_cl%d.tif'%((len(str(s.timesteps.count()))-len(str(t.index)))*'0' + str(t.index), cl))

              imsave(sec_image_path, output_image)

              # primary objects
              black_field = np.zeros(series_image.array.shape)

              for cell_instance in ci:
                # draw circle
                xx, yy = np.mgrid[:black_field.shape[0], :black_field.shape[1]]
                circle = (xx - cell_instance.row) ** 2 + (yy - cell_instance.column) ** 2 # distance from c
                black_field[circle<15] = 255 # radius of 10 px

              pri_image_path = os.path.join(base_output_path, e.name, str(s.index), 'primary_t%s_cl%d.tif'%((len(str(s.timesteps.count()))-len(str(t.index)))*'0' + str(t.index), cl))

              imsave(pri_image_path, black_field)

class CellInstance():
  def __init__(self, experiment, series, line):
    m = re.match(r'[0-9]+ (?P<id>[0-9]+) (?P<frame>[0-9]+) (?P<x>[0-9]+) (?P<y>[0-9]+) [-+]?[0-9]*\.?[0-9]+ [-+]?[0-9]*\.?[0-9]+ [0-9]+', line)
    self.experiment = experiment
    self.series = series
    self.id = int(m.group('id'))
    self.frame = int(m.group('frame'))
    self.row = int(m.group('y'))
    self.column = int(m.group('x'))
    self.z = None # set from gfp -> argmax from focus
    self.c = None # level class

  def __str__(self):
    return '[%s %s %d %d %d]' % (self.experiment, self.series, self.id, self.row, self.column)
