#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
PLOT_DIR = settings.PLOT_DIR

#local
from apps.cell.models import CellInstance, Cell, Extension
from apps.env.models import Region, Experiment

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

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 15}

# matplotlib.rc('font', **font)

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      '''
      ### PLOT 2A: trajectories

      Description: Smoothed trajectories of several cells that cross the barrier

      '''
###
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

#       colors = ['blue','red','green','yellow','purple','black','pink','gray','cyan']
#       for i,plot in enumerate(plots):
#         plt.plot(plot[0], plot[1], linewidth=3, alpha=0.7, color=colors[i])
#         plt.plot(plot[0][0], plot[1][0], 'd', color=colors[i])

#       plt.title('Distance from barrier against position y')
#       plt.xlabel('x position (pixels)')
#       plt.ylabel('y position (pixels)')
#       plt.show()
###

      '''
      ### PLOT 3A-1: 4 regions plots

      Description: Volume and surface area scatter plot
      X: Surface area
      Y: Volume
      Resources: cell instance list for each region
      Method: extract volume and surface area from each cell instance
      Tasks:
      1. for each region, get surface and volume of each cell instance
      2. using combined arrays, get 90% and 10% of all data.
      3. Fit lines for each group
      4. display x^1, x^1.5, 10%, and 90%.
      5. diplays data colored by region.

      '''
###
#       #tasks
#       #1. get all data points for volume and surface area
#       #2. fit lines to the upper and lower 10th percentiles of the data
#       #3. plot data, fit lines, x^1, x^1.5

#       fig = plt.figure()
#       axs = [141,142,143,144]

#       sa = [cell_instance.experiment.area(cell_instance.surface_area) for cell_instance in CellInstance.objects.all()]
#       min_sa = min(sa)
#       max_sa = max(sa)

#       v = [cell_instance.experiment.volume(cell_instance.volume) for cell_instance in CellInstance.objects.all()]
#       min_v = min(v)
#       max_v = max(v)

#       for region in Region.objects.all():
#         data = []
#         for cell_instance in region.cell_instances.all():
#           data.append(np.array([float(cell_instance.experiment.area(cell_instance.surface_area)), float(cell_instance.experiment.volume(cell_instance.volume)), float(cell_instance.experiment.area(cell_instance.surface_area))/float(cell_instance.experiment.volume(cell_instance.volume))]))

#         ax = fig.add_subplot(axs[region.index-1])

#         #lines
#         gradients = np.array([d[2] for d in data])
#         p10 = np.percentile(gradients, 10)
#         p90 = np.percentile(gradients, 90)
#         data10 = filter(lambda k: k[2]<p10, data)
#         data90 = filter(lambda k: k[2]>p90, data)

#         m10 = np.linalg.lstsq(np.array([g[0] for g in data10])[:,np.newaxis], np.array([g[1] for g in data10]))[0][0]
#         m90 = np.linalg.lstsq(np.array([g[0] for g in data90])[:,np.newaxis], np.array([g[1] for g in data90]))[0][0]

#         x = np.linspace(0,max_sa,max_sa)

#         y10 = m10*x
#         y90 = m90*x

#         ax.plot(x, y10, label='10pc (m=%.2f)'%m10)
#         ax.plot(x, y90, label='90pc (m=%.2f)'%m90)
#         ax.plot(x, x**1, label='y=x')
#         ax.plot(x, x**1.5, label='y=x^1.5')

#         #ranges
#         ax.set_xlim([min_sa, max_sa])
#         ax.set_ylim([min_v, max_v])

#         #scatter
#         ax.scatter([d[0] for d in data], [d[1] for d in data])
#         ax.legend()

