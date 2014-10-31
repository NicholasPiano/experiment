import os
from control.models import Experiment, Series, CellInstance
from image.models import BoundingBox, CellImage

#1. paths
name = '260714'
base_path = os.path.join('/','Volumes','transport','data','confocal',name)
input_path = os.path.join('backup','backup')
output_path = os.path.join('output')

# 2. scales
# x_microns_over_pixels = 0.5701647
# y_microns_over_pixels = 0.5696074
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
# E.image_templates.create(name='input', rx=r'%s_s(?P<series>.+)_ch(?P<channel>.+)_t(?P<timestep>.+)_z(?P<focus>.+)\.tiff'%name, reverse='260714_s%d_ch%d_t%d_z%d.tiff')
# E.image_templates.create(name='segmented', rx=r'%s_series(?P<series>.+)_cell(?P<cell_index>.+)_t(?P<timestep>.+)\.tif'%name, reverse='260714_series%d_cell%d_t%d.tif')

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
#         'x':355,'y':117,'w':389,'h':263,
#       },
#       'rr':list([1]*(21-1) + [2]*(37-22) + [3]*(78-38) + [3]*max_t),
#     },
#     2:
#     {
#       'bb':
#       {
#         'x':303,'y':182,'w':522,'h':262,
#       },
#       'rr':list([1]*(21-1) + [2]*(25-22) + [3]*(30-26) + [4]*(105-31) + [4]*max_t),
#     },
#     3:
#     {
#       'bb':
#       {
#         'x':488,'y':140,'w':305,'h':368,
#       },
#       'rr':list([1]*(65-1) + [1]*max_t),
#     },
#     4:
#     {
#       'bb':
#       {
#         'x':278,'y':20,'w':485,'h':267,
#       },
#       'rr':list([1]*(85-1) + [2]*3 + [3]*2 + [4]*40),
#     },
#     5:
#     {
#       'bb':
#       {
#         'x':581,'y':55,'w':378,'h':293,
#       },
#       'rr':list([1]*max_t),
#     },
#     6:
#     {
#       'bb':
#       {
#         'x':752,'y':158,'w':269,'h':217,
#       },
#       'rr':list([1]*max_t),
#     },
#     7:
#     {
#       'bb':
#       {
#         'x':599,'y':32,'w':274,'h':256,
#       },
#       'rr':list([1]*116 + [2]*max_t),
#     },
#   },
#   13:
#   {
#     1:
#     {
#       'bb':
#       {
#         'x':732,'y':185,'w':213,'h':269,
#       },
#       'rr':list([1]*max_t),
#     },
#     2:
#     {
#       'bb':
#       {
#         'x':0,'y':46,'w':525,'h':252,
#       },
#       'rr':list([3]*27 + [4]*max_t),
#     },
#     5:
#     {
#       'bb':
#       {
#         'x':229,'y':18,'w':436,'h':257,
#       },
#       'rr':list([1]*23 + [2]*4 + [3]*max_t),
#     },
#   },
#   14:
#   {
#     1:
#     {
#       'bb':
#       {
#         'x':0,'y':43,'w':762,'h':413,
#       },
#       'rr':list([1]*13 + [2]*6 + [3]*max_t),
#     },
#     2:
#     {
#       'bb':
#       {
#         'x':173,'y':61,'w':480,'h':447,
#       },
#       'rr':list([1]*max_t),
#     },
#     3:
#     {
#       'bb':
#       {
#         'x':295,'y':189,'w':528,'h':288,
#       },
#       'rr':list([1]*55 + [2]*(91-56) + [3]*max_t),
#     },
#     4:
#     {
#       'bb':
#       {
#         'x':362,'y':29,'w':447,'h':293,
#       },
#       'rr':list([1]*83 + [2]*(97-84) + [3]*max_t),
#     },
#     6:
#     {
#       'bb':
#       {
#         'x':454,'y':56,'w':343,'h':455,
#       },
#       'rr':list([1]*max_t),
#     },
#     7:
#     {
#       'bb':
#       {
#         'x':454,'y':56,'w':343,'h':455,
#       },
#       'rr':list([1]*68 + [2]*3 + [3]*15 + [4]*max_t),
#     },
#   },
#   15:
#   {
#     2:
#     {
#       'bb':
#       {
#         'x':495,'y':197,'w':189,'h':241,
#       },
#       'rr':list([2]*max_t),
#     },
#     4:
#     {
#       'bb':
#       {
#         'x':738,'y':24,'w':284,'h':284,
#       },
#       'rr':list([1]*max_t),
#     },
#     7:
#     {
#       'bb':
#       {
#         'x':157,'y':126,'w':358,'h':279,
#       },
#       'rr':list([4]*max_t),
#     },
#     8:
#     {
#       'bb':
#       {
#         'x':196,'y':126,'w':317,'h':292,
#       },
#       'rr':list([4]*max_t),
#     },
#     10:
#     {
#       'bb':
#       {
#         'x':284,'y':1,'w':227,'h':276,
#       },
#       'rr':list([3]*84 + [4]*max_t),
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




