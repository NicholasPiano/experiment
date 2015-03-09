# apps.env.models

# django
from django.db import models
from django.conf import settings

# local
from apps.env import algorithms

# util
import os

# vars
pipeline_path = os.path.join(settings.DATA_DIR, 'cp')

### Run
class Preprocess(models.Model):

  # properties
  name = models.CharField(max_length=255)
  algorithm = models.CharField(max_length=255)
  output_path = models.CharField(max_length=255)

  # methods
  def process(self):
    self.output_path = os.path.join(pipeline_path, self.name)
    self.save()

  def run(self):
    # get algorithm
    algorithm = getattr(algorithms, self.algorithm)

    # run
    algorithm(output_path=self.output_path, name=self.name)
