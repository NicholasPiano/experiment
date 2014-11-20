#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell, Extension
from apps.env.models import Region

#util
import matplotlib.pyplot as plt
import numpy as np
import math
from numpy.linalg import norm
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d
import scipy.optimize as optimization

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
      x = np.linspace(0, 10**4, 10**4)

      for region in Region.objects.filter(index__range=(1,1)):

        #1. for each region, need upper and lower bounds in terms of gradient.
        #- get histogram of V/A
        v = []
        v_over_a = []
        a = []
        for cell_instance in region.cell_instances.all():
          v.append(float(cell_instance.volume))
          v_over_a.append(float(cell_instance.volume)/float(cell_instance.surface_area+1))
          a.append(cell_instance.surface_area)

        A = np.vstack([a, np.ones(len(a))]).T
        m, c = np.linalg.lstsq(A, v)[0]
        y_c = m*x
        print([m,c])
        plt.plot(y_c)

        v = np.array(v)

        #plot
#         plt.plot(a, v, '*')
#         plt.hist(v_over_a, 50)
        plt.loglog(a, v, '*')

      #gradient lines

      y_1p0 = x
      y_1p5 = x**1.5
      plt.plot(x, y_1p0)
      plt.plot(x, y_1p5)

      plt.show()


#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
