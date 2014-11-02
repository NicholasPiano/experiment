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
  segmented_path = models.CharField(default='segmented_path', max_length=255)

  #-scaling
  x_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  y_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  z_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  time_per_frame = models.DecimalField(default=0.0, decimal_places=4, max_digits=10)

  #methods
  def create_images_from_input_directory(self):
    pass

  def create_cells_from_segmented_directory(self):
    pass



### Series
class Series(models.Model):

  #properties
  experiment = models.ForeignKey(Experiment, related_name='series')
  index = models.IntegerField(default=0)

### Timestep
class Timestep(models.Model):

  #properties
