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
nullfmt   = NullFormatter()

# matplotlib.rc('font', **font)

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      '''
      PLOT 4: SV

      '''

      def count_histogram(data):
        hist, bins = np.histogram(data, bins=get_bins(data, mod=0.5))
        hist = np.array(hist, dtype=float)/np.sum(hist) #all bar heights add up to one
        return (hist, bins)

      #start with a rectangular Figure
      colours = ['blue','red','green','yellow']
      fig = plt.figure(1, figsize=(10,10))

      #min and max for axes
      sa = [cell_instance.experiment.area(cell_instance.surface_area) for cell_instance in CellInstance.objects.all()]
      min_sa = 0
      max_sa = 3000

      v = [cell_instance.experiment.volume(cell_instance.volume) for cell_instance in CellInstance.objects.all()]
      min_v = 0
      max_v = 15000

      #region
      region_index = 1
      region = Region.objects.get(index=region_index)
      data = []
      for cell_instance in region.cell_instances.all():
        data.append(np.array([float(cell_instance.experiment.area(cell_instance.surface_area)), float(cell_instance.experiment.volume(cell_instance.volume)), float(cell_instance.experiment.area(cell_instance.surface_area))/(float(cell_instance.experiment.volume(cell_instance.volume))+1)]))

      data = filter(lambda x: x[1] > 2000 and x[0]<3000 and x[1]<15000, data)

      #definitions for the axes
      left, width = 0.1, 0.60
      bottom, height = 0.1, 0.60
      bottom_h = left_h = left+width+0.04

      rect_scatter = [left, bottom, width, height]
      rect_x_density = [left, bottom_h, width, 0.2]
      rect_y_density = [left_h, bottom, 0.2, height]

      #axes
      ax = plt.axes(rect_scatter)
      ax_x_density = plt.axes(rect_x_density)
      ax_y_density = plt.axes(rect_y_density)

      #lines
      gradients = np.array([d[2] for d in data])
      p10 = np.percentile(gradients, 10)
      p90 = np.percentile(gradients, 90)
      data10 = filter(lambda k: k[2]<p10, data)
      data90 = filter(lambda k: k[2]>p90, data)

      m10 = np.linalg.lstsq(np.array([math.log(g[0]) for g in data10])[:,np.newaxis], np.array([math.log(g[1]) for g in data10]))[0][0]
      m90 = np.linalg.lstsq(np.array([math.log(g[0]) for g in data90])[:,np.newaxis], np.array([math.log(g[1]) for g in data90]))[0][0]

      x = np.linspace(0,max_sa,max_sa)

      y10 = x**m10
      y90 = x**m90

      ax.plot(x, y10, label='10pc (   =%.2f)'%m10)
      ax.plot(x, y90, label='90pc (   =%.2f)'%m90)
      ax.plot(x, x**1, label='y=x')
      ax.plot(x, x**1.5, label='y=x^1.5')

      #ranges
      ax.set_xlim([min_sa, max_sa])
      ax.set_ylim([min_v, 5000])
      ax_x_density.set_xlim([min_sa, max_sa])
      ax_y_density.set_ylim([min_v, 5000])

      #scatter
      x = np.array([d[0] for d in data])
      y = np.array([d[1] for d in data])

      ax.scatter(x, y, c=colours[region_index-1])

      #histograms
      ax_x_density.xaxis.set_major_formatter(nullfmt)
      ax_y_density.yaxis.set_major_formatter(nullfmt)

      x_hist, x_bins = count_histogram(x)
      y_hist, y_bins = count_histogram(y)

      ax_x_density.bar(x_bins[:-1], x_hist, width=np.diff(x_bins), facecolor=colours[region_index-1])
      ax_y_density.barh(y_bins[:-1], y_hist, height=np.diff(y_bins), facecolor=colours[region_index-1])

#       ax_x_density.set_ylim([0,0.007])
#       ax_y_density.set_xlim([])
#       ax_x_density.yaxis.set_ticks([0.007])
#       ax_y_density.xaxis.set_ticks([0.007])

      ax.set_xlabel(r'Segmented mask area ($\mu m^2$)')
      ax.set_ylabel(r'GFP volume ($\mu m^3$)')

      plt.show()
