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
      for cell_instance in CellInstance.objects.all():
        self.stdout.write('running calculations for CellInstance %d: %s, %d, %d, %d'%(cell_instance.pk, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))
        cell_instance.run_calculations()

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
