#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
PLOT_DIR = settings.PLOT_DIR

#local
from apps.image.models import SourceImage
from apps.cell.models import CellInstance, Cell, Extension
from apps.env.models import Region, Experiment
from apps.image.util.life.life import Life
from apps.image.util.life.rule import CoagulationsFillInVote
from apps.image.util.tools import get_surface_elements

#util
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import os
import math
from numpy.linalg import norm
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d
import scipy.optimize as optimization
from scipy.misc import imread, imsave
from scipy.ndimage import binary_dilation as dilate

# matplotlib.rc('font', **font)

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      '''
      PLOT 1: Barrier: brightfield and gfp
      Just print out GFP superimposed on the brightfield

      '''
      #load brightfield and gfp for cell instance 747
      cell_instance = CellInstance.objects.get(pk=747)

      #images details
      experiment_name = cell_instance.experiment.name
      series_index = cell_instance.series.index
      timestep_index = cell_instance.timestep.index
      focus = cell_instance.position_z

      #get brightfield and gfp
      brightfield_set = SourceImage.objects.filter(experiment__name=experiment_name, series__index=series_index, timestep__index=timestep_index, channel=0)
      gfp_set = SourceImage.objects.filter(experiment__name=experiment_name, series__index=series_index, timestep__index=timestep_index, channel=1)

      output_path = os.path.join('/','Volumes','transport','data','confocal','ppt')

      for image in brightfield_set:
        image.load()
        imsave(os.path.join(output_path, '747', 'bf', image.file_name), image.array)

      for image in gfp_set:
        image.load()
        imsave(os.path.join(output_path, '747', 'gfp', image.file_name), image.array)




