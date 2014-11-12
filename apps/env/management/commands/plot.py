#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell, Extension
from apps.env.models import Region

#util
import matplotlib.pyplot as plt
import numpy as np
import math

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      '''
      ### PLOT 1

      Description: Volume and surface area scatter plot, colored by region
      X: Surface area
      Y: Volume
      Resources: cell instance list for each region
      Method: extract volume and surface area from each cell instance

      '''

#       plots = []
#       for region in Region.objects.all():
#         plot = ([],[])
#         for cell_instance in region.cell_instances.all():
#           plot[0].append(cell_instance.surface_area) ### Translate into microns
#           plot[1].append(cell_instance.volume)
#         plots.append(plot)

#       fig = plt.figure()
#       ax = plt.gca()

#       #data
#       colors = ['blue', 'red', 'green', 'yellow']
#       for i,plot in enumerate(plots):
#         ax.plot(plot[0], plot[1], 'o', c=colors[i], alpha=0.5, label='region %d'%(i+1))

#       #lines
#       x = np.linspace(0, 10**6, 1000000)
#       y0 = x
#       ax.plot(x, y0, label='y=x')
#       y1 = x**1.5
#       ax.plot(x, y1, label='y=x^1.5')

#       ax.set_yscale('log')
#       ax.set_xscale('log')
#       ax.legend()
#       plt.title('Volume vs. Surface area')
#       plt.ylabel('log V (pixels^3)')
#       plt.xlabel('log S (pixels^2)')

#       plt.show()

      '''
      ### PLOT 2

      Description: For cells that cross the barrier, plot their maximum extension length against x.
      X: x position
      Y: maximum extension length at x
      Resources: cell list
      Method: for cell_instance, plot a single bar for its maximum colored by region

      '''

#       plots = [] #list of tuples
#       colors = ['blue', 'red', 'green', 'yellow'] #regions

#       for cell in Cell.objects.filter(barrier_crossing_timestep__gt=-1):
#         x_barrier = cell.cell_instances.get(timestep__index=cell.barrier_crossing_timestep).position_x
#         for cell_instance in cell.cell_instances.all():
#           plots.append((x_barrier-cell_instance.position_x, cell_instance.max_extension_length, colors[cell_instance.region.index-1]))

#       fig = plt.figure()
#       ax = plt.gca()

#       color_switch = {'blue':True, 'red':True, 'green':True, 'yellow':True}
#       for plot in plots:
#         if color_switch[plot[2]]:
#           ax.plot(plot[0], plot[1], '-o', color=plot[2], alpha=0.5, label='region %d'%(colors.index(plot[2])+1))
#           color_switch[plot[2]] = False
#         else:
#           ax.plot(plot[0], plot[1], '-o', color=plot[2], alpha=0.5)

#       plt.legend()
#       plt.title('maximum extension length approaching barrier')
#       plt.ylabel('maximum extension length (pixels)')
#       plt.xlabel('x distance from barrier (pixels)')
#       plt.show()

      '''
      ### PLOT 3

      Description: Same as 2, but with velocity
      X: x position
      Y: velocity at x
      Resources: cell list
      Method:

      '''

#       plots = [] #list of tuples
#       colors = ['blue', 'red', 'green', 'yellow'] #regions

#       for cell in Cell.objects.filter(barrier_crossing_timestep__gt=-1):
#         x_barrier = cell.cell_instances.get(timestep__index=cell.barrier_crossing_timestep).position_x
#         for cell_instance in cell.cell_instances.all():
#           plots.append((x_barrier-cell_instance.position_x, np.linalg.norm(cell_instance.velocity()), colors[cell_instance.region.index-1]))

#       fig = plt.figure()
#       ax = plt.gca()

#       color_switch = {'blue':True, 'red':True, 'green':True, 'yellow':True}
#       for plot in plots:
#         if color_switch[plot[2]]:
#           ax.plot(plot[0], plot[1], '-o', color=plot[2], alpha=0.5, label='region %d'%(colors.index(plot[2])+1))
#           color_switch[plot[2]] = False
#         else:
#           ax.plot(plot[0], plot[1], '-o', color=plot[2], alpha=0.5)

#       plt.legend()
#       plt.title('speed approaching barrier')
#       plt.ylabel('speed (pixels/timestep)')
#       plt.xlabel('x distance from barrier (pixels)')
#       plt.show()

      '''
      ### PLOT 4

      Description: boxplot of extension lengths in each region
      X: region
      Y: boxplot of extension length
      Resources: cell list
      Method:

      '''

#       plots = []
#       for region in Region.objects.all():
#         plot = []
#         for extension in region.extensions.all():
#           plot.append(float(extension.length))
#         plots.append(plot)

#       plt.boxplot(plots, 0, '')

#       plt.title('regional extension length distributions')
#       plt.xlabel('region')
#       plt.ylabel('extension length (pixels)')
#       plt.show()

      '''
      ### PLOT 4

      Description: boxplot of velocity in each region
      X: region
      Y: boxplot of velocity
      Resources: cell list
      Method:

      '''

#       plots = []
#       for region in Region.objects.all():
#         plot = []
#         for cell_instance in region.cell_instances.all():
#           plot.append(np.linalg.norm(cell_instance.velocity()))
#         plots.append(plot)

#       plt.boxplot(plots, 0, '')

#       plt.title('regional velocity distributions')
#       plt.xlabel('region')
#       plt.ylabel('velocity (pixels/timestep)')
#       plt.show()

      '''
      ### PLOT 5

      Description: scatter plot of z position by region
      X: region
      Y: boxplot of velocity
      Resources: cell list
      Method:

      '''

      plots = [] #list of tuples
      colors = ['blue', 'red', 'green', 'yellow'] #regions

      for cell in Cell.objects.filter(barrier_crossing_timestep__gt=-1):
        x_barrier = cell.cell_instances.get(timestep__index=cell.barrier_crossing_timestep).position_x
        for cell_instance in cell.cell_instances.all():
          plots.append((x_barrier-cell_instance.position_x, cell_instance.position_z, colors[cell_instance.region.index-1]))

      fig = plt.figure()
      ax = plt.gca()

      color_switch = {'blue':True, 'red':True, 'green':True, 'yellow':True}
      for plot in plots:
        if color_switch[plot[2]]:
          ax.plot(plot[0], plot[1], '-o', color=plot[2], alpha=0.5, label='region %d'%(colors.index(plot[2])+1))
          color_switch[plot[2]] = False
        else:
          ax.plot(plot[0], plot[1], '-o', color=plot[2], alpha=0.5)

      plt.legend()
      plt.title('z position approaching barrier')
      plt.ylabel('z position (pixels)')
      plt.xlabel('x distance from barrier (pixels)')
      plt.show()

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
