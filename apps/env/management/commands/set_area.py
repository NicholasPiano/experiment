# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# local
from apps.img.models import *
from apps.cell.models import CellInstance

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

      # load cell profiler output files:
      # 1. MaskedCells.csv
      masked_cells = []
      with open(os.path.join(settings.DATA_DIR, series.experiment.name, str(series.index), 'cp/out/MaskedCells.csv')) as open_masked:
        for i, line in enumerate(open_masked.readlines()[1:]):
          tokens = [float(lm) for lm in line.rstrip().split(',')]
          cell_dict = {
            'frame':int(tokens[0]-1),
            'row_f':tokens[21],
            'column_f':tokens[20],
            'area':int(tokens[2]),
            'ecc':tokens[6],
            'parent':int(tokens[23]),
          }
          masked_cells.append(cell_dict)

      # parents and frames
      unique_parents = list(np.unique([m['parent'] for m in masked_cells]))
      unique_frames = list(np.unique([m['frame'] for m in masked_cells]))

      # 2. MaskedNuclei.csv
      masked_nuclei = []
      with open(os.path.join(settings.DATA_DIR, series.experiment.name, str(series.index), 'cp/out/MaskedNuclei.csv')) as open_masked:
        for i, line in enumerate(open_masked.readlines()[1:]):
          tokens = [float(lm) for lm in line.rstrip().split(',')]
          cell_dict = {
            'frame':int(tokens[0]-1),
            'row_f':tokens[21],
            'column_f':tokens[20],
            'area':-1,
            'ecc':-1,
            'parent':int(tokens[23]),
          }
          masked_nuclei.append(cell_dict)

      # 1. for each instance in C, match 'parent object' with N -> transfer area
      for frame in unique_frames:

        cif = CellInstance.objects.filter(series=series, frame__index=frame)

        for parent in unique_parents:
          cell = filter(lambda x: x['frame']==frame and x['parent']==parent, masked_cells)
          nucleus = filter(lambda x: x['frame']==frame and x['parent']==parent, masked_nuclei)
          if nucleus and cell:
            cell = cell[0]
            nucleus = nucleus[0]

            # match nucleus with cell instance
            for c in cif:
              d = c.d(nucleus['row_f'], nucleus['column_f'])
              if d<4:
                # match has occurred
                c.area = cell['area']
                c.row = int(cell['row_f'])
                c.column = int(cell['column_f'])
                c.save()

      # 2. for each N, match instance by position
      # 3. set area of cell instance from N
      # 4. save
