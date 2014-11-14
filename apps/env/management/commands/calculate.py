#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell
from apps.env.models import Region

#util
import os
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.misc import imsave
from scipy.ndimage import binary_dilation as dilate

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      for cell_instance in CellInstance.objects.all():
        #print details
        self.stdout.write('CellInstance %d: %s, %d, %d, %d'%(cell_instance.pk, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))

        #print out outline of bounding box onto original bf image
        brightfield_image = cell_instance.experiment.images.get(series=cell_instance.series, timestep=cell_instance.timestep, focus=cell_instance.position_z, channel=1)
        (x,y,w,h) = cell_instance.cell.bounding_box.get().all()

        brightfield_image.load()

        bf_array = brightfield_image.array
        bf_max = bf_array.max()

        outline_image = np.zeros(bf_array.shape, dtype=bool)

        #bounding box
        outline_image[y:y+h-1,x] = True
        outline_image[y:y+h-1,x+w] = True
        outline_image[y,x:x+w-1] = True
        outline_image[y+h-1,x:x+w-1] = True

        #cell instance mask
        mask_array = cell_instance.mask_image().astype(int)
        mask_array[mask_array==255] = 1
        dilated_mask_array = dilate(mask_array)

        edge_array = np.array(dilated_mask_array - mask_array, dtype=bool)

        outline_image[y+1:y+h-1,x+1:x+w-1] = edge_array[1:-1,1:-1]

        #apply outline
        bf_array[outline_image] = 255

        file_name = '%d_%d_'%(cell_instance.pk, cell_instance.cell.index) + brightfield_image.file_name

        imsave(os.path.join(cell_instance.experiment.base_path, 'test', 'all', file_name), bf_array)

      ### SINGLE
#       experiment_name = '050714'
#       series_index = 13
#       cell_index = 1
#       timestep_index = 1

#       experiment_name = '190714'
#       series_index = 13
#       cell_index = 1
#       timestep_index = 20

#       cell_instance = CellInstance.objects.get(experiment__name=experiment_name, series__index=series_index, cell__index=cell_index, timestep__index=timestep_index)
#       cell_instance.save_image_stages()

      ### ALL
#       for cell_instance in CellInstance.objects.all():
#         self.stdout.write('running calculations for CellInstance %d: %s, %d, %d, %d'%(cell_instance.pk, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))
#         cell_instance.run_calculations()

      ### SINGLE
#       experiment_name = '050714'
#       series_index = 13
#       cell_index = 1

#       cell = Cell.objects.get(experiment__name=experiment_name, series__index=series_index, index=cell_index)
#       cell.run_calculations()

      ### ALL
#       for cell in Cell.objects.all():
#         self.stdout.write('processing cell %d: %s, %d'%(cell.index, cell.experiment.name, cell.series.index))
#         cell.run_calculations()
#       cell_instance_set = CellInstance.objects.filter(position_z__lt=10)

#       for cell_instance in cell_instance_set:
#         print('cell_instance %d: %s, %d, %d, %d, %d'%(cell_instance.pk, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index, cell_instance.region.index))

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
