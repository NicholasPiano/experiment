'''
Checks intensity variations in brightfield and gfp images.

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
    base_output_path = '/Volumes/transport/data/cp/centre-ij/intensity'

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

        # get images
        bf = s.experiment.images.filter(series=s, channel=1)
        gfp = s.experiment.images.filter(series=s, channel=0)
        series_image = s.experiment.images.get(series=s, channel=0, timestep__index=0, focus=0)
        series_image.load()

        # data
        time = []
        bf_mean = []
        gfp_mean = []

        # get cells
        cell_instances = []
        with open(os.path.join(base_input_path, e.name, str(s.index), 'tracks.xls')) as tracks_file:
          for line in tracks_file.readlines():
            if int('0' + line.split('\t')[0])>0:
              cell_instances.append(CellInstance(e.name, str(s.index), ' '.join(line.rstrip().split('\t'))))

        # loop through timesteps
        all_timestep_indices = [t.index for t in s.timesteps.order_by('index')]
        for t in s.timesteps.order_by('index'):
          time.append(t.index)
          print('%s %d %d'%(e.name, s.index, t.index))

          # make mask
          ci = filter(lambda c: c.frame==all_timestep_indices.index(t.index)+1, cell_instances)

          cell_mask = np.ones(series_image.array.shape, dtype=bool)

          for cell_instance in ci:
            # draw circle
            xx, yy = np.mgrid[:cell_mask.shape[0], :cell_mask.shape[1]]
            circle = (xx - cell_instance.row) ** 2 + (yy - cell_instance.column) ** 2 # distance from c
            cell_mask[circle<20] = False # radius of 20 px

          # compile mean bf
          bf_t = bf.filter(timestep=t)
          bf_mean_t = 0
          for bf_i in bf_t:
            bf_i.load()
            masked_bf = np.ma.array(bf_i.array, mask=cell_mask)
            bf_mean_t += masked_bf.mean() / float(len(bf_t))

          bf_mean.append(bf_mean_t)

          # compile mean gfp
          gfp_t = gfp.filter(timestep=t)
          gfp_mean_t = 0
          for gfp_i in gfp_t:
            gfp_i.load()
            masked_gfp = np.ma.array(gfp_i.array, mask=cell_mask)
            gfp_mean_t += masked_gfp.mean() / float(len(gfp_t))

          gfp_mean.append(gfp_mean_t)

        # normalise
        bf_mean = list(np.array(bf_mean) / np.max(bf_mean))
        gfp_mean = list(np.array(gfp_mean) / np.max(gfp_mean))

        # save for series
        plt.plot(time, bf_mean, label='bf')
        plt.plot(time, gfp_mean, label='gfp')

        plot_path = os.path.join(base_output_path, e.name, str(s.index), 'intensity_masked.png')
        plt.legend()
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

  def __str__(self):
    return '[%s %s %d %d %d]' % (self.experiment, self.series, self.id, self.row, self.column)
