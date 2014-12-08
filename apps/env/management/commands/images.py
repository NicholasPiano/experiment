#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.image.models import SourceImage
from apps.cell.models import CellInstance

#util
import os
from scipy.misc import imsave, imread
import numpy as np
from skimage import filter as ft
from skimage import exposure as ex

#command
class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      #get full stack of brightfield and corresponding gfp
      #get set of all mask images -> get all cell instances

      #details
      experiment_name = '260714'
      series_index = 15
      timestep_index = 10

      output_path = os.path.join('/','Volumes','transport','data','imgrec')

      #1. brightfield
      bf_image_set = SourceImage.objects.filter(experiment__name=experiment_name, series__index=series_index, timestep__index=timestep_index, channel=1).order_by('focus')

      #2. gfp
      gfp_image_set = SourceImage.objects.filter(experiment__name=experiment_name, series__index=series_index, timestep__index=timestep_index, channel=0).order_by('focus')

      #3. cell_instances
      cell_instances_all = CellInstance.objects.all()
      cell_instances_filter = CellInstance.objects.filter(experiment__name=experiment_name, series__index=series_index, timestep__index=timestep_index)

      ### STEPS

      #1. get histogram stretched images
      bf = []
      for image in bf_image_set:
        image.load()
        bf.append(ex.equalize_hist(image.array))

      gfp = []
      for image in gfp_image_set:
        image.load()
        gfp.append(ex.equalize_hist(image.array))

      #2. get all masks and composite
      masks = []
      for cell_instance in cell_instances_all:
        mask = cell_instance.mask_array()
        masks.append(mask)

      composite_path = os.path.join(output_path, 'composite.tiff')
      composite = make_composite(composite_path) if not os.path.exists(composite_path) else imread(composite_path)

      #3. run canny over each brightfield image
      bf_canny = []
      for i, image in enumerate(bf):
        edges = ft.canny(image, sigma=3)
        imsave(os.path.join(output_path, 'image_%d.tiff'%i), edges)
        bf_canny.append(edges)

      #4.


def make_composite(composite_path):
  #get all mask images
  max_width = 0
  for cell_instance in CellInstance.objects.all():
    (x_b,y_b,w,h) = cell_instance.cell.bounding_box.get().all()
    (x,y) = (cell_instance.position_x, cell_instance.position_y)
    cell_instance_max = max([x-x_b,y-y_b,w-x+x_b,h-y+y_b])
    max_width = max_width if max_width>cell_instance_max else cell_instance_max

  full_mask_shape = (2*max_width, 2*max_width)

  complete_full_mask = np.zeros(full_mask_shape)
  for cell_instance in CellInstance.objects.all():
    #metrics
    (x_b,y_b,w,h) = cell_instance.cell.bounding_box.get().all()
    (x,y) = (cell_instance.position_x, cell_instance.position_y)
    center_column = x-x_b
    center_row = y-y_b
    column_shift = max_width-center_column
    row_shift = max_width-center_row

    #load image
    full_mask = np.zeros(full_mask_shape)
    mask = cell_instance.mask_array()/255.0

    #position image
    full_mask[row_shift:row_shift+h,column_shift:column_shift+w] = mask
    complete_full_mask += full_mask

  complete_full_mask.dtype = float

  #cut to size
  b = (complete_full_mask==0) #find the first row where everything is NOT equal to zero, so zero is "True"
  columns = np.all(b, axis=0)
  rows = np.all(b, axis=1)

  firstcol = columns.argmin()
  firstrow = rows.argmin()

  lastcol = len(columns) - columns[::-1].argmin()
  lastrow = len(rows) - rows[::-1].argmin()

  composite = complete_full_mask[firstrow:lastrow,firstcol:lastcol]
  imsave(composite_path, composite)
  return composite
