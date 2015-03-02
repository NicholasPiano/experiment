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
from skimage import exposure, filter

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    #1. for each series in each experiment, compile z-stacked gfp with z-stack (30-40) bf. Output time series to relevant directory
    base_output_path = '/Volumes/transport/data/cp/centre-ij/input2'

    for e in Experiment.objects.all():

      #make directory
      if not os.path.exists(os.path.join(base_output_path, e.name)):
        os.mkdir(os.path.join(base_output_path, e.name))

      for s in e.series.all():

        #make directory
        if not os.path.exists(os.path.join(base_output_path, e.name, str(s.index))):
          os.mkdir(os.path.join(base_output_path, e.name, str(s.index)))

        #get image set
        bf = s.experiment.images.filter(series=s, channel=1)
        gfp = s.experiment.images.filter(series=s, channel=0)

        #loop through timesteps
        for t in s.timesteps.order_by('index'):
          print('%s %d %d'%(e.name, s.index, t.index))
          bf_t = bf.filter(timestep=t)
          gfp_t = gfp.filter(timestep=t)

          #1. global mean threshold gfp
          #2. 3D smooth gfp
          #3. multiply bf
          #4. output z-projection

          bf_3D = []
          for b in bf_t:
            b.load()
            bf_3D.append(b.array)

          bf_3D = np.array(bf_3D)

          gfp_3D = []
          for g in gfp_t:
            g.load()
            gfp_3D.append(g.array)

          gfp_3D = np.array(gfp_3D)

          gfp_threshold = np.array(gfp_3D)
          gfp_threshold[gfp_3D<gfp_3D.mean()] = 0

          gfp_smooth = filter.gaussian_filter(gfp_threshold, sigma=5)

          #add images
          output_stack = gfp_smooth * exposure.equalize_hist(bf_3D)

          output_image = np.sum(output_stack, axis=0)

          #save
          imsave(os.path.join(base_output_path, e.name, str(s.index), 'stack_t%s.tif'%(('00' if int(t.index)<10 else ('0' if int(t.index)<100 else '')) + str(t.index))), output_image)
