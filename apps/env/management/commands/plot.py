#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
PLOT_DIR = settings.PLOT_DIR

#local
from apps.cell.models import CellInstance, Cell, Extension
from apps.env.models import Region

#util
import matplotlib.pyplot as plt
import numpy as np
import os
import math
from numpy.linalg import norm
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d
import scipy.optimize as optimization
from scipy.misc import imread, imsave

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      '''
      ### PLOT 1

      Description: Volume and surface area scatter plot, colored by region
      X: Surface area (log scale)
      Y: Volume (log scale)
      Resources: cell instance list for each region
      Method: extract volume and surface area from each cell instance

      '''
#       x = np.linspace(0, 10**3, 10**2)

#       for region in Region.objects.filter(index__range=(1,1)):

#         #1. for each region, need upper and lower bounds in terms of gradient.
#         #- get histogram of V/A
#         v = []
#         v_over_a = []
#         a = []
#         for cell_instance in region.cell_instances.all():
#           v.append(float(cell_instance.volume))
#           v_over_a.append(float(cell_instance.volume)/float(cell_instance.surface_area+1))
#           a.append(cell_instance.surface_area)

#         A = np.vstack([np.array(a), np.ones(len(a))]).T
#         m, c = np.linalg.lstsq(A, np.log(np.array(v)))[0]
#         y_c = m*x
#         print(y_c)
#         plt.plot(x, np.power(y_c, 10))

#         v = np.array(v)

#         #plot
#         plt.plot(a, v, '*')
# #         plt.hist(v_over_a, 50)
# #         plt.loglog(a, v, '*')

#       #gradient lines

#       y_1p0 = x
#       y_1p5 = x**1.5
# #       plt.plot(x, y_1p0)
# #       plt.plot(x, y_1p5)

#       plt.show()

      #get all mask images
      max_width = 0
      for cell_instance in CellInstance.objects.all():
        (x_b,y_b,w,h) = cell_instance.cell.bounding_box.get().all()
        (x,y) = (cell_instance.position_x, cell_instance.position_y)
        cell_instance_max = max([x-x_b,y-y_b,w-x+x_b,h-y+y_b])
        max_width = max_width if max_width>cell_instance_max else cell_instance_max

      full_mask_shape = (2*max_width, 2*max_width)

      complete_full_mask = np.zeros(full_mask_shape)
      for cell_instance in CellInstance.objects.all():
        print(cell_instance.pk)
        #metrics
        (x_b,y_b,w,h) = cell_instance.cell.bounding_box.get().all()
        (x,y) = (cell_instance.position_x, cell_instance.position_y)
        center_column = x-x_b
        center_row = y-y_b
        column_shift = max_width-center_column
        row_shift = max_width-center_row

        #load image
        full_mask = np.zeros(full_mask_shape)
        mask = cell_instance.mask_array()/255.0

        #position image
        full_mask[row_shift:row_shift+h,column_shift:column_shift+w] = mask
        complete_full_mask += full_mask

      complete_full_mask.dtype = float

      #cut to size
      b = (complete_full_mask!=0)
      columns = np.all(b, axis=0)
      rows = np.all(b, axis=1)

      firstcol = columns.argmin()
      firstrow = rows.argmin()

      lastcol = len(columns) - columns[::-1].argmin()
      lastrow = len(rows) - rows[::-1].argmin()

      complete_full_mask = complete_full_mask[firstrow:lastrow,firstcol:lastcol]

      #save image series
      count = 0
      while complete_full_mask.max()>0:
        imsave(os.path.join(PLOT_DIR, 'density', 'image_%d.png'%count), complete_full_mask)
        complete_full_mask[complete_full_mask==complete_full_mask.max()] = 0
        count += 1


#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
