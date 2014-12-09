#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.image.models import SourceImage
from apps.cell.models import CellInstance

#util
import os
import matplotlib.pyplot as plt
from scipy.misc import imsave, imread
from scipy.signal import gaussian
from scipy.ndimage import distance_transform_edt
from scipy.ndimage.morphology import binary_dilation as dilate
from scipy.ndimage.morphology import distance_transform_edt as distance
from scipy.ndimage.measurements import center_of_mass
from scipy.ndimage.filters import convolve
import numpy as np
from skimage import filter as ft
from skimage import feature, exposure
import math

#command
class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      #load brightfield and gfp for cell instance 747
      cell_instance = CellInstance.objects.get(pk=747)

      #images details
      experiment_name = cell_instance.experiment.name
      series_index = cell_instance.series.index
      timestep_index = cell_instance.timestep.index
      focus = cell_instance.position_z

      #get brightfield
      brightfield_image = SourceImage.objects.get(experiment__name=experiment_name, series__index=series_index, timestep__index=timestep_index, channel=1, focus=focus)
      brightfield_image.load()
      bf = brightfield_image.array

      #get gfp
      gfp_image = SourceImage.objects.get(experiment__name=experiment_name, series__index=series_index, timestep__index=timestep_index, channel=0, focus=focus)
      gfp_image.load()
      gfp = gfp_image.array

      #get mask
      mask_array = cell_instance.mask_array()

      #make white mask with the same size as source image
      mask = np.zeros(bf.shape)

      y,x = np.unravel_index(distance(mask_array).argmax(), mask_array.shape)
      rows, columns = mask_array.shape[0], mask_array.shape[1]
      pos_x, pos_y = cell_instance.position_x, cell_instance.position_y

      row0 = pos_y - y
      row0_difference = 0
      if row0<0:
        row0_difference = -row0
        row0 = 0

      row1 = pos_y - y + rows
      row1_difference = mask_array.shape[0]
      if row1>=mask.shape[0]:
        row1_difference = mask_array.shape[0] + mask.shape[0] - row1
        row1 = mask.shape[0]

      column0 = pos_x - x
      column0_difference = 0
      if column0<0:
        column0_difference = -column0
        column0 = 0

      column1 = pos_x - x + columns
      column1_difference = mask_array.shape[1]
      if column1>=mask.shape[1]:
        column1_difference = mask_array.shape[1] + mask.shape[1] - column1
        column1 = mask.shape[1]

      mask[row0:row1,column0:column1] = mask_array[row0_difference:row1_difference, column0_difference:column1_difference]

      #make mask outline
      dilated = np.array(dilate(mask), dtype=int)*255
      outline = np.array(dilated - mask)

      ### IMAGES
      output_path = os.path.join('/','Volumes','transport','data','confocal','ppt','747')

      #1. brightfield solo
#       imsave(os.path.join(output_path, 'bf.tiff'), bf)

      #2. gfp solo
#       imsave(os.path.join(output_path, 'gfp.tiff'), gfp)

      #3. mask outline+bf
      bf[outline>0] = bf.max()
#       imsave(os.path.join(output_path, 'outline_bf.tiff'), bf)

      #4. mask outline+gfp
      gfp[outline>0] = gfp.max()
#       imsave(os.path.join(output_path, 'outline_gfp.tiff'), gfp)

      #5. white mask
#       imsave(os.path.join(output_path, 'mask.tiff'), mask)

      #6. signal from edge of mask
      #-1. define edgle object
      class edgel():
        def __init__(self, index=0, x=0, y=0, d=0, a=0):
          self.index = index
          self.x = x
          self.y = y
          self.d = d
          self.a = a

      #-2. center of mass and edge
      transform = distance_transform_edt(mask)
      self.cm = np.rint(center_of_mass(transform)).astype(int)
      transform[transform==0] = transform.max() #max all zeros equal to max
      edge = np.argwhere(transform==transform.min()) #edge is the min of the new transform image -> (n, 2) np array

      #-3. get distances and angles from COM
      data = [edgel(i, e[0], e[1], math.sqrt((e[0]-self.cm[0])**2+(e[1]-self.cm[1])**2), math.atan2(e[0]-self.cm[0], e[1]-self.cm[1])*180.0/math.pi) for (i,e) in enumerate(edge)]

      #-4. trace along edge
      count = 0
      length = len(data)
      sorted_data = [data[0]] #index, x, y, length, angle

      while count<length-1:
        #get current point
        current_datum = sorted_data[count]

        #look for closest point to current that is not previous or current
        sorted_distance = sorted(data, key=lambda edg: math.sqrt((edg.x-current_datum.x)**2+(edg.y-current_datum.y)**2))
        min_list = filter(lambda edg: edg.index not in [d.index for d in sorted_data], sorted_distance)

        #add it to sorted_data
        sorted_data.append(min_list[0])

        count+=1

      #-5. plot
      angle = []
      length = []

      for datum in sorted_data:
        angle.append(datum.a)
        length.append(datum.d)

      plt.title('Cell instance perimeter signal')
      plt.xlabel('Angle (degrees)')
      plt.ylabel('Distance from center of cell  ')

      plt.plot(angle, length)
      plt.show()
