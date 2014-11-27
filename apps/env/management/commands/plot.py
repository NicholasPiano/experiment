#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
PLOT_DIR = settings.PLOT_DIR

#local
from apps.cell.models import CellInstance, Cell, Extension
from apps.env.models import Region, Experiment

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
      Tasks:
      1. for each region, get surface and volume of each cell instance
      2. using combined arrays, get 90% and 10% of all data.
      3. Fit lines for each group
      4. display x^1, x^1.5, 10%, and 90%.
      5. diplays data colored by region.

      '''

      fig = plt.figure()
      ax = fig.add_subplot(111)

      ### LINES

      #x
      x = np.linspace(0,10000,1000)

      #data
      grad10 = 0
      grad90 = 0

      grad = []
      for cell_instance in CellInstance.objects.filter(region=Region.objects.get(index=4)):
        grad.append(np.array([float(cell_instance.surface_area), float(cell_instance.volume), float(cell_instance.volume)/float(cell_instance.surface_area+1)]))

      #10%
      p10 = np.percentile([g[2] for g in grad], 10)
      data_10 = filter(lambda x: x[2]<p10, grad)
      m_10 = np.linalg.lstsq(np.array([g[0] for g in data_10])[:,np.newaxis], np.array([g[1] for g in data_10]))[0][0]

      y_10 = m_10*x

      #90%
      p90 = np.percentile([g[2] for g in grad], 90)
      data_90 = filter(lambda x: x[2]>p90, grad)
      m_90 = np.linalg.lstsq(np.array([g[0] for g in data_90])[:,np.newaxis], np.array([g[1] for g in data_90]))[0][0]

      y_90 = m_90*x

      #x^1
      y_1 = x

      #x^1.5
      y_15 = np.power(x, 1.5)

      ax.plot(x, y_10, label='10th percentile (%f)' % m_10, alpha=0.5)
      ax.plot(x, y_90, label='90th percentile (%f)' % m_90, alpha=0.5)
      ax.plot(x, y_1, label='x^1', alpha=0.5)
      ax.plot(x, y_15, label='x^1.5', alpha=0.5)

      ### SCATTER

      colors = ['blue','red','green','yellow']
      plots = []
      for region in Region.objects.all():
        plot = ([],[])
        for cell_instance in region.cell_instances.all():
          plot[0].append(cell_instance.surface_area)
          plot[1].append(cell_instance.volume)
        plots.append(plot)

      for i,plot in enumerate(plots):
        color = colors[i]
        x = plot[0]
        y = plot[1]
        ax.scatter(x,y, color=color, alpha=0.5, label='region %d'%(i+1))

      ### SHOW

#       ax.set_xscale('log')
#       ax.set_yscale('log')

      plt.legend()
      plt.show()

      '''
      ### PLOT 2

      Description: 12 density scatter plots of extension length and extension angle (polar)

      '''

#       fig = plt.figure()

#       for i,region in enumerate(Region.objects.all()):
#         for j,experiment in enumerate(Experiment.objects.all()):
#           ax = fig.add_subplot(3, 4, i*3+j+1, polar=False)
#           x = []
#           y = []

#           for cell_instance in experiment.cell_instances.filter(region=region):
#             for extension in cell_instance.extensions.all():
#               x.append(float(extension.length))
#               y.append(float(extension.angle))

#           x = np.array(x)
#           y = np.array(y)
#           if len(x)!=0:
#             xy = np.vstack([x,y])
#             z = gaussian_kde(xy)(xy)
#             idx = z.argsort()
#             x, y, z = x[idx], y[idx], z[idx]

#             ax.scatter(y, x, c=z, s=50, edgecolor='')

#       plt.show()

      '''
      ### PLOT 3

      Description: 12 density scatter plots of extension length and extension angle (polar)

      '''

#       fig = plt.figure()

#       for i,region in enumerate(Region.objects.all()):
#         for j,experiment in enumerate(Experiment.objects.all()):
#           ax = fig.add_subplot(3, 4, i*3+j+1, polar=False)
#           x = []
#           y = []

#           for cell_instance in experiment.cell_instances.filter(region=region):
#             x.append(float(cell_instance.max_extension_length))
#             y.append(float(math.atan2(cell_instance.velocity_y, cell_instance.velocity_x)))

#           print(y)
#           x = np.array(x)
#           y = np.array(y)
#           if len(x)!=0:
#             xy = np.vstack([x,y])
#             z = gaussian_kde(xy)(xy)
#             idx = z.argsort()
#             x, y, z = x[idx], y[idx], z[idx]

#             ax.scatter(y, x, c=z, s=50, edgecolor='')

#       plt.show()

      #get cells with high number of timepoints and low velocity
#       cells = sorted(Cell.objects.filter(barrier_crossing_timestep__gt=0), key=lambda x: x.cell_instances.count())[:20]

#       plots = []

#       for cell in cells:
#         plot = ([],[])

#         if max([norm(cell_instance.velocity()) for cell_instance in cell.cell_instances.all()]) < 100:
#           for cell_instance in cell.cell_instances.all():
#             plot[0].append(cell_instance.position_x - cell.cell_instances.get(timestep__index=cell.barrier_crossing_timestep).position_x)
#             plot[1].append(cell_instance.position_y)

#         if len(plot[0])>0:
# #           f = interp1d(plot[0], plot[1], kind='cubic')
# #           plots.append((plot[0], f(plot[0])))
#           plots.append(plot)

#       colors = ['blue','red','green','yellow','purple','black','pink','gray']
#       for i,plot in enumerate(plots):
#         plt.plot(plot[0], plot[1], linewidth=3, alpha=0.7, color=colors[i])
#         plt.plot(plot[0][0], plot[1][0], 'd', color=colors[i])

#       plt.title('Distance from barrier against position y')
#       plt.xlabel('x position (pixels)')
#       plt.ylabel('y position (pixels)')
#       plt.show()


#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
