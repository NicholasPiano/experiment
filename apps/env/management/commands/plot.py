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
#         ax.plot(plot[0], plot[1], 'o', c=colors[i], alpha=0.5)

#       #lines
#       x = np.linspace(0, 10**6, 1000000)
#       y0 = x
#       ax.plot(x, y0)
#       y1 = x**1.5
#       ax.plot(x, y1)

#       ax.set_yscale('log')
#       ax.set_xscale('log')

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
#           plots.append((cell_instance.position_x-x_barrier, cell_instance.max_extension_length, colors[cell_instance.region.index-1]))
#           print([cell_instance.position_x-x_barrier, cell_instance.max_extension_length, colors[cell_instance.region.index-1]])

#       fig = plt.figure()
#       ax = plt.gca()

#       for plot in plots:
#         ax.bar(plot[0], plot[1], color=plot[2], alpha=0.5)

#       plt.show()



#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
