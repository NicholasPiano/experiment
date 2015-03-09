# apps.env.models

# django
from django.db import models
from django.conf import settings

# local
from apps.env import algorithms
from apps.img.models import Series

# util
import os

# vars
ij = 'ij-input'
cp = 'cp-input'

### Run
class Preprocess(models.Model):

  # properties
  name = models.CharField(max_length=255)
  category = models.CharField(max_length=255) #ij-tracking, cp-input
  algorithm = models.CharField(max_length=255)

  # methods
  def run(self):
    # make folders



    # get algorithm
    algorithm = getattr(algorithms, self.algorithm)

    # run
    algorithm(name=self.name, category=self.category)
