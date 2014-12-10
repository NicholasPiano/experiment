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
      #for each experiment, get the x values of the cells when they first enter region 2
      #take the average
      #use the result as the x value of the barrier
      #use for all cells in the experiment

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

      #plots
      colours = ['blue','red','green','yellow']
      plots = []
      for region in Region.objects.all():
       data = ([],[])
       for cell_instance in region.cell_instances.all():
         key = cell_instance.experiment.name+str(cell_instance.series.index)
         if key in experiment_barrier_location_dict.keys():
           data[0].append((experiment_barrier_location_dict[key] - cell_instance.position_x)*cell_instance.experiment.x_microns_over_pixels)
           data[1].append(cell_instance.max_extension_length*cell_instance.experiment.x_microns_over_pixels)
       plots.append(data)

      for i, plot in enumerate(plots):
       plt.scatter(plot[0], plot[1], c=colours[i], label='region %d'%(i+1))

      plt.gca().yaxis.set_major_locator(MaxNLocator(prune='lower'))
      plt.legend()

      plt.title('Cell protrusion length vs. distance from barrier')
      plt.xlabel('Distance from barrier ($\mu$)') #microns
      plt.ylabel('Cell protrusion length ($\mu$)') #microns per minute

      plt.show()
