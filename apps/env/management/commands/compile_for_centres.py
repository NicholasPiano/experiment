#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

#local
from apps.cell.models import Cell
from apps.env.models import Experiment, Series

#util
import os
import numpy as np
from scipy.misc import imsave
from scipy.ndimage.morphology import binary_dilation as dilate
import matplotlib.pyplot as plt

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    #1. for each series in each experiment, compile z-stacked gfp with z-stack (30-40) bf. Output time series to relevant directory
    base_output_path = '/Volumes/transport/data/cp/centre-ij/input'

    for e in Experiment.objects.all():

      #make directory
      if not os.path.exists(os.path.join(base_output_path, e.name)):
        os.mkdir(os.path.join(base_output_path, e.name))

      for s in e.series.all()[0]:

        #make directory
        if not os.path.exists(os.path.join(base_output_path, e.name, str(s.index))):
          os.mkdir(os.path.join(base_output_path, e.name, str(s.index)))

        #get image set
        bf = s.experiment.images.filter(series=s, channel=1, focus__lt=40, focus__gt=30)
        gfp = s.experiment.images.filter(series=s, channel=0)

        #loop through timesteps
        for t in s.timesteps.all()[0]:
          print('%s %d %d'%(e.name, s.index, t.index))
          bf_t = bf.filter(timestep=t)
          gfp_t = gfp.filter(timestep=t)

          # stack images
          bf_sample = bf_t[0]
          bf_sample.load()
          bf_stack = np.zeros(bf_sample.array.shape)
          for b in bf_t:
            b.load()
            bf_stack += b.array

          gfp_stack = np.zeros(bf_sample.array.shape)
          for g in gfp_t:
            g.load()
            gfp_stack += g.array

          #add images
          stack_sum = gfp_stack + bf_stack
          imsave(os.path.join(base_output_path, e.name, str(s.index), 'stack_t%d.tif'%t.index))
