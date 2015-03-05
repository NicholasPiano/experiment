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

        # data
        time = []
        bf_mean = []
        gfp_mean = []

        # loop through timesteps
        for t in s.timesteps.order_by('index'):
          time.append(t.index)
          print('%s %d %d'%(e.name, s.index, t.index))

          #compile mean bf
          bf_t = bf.filter(timestep=t)
          bf_mean_t = 0
          for bf_i in bf_t:
            bf_i.load()
            bf_mean_t += bf_i.array.mean() / float(len(bf_t))

          bf_mean.append(bf_mean_t)

          #compile mean gfp
          gfp_t = gfp.filter(timestep=t)
          gfp_mean_t = 0
          for gfp_i in gfp_t:
            gfp_i.load()
            gfp_mean_t += gfp_i.array.mean() / float(len(gfp_t))

          gfp_mean.append(gfp_mean_t)

        # normalise
        bf_mean = list(np.array(bf_mean) / np.max(bf_mean))
        gfp_mean = list(np.array(gfp_mean) / np.max(gfp_mean))

        # save for series
        plt.plot(time, bf_mean, label='bf')
        plt.plot(time, gfp_mean, label='gfp')

        plot_path = os.path.join(base_output_path, e.name, str(s.index), 'intensity.png')
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
