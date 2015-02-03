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
from apps.image.util.tools import get_surface_elements, get_bins

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
from matplotlib.ticker import NullFormatter
matplotlib.rcParams.update({'font.size': 18})
nullfmt = NullFormatter()

# matplotlib.rc('font', **font)

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      '''
      PLOT 3: Protrusion length vs angle
      '''

      def count_histogram(data, number_of_bins=None):
        hist, bins = np.histogram(data, bins=get_bins(data, mod=1) if number_of_bins is None else number_of_bins)
        hist = np.array(hist, dtype=float)/np.sum(hist) #all bar heights add up to one
        return (hist, bins)

      #start with a rectangular Figure
      colours = ['blue','red','green','yellow']
      fig = plt.figure(1, figsize=(10,10))

      #min and max for axes
      length = [extension.length for extension in Extension.objects.all()]
      max_length = 80
      min_length = 0

      #region
      corrections = {'050714':(1, math.pi/2.0),
                     '190714':(-1, math.pi),
                     '260714':(1, math.pi),}

      region_index = 1
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
      y = np.array([float(d[0]) for d in data])
      x = np.array([float(d[1]) for d in data])

      x[x>180] -= 360
      x[x<-180] += 360

      ax.set_ylim([float(min_length), float(max_length)])
      ax.set_xlim([-180,180])
      ax.set_xticks(np.arange(-180,181,45))
      ax.plot([90,90],[0,100], '-', c='red', alpha=0.7)
      ax.plot([0,0],[0,100], '-', c='red', alpha=0.7)
      ax.plot([-90,-90],[0,100], '-', c='red', alpha=0.7)
      ax.scatter(x, y, c=colours[region_index-1])

      #histograms
      ax_x_density.xaxis.set_major_formatter(nullfmt)
      ax_y_density.yaxis.set_major_formatter(nullfmt)

      x_hist, x_bins = count_histogram(x, number_of_bins=27)
      y_hist, y_bins = count_histogram(y, number_of_bins=55)

      ax_x_density.bar(x_bins[:-1], x_hist, width=np.diff(x_bins), facecolor=colours[region_index-1])
      ax_y_density.barh(y_bins[:-1], y_hist, height=np.diff(y_bins), facecolor=colours[region_index-1])

      ax_x_density.set_ylim([0,0.1])
      ax_y_density.set_xlim([0,0.09])
      ax_x_density.yaxis.set_ticks([0.1])
      ax_y_density.xaxis.set_ticks([0.09])

      ax.set_xlabel(r'Angle from barrier, $\theta$ (degrees)')
      ax.set_ylabel(r'Extension length ($\mu m$)')

      plt.show()
