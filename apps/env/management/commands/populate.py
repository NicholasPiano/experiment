#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.env.models import Region, Experiment
from apps.env.data import regions, experiments, templates

#util

class Command(BaseCommand):
    args = '<none>'
    help = 'Populate database with predefined region, experiment, and cell objects'

    def handle(self, *args, **options):
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
          experiment.input_path=e.input_path
          experiment.segmented_path=e.segmented_path
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
#         experiment.create_images_from_input_directory()


#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
