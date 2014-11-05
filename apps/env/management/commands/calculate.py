#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance

#util

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      #all cell_instances
      for cell_instance in CellInstance.objects.filter(pk=1225):
        self.stdout.write('processing cell instance %d: %s, %d, %d, %d'%(cell_instance.pk, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))
        cell_instance.run_calculations()

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
