# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# local
from apps.img.models import *

# util
import os
import numpy as np

### Command
# https://docs.djangoproject.com/en/1.7/howto/custom-management-commands/
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    # load exactly one image and set dimensions from that image
    for series in Series.objects.all():

      # rows and columns
      gfp_image = series.images.get(channel__index=0, frame__index=0, level=0)
      gfp_image.load()
      series.rows = gfp_image.array.shape[0]
      series.columns = gfp_image.array.shape[1]

      # set levels
      z_set = series.images.filter(channel__index=0, frame__index=0)
      series.levels = z_set.count()

      # set channels
      c_set = series.images.filter(frame__index=0, level=0)
      series.max_channels = c_set.count()

      # set frames
      f_set = series.images.filter(channel__index=0, level=0)
      series.max_frames = f_set.count()

      series.save()
