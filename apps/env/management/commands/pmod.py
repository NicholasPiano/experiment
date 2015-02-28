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
from skimage import filter as ft
from scipy.stats import gaussian_kde
from scipy.ndimage import gaussian_filter
from skimage import exposure
from scipy.ndimage.morphology import distance_transform_edt as distance

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    image_path = '/Volumes/transport/data/cp/combine/input/modified/pmod'

    ##get images
    experiment = Experiment.objects.get(name='050714')
    bf = experiment.images.filter(series__index=14, channel=1, focus=30)
    gfp = experiment.images.filter(series__index=14, channel=0, focus=30)

    for b in bf[:1]:
      g = gfp.get(timestep__index=b.timestep.index)
      b.load()
      g.load()
      ga = g.array
      ba = b.array

      #1. edges
      edges = np.zeros(ba.shape)

      for sigma in range(5):
        canny = ft.canny(ba, sigma=sigma)
        edges += canny

      nonzero_mean_edges = nonzero_mean(edges)
      edges[edges<nonzero_mean_edges] = 0

      #2. raise intensity of gfp near edges to mean of the gfp at that distance from an edge
      # HIGH EDGE DENSITY -> look for centers

      #3. gfp density
      threshold_gfp = ga
      threshold_gfp[threshold_gfp<7] = 0
      indices = np.vstack(np.nonzero(threshold_gfp))

      z = gaussian_kde(indices)(indices)

      gfp_density = np.zeros(ga.shape)

      for i, n in enumerate(np.swapaxes(indices, 0, 1)):
        row, column = tuple(n)
        gfp_density[row, column] = z[i]

      gfp_density = gaussian_filter(gfp_density, sigma=5)

      gfp_density[gfp_density<gfp_density.mean()] = 0

      edges *= gfp_density

      # imshow(edges)

      #4. equalise histogram
      edges_ex = exposure.equalize_hist(edges)
      edges_ex = 1 - edges_ex

      #5. threshold edges
      edges_t = np.zeros(edges_ex.shape)
      edges_t[edges_ex>edges_ex.mean()] = 1

      # imshow(edges_t)

      d = distance(edges_t)
      d = exposure.equalize_hist(d.max() - d) #lower further from edges
      d = d*d*d*d

      w_bf = ba * d * exposure.equalize_hist(gfp_density)
      # imshow(w_bf)

      #
      # density_ex = exposure.equalize_hist(gfp_density)
      # # density_ex[density_ex<density_ex.mean()] = 0
      #
      # weights = density_ex * edges_ex
      #
      # #5. weighted bf
      # w_bf = ba * weights
      # w_bf = exposure.equalize_hist(w_bf)
      # # imshow(w_bf)
      imsave(os.path.join(image_path, 'pmod_050714.tiff'), w_bf)

def nonzero_mean(array):
  nonzero_mask = array == 0
  masked = np.ma.array(array, mask=nonzero_mask)
  nonzero_mean = masked.mean()
  return nonzero_mean

def imshow(array, cmap='Greys_r'):
  plt.imshow(array, cmap=cmap)
  plt.show()
