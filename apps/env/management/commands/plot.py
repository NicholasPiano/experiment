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
from matplotlib.ticker import NullFormatter
nullfmt   = NullFormatter()

# matplotlib.rc('font', **font)

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      '''
      PLOT 8: Angle vs protrusion length
      '''

      #start with a rectangular Figure
      fig = plt.figure(1, figsize=(10,10))

      #min and max for axes
      length = [extension.length for extension in Extension.objects.all()]
      max_length = max(length)
      min_length = min(length)

      #region
      corrections = {'050714':(1, math.pi/2.0),
                     '190714':(-1, math.pi),
                     '260714':(1, math.pi),}

      region_index = 4
      region = Region.objects.get(index=region_index)
      data = []
      for extension in region.extensions.all():
        c = corrections[extension.cell.experiment.name]
        data.append((extension.length*extension.cell.experiment.x_microns_over_pixels, (float(c[0])*float(extension.angle) + float(c[1]))*float(180.0/math.pi)))

      #definitions for the axes
      left, width = 0.1, 0.65
      bottom, height = 0.1, 0.65
      bottom_h = left_h = left+width+0.02

      rect_scatter = [left, bottom, width, height]
      rect_x_density = [left, bottom_h, width, 0.2]
      rect_y_density = [left_h, bottom, 0.2, height]

      #axes
      ax = plt.axes(rect_scatter)
      ax_x_density = plt.axes(rect_x_density)
      ax_y_density = plt.axes(rect_y_density)

      #scatter
      y = np.array([d[0] for d in data])
      x = np.array([d[1] for d in data])

      x[x>180] -= 360
      x[x<-180] += 360

      ax.set_ylim([float(min_length), float(max_length)])
      ax.scatter(x, y)

      #histograms
      x_binwidth = 3
      y_binwidth = 2

      ax_x_density.xaxis.set_major_formatter(nullfmt)
      ax_y_density.yaxis.set_major_formatter(nullfmt)

      x_bins = np.arange(-180, 180+x_binwidth, x_binwidth)
      y_bins = np.arange(float(min_length), float(max_length)+y_binwidth, y_binwidth)

      ax_x_density.hist(x, bins=x_bins)
      ax_y_density.hist(y, bins=y_bins, orientation='horizontal')

      ax.set_xlabel(r'Angle from barrier (degrees)')
      ax.set_ylabel(r'Extension length ($\mu$)')

      plt.show()
