#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell
from apps.env.models import Region
from apps.image.util.life.life import Life
from apps.image.util.life.rule import *
from apps.image.util.tools import get_neighbour_array_3D

#util
import matplotlib.pyplot as plt
import numpy as np
import math
import os
from scipy.misc import imsave

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):

      #get cell_instance details
      experiment_name = '050714'
      series_index = 13
      cell_index = 1
      timestep_index = 1

      cell_instance = CellInstance.objects.get(experiment__name=experiment_name, series__index=series_index, cell__index=cell_index, timestep__index=timestep_index)

      #run volume and surface area calculations
      #1. resources:
      #- segmented image and mask
      segmented_image = cell_instance.mask_image() #numpy array
      mask = np.array(np.invert(segmented_image), dtype=bool) #true values are ignored

      #- bounding box
      bounding_box = cell_instance.cell.bounding_box.get()

      #- focus image set
      focus_image_queryset = cell_instance.experiment.images.filter(series=cell_instance.series, timestep=cell_instance.timestep, channel=0)

      #convert image set and run life for noise reduction
      global_mean = 0
      for focus_image in focus_image_queryset:
        #load and cut
        focus_image.load()
        new_array = bounding_box.cut(focus_image.array)

        #mask and fill
        new_array = np.ma.array(new_array, mask=mask, fill_value=0)
        global_mean += new_array.mean()/focus_image_queryset.count()
        new_array = new_array.filled()

        focus_image.array = new_array

      #run life
      array_3D = []
      for focus_image in focus_image_queryset:
        focus_image.array[focus_image.array<global_mean] = 0
        focus_image.array[focus_image.array>0] = 1

        #life
        life = Life(focus_image.array)
        life.ruleset = CoagulationsFillInVote()
        life.ruleset.timestamps = [2,4,4]
        life.update_cycle()

        focus_image.array = life.array
        focus_image.array[focus_image.array==1] = 255
        array_3D.append(life.array)
      array_3D = np.array(array_3D)

      get_neighbour_array_3D(np.array([[1,0,1],[1,1,0],[0,0,1]]))

      #print all images to output
#       output_path = os.path.join(cell_instance.experiment.base_path, 'test', 'output')
#       for focus_image in focus_image_queryset:
#         imsave(os.path.join(output_path, focus_image.file_name), focus_image.array)



#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
