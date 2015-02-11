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
    output_dir = os.path.join(settings.PLOT_DIR, 'mask')

    for cell in Cell.objects.all():
      #0. make directory for each experiment, series, and cell
      exp_path = os.path.join(output_dir, 'experiment_%s' % cell.experiment.name)
      if not os.path.exists(exp_path):
        os.mkdir(exp_path)
      ser_path = os.path.join(exp_path, 'series_%d' % int(cell.series.index))
      if not os.path.exists(ser_path):
        os.mkdir(ser_path)
      path = os.path.join(ser_path, 'cell_%d' % int(cell.index))
      if not os.path.exists(path):
        os.mkdir(path)

      #1. get bounding box
      bb = cell.bounding_box.get()
      row, column, rows, columns = bb.y, bb.x, bb.h, bb.w

      #2. loop through cell instances
      for cell_instance in cell.cell_instances.all():
        #3. load image corresponding to focus level of cell
        bf_image = cell_instance.experiment.images.get(series=cell_instance.series, timestep=cell_instance.timestep, focus=cell_instance.position_z, channel=1)
        bf_image.load()
        bf = bf_image.array

        #4. make black field in which to place mask
        black = np.zeros(bf.shape)

        #4. place mask in image according to the dimensions of the bounding box.
        mask = cell_instance.mask_array()
        black[row:row+rows, column:column+columns] = mask

        outline = dilate(black) - black
        outline[outline<0] = 0

        bf[outline>0] = bf.max()

        #5. save image

        #save "bf"
        bf_path = os.path.join(path, 'bf')
        if not os.path.exists(bf_path):
          os.mkdir(bf_path)

        imsave(os.path.join(bf_path, 'bf_%s_s%d_c%d_t%d.tiff' % (cell.experiment.name, cell.series.index, cell.index, cell_instance.timestep.index)), bf)
        #save "black"
        mask_path = os.path.join(path, 'mask')
        if not os.path.exists(mask_path):
          os.mkdir(mask_path)

        imsave(os.path.join(mask_path, 'mask_%s_s%d_c%d_t%d.tiff' % (cell.experiment.name, cell.series.index, cell.index, cell_instance.timestep.index)), black)
        print('%s %d %d %d' % (cell.experiment.name, cell.series.index, cell.index, cell_instance.timestep.index))
