#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance
from apps.image.models import SourceImage

#util

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      #1. get specific cell_instance for testing
      experiment_name = '050714'
      series_index = 13
      cell_index = 4
      timestep_index = 30

      cell_instance = CellInstance.objects.get(experiment__name=experiment_name, series__index=series_index, cell__index=cell_index, timestep__index=timestep_index)
      cell_instance.run_calculations()

      #2. get list of image files in the z-stack
#       z_image_set = SourceImage.objects.filter(experiment__name=experiment_name, series__index=series_index, timestep__index=timestep_index, channel=0)

      #3. get image arrays, but cropped with the bounding box of the cell_instance


#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
