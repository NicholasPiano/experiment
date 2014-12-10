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
from scipy.misc import imread, imsave
from scipy.ndimage import binary_dilation as dilate

# matplotlib.rc('font', **font)

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      '''
      PLOT 5: Protrusion length vs region

      '''

      data = []
      for region in Region.objects.all():
        region_data = []
        for extension in region.extensions.all():
          region_data.append(float(extension.length*extension.cell.experiment.x_microns_over_pixels))
        data.append(region_data)

      plt.boxplot(data)

      plt.title('Comparison of cell extension length in each region')
      plt.ylabel('Extension length   ')
      plt.xlabel('Region')

      plt.show()




