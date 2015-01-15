#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

#local
from apps.cell.models import CellInstance, Cell
from apps.env.models import Region
from apps.image.util.life.life import Life
from apps.image.util.life.rule import *
from apps.image.util.tools import get_surface_elements, array_to_vmd_xyz

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

      cell_instances = sorted(CellInstance.objects.all(), key=lambda x: sum([float(extension.length) for extension in x.extensions.all()]))

      cell_instance = cell_instances[100]

      mask = cell_instance.mask_array()
#       model = cell_instance.reconstruction_3D()

#       array_to_vmd_xyz(model, settings.PLOT_DIR, '%d.xyz'%(cell_instance.pk))
