#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
PLOT_DIR = settings.PLOT_DIR

#local
from apps.image.models import SourceImage
from apps.cell.models import CellInstance, Cell, Extension
from apps.env.models import Region, Experiment
from apps.image.util.life.life import Life
from apps.image.util.life.rule import CoagulationsFillInVote
from apps.image.util.tools import get_surface_elements

#util
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import os
import math
from numpy.linalg import norm
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d
import scipy.optimize as optimization
from scipy.optimize import curve_fit
from scipy.misc import imread, imsave
from scipy.ndimage import binary_dilation as dilate
from scipy.ndimage import gaussian_filter as blur
from matplotlib.ticker import NullFormatter
from skimage import filter, exposure
nullfmt   = NullFormatter()

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    #details
    experiment_name = '260714'
    series_index = 16
    timestep_index = 10

    products = []
    for focus in range(75):
      print(focus)
      product = strong_edges(experiment_name, series_index, timestep_index, focus)
      products.append(product)

#     for i,product in enumerate(products):
#       print(i)
#       product_i = np.array(product)
#       for j,product_j in enumerate(products):
#         if i!=j:
#           product_i = product_i + product_j * 1.0/float(abs(i-j))
#       imsave(os.path.join(settings.PLOT_DIR, 'edges', 'edges_z%d.tiff'%i), product_i)


#     plt.imshow(product, cmap='Greys', interpolation='nearest')
#     plt.show()

def strong_edges(experiment_name, series_index, timestep_index, focus, bf_3D_array=None, gfp_3D_array=None): #takes a bf and a gfp block of the same dimensions
  #1. Equalise histogram of 3D BF array
  #2. Apply Canny edge detection with a small sigma to the BF
  #3. Rescale GFP intensity for use as a modifier (needs to have a zero point)
  #4. Reduce GFP noise with nonzero mean threshold and Life
  #5. Blur the GFP for use as a proximity measure.
  #6. Apply GFP proximity to Step #2.
  #7. Maybe dilate or use fill-in Life algorithms.

  ###

  #1. get single brightfield image and corresponding gfp
  bf = SourceImage.objects.get(experiment__name=experiment_name,
                               series__index=series_index,
                               timestep__index=timestep_index,
                               focus=focus,
                               channel=1)

  gfp = SourceImage.objects.get(experiment__name=experiment_name,
                               series__index=series_index,
                               timestep__index=timestep_index,
                               focus=focus,
                               channel=0)

  #2. get canny of brightfield
  bf.load()
  imsave(os.path.join(settings.PLOT_DIR, 'bf', 'bf_z%d.tiff'%focus), bf.array)
  bf.array = exposure.equalize_hist(bf.array)
  canny = np.array(filter.canny(bf.array, sigma=1), dtype=int)*255

  #3. gaussian gfp
  gfp.load()
  imsave(os.path.join(settings.PLOT_DIR, 'gfp', 'gfp_z%d.tiff'%focus), gfp.array)
  gfp.array = exposure.rescale_intensity(gfp.array)

  gfp.array = nonzero_mean_threshold(gfp.array, steps=1)

  bl = np.array(blur(gfp.array, sigma=5), dtype=float)
  bl = bl/np.max(bl)

  #4. get canny*gaussian
  product = canny * bl
  original_product = np.array(product)

  #5. mean threshold product
  product = nonzero_mean_threshold(product, steps=2)
  product[product>0] = 255

  #6. gaussian blur product and apply to original product
  product_blur = blur(product, sigma=2)
  product_blur[product_blur>0] = 255

  product = np.ma.array(original_product, mask=np.array(product_blur==0), fill_value=0)
  product = product.filled()

  return product

def nonzero_mean_threshold(array, steps=1):
  for step in range(steps):
    array_masked = np.ma.array(array, mask=np.array(array==0), fill_value=0)
    array[array<array_masked.mean()] = 0

  return array
