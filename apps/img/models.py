# apps.image.models

# django
from django.db import models
from django.conf import settings

# local
from apps.env.models import *

# util
import re
import os
from scipy.misc import imread, imsave
import numpy as np

# vars
image_channels = {
  0:'gfp',
  1:'bf',
}

base_path = settings.DATA_DIR
img_path = 'img'
cell_path = 'cells'
plot_path = 'plots'

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

  # scaling
  rmop = models.FloatField(default=0.0)
  cmop = models.FloatField(default=0.0)
  zmop = models.FloatField(default=0.0)

  def mop(self):
    return np.array([self.rmop, self.cmop, self.zmop])

  tpf = models.FloatField(default=0.0) # time per frame

  # methods
  def path(self, path):
    return os.path.join(base_path, self.name, path)

  def input_images(self):
    # search input folder for images not currently added
    # 1. get list of files
    input_path = self.path(img_path)
    print(input_path)
    # file_list = [image_file_name for image_file_name in os.listdir(input_path) if re.search(r'\.ti[f]{1,2}$', image_file_name) is not None]
    # template = self.image_templates.get(name='input')
    #
    # # 2. extract details from each file_name and get or create objects
    # for file_name in file_list:
    #   match = template.match(file_name)
    #
    #   series_index = int(match.group('series'))+1
    #   frame_index = match.group('frame')
    #   channel_index = int(match.group('channel'))
    #   focus = int(match.group('focus'))
    #
    #   # get details and create image
    #   series = self.series.get(index=series_index)
    #   channel = self.channels.get(series=series, index=channel_index)
    #   frame = self.timesteps.get(series=series, index=frame_index)
    #   image, created = self.images.get_or_create(file_name=file_name, input_path=input_path, series=series, frame=frame, channel=channel, level=level)
    #
    #   if created:
    #     print('processing input ... ' + file_name + (' (created)' if created else ''))
    #   else:
    #     print('skipping unneeded image file ... ' + file_name)

  def input_cells(self):
    # search cell folder and read lines of csv tracking files

    #
    pass

### Series
class Series(models.Model):

  # connections
  experiment = models.ForeignKey(Experiment, related_name='series')

  # properties
  index = models.IntegerField(default=0)

  # limits
  max_channels = models.IntegerField(default=0)
  max_frames = models.IntegerField(default=0)
  rows = models.IntegerField(default=0)
  columns = models.IntegerField(default=0)
  levels = models.IntegerField(default=0)

  # methods
  def process(self):
    # populate parameters from images
    image_set = self.experiment.images.all()

### Channel
class Channel(models.Model):

  # connections
  experiment = models.ForeignKey(Experiment, related_name='channels')
  series = models.ForeignKey(Series, related_name='channels')

  # properties
  index = models.IntegerField(default=0)
  name = models.CharField(max_length=255)

### Frame
class Frame(models.Model):

  # connections
  experiment = models.ForeignKey(Experiment, related_name='frames')
  series = models.ForeignKey(Series, related_name='frames')

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
    pass

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
