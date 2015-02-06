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
      # Get volume over time for a single cell instance
      # cell = Cell.objects.get(pk=20)

      class C():
        t = 0
        v = 0
        def __init__(self, t=0, v=0):
          self.t=t
          self.v=v

      for cell in Cell.objects.all():

        cells = []

        for cell_instance in cell.cell_instances.filter(volume__gt=0).order_by('timestep'):
          cells.append(C(t=cell_instance.experiment.time(cell_instance.timestep.index), v=cell_instance.experiment.volume(cell_instance.volume)))

        cells = sorted(cells, key=lambda c: c.t)

        timesteps = [c.t for c in cells]
        volumes = [c.v for c in cells]

        plt.plot(timesteps, volumes)

      plt.title('Cell volume over time for all cells')
      plt.xlabel(r'Time, t (minutes)')
      plt.ylabel(r'Volume, V ($\mu m ^ 3$)')

      plt.show()
