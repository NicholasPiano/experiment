import os
from control.models import Experiment, Series, CellInstance
from image.models import BoundingBox, CellImage

#1. paths
name = '190714'
base_path = os.path.join('/','Volumes','transport','data','confocal',name)
input_path = os.path.join('backup','backup')
output_path = os.path.join('output')

#2. scales
# x_microns_over_pixels = 513.53/1024.0
# y_microns_over_pixels = 256.51/512.0
# z_microns_over_pixels = 1.482
# time_per_frame = 600 #seconds

# E = Experiment.objects.create(name=name,
#                               base_path=base_path,
#                               input_path=input_path,
#                               output_path=output_path,
#                               x_microns_over_pixels=x_microns_over_pixels,
#                               y_microns_over_pixels=y_microns_over_pixels,
#                               z_microns_over_pixels=z_microns_over_pixels,
#                               time_per_frame=time_per_frame)

E = Experiment.objects.get(name=name)

#3. templates
# E.image_templates.create(name='input', rx=r'%s_s(?P<series>.+)_ch(?P<channel>.+)_t(?P<timestep>.+)_z(?P<focus>.+)\.tiff'%name, reverse='190714_s%d_ch%d_t%d_z%d.tiff')
# E.image_templates.create(name='segmented', rx=r'%s_series(?P<series>.+)_cell(?P<cell_index>.+)_t(?P<timestep>.+)\.tif'%name, reverse='190714_series%d_cell%d_t%d.tif')

#4. regions
# E.regions.create(index=1, description='In medium')
# E.regions.create(index=2, description='Front line of EA barrier')
# E.regions.create(index=3, description='On EA Barrier and backline of EA barrier')
# E.regions.create(index=4, description='Gel (no EA)')

#5. gather input
# E.gather_from_input()

#6. gather segmented
# max_t = E.images.filter(series=E.series.get(index=13), focus=0, channel=0).count()

# data = {
#   12:
#   {
#     1:
#     {
#       'bb':
#       {
#         'x':387,'y':233,'w':131,'h':163,
#       },
#       'rr':list([2]*max_t),
#     },
#     2:
#     {
#       'bb':
#       {
#         'x':384,'y':162,'w':128,'h':191,
#       },
#       'rr':list([2]*max_t),
#     },
#     3:
#     {
#       'bb':
#       {
#         'x':411,'y':190,'w':123,'h':255,
#       },
#       'rr':list([3]*max_t),
#     },
#     4:
#     {
#       'bb':
#       {
#         'x':427,'y':45,'w':109,'h':228,
#       },
#       'rr':list([1]*max_t),
#     },
#   },
#   13:
#   {
#     1:
#     {
#       'bb':
#       {
#         'x':688,'y':109,'w':251,'h':170,
#       },
#       'rr':list([2]*max_t),
#     },
#     2:
#     {
#       'bb':
#       {
#         'x':417,'y':323,'w':158,'h':170,
#       },
#       'rr':list([2]*max_t),
#     },
#   },
# }

# E.gather_segmented_images(data)

# for series in E.series.all():
#   for cell in series.cells.all():
#     d = data[series.index][cell.index]['bb']
#     bb = BoundingBox(cell=cell, x=d['x'], y=d['y'], w=d['w'], h=d['h'])
#     bb.save()

# E.cells.all().delete()

### Calculate
#1. individual cell instances
# for cell_instance in E.cell_instances.all():
#   cell_instance.delete()
#   cell_instance.process_isolated()

#2. whole cells
# for cell in E.cells.all():
#   cell.calculate_instance_velocities()

