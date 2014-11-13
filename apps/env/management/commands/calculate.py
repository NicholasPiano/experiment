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
      pass

      ### SINGLE
#       experiment_name = '050714'
#       series_index = 13
#       cell_index = 1
#       timestep_index = 1

      experiment_name = '190714'
      series_index = 13
      cell_index = 1
      timestep_index = 20

      cell_instance = CellInstance.objects.get(experiment__name=experiment_name, series__index=series_index, cell__index=cell_index, timestep__index=timestep_index)

      print(cell_instance.volume)
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
#       cell_instance_set = CellInstance.objects.filter(position_z__lt=10)

#       for cell_instance in cell_instance_set:
#         print('cell_instance %d: %s, %d, %d, %d, %d'%(cell_instance.pk, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index, cell_instance.region.index))

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
