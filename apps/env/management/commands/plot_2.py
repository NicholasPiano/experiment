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

      Plot 2b and 2c: Velocity and protrusion length against distance from barrier: 4 histograms each.

      '''

      colours = ['blue','red','green','yellow']

      def count_histogram(data, number_of_bins=None):
        hist, bins = np.histogram(data, bins=get_bins(data, mod=1) if number_of_bins is None else number_of_bins)
        hist = np.array(hist, dtype=float)/np.sum(hist) #all bar heights add up to one
        return (hist, bins)

#       ### 2C

#       r1 = [float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels) for extension in Extension.objects.filter(region__index=1)]
#       r2 = [float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels) for extension in Extension.objects.filter(region__index=2)]
#       r3 = [float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels) for extension in Extension.objects.filter(region__index=3)]
#       r4 = [float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels) for extension in Extension.objects.filter(region__index=4)]

#       max_l = max(r1+r2+r3+r4)

#       #histogram for each in one figure
#       fig = plt.figure()
#       ax4 = fig.add_subplot(414)
#       ax1 = fig.add_subplot(411, sharex=ax4)
#       ax2 = fig.add_subplot(412, sharex=ax4)
#       ax3 = fig.add_subplot(413, sharex=ax4)

#       hist1, bins1 = count_histogram(r1)
#       hist2, bins2 = count_histogram(r2)
#       hist3, bins3 = count_histogram(r3)
#       hist4, bins4 = count_histogram(r4)

#       ax1.bar(bins1[:-1], hist1, width=np.diff(bins1), facecolor=colours[0])
#       ax2.bar(bins2[:-1], hist2, width=np.diff(bins2), facecolor=colours[1])
#       ax3.bar(bins3[:-1], hist3, width=np.diff(bins3), facecolor=colours[2])
#       ax4.bar(bins4[:-1], hist4, width=np.diff(bins4), facecolor=colours[3])

#       plot_max = 0.1

#       ax1.set_ylim([0,plot_max])
#       ax2.set_ylim([0,plot_max])
#       ax3.set_ylim([0,plot_max])
#       ax4.set_ylim([0,plot_max])

#       ax1.yaxis.set_ticks([plot_max])
#       ax2.yaxis.set_ticks([plot_max])
#       ax3.yaxis.set_ticks([plot_max])
#       ax4.yaxis.set_ticks([plot_max])

#       plt.setp(ax1.get_xticklabels(), visible=False)
#       plt.setp(ax2.get_xticklabels(), visible=False)
#       plt.setp(ax3.get_xticklabels(), visible=False)

#       ax4.set_xlabel('Extension length ($\mu m$)')
#       plt.ylabel('Frequency')

#       plt.show()

      ### 2B

      r1 = [norm(cell_instance.velocity())*float(cell_instance.cell.experiment.x_microns_over_pixels) for cell_instance in CellInstance.objects.filter(region__index=1)]
      r2 = [norm(cell_instance.velocity())*float(cell_instance.cell.experiment.x_microns_over_pixels) for cell_instance in CellInstance.objects.filter(region__index=2)]
      r3 = [norm(cell_instance.velocity())*float(cell_instance.cell.experiment.x_microns_over_pixels) for cell_instance in CellInstance.objects.filter(region__index=3)]
      r4 = [norm(cell_instance.velocity())*float(cell_instance.cell.experiment.x_microns_over_pixels) for cell_instance in CellInstance.objects.filter(region__index=4)]

      #mean
#       m1,m2,m3,m4 = tuple([np.mean(r) for r in [r1,r2,r3,r4]])
#       print((m1,m2,m3,m4))

#       max_l = max(r1+r2+r3+r4)

      #histogram for each in one figure
      fig = plt.figure()
      ax4 = fig.add_subplot(414)
      ax4.set_xlim([0,20])
      ax1 = fig.add_subplot(411, sharex=ax4)
      ax1.set_xlim([0,20])
      ax2 = fig.add_subplot(412, sharex=ax4)
      ax2.set_xlim([0,20])
      ax3 = fig.add_subplot(413, sharex=ax4)
      ax3.set_xlim([0,20])

      plot_max = 0.15

      ax1.set_ylim([0,plot_max])
      ax2.set_ylim([0,plot_max])
      ax3.set_ylim([0,plot_max])
      ax4.set_ylim([0,plot_max])

      ax1.yaxis.set_ticks([plot_max])
      ax2.yaxis.set_ticks([plot_max])
      ax3.yaxis.set_ticks([plot_max])
      ax4.yaxis.set_ticks([plot_max])

      hist1, bins1 = count_histogram(r1, number_of_bins=100)
      hist2, bins2 = count_histogram(r2, number_of_bins=40)
      hist3, bins3 = count_histogram(r3, number_of_bins=100)
      hist4, bins4 = count_histogram(r4, number_of_bins=40)

      ax1.bar(bins1[:-1], hist1, width=np.diff(bins1), facecolor=colours[0])
      ax2.bar(bins2[:-1], hist2, width=np.diff(bins2), facecolor=colours[1])
      ax3.bar(bins3[:-1], hist3, width=np.diff(bins3), facecolor=colours[2])
      ax4.bar(bins4[:-1], hist4, width=np.diff(bins4), facecolor=colours[3])

      plt.setp(ax1.get_xticklabels(), visible=False)
      plt.setp(ax2.get_xticklabels(), visible=False)
      plt.setp(ax3.get_xticklabels(), visible=False)

      ax4.set_xlabel('Cell velocity ($\mu m$/minute)')
      plt.ylabel('Frequency')

      plt.ion()
      plt.show()
