#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone as tz

#local
from apps.cell.models import Cell
from apps.env.models import Experiment, Series

#util
import os
import numpy as np
from scipy.misc import imsave
from scipy.ndimage.morphology import binary_dilation as dilate
import matplotlib.pyplot as plt

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    #path
    path = '/Volumes/WINDOWSSWAP/Segmentation/img/050714'

    e = Experiment.objects.get(name='050714')

    count = e.images.count()
    start = tz.now()
    for i, image in enumerate(e.images.all()):
      image.load()
      imsave(os.path.join(path, image.file_name), image.array)
      time = tz.now() - start
      print('%s: %d/%d %s' % (str(time),i,count,image.file_name))
