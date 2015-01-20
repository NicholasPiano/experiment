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
    cell_instance = CellInstance.objects.get(pk=931)

    #get masked brightfield at level of brightest GFP
    bf = cell_instance.brightfield_3D_array()
    print(bf.shape)
#     gfp = cell_instance.gfp_3D_array()

    #mask
#       mask = cell_instance.mask_array()
#       print(center_of_mass(mask)) #gives 209 row, 375 column

    #going down through the levels in a sigle column, get the values of each row as an array
    fig = plt.figure()
#     out = os.path.join(settings.PLOT_DIR, 'intensity', 'stack_%d.png')
    out = os.path.join(settings.PLOT_DIR, 'image', 'stack_%d.png')
    for i, stack in enumerate(bf):
      ax = fig.add_subplot(111)
#       ax.set_ylim([0,350])
#       for j, sl in enumerate(stack):
#         a = []
#         for pixel in sl:
#           a.append(int(pixel+10*j))

#         ax.plot(a)
      ax.imshow(stack)
      plt.savefig(out%i)
      plt.cla()
