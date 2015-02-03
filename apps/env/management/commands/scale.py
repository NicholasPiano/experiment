#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import Cell
from apps.env.models import Experiment, Series

#util


class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    #1. redo all timepoint scalings from images
    scaling_dictionary = {
      '260714':(0.5702,0.5696,1.482,7.68066666666667),
      '190714':(0.5015,0.501,1.482,9.74083333333333),
      '050714':(0.5369,0.5369,1.482,10.70033333333333),
    }

    for experiment_name, (x_microns_over_pixels, y_microns_over_pixels, z_microns_over_pixels, time_per_frame) in scaling_dictionary.items():
      experiment = Experiment.objects.get(name=experiment_name)
      experiment.x_microns_over_pixels = x_microns_over_pixels
      experiment.y_microns_over_pixels = y_microns_over_pixels
      experiment.z_microns_over_pixels = z_microns_over_pixels
      experiment.time_per_frame = time_per_frame
      experiment.save()
