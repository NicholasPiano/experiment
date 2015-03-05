'''
1. Grabs 'tracks.xls' from each series directory and extracts positions.
2. Loads one image from each series and inserts circles of an constant diameter into a black field of the same size as the series image. Saves.
3. Detects conflicts. Saves one image for each conflict. Includes id's of conflicting cells in filename.

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
    base_output_path = '/Volumes/transport/data/cp/centre-ij/cp-in'

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
        series_image = s.experiment.images.get(series=s, channel=1, focus=0, timestep__index=0)
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

          # make black field
          b = np.zeros(series_image.array.shape)

          for cell_instance in ci:
            # draw circle
            xx, yy = np.mgrid[:b.shape[0], :b.shape[1]]
            circle = (xx - cell_instance.row) ** 2 + (yy - cell_instance.column) ** 2 # distance from c
            b[circle<10] = 255 # radius of 10 px

          # save
          imsave(os.path.join(base_output_path, e.name, str(s.index), 'tracks_t%s.tif'%(('00' if int(t.index)<10 else ('0' if int(t.index)<100 else '')) + str(t.index))), b)

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