#       plt.show()
###

      '''
      ### PLOT 3A-2: 4 region plots

      Description: Same as 3A-1 but in a log-log scale
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
###
#       #tasks
#       #1. get all data points for volume and surface area
#       #2. fit lines to the upper and lower 10th percentiles of the data
#       #3. plot data, fit lines, x^1, x^1.5

#       fig = plt.figure()
#       axs = [141,142,143,144]

#       sa = [cell_instance.experiment.area(cell_instance.surface_area) for cell_instance in CellInstance.objects.all()]
#       min_sa = min(sa)
#       max_sa = max(sa)

#       v = [cell_instance.experiment.volume(cell_instance.volume) for cell_instance in CellInstance.objects.all()]
#       min_v = min(v)
#       max_v = max(v)

#       for region in Region.objects.all():
#         data = []
#         for cell_instance in region.cell_instances.all():
#           data.append(np.array([float(cell_instance.experiment.area(cell_instance.surface_area)), float(cell_instance.experiment.volume(cell_instance.volume)), float(cell_instance.experiment.area(cell_instance.surface_area))/float(cell_instance.experiment.volume(cell_instance.volume))]))

#         ax = fig.add_subplot(axs[region.index-1])

#         #lines
#         gradients = np.array([d[2] for d in data])
#         p10 = np.percentile(gradients, 10)
#         p90 = np.percentile(gradients, 90)
#         data10 = filter(lambda k: k[2]<p10, data)
#         data90 = filter(lambda k: k[2]>p90, data)

#         m10 = np.linalg.lstsq(np.array([g[0] for g in data10])[:,np.newaxis], np.array([g[1] for g in data10]))[0][0]
#         m90 = np.linalg.lstsq(np.array([g[0] for g in data90])[:,np.newaxis], np.array([g[1] for g in data90]))[0][0]

#         x = np.linspace(0,max_sa,max_sa)

#         y10 = m10*x
#         y90 = m90*x

#         ax.plot(x, y10, label='10pc (m=%.2f)'%m10)
#         ax.plot(x, y90, label='90pc (m=%.2f)'%m90)
#         ax.plot(x, x**1, label='y=x')
#         ax.plot(x, x**1.5, label='y=x^1.5')

#         #ranges
#         ax.set_xlim([min_sa, max_sa])
#         ax.set_ylim([min_v, max_v])

#         #scatter
#         ax.scatter([d[0] for d in data], [d[1] for d in data])
#         ax.set_xscale('log')
#         ax.set_yscale('log')
#         ax.legend(loc='lower center')

#       plt.show()
###

      '''
      ### PLOT 3B-1: 4 region plots

      Description: Cartesian plot of protrusion orientation angle and protrusion length with a density color scheme.
      X: Protrusion angle (radians, zero is towards barrier)
      Y: Protrusion length (microns)
      Resources: extension list for each region
      Method: extract details from extensions

      '''
###
#       fig = plt.figure()
#       axs = [141,142,143,144]
#       corrections = {'050714':(1, math.pi/2.0),
#                      '190714':(-1, math.pi),
#                      '260714':(1, math.pi),}

#       max_length = int(max([float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels) for extension in Extension.objects.all()]))

#       for region in Region.objects.all():
#         data = ([],[])
#         for extension in region.extensions.all():
#           c = corrections[extension.cell.experiment.name]
#           data[0].append(float(c[0])*float(extension.angle) + float(c[1]))
#           data[1].append(float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels))

#         ax = fig.add_subplot(axs[region.index-1])
#         ax.set_ylim([0,max_length])
#         ax.set_xlim([-4,4])

#         x = np.array(data[0])
#         y = np.array(data[1])

#         #translate
#         x[x>math.pi] -= 2*math.pi
#         x[x<-math.pi] += 2*math.pi

#         xy = np.vstack([x,y])
#         z = gaussian_kde(xy)(xy)
#         idx = z.argsort()
#         x, y, z = x[idx], y[idx], z[idx]

#         ax.scatter(x, y, c=z, s=50, edgecolor='')

#       plt.show()
###

#       cell_instance = CellInstance.objects.get(pk=1002)

#       mask = cell_instance.mask_array()

#       print([(float(extension.length), float(extension.angle)*180.0/math.pi) for extension in cell_instance.extensions.all()])

#       plt.imshow(mask)
#       plt.show()



      '''
      ### PLOT 3B-2: 4 region plots

      Description: Polar plot of protrusion orientation angle and protrusion length with a density color scheme.
      X: Protrusion angle (radians, zero is towards barrier)
      Y: Protrusion length (microns)
      Resources: extension list for each region
      Method: extract details from extensions

      '''
###
#       fig = plt.figure()
#       axs = [141,142,143,144]
#       corrections = {'050714':(1, math.pi/2.0),
#                      '190714':(-1, math.pi),
#                      '260714':(1, math.pi),}

#       max_length = int(max([float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels) for extension in Extension.objects.all()]))

#       for region in Region.objects.all():
#         data = ([],[])
#         for extension in region.extensions.all():
#           c = corrections[extension.cell.experiment.name]
#           data[0].append(float(c[0])*float(extension.angle) + float(c[1]))
#           data[1].append(float(extension.length)*float(extension.cell.experiment.x_microns_over_pixels))

#         ax = fig.add_subplot(axs[region.index-1], polar=True)
#         ax.set_ylim([0,max_length])

#         x = np.array(data[0])
#         y = np.array(data[1])

#         #translate
#         x[x>math.pi] -= 2*math.pi
#         x[x<-math.pi] += 2*math.pi

#         xy = np.vstack([x,y])
#         z = gaussian_kde(xy)(xy)
#         idx = z.argsort()
#         x, y, z = x[idx], y[idx], z[idx]

#         ax.scatter(x, y, c=z, s=50, edgecolor='')

#       plt.show()
###

      '''
      ### PLOT 3C: 4 region plots

      Description: Plot of extension angle vs cell instance velocity angle
      X: Protrusion angle (radians, zero is towards barrier)
      Y: Current cell instance velocity angle
      Resources: cell instance list for each region
      Method: extract details from extensions and cell instances

      '''



      '''
      ### PLOT 3D: 4 region plots

      Description: Plot of maximum extension length against number of protrusions.
      X: Protrusion angle (radians, zero is towards barrier)
      Y: Protrusion length (microns)
      Resources: extension list for each region
      Method: extract details from extensions

      '''
###
#       fig = plt.figure()
#       axs = [141, 142, 143, 144]

#       for region in Region.objects.all(): #one plot per region
#         ax = fig.add_subplot(axs[int(region.index-1)])

#         data = ([],[]) #number, length

#         for cell_instance in region.cell_instances.all():
#           data[0].append(cell_instance.extensions.count())
#           data[1].append(cell_instance.max_extension_length*cell_instance.experiment.x_microns_over_pixels)

#         ax.scatter(data[0], data[1])
#         ax.set_title('region %d'%region.index)

#       plt.show()
###

      '''
      ### PLOT 3E-1: density

      Description: Scatter plot of cell instance velocity against distance from barrier.
      X: Distance from barrier
      Y: Cell instance velocity
      Resources: cell instance list
      Method: cell instance max extension length and distance

      '''
###
#       #for each experiment, get the x values of the cells when they first enter region 2
#       #take the average
#       #use the result as the x value of the barrier
#       #use for all cells in the experiment

#       experiment_barrier_location_dict = {}

#       for experiment in Experiment.objects.all():
#         for series in experiment.series.all():
#           barrier_x_total = 0
#           count = 0
#           #get all cells
#           for cell in series.cells.all():
#             if cell.barrier_crossing_timestep!=-1:
#               count += 1
#               barrier_x_total += cell.cell_instances.get(timestep__index=cell.barrier_crossing_timestep).position_x

#           if count!=0:
#             experiment_barrier_location_dict[experiment.name+str(series.index)] = int(float(barrier_x_total)/float(count))

#       #setup fig and subplots
#       fig = plt.figure()
#       ax = fig.add_subplot(111)

#       data = ([],[])
#       for cell_instance in CellInstance.objects.all():
#         key = cell_instance.experiment.name+str(cell_instance.series.index)
#         if key in experiment_barrier_location_dict.keys():
#           data[0].append((experiment_barrier_location_dict[key] - cell_instance.position_x)*cell_instance.experiment.x_microns_over_pixels)
#           data[1].append(np.linalg.norm(cell_instance.velocity()*cell_instance.experiment.microns_over_pixels()/cell_instance.experiment.time_per_frame*60)) #microns per minute

#       #density heatmap
#       x = np.array(data[0], dtype=float)
#       y = np.array(data[1], dtype=float)
#       xy = np.vstack([x,y])
#       z = gaussian_kde(xy)(xy)
#       idx = z.argsort()
#       x, y, z = x[idx], y[idx], z[idx]

#       ax.scatter(x, y, c=z, s=50, edgecolor='')

#       plt.gca().yaxis.set_major_locator(MaxNLocator(prune='lower'))
#       plt.show()
###

      '''
      ### PLOT 3E-2: regions

      Description: Scatter plot of cell instance velocity against distance from barrier.
      X: Distance from barrier
      Y: Cell instance velocity
      Resources: cell instance list
      Method: cell instance max extension length and distance

      '''
###
#       #for each experiment, get the x values of the cells when they first enter region 2
#       #take the average
#       #use the result as the x value of the barrier
#       #use for all cells in the experiment

#       experiment_barrier_location_dict = {}

#       for experiment in Experiment.objects.all():
#         for series in experiment.series.all():
#           barrier_x_total = 0
#           count = 0
#           #get all cells
#           for cell in series.cells.all():
#             if cell.barrier_crossing_timestep!=-1:
#               count += 1
#               barrier_x_total += cell.cell_instances.get(timestep__index=cell.barrier_crossing_timestep).position_x

#           if count!=0:
#             experiment_barrier_location_dict[experiment.name+str(series.index)] = int(float(barrier_x_total)/float(count))

#       #plots
#       colours = ['blue','red','green','yellow']
#       plots = []
#       for region in Region.objects.all():
#         data = ([],[])
#         for cell_instance in region.cell_instances.all():
#           key = cell_instance.experiment.name+str(cell_instance.series.index)
#           if key in experiment_barrier_location_dict.keys():
#             data[0].append((experiment_barrier_location_dict[key] - cell_instance.position_x)*cell_instance.experiment.x_microns_over_pixels)
#             data[1].append(np.linalg.norm(cell_instance.velocity()*cell_instance.experiment.microns_over_pixels()/cell_instance.experiment.time_per_frame*60)) #microns per minute
#         plots.append(data)

#       for i, plot in enumerate(plots):
#         plt.scatter(plot[0], plot[1], c=colours[i])

#       plt.gca().yaxis.set_major_locator(MaxNLocator(prune='lower'))
#       plt.show()
###


#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
