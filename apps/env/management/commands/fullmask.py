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
    image_path = '/Volumes/transport/data/cp/combine/input/modified/fullmask'

    #1. get masks for 5 cells from 050714
    #2. position masks within field for each timestep and cell

    for cell in Cell.objects.filter(experiment__name='050714'):
      for cell_instance in cell.cell_instances.all():
        #output mask in black field
        #a. get bounding box
        bb = cell_instance.cell.bounding_box.get()
        row, column, rows, columns = bb.y, bb.x, bb.h, bb.w

        #get gfp stack
        shape = ()
        gfp = cell_instance.experiment.images.get(series=cell_instance.series, timestep=cell_instance.timestep, channel=0, focus=0)
        gfp.load()
        shape = gfp.array.shape

        #black field
        black = np.zeros(shape)
        mask = cell_instance.mask_array()

        black[row:row+rows, column:column+columns] = mask

        #output black
        imsave(os.path.join(image_path, 'fullmask_050714_s14_c%d_f%d.tiff'%(cell.index, cell_instance.timestep.index)), black)
