# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# local
from apps.img.models import *
from apps.cell.models import Cell, CellInstance

# util
import os
import numpy as np
from scipy.misc import imsave
import matplotlib.pyplot as plt

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

      for cell in series.cells.all():
        cell.calculate_velocity()

      with open(os.path.join(settings.DATA_DIR, series.experiment.name, str(series.index), 'cp/out/cell_instances.csv'), 'w') as open_ci:
        open_ci.write('frame, id, x (um), y (um), v (um/minute), A (um^2)\n')
        for ci in series.cell_instances.all():
          open_ci.write('%d,%d,%f,%f,%f,%f\n'%(ci.frame.index, ci.cell.pk, ci.x(), ci.y(), ci.v(), ci.a()))
