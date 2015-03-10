# apps.cell.models

# django
from django.db import models

# local
from apps.img.models import *

### Cell
class Cell(models.Model):

  # connections
  experiment = models.ForeignKey(Experiment, related_name='cells')
  series = models.ForeignKey(Series, related_name='cells')

  # properties
  index = models.IntegerField(default=0)
  barrier_enter_frame = models.IntegerField(default=-1)

  # methods
  

### CellInstance
class CellInstance(models.Model):

  # connections
  region = models.ForeignKey(Region, related_name='cell_instances')
  experiment = models.ForeignKey(Experiment, related_name='cell_instances')
  series = models.ForeignKey(Series, related_name='cell_instances')
  cell = models.ForeignKey(Cell, related_name='instances')
  frame = models.ForeignKey(Frame, related_name='cell_instances')

  # properties
  row = models.IntegerField(default=0)
  column = models.IntegerField(default=0)
  level = models.IntegerField(default=0)

  velocity_rows = models.IntegerField(default=0)
  velocity_columns = models.IntegerField(default=0)
  velocity_levels = models.IntegerField(default=0)

  volume = models.IntegerField(default=0)
  area = models.IntegerField(default=0)

  # methods


### Extension
class Extension(models.Model):

  # connections
  region = models.ForeignKey(Region, related_name='extensions')
  cell = models.ForeignKey(Cell, related_name='extensions')
  cell_instance = models.ForeignKey(CellInstance, related_name='extensions')
