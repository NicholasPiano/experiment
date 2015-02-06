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
import re
from numpy.linalg import norm
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d
import scipy.optimize as optimization
from scipy.optimize import curve_fit
from scipy.misc import imread, imsave
from scipy.ndimage import binary_dilation as dilate
from scipy.ndimage import gaussian_filter as blur
from scipy.ndimage.measurements import histogram
from scipy.stats import cumfreq
from matplotlib.ticker import NullFormatter
from skimage import filter, exposure
from scipy.ndimage.morphology import distance_transform_edt as distance
nullfmt   = NullFormatter()

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    class image():
      array = None
      level = 0
      def __init__(self, array=None, level=0):
        self.array = array
        self.level = level

    #paths
    base_path = os.path.join('/','Volumes','transport','data','confocal','2phasetest','singlecell')

    #load images
    bf_list = [image(array=imread(os.path.join(base_path, 'bf', filename)), level=int(re.match(r'.+_z(?P<level>[0-9]+)', filename).group('level'))) for filename in os.listdir(os.path.join(base_path, 'bf'))]
    gfp_list = [image(array=imread(os.path.join(base_path, 'gfp', filename)), level=int(re.match(r'.+_z(?P<level>[0-9]+)', filename).group('level'))) for filename in os.listdir(os.path.join(base_path, 'gfp'))]

    mask = image(array=np.array(imread(os.path.join(base_path, 'mask.tif')), dtype=bool), level=0)
    dt = distance(np.invert(mask.array))

    #1. get histogram of each masked bf image
    # types=['-.','-','-o','-+','-.','-','-o','-+','-.']
    # for i,bf in enumerate(sorted(bf_list, key=lambda bf: bf.level)):
    #   masked_bf = np.ma.array(bf.array, mask=mask.array, fill_value=0)
    #
    #   mask_hist = histogram(masked_bf.filled(), 0, 255, 255)
    #   mask_hist = np.array([0] + mask_hist[1:], dtype=float)
    #   plt.plot(mask_hist, types[i], label=str(i))
    # plt.xlim([0,100])
    # plt.legend()
    # plt.show()

    #2. get mean at a single distance transform value
    # bf = bf_list[0]

    fig = plt.figure()

    for i, bf in enumerate(bf_list):
      ax = fig.add_subplot(len(bf_list), 1, i+1)
      m = []
      d = []
      for value in np.unique(dt):
        d.append(value)

        dt_mask = (dt!=value)
        masked_bf = np.ma.array(bf.array, mask=dt_mask, fill_value=0)

        m.append(masked_bf.mean())

      ax.plot(d, m)

    plt.show()
