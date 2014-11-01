#django
from django.db import models

#local
from apps.env.models import Region, Experiment, Series, Timestep

#util


### Cell
class Cell(models.Model):
  #connections
  experiment = models.ForeignKey(Experiment, related_name='cells')
  series = models.ForeignKey(Series, related_name='cells')

  #properties


  #methods


### CellInstance
class CellInstance(models.Model):
  #connections
  region = models.ForeignKey(Region, related_name='cell_instances')
  experiment = models.ForeignKey(Experiment, related_name='cell_instances')
  series = models.ForeignKey(Series, related_name='cell_instances')
  cell = models.ForeignKey(Cell, related_name='cell_instances')
  timestep = models.ForeignKey(Timestep, related_name='cell_instances')

  #properties
  #-position and velocity
  position_x = models.IntegerField(default=0)
  position_y = models.IntegerField(default=0)
  position_z = models.IntegerField(default=0)

  velocity_x = models.IntegerField(default=0)
  velocity_y = models.IntegerField(default=0)
  velocity_z = models.IntegerField(default=0)

  displacement_x = models.IntegerField(default=0)
  displacement_y = models.IntegerField(default=0)
  displacement_z = models.IntegerField(default=0)

  #-volume and surface area
  volume = models.IntegerField(default=0)
  surface_area = models.IntegerField(default=0)

  #-extensions
  max_extension_length = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)

  #methods
  def run_calculations(self, ):
    #1.
    pass

  def rescale_model_image(self, ):
    pass

  def calculate_position(self, ):
    pass

  def calculate_extensions(self, ):
    pass

  def calculate_volume_and_surface_area(self, ):
    pass

### BoundingBox
class BoundingBox(models.Model):
  #connections
  cell = models.OneToOneField(Cell, related_name='bounding_box')

  #properties
  x = models.IntegerField(default=0)
  y = models.IntegerField(default=0)
  w = models.IntegerField(default=0)
  h = models.IntegerField(default=0)

  #methods
  #-convert for use in things

### Extension
class Extension(models.Model):
  #connections
  region = models.ForeignKey(Region, related_name='extensions')
  cell = models.ForeignKey(Cell, related_name='extensions')
  cell_instance = models.ForeignKey(CellInstance, related_name='extensions')

  #properties
  length = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
  angle = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
