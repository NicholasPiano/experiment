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
from mpl_toolkits.mplot3d import Axes3D

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      cell_instance = CellInstance.objects.get(pk=747)
      pks = [191,232,574,747] #region 4,3,2,1

      #1. get outline of mask

      #2. get gfp model
      model = reconstruction(747, ones=True)
      z,x,y = model.nonzero()

      #3. put in array with sphere of radius 14 microns

      #4. print out image series to a set of images.

      #3D reconstruction

      fig = plt.figure()
      ax = fig.add_subplot(111, projection='3d')
      ax.scatter(x, y, -z, zdir='z', c='red')

      plt.show()
