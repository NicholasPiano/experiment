#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

#local
from apps.cell.models import CellInstance, Cell
from apps.env.models import Region
from apps.env.models import Experiment, Series
from apps.image.util.life.life import Life
from apps.image.util.life.rule import *
from apps.image.util.tools import get_surface_elements, array_to_vmd_xyz, array_to_matlab_script, array_to_vmd_vtf

#util
import matplotlib.pyplot as plt
import numpy as np
import math
import os
from scipy.misc import imsave
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage.measurements import center_of_mass

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    cell_instance = CellInstance.objects.get(pk=2)

    for cell_instance in CellInstance.objects.all():
      (array_3D_masked, mean_list, above_mean_list, global_mean, above_global_mean_list) = cell_instance.volume_test()
      s = (array_3D_masked>0).sum()
      print([cell_instance.pk, cell_instance.volume, s])
      cell_instance.volume = s
      cell_instance.save()
