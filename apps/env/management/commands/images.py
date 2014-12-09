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
      brightfield_set = SourceImage.objects.filter(experiment__name=experiment_name, series__index=series_index, timestep__index=timestep_index, channel=0)

      output_path = os.path.join('/','Volumes','transport','data','imgrec','out')

      for image in brightfield_set:
        image.load()
        imsave(os.path.join(output_path, image.file_name), image.array)
