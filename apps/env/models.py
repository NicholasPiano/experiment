#apps.env.models

#django
from django.db import models

#local
from apps.cell.data import access

#util
import os

### Region
class Region(models.Model):

  #properties
  name = models.CharField(max_length=1)
  index = models.IntegerField(default=0)
  description = models.TextField(default='description')

### Experiment
class Experiment(models.Model):

  #properties
  name = models.CharField(max_length=255)

  #-paths
  base_path = models.CharField(default='base_path', max_length=255)
  input_path = models.CharField(default='input_path', max_length=255) #appended to base_path
  segmented_path = models.CharField(default='segmented_path', max_length=255)

  #-scaling
  x_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  y_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  z_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  time_per_frame = models.DecimalField(default=0.0, decimal_places=4, max_digits=10)

  #methods
  def create_images_from_input_directory(self):
    #1. get list of files
    input_path = os.path.join(self.base_path, self.input_path)
    file_list = [image_file_name for image_file_name in os.listdir(input_path) if re.search(r'\.ti[f]{1,2}$', image_file_name) is not None]
    template = self.image_templates.get(name='input')

    #2. extract details from each file_name and get or create objects
    for file_name in file_list:
      print('processing ... ' + file_name)
      match = template.match(file_name)

      series, created = self.series.get_or_create(index=match.group('series'))
      timestep, created = self.timesteps.get_or_create(series=series, index=match.group('timestep'))
      channel = int(match.group('channel'))
      focus = int(match.group('focus'))

      self.images.get_or_create(file_name=file_name, input_path=input_path, series=series, timestep=timestep, channel=channel, focus=focus)

  def create_cells_from_segmented_directory(self):
    pass

### Series
class Series(models.Model):

  #connections
  experiment = models.ForeignKey(Experiment, related_name='series')

  #properties
  index = models.IntegerField(default=0)
  max_timestep = models.IntegerField(default=0)
  max_focus = models.IntegerField(default=0)

### Timestep
class Timestep(models.Model):

  #connections
  experiment = models.ForeignKey(Experiment, related_name='timesteps')
  series = models.ForeignKey(Series, related_name='timesteps')

  #properties
  index = models.IntegerField(default=0)
