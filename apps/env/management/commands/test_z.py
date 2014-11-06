#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance
from apps.image.models import SourceImage

#util
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.misc import imsave

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

      z_image_set = SourceImage.objects.filter(experiment=cell_instance.experiment, series=cell_instance.series, timestep=cell_instance.timestep, channel=0)

      #testing volume and surface area

      #1. find z position
      mean_list = []
      for image in focus_image_set:
        #load
        image.load()

        #cut to bounding box
        cut_image = bounding_box.cut(image.array)

        #apply mask
        masked_image = np.ma.array(cut_image, mask=segmented_image, fill_value=0)

        mean_list.append(masked_image.mean())

      position_z = np.argmax(mean_list)

      #2. using mean of center image as threshold, count pixels in each zed that surpass it.


#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
