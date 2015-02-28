#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

#local
from apps.cell.models import Cell
from apps.env.models import Experiment, Series

#util
import os
import numpy as np
from scipy.misc import imsave
from scipy.ndimage.morphology import binary_dilation as dilate
import matplotlib.pyplot as plt

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    path = '/Volumes/WINDOWSSWAP/Segmentation/runs/mask-run-2'
    with open(os.path.join(path, 'ci.txt'), 'w+') as ci:
      for cell in Cell.objects.all():
        ci_set = cell.cell_instances.order_by('timestep__index')

        #cell instances
        c1 = ci_set[1]
        c2 = ci_set[2]

        #middle gfp image for each
        gfp1 = cell.experiment.images.get(series=cell.series, timestep=c1.timestep, focus=c1.position_z, channel=0)
        gfp2 = cell.experiment.images.get(series=cell.series, timestep=c2.timestep, focus=c2.position_z, channel=0)

        #print to file
        ci.write('experiment %s, series %d, cell #%d\n'%(cell.experiment.name, cell.series.index, cell.index))
        ci.write('cell instance 1: frame %d, dt %f, (mx, my, mz) -> (%f,%f,%f), N %d\n'%(c1.timestep.index, float(cell.experiment.time_per_frame), float(cell.experiment.x_microns_over_pixels), float(cell.experiment.y_microns_over_pixels), float(cell.experiment.z_microns_over_pixels), int(cell.experiment.images.filter(series=cell.series, timestep=c2.timestep, channel=0).count())))
        ci.write('cell instance 1: frame %d, dt %f, (mx, my, mz) -> (%f,%f,%f), N %d\n'%(c2.timestep.index, float(cell.experiment.time_per_frame), float(cell.experiment.x_microns_over_pixels), float(cell.experiment.y_microns_over_pixels), float(cell.experiment.z_microns_over_pixels), int(cell.experiment.images.filter(series=cell.series, timestep=c1.timestep, channel=0).count())))
        ci.write('\n')
