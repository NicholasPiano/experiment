# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# local
from apps.img.models import *

# util
import os
import numpy as np
from scipy.misc import imsave

### Command
# https://docs.djangoproject.com/en/1.7/howto/custom-management-commands/
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    series_set = Series.objects.all()
    if args:
      series_set = Series.objects.filter(experiment__name__in=args)

    # make a gfp sum for each experiment
    for series in series_set:
      bf_set = series.images.filter(channel__index=1, level=30)

      for frame in series.frames.order_by('index'):
        print('%s %s' % (series, frame))

        bf_frame = bf_set.get(frame=frame)

        # take bright field slice
        bf = bf_frame.load()

        # output to cp-in
        output_path = os.path.join(settings.DATA_DIR, series.experiment.name, str(series.index), 'cp/in')
        output_file_name = 'bf_f%s.tif' % str(frame)
        imsave(os.path.join(output_path, output_file_name), bf)
