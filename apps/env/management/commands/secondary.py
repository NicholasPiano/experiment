# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# local
from apps.img.models import *

# util
import os
import numpy as np
from scipy.misc import imsave
from scipy.ndimage.filters import gaussian_filter as gf
from skimage import exposure

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
      gfp_set = series.images.filter(channel__index=0)
      bf_set = series.images.filter(channel__index=1, level=30)

      for frame in series.frames.order_by('index'):
        print('%s %s' % (series, frame))

        gfp_frame = gfp_set.filter(frame=frame)
        bf_frame = bf_set.get(frame=frame)

        # gfp sum
        gfp_sum = np.zeros(series.shape())
        for gfp_level in gfp_frame:
          gfp_level.load()
          gfp_sum += gfp_level.array

        # threshold
        gfp_thresh = np.array(gfp_sum)
        gfp_thresh[gfp_thresh<gfp_thresh.mean()] = 0

        # smooth
        gfp_smooth = gf(gfp_thresh, 5)
        gfp = exposure.rescale_intensity(gfp_smooth)

        # take bright field slice
        bf = bf_frame.load()

        out = bf * gfp * gfp

        # output to cp-in
        output_path = os.path.join(settings.DATA_DIR, series.experiment.name, str(series.index), 'cp/in')
        output_file_name = 'secondary_f%s.tif' % str(frame)
        imsave(os.path.join(output_path, output_file_name), out)
