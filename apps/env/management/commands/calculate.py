#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell
from apps.env.models import Region

#util
import os
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.misc import imsave
from scipy.ndimage import binary_dilation as dilate

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):

