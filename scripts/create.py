import os
from control.models import Experiment, Series, CellInstance
from image.models import BoundingBox, CellImage

#1. paths
name = '050714'
base_path = os.path.join('/','Volumes','transport','data','confocal',name)
input_path = os.path.join('backup','backup')
output_path = os.path.join('output')

#2. scales
# x_microns_over_pixels = 274.89/512.0
# y_microns_over_pixels = 274.89/512.0
# z_microns_over_pixels = 143.7/98.0
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
# E.image_templates.create(name='segmented', rx=r'%s_series(?P<series>.+)_cell(?P<cell_index>.+)_t(?P<timestep>.+)\.tif'%name, reverse='050714_series%d_cell%d_t%d.tif')

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
#   13:
#   {
#     1:
#     {
#       'bb':
#       {
#         'x':225,'y':307,'w':226,'h':205,
#       },
#       'rr':list([1]*max_t),
#     },
#     2:
#     {
#       'bb':
#       {
#         'x':123,'y':49,'w':176,'h':172,
#       },
#       'rr':list([4]*23 + [3]*(max_t-23)),
#     },
#     3:
#     {
#       'bb':
#       {
#         'x':215,'y':60,'w':182,'h':167,
#       },
#       'rr':list([4]*29 + [3]*(max_t-29)),
#     },
#     4:
#     {
#       'bb':
#       {
#         'x':300,'y':29,'w':173,'h':181,
#       },
#       'rr':list([4]*max_t),
#     },
#     5:
#     {
#       'bb':
#       {
#         'x':62,'y':0,'w':232,'h':97,
#       },
#       'rr':list([4]*max_t),
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
for cell in E.cells.all():
  cell.calculate_instance_velocities()

