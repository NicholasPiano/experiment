#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell
from apps.env.models import Region
from apps.image.util.life.life import Life
from apps.image.util.life.rule import *
from apps.image.util.tools import get_surface_elements

#util
import matplotlib.pyplot as plt
import numpy as np
import math
import os
from scipy.misc import imsave

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      #get cell_instance details
#       experiment_name = '050714'
#       series_index = 14
#       cell_index = 1
#       timestep_index = 11

#       cell_instance = CellInstance.objects.get(experiment__name=experiment_name, series__index=series_index, cell__index=cell_index, timestep__index=timestep_index)
#       print([cell_instance.volume, cell_instance.surface_area])
#       cell_instance.position_volume_surface_area()
      total = CellInstance.objects.count()
      for cell_instance in CellInstance.objects.all():
        self.stdout.write('%d of %d: %s %d %d %d'%(cell_instance.pk, total, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))
        cell_instance.position_volume_surface_area()

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
