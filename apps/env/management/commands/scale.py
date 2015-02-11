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
    #print scales for each experiment
    for s in Series.objects.all():
      #scales
      x_microns_over_pixels = float(s.experiment.x_microns_over_pixels)
      y_microns_over_pixels = float(s.experiment.y_microns_over_pixels)
      z_microns_over_pixels = float(s.experiment.z_microns_over_pixels)
      time_per_frame = float(s.experiment.time_per_frame)

      #load first image
      image = s.experiment.images.get(series__index=s.index, timestep__index=0, channel=0, focus=0)
      image.load()
      shape = image.array.shape

      print([s.experiment.name, s.index, shape, x_microns_over_pixels, y_microns_over_pixels, z_microns_over_pixels, time_per_frame])
