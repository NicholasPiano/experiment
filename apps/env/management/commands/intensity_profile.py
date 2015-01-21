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
    focus = 25

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
    bf.array = bf.array
    bf.array = exposure.equalize_hist(bf.array)
    canny = np.array(filter.canny(bf.array, sigma=1), dtype=int)*255

#     plt.imshow(canny, cmap='Greys', interpolation='nearest')
#     plt.show()

    #3. gaussian gfp
    gfp.load()
    gfp.array = gfp.array
    gfp.array = exposure.rescale_intensity(gfp.array)

    gfp.array = nonzero_mean_threshold(gfp.array, steps=1)

    bl = np.array(blur(gfp.array, sigma=1), dtype=float)
    bl = bl/np.max(bl)

    plt.imshow(bl, cmap='Greys', interpolation='nearest')
    plt.show()

#     plt.imshow(bl, cmap='Greys', interpolation='nearest')
#     plt.show()

    #4. get canny*gaussian
    product = canny * bl
    original_product = np.array(product)

#     #5. mean threshold product
#     product = nonzero_mean_threshold(product, steps=2)
#     product[product>0] = 255

#     #6. gaussian blur product and apply to original product
#     product_blur = blur(product, sigma=2)
#     product_blur[product_blur>0] = 255

#     product = np.ma.array(original_product, mask=np.array(product_blur==0), fill_value=0)
#     product = product.filled()

#     plt.imshow(product, cmap='Greys', interpolation='nearest')
#     plt.show()

def strong_edges(bf, gfp):
  pass

def nonzero_mean_threshold(array, steps=1):
  for step in range(steps):
    array_masked = np.ma.array(array, mask=np.array(array==0), fill_value=0)
    array[array<array_masked.mean()] = 0

  return array
