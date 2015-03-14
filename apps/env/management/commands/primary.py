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

    # make primary objects for each set
    for series in series_set:
      gfp_set = series.images.filter(channel__index=1)

      for frame in series.frames.order_by('index'):
        print('%s %s' % (series, frame))

        b = np.zeros(series.shape())

        for cell_instance in series.cell_instances.filter(frame=frame):
          # draw circle
            xx, yy = np.mgrid[:b.shape[0], :b.shape[1]]
            circle = (xx - cell_instance.row) ** 2 + (yy - cell_instance.column) ** 2 # distance from c
            b[circle<10] = 255 # radius of 10 px

        # output to cp-in
        output_path = os.path.join(settings.DATA_DIR, series.experiment.name, str(series.index), 'cp/in')
        output_file_name = 'primary_f%s.tif' % str(frame)
        imsave(os.path.join(output_path, output_file_name), b)
