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

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      cell_instance = CellInstance.objects.get(pk=931)

      print(cell_instance.surface_area)

      ###output mask to PLOT_DIR
#       out = os.path.join(settings.PLOT_DIR, 'mask', '%d.tiff') % cell_instance.pk
#       imsave(out, cell_instance.mask_array())


      ###get 3D reconstruction
#       array_3D_masked, mean_list, above_mean_list, global_mean, above_global_mean_list = cell_instance.volume_test(7) # 7 microns radius

#       volume = (array_3D_masked>0).sum()
#       area = (cell_instance.mask_array()).sum()

#       e = cell_instance.cell.experiment
#       x,y,z = e.x_microns_over_pixels, e.y_microns_over_pixels, e.z_microns_over_pixels

#       v = float(x*y*z)
#       a = float(x*y)

#       opi = 1.0/math.pi
#       tf = 3.0*opi/4.0

#       v0 = v*volume
#       a1 = a*area

#       print(v0)

#       plt.plot(np.arange(len(mean_list)), np.array(mean_list, dtype=float), label='local mean')
#       plt.plot(np.arange(len(mean_list)), np.array([float(global_mean)]*len(mean_list)), label='global mean')
#       plt.legend()
#       plt.title('Cell instance')
#       plt.xlabel('Z stack')
#       plt.ylabel('Normalised value')
#       plt.show()

#       array_to_vmd_xyz(array_3D_masked, settings.PLOT_DIR, '%d.xyz'%cell_instance.pk)
