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
# #       for i,plot in enumerate(plots):
#       ax.plot(plots[1][0], plots[1][1], 'o', c=colors[1], alpha=0.5, label='region %d'%(1+1))
#       ax.plot(plots[1][0], plots[1][1], 'o', c=colors[1], alpha=0.5, label='region %d'%(1+1))

#       #lines
#       x = np.linspace(10**5, 10**6, 1000000)
#       y0 = x
#       ax.plot(x, y0, label='y=x')
#       y1 = x**1.5
#       ax.plot(x, y1, label='y=x^1.5')
#       y2 = x**0.8
#       ax.plot(x, y2, label='y=x^0.8')

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

#       plots = [] #list of tuples
#       colors = ['blue', 'red', 'green', 'yellow'] #regions

#       for cell in Cell.objects.filter(barrier_crossing_timestep__gt=-1):
#         x_barrier = cell.cell_instances.get(timestep__index=cell.barrier_crossing_timestep).position_x
#         for cell_instance in cell.cell_instances.all():
#           plots.append((x_barrier-cell_instance.position_x, cell_instance.position_y, colors[cell_instance.region.index-1]))

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
#       plt.title('z position approaching barrier')
#       plt.ylabel('z position (pixels)')
#       plt.xlabel('x distance from barrier (pixels)')
#       plt.show()

#       fig = plt.figure()
#       ax = plt.gca()

#       plots = []
#       for cell in sorted(Cell.objects.all(), key=lambda x: x.cell_instances.count())[:-10]:
#         plot = ([],[])
#         for cell_instance in cell.cell_instances.all():
#           plot[0].append(cell_instance.position_x)
#           plot[1].append(cell_instance.position_y)
#         plots.append(plot)

#       for plot in plots:
#         ax.plot(plot[0], plot[1], '-')

#       plt.show()


      '''
      ### PLOT 6

      Description: scatter plot of extension length against extension angle towards barrier -> by region
      X:
      Y:
      Resources:
      Method:

      '''


#       plots = [] #list of tuples
#       colors = ['blue', 'red', 'green', 'yellow'] #regions

#       for cell in Cell.objects.all():
#         for cell_instance in cell.cell_instances.all():
# #           for extension in cell_instance.extensions.all():
#           plots.append((float(cell_instance.max_extension_angle), float(cell_instance.max_extension_length), colors[cell_instance.region.index-1]))

#       fig = plt.figure()
#       ax = plt.gca(polar=True)

#       color_switch = {'blue':True, 'red':True, 'green':True, 'yellow':True}
#       for plot in plots:
#         if color_switch[plot[2]]:
#           ax.plot(plot[0], plot[1], '-o', color=plot[2], alpha=0.5, label='region %d'%(colors.index(plot[2])+1))
#           color_switch[plot[2]] = False
#         else:
#           ax.plot(plot[0], plot[1], '-o', color=plot[2], alpha=0.5)

#       plt.legend()
#       plt.show()

      '''
      ### PLOT 7

      Description: scatter plot of z position by region
      X: region
      Y: boxplot of velocity
      Resources: cell list
      Method:

      '''

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

#       for plot in plots:
#         plt.plot(plot[0], plot[1])

#       plt.title('Distance from barrier against position y')
#       plt.xlabel('x position (pixels)')
#       plt.ylabel('y position (pixels)')
#       plt.show()

      #cart
#       for region in Region.objects.all():
#         points = []
#         for cell_instance in region.cell_instances.all():
#           for extension in cell_instance.extensions.all():
#             points.append([float(extension.length), float(extension.angle)])

#         #put into array
#         y = np.array([point[0] for point in points])
#         x = np.array([point[1] for point in points])
#         xy = np.vstack([x,y])
#         z = gaussian_kde(xy)(xy)

#         idx = z.argsort()
#         x, y, z = x[idx], y[idx], z[idx]

#         fig, ax = plt.subplots()
#         ax.scatter(x, y, c=z, s=50, edgecolor='')

#         plt.title('Density plot of extension length vs. extension angle')
#         plt.ylabel('extension length (pixels)')
#         plt.xlabel('extension angle (rads)')

#         plt.savefig('plots/density_angle_length_region%d.png'%region.index)

      #polar
#       for region in Region.objects.all():
#         points = []
#         for cell_instance in region.cell_instances.all():
#           for extension in cell_instance.extensions.all():
#             points.append([float(extension.length), float(extension.angle)])

#         #put into array
#         y = np.array([point[0] for point in points])
#         x = np.array([point[1] for point in points])
#         xy = np.vstack([x,y])
#         z = gaussian_kde(xy)(xy)

#         idx = z.argsort()
#         x, y, z = x[idx], y[idx], z[idx]

#         fig = plt.figure()
#         ax = fig.add_subplot(1,1,1,polar=True)
#         ax.scatter(x, y, c=z, s=50, edgecolor='')

#         plt.title('Density plot of extension length vs. extension angle')
#         plt.ylabel('extension length (pixels)')
#         plt.xlabel('extension angle (rads)')

#         plt.savefig('plots/density_angle_length_region%d_polar.png'%region.index)





#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
