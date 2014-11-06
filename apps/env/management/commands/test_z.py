#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance
from apps.image.models import SourceImage
from apps.image.util import get_neighbour_image

#util
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.misc import imsave
import scipy
from scipy.ndimage import distance_transform_edt

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      experiment_name = '050714'
      series_index = 13
      cell_index = 1
      timestep_index = 11

      cell_instance = CellInstance.objects.get(experiment__name=experiment_name, series__index=series_index, cell__index=cell_index, timestep__index=timestep_index)
      mask = np.invert(cell_instance.mask_image())

      focus_image_set = SourceImage.objects.filter(experiment=cell_instance.experiment, series=cell_instance.series, timestep=cell_instance.timestep, channel=0)

      #testing volume and surface area

      #1. find z position
      mean_list = []
      masked_images = []
      for image in focus_image_set.order_by('focus'):
        #load
        image.load()

        #cut to bounding box
        cut_image = cell_instance.cell.bounding_box.get().cut(image.array)

        #apply mask
        masked_image = np.ma.array(cut_image, mask=mask, fill_value=0)
        masked_images.append(masked_image)

        mean_list.append(masked_image.mean())

#       plt.plot(np.array(mean_list)/np.max(mean_list))
      position_z = np.argmax(mean_list)

      #2. using mean of center image as threshold, count pixels in each z that surpass it.
      pixels_list = []

      #make sure range does not overlap
      z_min = position_z-10 if position_z-10>=0 else 0
      z_max = position_z+10 if position_z+10<len(mean_list) else len(mean_list)

      for image in masked_images[z_min:z_max]:
        pixels = (image>mean_list[position_z]).sum()
        pixels_list.append(pixels)

      #for pixel distribution
      area = cell_instance.mask_image().sum()/255.0
      area_list = area*(np.array(pixels_list)-np.min(pixels_list))/(np.max(pixels_list)-np.min(pixels_list))

      #volume
      volume = area_list.sum()

      #surface area
      surface_area = 0
      for z_area in area_list:
        eroded_mask = cell_instance.mask_image()
        #erode model until it matches the area
        while eroded_mask.sum()>z_area:
          eroded_mask = scipy.ndimage.binary_erosion(eroded_mask).astype(eroded_mask.dtype)

        #get edge of model
        if eroded_mask.sum()>0:
          transform = distance_transform_edt(eroded_mask)
          transform[transform==0] = transform.max() #max all zeros equal to max
          edge = np.argwhere(transform==transform.min()) #edge is the min of the new transform image -> (n, 2) np array
          surface_area += edge.shape[0]

      print(surface_area)

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
