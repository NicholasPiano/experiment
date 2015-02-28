#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

#local
from apps.cell.models import Cell
from apps.env.models import Experiment, Series

#util
import os
import numpy as np
from scipy.misc import imsave
from scipy.ndimage.morphology import binary_dilation as dilate
import matplotlib.pyplot as plt

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    #1.
    cell = Cell.objects.get(pk=1)

    path = '/Volumes/WINDOWSSWAP/Segmentation/runs/mask-run-2'

    cell_dictionary_list = []

    #make dictionary with timesteps as keys
    with open(os.path.join(path, 'cells.csv')) as csv:
      for line in csv.readlines()[1:]:
        cell_dictionary_list.append({'t':line.split(',')[8],'a':line.split(',')[10],'x':line.split(',')[11],'y':line.split(',')[12]})

    cell_dictionary_list = sorted(cell_dictionary_list, key=lambda c: int(c['t']))

    x1 = []
    y1 = []
    x2 = []
    y2 = []

    for c in cell_dictionary_list:
      cell_instance = cell.cell_instances.get(timestep__index=c['t'])

      x1.append(float(c['x']))
      x2.append(float(cell_instance.position_x))

      y1.append(float(c['y']))
      y2.append(float(cell_instance.position_y))

    plt.plot(x1,y1)
    plt.plot(x2,y2)
    plt.show()
