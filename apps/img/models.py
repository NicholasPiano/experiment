#apps.image.models

#django
from django.db import models

#local
from apps.env.models import *

#util
import re
from scipy.misc import imread, imsave
import numpy as np

### Region
class Region(models.Model):

  # properties
  name = models.CharField(max_length=255)
  index = models.IntegerField(default=0)
  description = models.TextField(default='region description')

### Experiment
class Experiment(models.Model):

  # properties
  name = models.CharField(max_length=255)

  # paths
  base_path = models.CharField(max_length=255)
  input_path = models.CharField(default=os.path.join('backup','backup'), max_length=255) #appended to base_path
  plot_path = models.CharField(default='plot', max_length=255)

  # scaling
  rmop = models.FloatField(default=0.0)
  cmop = models.FloatField(default=0.0)
  zmop = models.FloatField(default=0.0)

  def mop(self):
    return np.array([self.rmop, self.cmop, self.zmop])

  tpf = models.FloatField(default=0.0) # time per frame

  # methods
  def input(self):
    # search input folder for images not currently added

    #

### Series
class Series(models.Model):

  # connections
  experiment = models.ForeignKey(Experiment, related_name='series')

  # properties
  index = models.IntegerField(default=0)

  # limits
  channels = models.IntegerField(default=0)
  frames = models.IntegerField(default=0)
  rows = models.IntegerField(default=0)
  columns = IntegerField(default=0)
  levels = models.IntegerField(default=0)

  # methods
  def process(self):
    # populate parameters from images
    image_set = self.experiment.images.all()

### Channel
class Channel(models.Model):

  # connections
  experiment = models.ForeignKey(Experiment, related_name='timesteps')
  series = models.ForeignKey(Series, related_name='timesteps')

  # properties
  index = models.IntegerField(default=0)
  name = models.CharField(max_length=255)

### Frame
class Frame(models.Model):

  # connections
  experiment = models.ForeignKey(Experiment, related_name='timesteps')
  series = models.ForeignKey(Series, related_name='timesteps')

  # properties
  index = models.IntegerField(default=0)
  previous_index = models.IntegerField(default=0)
  next_index = models.IntegerField(default=0)

### Image
class Image(models.Model):

  # connections
  experiment = models.ForeignKey(Experiment, related_name='images')
  series = models.ForeignKey(Series, related_name='images')
  frame = models.ForeignKey(Frame, related_name='images')

  # properties
  file_name = models.CharField(default='file_name', max_length=255)
  input_path = models.CharField(default='input_path', max_length=255)

  # coordinates
  channel = models.CharField(max_length=255)
  level = models.IntegerField(default=0)

  # image properties
  max = models.FloatField(default=0.0)
  min = models.FloatField(default=0.0)
  mean = models.FloatField(default=0.0)
  sum = models.FloatField(default=0.0)

  # methods
  def load(self):
    self.array = imread(os.path.join(self.input_path, self.file_name))
    return self.array

  def unload(self):
    del self.array

  def save_array(self, new_path=''):
    if new_path!='':
      self.input_path = new_path
    imsave(os.path.join(self.input_path, self.file_name), self.array)
    self.save()

  def process(self):
    # load image

    # store properties

### ImageTemplate
class ImageTemplate(models.Model):

  # connections
  experiment = models.ForeignKey(Experiment, related_name='image_templates')
  image = models.ForeignKey(Image, related_name='image_templates', null=True)

  # properties
  name = models.CharField(max_length=255)
  rx = models.TextField(default='rx')
  reverse = models.TextField(default='reverse')

  # methods
  def match(self, file_name):
    return re.match(self.rx, file_name)
