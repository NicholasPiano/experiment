#django
from django.db import models

#local


#util


### Region
class Region(models.Model):
  #properties
  name = models.CharField(max_length=1)
  index = models.IntegerField(default=0)

### Experiment
class Experiment(models.Model):
  #properties
  name = models.CharField(max_length=255)

  #-paths
  base_path = models.CharField(default='base_path', max_length=255)
  input_path = models.CharField(default='input_path', max_length=255) #appended to base_path

  #-scaling
  x_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  y_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  z_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  time_per_frame = models.DecimalField(default=0.0, decimal_places=4, max_digits=10)

  #methods

### Series
class Series(models.Model):


### Timestep
class Timestep(models.Model):
