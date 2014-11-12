#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell
from apps.env.models import Region

#util
import matplotlib.pyplot as plt
import numpy as np
import math

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):

      ### SINGLE
      experiment_name = '050714'
      series_index = 13
      cell_index = 1
      timestep_index = 1

      cell_instance = CellInstance.objects.get(experiment__name=experiment_name, series__index=series_index, cell__index=cell_index, timestep__index=timestep_index)
      cell_instance.position_volume_and_surface_area()

      ### ALL
#       for cell_instance in CellInstance.objects.all():
#         self.stdout.write('running calculations for CellInstance %d: %s, %d, %d, %d'%(cell_instance.pk, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))
#         cell_instance.run_calculations()

      ### SINGLE
#       experiment_name = '050714'
#       series_index = 13
#       cell_index = 1

#       cell = Cell.objects.get(experiment__name=experiment_name, series__index=series_index, index=cell_index)
#       cell.run_calculations()

      ### ALL
#       for cell in Cell.objects.all():
#         self.stdout.write('processing cell %d: %s, %d'%(cell.index, cell.experiment.name, cell.series.index))
#         cell.run_calculations()

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
