#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell
from apps.env.models import Region
from apps.image.util.life.life import Life
from apps.image.util.life.rule import *
from apps.image.util.tools import get_surface_elements

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
      cell_instance = CellInstance.objects.get(pk=747)

      #1. get outline of mask

      #2. get gfp model

      #3. put in array with sphere of radius 14 microns

      #4. print out image series to a set of images.

      #3D reconstruction
      pks = [191,232,574,747] #region 4,3,2,1

      for pk in pks:
        cell_instance = CellInstance.objects.get(pk=pk)
        self.stdout.write('CellInstance %d: %s, %d, %d, %d'%(cell_instance.pk, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))
        #1. resources
        #- mask
        mask = np.array(np.invert(cell_instance.mask_array()), dtype=bool)

        #- bounding box
        bounding_box = cell_instance.cell.bounding_box.get()

        #- focus image set
        focus_image_set = cell_instance.experiment.images.filter(series=cell_instance.cell.series, timestep=cell_instance.timestep, channel=0) #only gfp

        #2. first loop:
        #- load images
        #- cut to bounding box
        #- mask with segmented image
        #- get mean list
        mean_list = []
        array_3D = []
        for focus_image in focus_image_set.order_by('focus'):
          #load
          focus_image.load()
          #cut
          cut_image = bounding_box.cut(focus_image.array)
          #mask
          focus_image.array = np.ma.array(cut_image, mask=mask, fill_value=0)
          #mean
          mean_list.append(focus_image.array.mean()) # <<< mean list
          focus_image.mean = focus_image.array.mean()
          focus_image.save()
          #3D
          array_3D.append(focus_image.array.filled())
          focus_image.unload()

        global_mean = np.sum(mean_list)/float(len(mean_list))
        array_3D = np.array(array_3D)

        #3. second loop
        #- threshold
        array_3D_binary = np.zeros(array_3D.shape)
        array_3D_binary[array_3D>global_mean] = 1

        #- run life
        for i in range(array_3D.shape[0]):
          array_binary = array_3D_binary[i]

          life = Life(array_binary)
          life.ruleset = CoagulationsFillInVote()
          life.ruleset.timestamps = [2,4,4]
          life.update_cycle()

          array_3D_binary[i] = life.array

        #5. mask 3D array
        array_3D_masked = np.ma.array(array_3D, mask=np.invert(np.array(array_3D_binary), dtype=bool), fill_value=0)
        array_3D_masked = array_3D_masked.filled()

        #print
        for i in range(array_3D_masked.shape[0]):
          array_masked = array_3D_masked[i]
          file_name = 'image_pk%d_z%d.tiff'%(pk, i)
          imsave(os.path.join('/','Volumes','transport','data','confocal','3D',str(pk),file_name), array_masked)
