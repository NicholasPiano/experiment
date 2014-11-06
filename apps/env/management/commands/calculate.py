#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell
from apps.env.models import Region

#util
import matplotlib.pyplot as plt
import numpy as np
import math

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      ### PLOT 1 : extension length crossing the barrier

#       plots = []

#       for cell in Cell.objects.all():
#         plot = [[],[]]
#         if cell.cell_instances.filter(region__index=1).count()!=0 and cell.cell_instances.filter(region__index=3).count()!=0:

#           #find minimum timestep in region 2
#           min_time = np.min([c.timestep.index for c in list(cell.cell_instances.filter(region__index=2))+list(cell.cell_instances.filter(region__index=3))])
#           min_x = cell.cell_instances.get(timestep__index=min_time).position_x

#           for cell_instance in cell.cell_instances.all():
#             plot[0].append(cell_instance.position_x-min_x)
#             plot[1].append(np.mean([extension.length for extension in cell_instance.extensions.all()]))

#         plots.append(plot)

#       for plot in plots:
#         plt.plot(plot[0], plot[1], 'o')

#       plt.show()

#       cells = Cell.objects.filter(experiment__name='260714', series__index=14)

#       plots = []

#       for cell in cells:
#         plot = [[],[]]
# #         if cell.cell_instances.filter(region__index=1).count()!=0 and cell.cell_instances.filter(region__index=3).count()!=0:
#         for cell_instance in cell.cell_instances.all():
#           plot[0].append(cell_instance.position_x)
# #           plot[1].append(np.mean([extension.length for extension in cell_instance.extensions.all()]))
# #           plot[1].append(np.max([extension.length for extension in cell_instance.extensions.all()]))
#           plot[1].append(cell_instance.position_y)
#         plots.append(plot)

#       for plot in plots:
#         plt.plot(plot[0], plot[1], 'o')

#       plt.show()

      ## PLOT 2 : volume vs. surface area, scatter plot
      plots = []

      for region in Region.objects.all():

        plot = [[],[]]
        for cell_instance in region.cell_instances.all():
          plot[1].append(math.log(cell_instance.volume*cell_instance.experiment.x_microns_over_pixels*cell_instance.experiment.y_microns_over_pixels*cell_instance.experiment.z_microns_over_pixels))
          plot[0].append(math.log(cell_instance.mask_image().sum()/255.0))

        plots.append(plot)

      x = np.linspace(4, 2000, 50)
      y = x
      plots.append([[math.log(i) for i in x],[math.log(i) for i in y]])
      y = x**1.5
      plots.append([[math.log(i) for i in x],[math.log(i) for i in y]])

      colors = ['red','blue','cyan','purple', 'green','yellow']

      for i,plot in enumerate(plots):
        plt.scatter(plot[0], plot[1], c=colors[i], alpha=0.25)

#       plt.xlim([4,11])
      plt.show()




#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
