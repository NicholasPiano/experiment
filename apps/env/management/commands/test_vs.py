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


