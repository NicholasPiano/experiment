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
    base_output_path = '/Volumes/transport/data/cp/centre-ij/tracks'

    for e in Experiment.objects.filter(name='050714'):

      #make directory
      if not os.path.exists(os.path.join(base_output_path, e.name)):
        os.mkdir(os.path.join(base_output_path, e.name))

      for s in e.series.all():

        #make directory
        if not os.path.exists(os.path.join(base_output_path, e.name, str(s.index))):
          os.mkdir(os.path.join(base_output_path, e.name, str(s.index)))
        # os.makedirs(os.path.join(base_output_path, e.name, str(s.index)))

        #get image set
        bf = s.experiment.images.filter(series=s, channel=1)
        gfp = s.experiment.images.filter(series=s, channel=0)

        #load tracks file
        cell_instances = []
        with open(os.path.join(base_input_path, e.name, str(s.index), 'tracks.xls')) as tracks_file:
          for line in tracks_file.readlines():
            if int('0' + line.split('\t')[0])>0:
              cell_instances.append(CellInstance(e.name, str(s.index), ' '.join(line.rstrip().split('\t'))))

        #loop through timesteps
        for t in s.timesteps.order_by('index'):
          ci = filter(lambda c: c.frame==int(t.index)+1, cell_instances)
          print('%s %d %d \n%s\n'%(e.name, s.index, t.index, '\n'.join([str(c) for c in ci])))
          bf_t = bf.filter(timestep=t)
          bf_first = bf_t.get(focus=0)
          bf_first.load()

          b = np.zeros(bf_first.array.shape)
          for bf_z in bf_t:
            bf_z.load()
            b += bf_z.array / float(len(bf_t))

          # b = np.dstack([b, b, b, np.zeros(b.shape)]) # mean brightfield in rgba

          # print(b.shape)

          # for each cell instance in 'ci', put white circle in [row, column]
          # surface = cairo.ImageSurface.create_for_data(b, cairo.FORMAT_ARGB32, b.shape[0], b.shape[1])
          # cr = cairo.Context(surface)
          #
          for c in ci:
            b[c.row-5:c.row+5, c.column-5:c.column+5] = 255
          #   cr.arc(c.column, c.row, 5, 0, 2*math.pi)
          #   cr.set_line_width(1)
          #   cr.set_source_rgb(1.0, 0.0, 0.0)
          #   cr.stroke()

          # save image
          image_path = os.path.join(base_output_path, e.name, str(s.index), 'tracks_%s.png'%(('00' if int(t.index)<10 else ('0' if int(t.index)<100 else '')) + str(t.index)))
          imsave(image_path, b)

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
