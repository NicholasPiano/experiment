#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.image.models import SourceImage
from apps.cell.models import CellInstance

#util
import os
from scipy.misc import imsave, imread
from scipy.signal import gaussian
from scipy.ndimage.morphology import binary_dilation as dilate
from scipy.ndimage.morphology import distance_transform_edt as distance
from scipy.ndimage.filters import convolve
import numpy as np
from skimage import filter, feature, exposure
import math

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
      cell_instance_904 = CellInstance.objects.get(pk=904)

      mask = cell_instance_904.mask_array()
      b = (mask==0) #find the first row where everything is NOT equal to zero, so zero is "True"
      columns = np.all(b, axis=0)
      rows = np.all(b, axis=1)

      firstcol = columns.argmin()
      firstrow = rows.argmin()

      lastcol = len(columns) - columns[::-1].argmin()
      lastrow = len(rows) - rows[::-1].argmin()

      mask = mask[firstrow:lastrow,firstcol:lastcol]

      ### STEPS

      #1. get histogram stretched images
      bf = []
      for i, image in enumerate(bf_image_set):
        image.load()
        ex = exposure.equalize_hist(image.array)
#         ex = convolve(ex, mask)

#         imsave(os.path.join(output_path, 'cell_convolve', 'image_%d.tiff'%i), ex)

        bf.append(ex)

#       gfp = []
#       for image in gfp_image_set:
#         image.load()
#         gfp.append(exposure.equalize_hist(image.array))

      #2. get all masks and composite
###
#       combined_masks = np.zeros(bf[0].shape)
#       for cell_instance in cell_instances_filter:
#         #get outline
#         mask = cell_instance.mask_array()
#         dilated = np.array(dilate(mask), dtype=int)*255
#         outline = np.array(dilated - mask)

#         #position outline in source image
#         y,x = np.unravel_index(distance(mask).argmax(), mask.shape)
#         rows, columns = mask.shape[0], mask.shape[1]
#         pos_x, pos_y = cell_instance.position_x, cell_instance.position_y

#         field = np.zeros(bf[0].shape)

#         row0 = pos_y - y
#         row0_difference = 0
#         if row0<0:
#           row0_difference = -row0
#           row0 = 0

#         row1 = pos_y - y + rows
#         row1_difference = mask.shape[0]
#         if row1>=field.shape[0]:
#           row1_difference = mask.shape[0] + field.shape[0] - row1
#           row1 = field.shape[0]

#         column0 = pos_x - x
#         column0_difference = 0
#         if column0<0:
#           column0_difference = -column0
#           column0 = 0

#         column1 = pos_x - x + columns
#         column1_difference = mask.shape[1]
#         if column1>=field.shape[1]:
#           column1_difference = mask.shape[1] + field.shape[1] - column1
#           column1 = field.shape[1]

#         field[row0:row1,column0:column1] = outline[row0_difference:row1_difference, column0_difference:column1_difference]

#         combined_masks += field

#       imsave(os.path.join(output_path, 'combined.tiff'), combined_masks)


#       composite_path = os.path.join(output_path, 'composite.tiff')
#       composite = make_composite(composite_path) if not os.path.exists(composite_path) else imread(composite_path)
###

      #3. run canny over each brightfield image
###
#       bf_canny = []
#       for i, image in enumerate(bf):
#         sigma = 3
#         edges = filter.canny(image, sigma=sigma)
# #         imsave(os.path.join(output_path, 'edge', 'canny_%d_%d.tiff'%(sigma, i)), edges)
#         bf_canny.append(np.array(edges, dtype=int))
###

      #4. add canny images and cut below max -> only edges that stay
###
#       canny_sum = np.zeros(bf_canny[0].shape)
#       for c in bf_canny:
#         canny_sum += c

#       for i, c in enumerate(bf_canny):
#         c *= canny_sum

#         imsave(os.path.join(output_path, 'canny_composite', 'image_%d.tiff'%i), c)
###

      #5. find blobs with size comparable to size of composite
###
#       #- find blob radius
#       composite_blob = np.zeros(composite.shape)
#       composite_blob[composite>composite.mean()] = 1
#       min_blob_radius = math.sqrt(float(composite_blob.sum())/float(4*math.pi))
#       max_blob_radius = math.sqrt(float(composite_blob.shape[0]*composite_blob.shape[1])/float(4*math.pi))

#       #- find blobs in image
#       bf_blobs = []
#       for i, image in enumerate(bf):
#         blobs = feature.blob_log(image)
#         bf_blobs.append(blobs)
###




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
