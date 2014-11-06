#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance
from apps.image.models import SourceImage
from apps.image.util import get_neighbour_image

#util
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.misc import imsave
import scipy
from scipy.ndimage import distance_transform_edt

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
#       for cell_instance in CellInstance.objects.filter(pk__gt=303):
#         self.stdout.write('cell instance %d: %s, %d, %d, %d'%(cell_instance.pk, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))
#         cell_instance.run_calculations()
#         self.stdout.write('volume: %d, surface_area: %d'%(cell_instance.volume, cell_instance.surface_area))
        #get cell
      c = CellInstance.objects.get(experiment__name='260714', series__index=13, cell__index=2, timestep__index=33)
      c.calculate_volume_and_surface_area()

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
