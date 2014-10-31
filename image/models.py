#image.models

#django
from django.db import models

#local
from control.models import Experiment, Series, Timestep, Cell, CellInstance
from plot.models import Plot

#util
import os
from scipy.misc import imsave, imread, imresize

class Image(models.Model): #single image
  #sub:

  #properties
  file_name = models.CharField(default='file_name', max_length=255)
  input_path = models.CharField(default='input_path', max_length=255)
  series = models.ForeignKey(Series, related_name='images')
  timestep = models.ForeignKey(Timestep, related_name='images')

  #methods
  def load(self):
    self.array = imread(os.path.join(self.input_path, self.file_name))

  def unload(self):
    del self.array

  def save_array(self):
    imsave(os.path.join(self.input_path, self.file_name), self.array)

  def delete(self, *args, **kwargs):
    #remove file
    os.remove(self.input_path())
    super(Image, self).delete(args, kwargs)

class SourceImage(Image):
  experiment = models.ForeignKey(Experiment, related_name='images')
  channel = models.IntegerField(default=0)
  focus = models.IntegerField(default=0)

class CellImage(Image): #contextual image of a cell
  #sub:

  #properties
  cell_instance = models.ForeignKey(CellInstance, related_name='image')

  #methods

class ModifiedImage(Image): #stores any change to an image that needs to be written to a file, such as plotting
  #properties
  image = models.ForeignKey(Image, related_name='modified')
  description = models.TextField(default='description')

  #methods

class PlotImage(ModifiedImage): #putting an image in a plot context requires writing to a file
  #sub:

  #properties
  plot = models.ForeignKey(Plot, related_name='images')

  #methods

class BoundingBox(models.Model): #crop to restrict to a context
  #sub:

  #properties
  cell = models.OneToOneField(Cell, related_name='bounding_box', default=None)
  x = models.IntegerField(default=0)
  y = models.IntegerField(default=0)
  w = models.IntegerField(default=0)
  h = models.IntegerField(default=0)

  #methods
  def cut(self, array):
    return array[self.y:self.y+self.h,self.x:self.x+self.w]

class ImageTemplate(models.Model):
  #properties
  experiment = models.ForeignKey(Experiment, related_name='image_templates')
  name = models.TextField()
  rx = models.CharField(default='rx', max_length=255) #input
  reverse = models.CharField(default='reverse', max_length=255) #output

  #methods
