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
      #load brightfield and gfp for cell instance 747
      cell_instance = CellInstance.objects.get(pk=747)

      experiment_name = cell_instance.experiment.name
      print(experiment_name)
