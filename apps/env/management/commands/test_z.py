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

      ### SINGLE CELL INSTANCE
      #1. get specific cell_instance for testing
      experiment_name = '050714'
      series_index = 13
      cell_index = 1
      timestep_index = 11

      cell_instance = CellInstance.objects.get(experiment__name=experiment_name, series__index=series_index, cell__index=cell_index, timestep__index=timestep_index)

      mask = np.invert(cell_instance.mask_image())

      #2. get list of image files in the z-stack
      z_image_set = SourceImage.objects.filter(experiment=cell_instance.experiment, series=cell_instance.series, timestep=cell_instance.timestep, channel=0)

      #- mean and max intentity
      #3. get image arrays, but cropped with the bounding box of the cell_instance
      max_list = []
      mean_list = []

      for image in z_image_set:
        #load
        image.load()

        #cut to bounding box
        cut_image = cell_instance.cell.bounding_box.get().cut(image.array)

        #apply mask
        masked_image = np.ma.array(cut_image, mask=mask, fill_value=0)

        max_list.append(masked_image.max())
        mean_list.append(masked_image.mean())

      max_list = np.array(max_list)/float(np.max(max_list))
      mean_list = np.array(mean_list)/float(np.max(mean_list))

      plt.plot(max_list, label='max')
      plt.plot(mean_list, label='mean')

      plt.legend(loc='upper left', numpoints = 1)
      plt.show()
#       output_path = os.path.join(cell_instance.experiment.base_path, 'plot', '%s_%d_%d_%d'%(cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))
#       plt.savefig(output_path)
#       plt.close()

      #- rescaled area
      #3. get image arrays, but cropped with the bounding box of the cell_instance
#       area_list = []

#       for image in z_image_set:
#         #load
#         image.load()

#         #cut to bounding box
#         cut_image = cell_instance.cell.bounding_box.get().cut(image.array)

#         #apply mask
#         masked_image = np.ma.array(cut_image, mask=mask, fill_value=0)

#         max_list.append(masked_image.max())
#         mean_list.append(masked_image.mean())

#       max_list = np.array(max_list)/float(np.max(max_list))
#       mean_list = np.array(mean_list)/float(np.max(mean_list))

#       plt.plot(max_list, label='max')
#       plt.plot(mean_list, label='mean')

#       plt.legend(loc='upper left', numpoints = 1)
#       plt.show()

      #- print images
      #3. get image arrays, but cropped with the bounding box of the cell_instance
#       for image in z_image_set:
#         #load
#         image.load()

#         #cut to bounding box
#         cut_image = cell_instance.cell.bounding_box.get().cut(image.array)

#         #apply mask
#         masked_image = np.ma.array(cut_image, mask=mask, fill_value=0)

#         output_path = os.path.join(cell_instance.experiment.base_path, 'mask', image.file_name)
#         imsave(output_path, masked_image.filled())

      ### ALL CELL INSTANCES
#       for cell_instance in CellInstance.objects.all():
#         mask = np.invert(cell_instance.mask_image())

#         #2. get list of image files in the z-stack
#         z_image_set = SourceImage.objects.filter(experiment=cell_instance.experiment, series=cell_instance.series, timestep=cell_instance.timestep, channel=0)

#         #- mean and max intentity
#         #3. get image arrays, but cropped with the bounding box of the cell_instance
#         max_list = []
#         mean_list = []

#         for image in z_image_set:
#           #load
#           image.load()

#           #cut to bounding box
#           cut_image = cell_instance.cell.bounding_box.get().cut(image.array)

#           #apply mask
#           masked_image = np.ma.array(cut_image, mask=mask, fill_value=0)

#           max_list.append(masked_image.max())
#           mean_list.append(masked_image.mean())

#         max_list = np.array(max_list)/float(np.max(max_list))
#         mean_list = np.array(mean_list)/float(np.max(mean_list))

#         plt.plot(max_list, label='max')
#         plt.plot(mean_list, label='mean')

#         plt.legend(loc='upper left', numpoints = 1)
#         output_path = os.path.join(cell_instance.experiment.base_path, 'plot', '%s_%d_%d_%d'%(cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))
#         plt.savefig(output_path)
#         plt.close()


#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
