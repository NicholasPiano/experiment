#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell, Extension
from apps.env.models import Region

#util
from numpy.linalg import norm
import os
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.misc import imsave
from scipy.ndimage import binary_dilation as dilate
from scipy.stats.mstats import mode
from scipy.stats import sem

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      def count_histogram(data, number_of_bins=None):
        hist, bins = np.histogram(data, bins=get_bins(data, mod=1) if number_of_bins is None else number_of_bins)
        hist = np.array(hist, dtype=float)/np.sum(hist) #all bar heights add up to one
        return (hist, bins)

      #1. get average z in region 2, difference from average z in region 1
      for region_index in [1,2,3,4]:
        cell_instance_set = CellInstance.objects.filter(region__index=region_index)
        z = []
        for cell_instance in cell_instance_set:
          z.append(float(cell_instance.position()[2]))
        z_mean = np.mean(z)
        z_sem = sem(z)
        z_mode = mode(np.array(z, dtype=int))
        print([z_mean, z_sem, z_mode])

      #2. mode velocity
#       def count_histogram(data, number_of_bins=None):
#         hist, bins = np.histogram(data, bins=get_bins(data, mod=1) if number_of_bins is None else number_of_bins)
#         hist = np.array(hist, dtype=float)/np.sum(hist) #all bar heights add up to one
#         return (hist, bins)

#       for region_index in [1,2,3,4]:
#         v = [norm(cell_instance.velocity())*float(cell_instance.cell.experiment.x_microns_over_pixels) for cell_instance in CellInstance.objects.filter(region__index=region_index)]
#         hist, bins = count_histogram(v, number_of_bins=100)
#         mode_arg = np.argmax(hist)
#         mode = bins[mode_arg+1] - bins[mode_arg]
#         print(mode)

      #3. mode extension length


#       for region_index in [1,2,3,4]:
#         l = [int(float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels)) for extension in Extension.objects.filter(region__index=region_index)]
#         m = mode(l)
#         print(m)




