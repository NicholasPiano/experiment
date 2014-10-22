#image.models

#django
from django.db import models

#local
from control.models import Experiment, Series, Timestep, Cell, CellInstance
from plot.models import Plot

#util
import os

class Image(models.Model): #single image
  #sub:

  #properties
  file_name = models.CharField(default='file_name', max_length=255)
  experiment = models.ForeignKey(Experiment, related_name='images')
  series = models.ForeignKey(Series, related_name='images')
  timestep = models.ForeignKey(Timestep, related_name='images')
  channel = models.IntegerField(default=0)
  focus = models.IntegerField(default=0)

  #methods
  def input_path(self):
    root = self.experiment.input_path
    return os.path.join(root, str(self.series.index), self.file_name)

  def load(self):
    self.array = imread(self.input_path())

  def unload(self):
    del self.array

  def delete(self, *args, **kwargs):
    #remove file
    os.remove(self.input_path())
    super(Image, self).delete(args, kwargs)

class ModifiedImage(Image): #stores any change to an image that needs to be written to a file, such as plotting
  #properties
  image = models.ForeignKey(Image, related_name='modified')
  description = models.TextField()

  #methods

class CellImage(ModifiedImage): #contextual image of a cell
  #sub:

  #properties
  cell_instance = models.ForeignKey(CellInstance, related_name='images')

  #methods

class PlotImage(ModifiedImage): #putting an image in a plot context requires writing to a file
  #sub:

  #properties
  plot = models.ForeignKey(Plot, related_name='images')

  #methods

class BoundingBox(models.Model): #crop to restrict to a context
  #sub:

  #properties
  image = models.OneToOneField(ModifiedImage, related_name='bounding_box')
  x = models.IntegerField(default=0)
  y = models.IntegerField(default=0)
  w = models.IntegerField(default=0)
  h = models.IntegerField(default=0)

  #methods

class ImageTemplate(models.Model):
  #properties
  experiment = models.ForeignKey(Experiment, related_name='image_templates')
  name = models.TextField()
  rx = models.CharField(default='rx', max_length=255) #input
  reverse = models.CharField(default='reverse', max_length=255) #output

  #methods
