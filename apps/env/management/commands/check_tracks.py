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
import cairocffi as cairo
import math

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    #1. for each series in each experiment, compile z-stacked gfp with z-stack (30-40) bf. Output time series to relevant directory
    base_input_path = '/Volumes/transport/data/cp/centre-ij/input'
    base_output_path = '/Volumes/transport/data/cp/centre-ij/tracks_cp'

    for e in Experiment.objects.filter(name='050714'):

      # make directory
      if not os.path.exists(os.path.join(base_output_path, e.name)):
        os.mkdir(os.path.join(base_output_path, e.name))

      for s in e.series.all():

        # make directory
        if not os.path.exists(os.path.join(base_output_path, e.name, str(s.index))):
          os.mkdir(os.path.join(base_output_path, e.name, str(s.index)))

        # get image set
        bf = s.experiment.images.filter(series=s, channel=1)
        gfp = s.experiment.images.filter(series=s, channel=0)

        # load tracks file
        cell_instances = []
        with open(os.path.join(base_input_path, e.name, str(s.index), 'tracks.xls')) as tracks_file:
          for line in tracks_file.readlines():
            if int('0' + line.split('\t')[0])>0:
              cell_instances.append(CellInstance(' '.join(line.rstrip().split('\t'))))

        # load cell profiler file
        with open(os.path.join(base_output_path, e.name, str(s.index), 'Nuclei.csv')) as cp_file:
          for line in cp_file.readlines():
            if line.split(',')[0]!='ImageNumber':
              cell_instances.append(CellInstance(line, cp=True))

        # loop through timesteps
        cells = []

        cell_count = 0
        recog_count = 0

        for t in s.timesteps.order_by('index'):
          ci = filter(lambda c: c.frame==int(t.index)+1, cell_instances)
          ci_track = filter(lambda c: not c.cp, ci)
          ci_cp = filter(lambda c: c.cp, ci)

          for cell_track in ci_track:
            cell_count += 1
            # if cell_track.id in [1, 2, 3, 4, 5]:
            count = 0
            for cell_cp in ci_cp:
              count += cell_track.check_proximity(cell_cp)
            recog_count += count

        print(cell_count, recog_count, float(recog_count/float(cell_count)))


class CellInstance():
  def __init__(self, line, cp=False):
    m = re.match(r'[0-9]+ (?P<id>[0-9]+) (?P<frame>[0-9]+) (?P<x>[0-9]+) (?P<y>[0-9]+) [-+]?[0-9]*\.?[0-9]+ [-+]?[0-9]*\.?[0-9]+ [0-9]+', line)
    if cp:
      m = re.match(r'(?P<frame>[0-9]+),(?P<id>[0-9]+),[0-9]+,(?P<x>[-+]?[0-9]*\.?[0-9]+),(?P<y>[-+]?[0-9]*\.?[0-9]+),.*', line)
    self.id = int(float(m.group('id')))
    self.cp = cp
    self.frame = int(float(m.group('frame')))
    self.row = int(float(m.group('y')))
    self.column = int(float(m.group('x')))

  def check_proximity(self, cell_instance):
    # return yes if positions are within 10 pixels
    return ((self.row-cell_instance.row)**2 + (self.column-cell_instance.column)**2 < 10.0)

  def __str__(self):
    return '[%s %s %d %d %d]' % (self.experiment, self.series, self.id, self.row, self.column)
