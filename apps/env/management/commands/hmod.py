#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

#local
from apps.cell.models import Cell
from apps.env.models import Experiment, Series

#util
import os
import cv2
import numpy as np
from scipy.misc import imsave
from scipy.ndimage.morphology import binary_dilation as dilate
from scipy import ndimage
import matplotlib.pyplot as plt

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    image_path = '/Volumes/transport/data/cp/combine/input/modified/hmod'

    #load images
    experiment = Experiment.objects.get(name='050714')
    bf = experiment.images.filter(focus=30, channel=1)
    gfp = experiment.images.filter(focus=30, channel=0)

    for b in bf[:1]:
      g = gfp.get(timestep__index=b.timestep.index)
      b.load()
      g.load()

      #1. set block and pillar to be black (don't want this to interfere with the calculations)


      #2. smooth gfp (sigma=10)
      smooth_g = ndimage.gaussian_filter(g.array, sigma=5, mode='constant', cval=0)
      plt.imshow(smooth_g, cmap='Greys_r')
      plt.show()

      #3. threshold gfp with Otsu http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
      #4. stretch gfp histogram
      #5. multiply gfp and bf
      #6. output
