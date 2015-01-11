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
from matplotlib.ticker import NullFormatter
nullfmt   = NullFormatter()

# matplotlib.rc('font', **font)

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      '''

      Plot 2b and 2c: Velocity and protrusion length against distance from barrier: 4 histograms each.

      '''

      colours = ['blue','red','green','yellow']

      ### 2C

      r1 = [float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels) for extension in Extension.objects.filter(region__index=1)]
      r2 = [float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels) for extension in Extension.objects.filter(region__index=2)]
      r3 = [float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels) for extension in Extension.objects.filter(region__index=3)]
      r4 = [float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels) for extension in Extension.objects.filter(region__index=4)]

#       max_l = max(r1+r2+r3+r4)

#       #histogram for each in one figure
#       fig = plt.figure()
#       ax4 = fig.add_subplot(414)
#       ax1 = fig.add_subplot(411, sharex=ax4)
#       ax2 = fig.add_subplot(412, sharex=ax4)
#       ax3 = fig.add_subplot(413, sharex=ax4)


#       bin_width = 2
#       bins = np.arange(0, max_l+bin_width, bin_width)

#       ax1.hist(r1, bins=bins, facecolor=colours[0], normed=True)
#       ax2.hist(r2, bins=bins, facecolor=colours[1], normed=True)
#       ax3.hist(r3, bins=bins, facecolor=colours[2], normed=True)
#       ax4.hist(r4, bins=bins, facecolor=colours[3], normed=True)

#       plt.setp(ax1.get_xticklabels(), visible=False)
#       plt.setp(ax2.get_xticklabels(), visible=False)
#       plt.setp(ax3.get_xticklabels(), visible=False)

#       ax4.set_xlabel('Extension length ($\mu m$)')
#       plt.ylabel('Frequency')

#       plt.show()

      ### 2B

#       r1 = [norm(cell_instance.velocity())*float(cell_instance.cell.experiment.x_microns_over_pixels) for cell_instance in CellInstance.objects.filter(region__index=1)]
#       r2 = [norm(cell_instance.velocity())*float(cell_instance.cell.experiment.x_microns_over_pixels) for cell_instance in CellInstance.objects.filter(region__index=2)]
#       r3 = [norm(cell_instance.velocity())*float(cell_instance.cell.experiment.x_microns_over_pixels) for cell_instance in CellInstance.objects.filter(region__index=3)]
#       r4 = [norm(cell_instance.velocity())*float(cell_instance.cell.experiment.x_microns_over_pixels) for cell_instance in CellInstance.objects.filter(region__index=4)]

      #mean
#       m1,m2,m3,m4 = tuple([np.mean(r) for r in [r1,r2,r3,r4]])
#       print((m1,m2,m3,m4))

#       max_l = max(r1+r2+r3+r4)

#       #histogram for each in one figure
#       fig = plt.figure()
#       ax4 = fig.add_subplot(414)
#       ax4.set_xlim([0,30])
#       ax1 = fig.add_subplot(411, sharex=ax4)
#       ax1.set_xlim([0,30])
#       ax2 = fig.add_subplot(412, sharex=ax4)
#       ax2.set_xlim([0,30])
#       ax3 = fig.add_subplot(413, sharex=ax4)
#       ax3.set_xlim([0,30])


#       bin_width = 0.6
#       bins = np.arange(0, max_l+bin_width, bin_width)

#       ax1.hist(r1, bins=bins, facecolor=colours[0], normed=True)
#       ax2.hist(r2, bins=bins, facecolor=colours[1], normed=True)
#       ax3.hist(r3, bins=bins, facecolor=colours[2], normed=True)
#       ax4.hist(r4, bins=bins, facecolor=colours[3], normed=True)

#       plt.setp(ax1.get_xticklabels(), visible=False)
#       plt.setp(ax2.get_xticklabels(), visible=False)
#       plt.setp(ax3.get_xticklabels(), visible=False)

#       ax4.set_xlabel('Cell velocity ($\mu m$/minute)')
#       plt.ylabel('Frequency')

#       plt.show()
