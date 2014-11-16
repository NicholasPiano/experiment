#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.env.models import Region, Experiment
from apps.cell.models import Cell, CellInstance
from apps.env.data import regions, experiments, templates

#util
from datetime import datetime as dt

class Command(BaseCommand):
    args = '<none>'
    help = 'Populate database with predefined region, experiment, and cell objects'

    def handle(self, *args, **options):
      start = dt.now()
      print(start)
      #1. create regions from prototypes
      all_created = 0
      for r in regions:
        region, created = Region.objects.get_or_create(name=r.name, index=r.index, description=r.description)
        if created:
          all_created += 1
          self.stdout.write('created region %s' % region.name)

      self.stdout.write('created %d regions' % all_created)

      #2. create experiments and create input and segmented images
      all_created = 0
      for e in experiments:
        experiment, created = Experiment.objects.get_or_create(name=e.name)
        if created:
          experiment.base_path=e.base_path
          experiment.x_microns_over_pixels=e.x_microns_over_pixels
          experiment.y_microns_over_pixels=e.y_microns_over_pixels
          experiment.z_microns_over_pixels=e.z_microns_over_pixels
          experiment.time_per_frame=e.time_per_frame
          experiment.save()

          all_created += 1

          for template in templates:
            experiment.image_templates.create(name=template.name, rx=template.rx, reverse=template.reverse)

          self.stdout.write('created experiment %s' % experiment.name)

      self.stdout.write('created %d experiments' % all_created)

      #3. for each experiment now in the database, get input and segmented
      for experiment in Experiment.objects.all():
        experiment.create_cells_from_segmented_directory()
        experiment.create_images_from_input_directory()

      #4. run individual cell_instance calculations
      for cell_instance in CellInstance.objects.all():
        self.stdout.write('cell instance %d: %s, %d, %d, %d'%(cell_instance.pk, cell_instance.experiment.name, cell_instance.series.index, cell_instance.cell.index, cell_instance.timestep.index))
        cell_instance.run_calculations()

      #5. run combined cell calculations
      for cell in Cell.objects.all():
        self.stdout.write('cell %d: %s, %d, %d'%(cell.pk, cell.experiment.name, cell.series.index, cell.index))
        cell.run_calculations()

      total_time = dt.now() - start
      print([start, total_time])

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
