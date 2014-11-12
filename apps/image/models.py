#apps.image.models

#django
from django.db import models

#local
from apps.env.models import Experiment, Series, Timestep
from apps.cell.models import CellInstance

#util
import os
import re
import scipy
from scipy.ndimage import distance_transform_edt
from scipy.misc import imsave, imread, imresize
import numpy as np
import string
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math

### Image
class Image(models.Model):

  #connections
  series = models.ForeignKey(Series, related_name='images')
  timestep = models.ForeignKey(Timestep, related_name='images')

  #properties
  file_name = models.CharField(default='file_name', max_length=255)
  input_path = models.CharField(default='input_path', max_length=255)

  #-image properties
  pixels = models.IntegerField(default=0)
  max = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  min = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  mean = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  sum = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)

  #methods
  def load(self):
    self.array = imread(os.path.join(self.input_path, self.file_name))

  def unload(self):
    del self.array

  def save_array(self):
    imsave(os.path.join(self.input_path, self.file_name), self.array)

### SourceImage
class SourceImage(Image):

  #connections
  experiment = models.ForeignKey(Experiment, related_name='images')

  #properties
  channel = models.IntegerField(default=0)
  focus = models.IntegerField(default=0)

### CellImage
class CellImage(Image):

  #connections
  cell_instance = models.ForeignKey(CellInstance, related_name='image')

  #methods
  def array_to_plot_to_image(self, array, description):
    plt.imshow(array, cmap=cm.Greys_r)
    plt.axis('off')

    root, ext = os.path.splitext(self.file_name)
    modified_image = self.modified.create(file_name=root+'_'+description+ext, input_path=os.path.join(self.cell_instance.experiment.base_path, 'black'), series=self.series, timestep=self.timestep, description=description)
    plt.savefig(os.path.join(modified_image.input_path, modified_image.file_name))
    plt.close()

    return modified_image

### ModifiedImage
class ModifiedImage(Image):

  #connections
  image = models.ForeignKey(Image, related_name='modified')

  #properties
  description = models.TextField(default='description')

### ImageTemplate
class ImageTemplate(models.Model):

  #connections
  experiment = models.ForeignKey(Experiment, related_name='image_templates')

  #properties
  name = models.CharField(max_length=255)
  rx = models.TextField(default='rx')
  reverse = models.TextField(default='reverse')

  #methods
  def match(self, file_name):
    return re.match(self.rx, file_name)
