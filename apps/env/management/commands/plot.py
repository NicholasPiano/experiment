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
      PLOT 2b: Velocity against distance from barrier
      '''
      #for each experiment, get the x values of the cells when they first enter region 2
      #take the average
      #use the result as the x value of the barrier
      #use for all cells in the experiment

      ### data
      min_length = 0
      max_length = 0

      experiment_barrier_location_dict = {}

      for experiment in Experiment.objects.all():
       for series in experiment.series.all():
         barrier_x_total = 0
         count = 0
         #get all cells
         for cell in series.cells.all():
           if cell.barrier_crossing_timestep!=-1:
             count += 1
             barrier_x_total += cell.cell_instances.get(timestep__index=cell.barrier_crossing_timestep).position_x

         if count!=0:
           experiment_barrier_location_dict[experiment.name+str(series.index)] = int(float(barrier_x_total)/float(count))

      colours = ['blue','red','green','yellow']
      plots = []
      for region in Region.objects.all():
       data = ([],[])
       for cell_instance in region.cell_instances.all():
         key = cell_instance.experiment.name+str(cell_instance.series.index)
         if key in experiment_barrier_location_dict.keys():
           velocity = np.linalg.norm(cell_instance.velocity()*cell_instance.experiment.microns_over_pixels()/cell_instance.experiment.time_per_frame*60)
           if velocity < 1.6:
             max_length = velocity if velocity > max_length else max_length
             data[0].append((experiment_barrier_location_dict[key] - cell_instance.position_x)*cell_instance.experiment.x_microns_over_pixels)
             data[1].append(velocity) #microns per minute
       plots.append(data)

      ### plots

      #fig and rects
      fig = plt.figure(1, figsize=(10,10))

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

      ax_x_density.xaxis.set_major_formatter(nullfmt)
      ax_y_density.yaxis.set_major_formatter(nullfmt)

      x_binwidth = 8
      y_binwidth = 0.05

      #plot
      for i, plot in enumerate(plots):
        x,y = plot[0],plot[1]

        #scatter
        ax.scatter(x, y, c=colours[i], label='region %d'%(i+1), alpha=0.5)

        #histograms
        x_bins = np.arange(-180, 180+x_binwidth, x_binwidth)
        y_bins = np.arange(float(min_length), float(max_length)+y_binwidth, y_binwidth)

        ax_x_density.hist(x, bins=x_bins, facecolor=colours[i], normed=True, alpha=0.5)
        ax_y_density.hist(y, bins=y_bins, orientation='horizontal', facecolor=colours[i], normed=True, alpha=0.5)

      ax.legend()

      ax.set_xlabel('Distance from barrier ($\mu m$)') #microns
      ax.set_ylabel('Cell velocity ($\mu m$/minute)') #microns per minute
      ax.set_ylim([0,1.6])
      ax.set_xlim([-200,200])
      ax_y_density.set_ylim([0,1.6])
      ax_x_density.set_xlim([-200,200])
      ax_x_density.set_yticks(np.arange(0, 0.08, 0.02))

      plt.show()

