#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

#local
from apps.cell.models import Cell, CellInstance
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
    output_path = os.path.join('/Volumes/WINDOWSSWAP/Segmentation/img/stack/')

    #1. get single cell instance
    cell_instance = CellInstance.objects.get(pk=1000)

    #2. output mask in black field
    #a. get bounding box
    bb = cell_instance.cell.bounding_box.get()
    row, column, rows, columns = bb.y, bb.x, bb.h, bb.w

    #b. get gfp stack
    shape = ()
    gfp_stack = cell_instance.experiment.images.filter(series=cell_instance.series, timestep=cell_instance.timestep, channel=0)

    for gfp in gfp_stack:
      gfp.load()
      shape = gfp.array.shape
      gfp.save_array(path=os.path.join(output_path, 'gfp'))

    #black field
    black = np.zeros(shape)
    mask = cell_instance.mask_array()
    
