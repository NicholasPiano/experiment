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
      PLOT 3: Protrusion length vs angle
      '''

      colours = ['blue','red','green','yellow']

      r1 = [float(extension.angle)*180.0/math.pi for extension in Extension.objects.filter(region__index=1)]
      r2 = [float(extension.angle)*180.0/math.pi for extension in Extension.objects.filter(region__index=2)]
      r3 = [float(extension.angle)*180.0/math.pi for extension in Extension.objects.filter(region__index=3)]
      r4 = [float(extension.angle)*180.0/math.pi for extension in Extension.objects.filter(region__index=4)]

      #histogram for each in one figure
      fig = plt.figure()
      ax4 = fig.add_subplot(414)
      ax4.xaxis.set_ticks([-180, -135, -90, -45, 0, 45, 90, 135, 180])
      ax1 = fig.add_subplot(411, sharex=ax4)
      ax2 = fig.add_subplot(412, sharex=ax4)
      ax3 = fig.add_subplot(413, sharex=ax4)

      ax1.hist(r1, bins=get_bins(r1), facecolor=colours[0], normed=True)
      ax2.hist(r2, bins=get_bins(r2), facecolor=colours[1], normed=True)
      ax3.hist(r3, bins=get_bins(r3), facecolor=colours[2], normed=True)
      ax4.hist(r4, bins=get_bins(r4), facecolor=colours[3], normed=True)

      ax1.set_ylim([0,0.007])
      ax2.set_ylim([0,0.007])
      ax3.set_ylim([0,0.007])
      ax4.set_ylim([0,0.007])

      ax1.yaxis.set_ticks([0.007])
      ax2.yaxis.set_ticks([0.007])
      ax3.yaxis.set_ticks([0.007])
      ax4.yaxis.set_ticks([0.007])

      #lines
      y = [0,0.007]
      x1 = [-90,-90]
      x2 = [0,0]
      x3 = [90,90]

      ax1.plot(x1, y, color='red')
      ax1.plot(x2, y, color='red')
      ax1.plot(x3, y, color='red')

      ax2.plot(x1, y, color='red')
      ax2.plot(x2, y, color='red')
      ax2.plot(x3, y, color='red')

      ax3.plot(x1, y, color='red')
      ax3.plot(x2, y, color='red')
      ax3.plot(x3, y, color='red')

      ax4.plot(x1, y, color='red')
      ax4.plot(x2, y, color='red')
      ax4.plot(x3, y, color='red')

      plt.setp(ax1.get_xticklabels(), visible=False)
      plt.setp(ax2.get_xticklabels(), visible=False)
      plt.setp(ax3.get_xticklabels(), visible=False)

      ax4.set_xlabel(r'Extension angle, $\theta$ (degrees)')
      plt.ylabel('Frequency')
      plt.xlim([-190, 190])

      plt.show()

