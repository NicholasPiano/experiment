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
  def calculate_velocity(self):
    row, column = (0,0)
    for i,cell_instance in enumerate(self.instances.order_by('frame__index')):
      if i==0:
        first = cell_instance
        cell_instance.velocity_rows = 0
        cell_instance.velocity_columns = 0
      else:
        cell_instance.velocity_rows = cell_instance.row - row
        cell_instance.velocity_columns = cell_instance.column - column
      row, column = cell_instance.row, cell_instance.column
      cell_instance.save()


### CellInstance
class CellInstance(models.Model):

  # connections
  region = models.ForeignKey(Region, related_name='cell_instances', null=True)
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
  def d(self, row, column):
    return ((self.column-column)**2 + (self.row-row)**2)**0.5

  def x(self):
    return float(self.column*self.experiment.cmop)

  def y(self):
    return float(self.row*self.experiment.rmop)

  def v(self):
    return (((self.velocity_rows*self.experiment.rmop)**2 + (self.velocity_columns*self.experiment.cmop)**2)**0.5)/self.experiment.tpf

  def a(self):
    return self.area*self.experiment.cmop*self.experiment.rmop

### Extension
class Extension(models.Model):

  # connections
  region = models.ForeignKey(Region, related_name='extensions')
  cell = models.ForeignKey(Cell, related_name='extensions')
  cell_instance = models.ForeignKey(CellInstance, related_name='extensions')
