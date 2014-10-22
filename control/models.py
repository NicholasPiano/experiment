#control.models

#django
from django.db import models

#local

#util

# Create your models here.
class Experiment(models.Model): #contains everything about a certain experiment
  #sub: Series, Timestep,

  #properties
  name = models.CharField(default='name', max_length=255)

  #-paths
  base_path = models.CharField(default='base_path', max_length=255)
  input_path = models.CharField(default='input_path', max_length=255) #appended to base_path
  output_path = models.CharField(default='output_path', max_length=255)

  #-scaling
  x_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  y_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  z_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)

  #methods
  def gather_from_input(self):
    #get list of files
    file_list = [image_file_name for image_file_name in os.listdir(self.input_path) if re.search(r'\.ti[f]{1,2}$', image_file_name) is not None]

    for file_name in file_list:
      #extract data from file name
      template = self.image_templates.get(name='input')
      match = re.match(template, file_name)

      series = self.series.get_or_create(index=match.group('series'))
      timestep = self.timesteps.get_or_create(series=series, index=match.group('timestep'))
      channel = int(match.group('channel'))
      focus = int(match.group('focus'))

      self.images.create(series=series, timestep=timestep, channel=channel, focus=focus)

class Series(models.Model):
  #sub:

  #properties
  experiment = models.ForeignKey(Experiment, related_name='series')
  index = models.IntegerField(default=0)

  #methods

class Timestep(models.Model):
  #sub:

  #properties
  experiment = models.ForeignKey(Experiment, related_name='timesteps')
  series = models.ForeignKey(Series, related_name='timesteps')
  index = models.IntegerField(default=0)

  #methods

class Region(models.Model): #a single region of the experiment. Changes with time
  #sub:

  #properties
  experiment = models.ForeignKey(Experiment, related_name='regions')
  index = models.IntegerField(default=0)

  #methods

class Cell(models.Model): #contains all information about a single cell
  #sub: CellInstance, Extension

  #properties
  series = models.ForeignKey(Series, related_name='cells')

  #methods

class CellInstance(models.Model): #describes single cell at a particular timestep
  #sub:

  #properties
  cell = models.ForeignKey(Cell, related_name='cell_instances')
  region = models.ForeignKey(Region, related_name='cell_instances')
  timestep = models.ForeignKey(Timestep, related_name='cell_instances')

  #-position and velocity
  position_x = models.IntegerField(default=0)
  position_y = models.IntegerField(default=0)
  position_z = models.IntegerField(default=0)

  velocity_x = models.IntegerField(default=0)
  velocity_y = models.IntegerField(default=0)
  velocity_z = models.IntegerField(default=0)

  max_z = models.IntegerField(default=0) #focus extent of cell
  min_z = models.IntegerField(default=0)

  #methods

class Extension(models.Model): #contains a single cell protrusion length
  #sub:

  #properties
  cell = models.ForeignKey(Cell, related_name='extensions')
  cell_instance = models.ForeignKey(CellInstance, related_name='extensions')

  length = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)

  #methods
