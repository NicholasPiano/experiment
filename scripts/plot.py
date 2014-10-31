from control.models import Cell, Region, CellInstance, Series, Experiment, Extension
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
import math
import scipy

#plots

regions = ['a','b','c','d','e']

# z = []
# for cell_instance in CellInstance.objects.all():
#   if cell_instance.region.index==2:
#     z.append(cell_instance.position_z)

# print(np.mean(z))

######
####1. box and whisker maximum protrusion lengths for different regions
# region_dict = {1:[], 2:[], 3:[], 4:[],}

# for cell_instance in CellInstance.objects.all():
#   extensions = list(cell_instance.extensions.order_by('length'))[-1:]
#   region_dict[cell_instance.region.index].extend([float(extension.length*cell_instance.experiment.x_microns_over_pixels) for extension in extensions])

# data = []
# for key in region_dict:
#   data.append(region_dict[key])

# plt.boxplot(data)
# plt.show()

######
####2. position of cells that cross the barrier

# -260714
cells = {
#   12:[2,4],
  13:[5],
#   14:[1,3,4,7],
}

experiment = Experiment.objects.get(name='260714')

plots = []

for series in cells:
  for cell_id in cells[series]:
    cell = Cell.objects.get(experiment=experiment, series=experiment.series.get(index=series), index=cell_id)
    x = []
    y = []
    x0 = 0
    time_array = [c.timestep.index for c in cell.cell_instances.all()]
    for i in sorted(time_array):
      cell_instance = cell.cell_instances.get(timestep=cell.series.timesteps.get(index=i))
      if x0==0 and cell_instance.region.index==2:
        x0 = cell_instance.position_x
      if cell_instance.position_x!=229 and cell_instance.position_y!=18:
        x.append(cell_instance.position_x)
        y.append(cell_instance.position_y)
    plots.append((np.array(x)-x0,np.array(y)))
    print((np.array(x)-x0)[0],np.array(y)[0])

for plot in plots:
  plt.plot(plot[0],plot[1], '-')
#   print([plot[0]])

plt.show()

######
####3. velocity of cells crossing the barrier rescaled to the barrier crossing

# -260714
# cells = {
#   12:[2,4],
#   13:[5],
#   14:[1,3,4,7],
# }

# experiment = Experiment.objects.get(name='260714')

# plots = []

# for series in cells:
#   for cell_id in cells[series]:
#     cell = Cell.objects.get(experiment=experiment, series=experiment.series.get(index=series), index=cell_id)
#     velocity = []
#     time = []
#     x0 = 0
#     #find cell_instance with greatest timestep
#     max_t = np.array([c.timestep.index for c in cell.cell_instances.all()]).max()
#     for i in range(max_t+1):
#       if i in [c.timestep.index for c in cell.cell_instances.all()]:
#         cell_instance = cell.cell_instances.get(timestep=cell.series.timesteps.get(index=i))
#         if x0==0 and cell_instance.region.index==2:
#           x0 = cell_instance.position_x
#         velocity.append(math.sqrt((float(experiment.y_microns_over_pixels)*cell_instance.velocity_x)**2 + (float(experiment.y_microns_over_pixels)*cell_instance.velocity_y)**2))
#         time.append(cell_instance.timestep.index)
#     plots.append((time,velocity))

# for plot in plots:
#   time = plot[0]
#   velocity = scipy.ndimage.filters.gaussian_filter1d(plot[1], 3)
#   plt.plot(time, velocity)

# plt.show()

######
####1. box and whisker velocity for different regions
# region_dict = {1:[], 2:[], 3:[], 4:[],}

# for cell_instance in CellInstance.objects.all():
#   region_dict[cell_instance.region.index].append(math.sqrt((float(cell_instance.experiment.x_microns_over_pixels)*cell_instance.velocity_x)**2+(float(cell_instance.experiment.x_microns_over_pixels)*cell_instance.velocity_y)**2)/float(cell_instance.experiment.time_per_frame))

# data = []
# for key in region_dict:
#   data.append(region_dict[key])

# boxplot(data,0,'')
# show()

# plots = []
# cells = []

# for cell in Cell.objects.all():
#   plot = []
#   for cell_instance in cell.cell_instances.all():
#     if cell_instance.position_z > 80
#       plot.append(cell_instance.position_z)
#   plots.append(plot)

# for cell in Cell.objects.all():
#   plot = []
#   for cell_instance in cell.cell_instances.all():
#     plot.append(cell_instance.position_z)
#   plots.append(plot)

# for plot in plots:
#   plt.plot(plot)

# plt.show()

# series = Experiment.objects.get(name='260714').series.get(index=14)

# areas = []

# for cell in series.cells.all():
#   area = []
#   for cell_instance in cell.cell_instances.all():
#     area.append(cell_instance.volume*series.experiment.z_microns_over_pixels*series.experiment.x_microns_over_pixels*series.experiment.y_microns_over_pixels)
#   areas.append(area)

# for area in areas:
#   plt.plot(area)

# plt.show()


