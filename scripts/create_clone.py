#create experiments with base path

import os
from control.models import Experiment, Series, CellInstance
from image.models import BoundingBox, CellImage

#>>>050714 ######################################################################################

name = '050714'

### Initial
base_path = os.path.join('/','Volumes','transport','data','confocal','050714')
input_path = os.path.join('backup','backup')
output_path = os.path.join('output')

x_microns_over_pixels = 274.89/512.0
y_microns_over_pixels = 274.89/512.0
z_microns_over_pixels = 143.7/98.0

Experiment.objects.create(name=name,
                          base_path=base_path,
                          input_path=input_path,
                          output_path=output_path,
                          x_microns_over_pixels=x_microns_over_pixels,
                          y_microns_over_pixels=y_microns_over_pixels,
                          z_microns_over_pixels=z_microns_over_pixels)

E = Experiment.objects.get(name=name)

### Input template

template_name = 'input'
rx = r'050714_s(?P<series>.+)_ch(?P<channel>.+)_t(?P<timestep>.+)_z(?P<focus>.+)\.tiff'
reverse = '050714_s%d_ch%d_t%d_z%d.tiff'

E.image_templates.create(name=template_name, rx=rx, reverse=reverse)

### Gather

E.gather_from_input()

### Cells
#-series 14
series = E.series.get(index=13)

series.cells.create(index=1, description='Mid focus. In the medium at the bottom of the image. Triangular shape initially.')
series.cells.create(index=2, description='High focus. Group of three at the top of the image. In the gel. Left, nearer large pillar.')
series.cells.create(index=3, description='High focus. Group of three at the top of the image. In the gel. Middle.')
series.cells.create(index=4, description='High focus. Group of three at the top of the image. In the gel. Right.')
series.cells.create(index=5, description='Mid focus. In the gel. A bit boring. Adjacent to large pillar.')

### Regions
series.regions.create(index=1, description='In medium')
series.regions.create(index=2, description='Front line of EA barrier')
series.regions.create(index=3, description='On EA Barrier and backline of EA barrier')
series.regions.create(index=4, description='Gel (no EA)')

### Segmented image template

template_name = 'segmented'
rx = r'050714_series(?P<series>.+)_cell(?P<cell_index>.+)_t(?P<timestep>.+)\.tif'
reverse = '050714_series%d_cell%d_t%d.tif'

E.image_templates.create(name=template_name, rx=rx, reverse=reverse)

### Segmented images

def region_ranges(cell_number, timestep):
  if cell_number==1: return 1
  elif cell_number==2:
    return 4 if timestep<=23 else 3
  elif cell_number==3:
    return 4 if timestep<=29 else 3
  elif cell_number==4: return 4
  elif cell_number==5: return 4

E.gather_segmented_images(region_ranges)

### Bounding boxes

bounding_boxes = {1:{'x':225,'y':307,'w':226,'h':205,},
                  2:{'x':123,'y':49,'w':176,'h':172,},
                  3:{'x':215,'y':60,'w':182,'h':167,},
                  4:{'x':300,'y':29,'w':173,'h':181,},
                  5:{'x':62,'y':0,'w':232,'h':97,},}

for cell in series.cells.all():
  d = bounding_boxes[cell.index]
  bb = BoundingBox(cell=cell, x=d['x'], y=d['y'], w=d['w'], h=d['h'])
  bb.save()

### Calculate
for cell_instance in CellInstance.objects.all():
  cell_instance.process_isolated()


#<<<050714 ######################################################################################

#>>>190714 ######################################################################################

#1. paths
name = '190714'
base_path = os.path.join('/','Volumes','transport','data','confocal',name)
input_path = os.path.join('backup','backup')
output_path = os.path.join('output')

#2. scales
x_microns_over_pixels = 274.89/512.0
y_microns_over_pixels = 274.89/512.0
z_microns_over_pixels = 143.7/98.0
time_per_frame = 600 #seconds

E = Experiment.objects.create(name=name,
                              base_path=base_path,
                              input_path=input_path,
                              output_path=output_path,
                              x_microns_over_pixels=x_microns_over_pixels,
                              y_microns_over_pixels=y_microns_over_pixels,
                              z_microns_over_pixels=z_microns_over_pixels,
                              time_per_frame=time_per_frame)

#3. templates
E.image_templates.create(name='input', rx=r'%s_s(?P<series>.+)_ch(?P<channel>.+)_t(?P<timestep>.+)_z(?P<focus>.+)\.tiff'%name, reverse='190714_s%d_ch%d_t%d_z%d.tiff')
E.image_templates.create(name='segmented', rx=r'%s_series(?P<series>.+)_cell(?P<cell_index>.+)_t(?P<timestep>.+)\.tif'%name, reverse='050714_series%d_cell%d_t%d.tif')

#4. regions
E.regions.create(index=1, description='In medium')
E.regions.create(index=2, description='Front line of EA barrier')
E.regions.create(index=3, description='On EA Barrier and backline of EA barrier')
E.regions.create(index=4, description='Gel (no EA)')

#5. gather input
E.gather_from_input()

#6. gather segmented
max_t = E.images.filter(series=13, focus=0, channel=0).count()

data = {
  13:
  {
    1:
    {
      'bb':
      {
        'x':225,'y':307,'w':226,'h':205,
      },
      'rr':list([1]*max_t)
    }
    2:
    {
      'bb':
      {
        'x':123,'y':49,'w':176,'h':172,
      },
      'rr':list([4]*23 + [3]*(max_t-23))
    },
    3:
    {
      'bb':
      {
        'x':215,'y':60,'w':182,'h':167,
      },
      'rr':list([4]*29 + [3]*(max_t-29))
    },
    4:
    {
      'bb':
      {
        'x':300,'y':29,'w':173,'h':181,
      },
      'rr':list([4]*max_t)
    }
    5:
    {
      'bb':
      {
        'x':62,'y':0,'w':232,'h':97,
      },
      'rr':list([4]*max_t)
    }
  },
}

E.gather_segmented_images(data)

for series in E.series.all():
  for cell in series.cells.all():
    d = data[series.index][cell.index]['bb']
    bb = BoundingBox(cell=cell, x=d['x'], y=d['y'], w=d['w'], h=d['h'])
    bb.save()

#9. cell bounding boxes


### Calculate


#<<<190714 ######################################################################################

#create experiments with base path

import os
from control.models import Experiment, Series, CellInstance
from image.models import BoundingBox, CellImage

#>>>050714 ######################################################################################

name = '050714'

### Initial
# base_path = os.path.join('/','Volumes','transport','data','confocal','050714')
# input_path = os.path.join('backup','backup')
# output_path = os.path.join('output')

# x_microns_over_pixels = 274.89/512.0
# y_microns_over_pixels = 274.89/512.0
# z_microns_over_pixels = 143.7/98.0
# time_per_frame = 600 #seconds

# Experiment.objects.create(name=name,
#                           base_path=base_path,
#                           input_path=input_path,
#                           output_path=output_path,
#                           x_microns_over_pixels=x_microns_over_pixels,
#                           y_microns_over_pixels=y_microns_over_pixels,
#                           z_microns_over_pixels=z_microns_over_pixels,
#                           time_per_frame=time_per_frame)

E = Experiment.objects.get(name=name)

### Input template

# template_name = 'input'
# rx = r'050714_s(?P<series>.+)_ch(?P<channel>.+)_t(?P<timestep>.+)_z(?P<focus>.+)\.tiff'
# reverse = '050714_s%d_ch%d_t%d_z%d.tiff'

# E.image_templates.create(name=template_name, rx=rx, reverse=reverse)

### Gather

# E.gather_from_input()

### Cells
#-series 14
series = E.series.get(index=13)

### Regions
# series.regions.create(index=1, description='In medium')
# series.regions.create(index=2, description='Front line of EA barrier')
# series.regions.create(index=3, description='On EA Barrier and backline of EA barrier')
# series.regions.create(index=4, description='Gel (no EA)')

### Segmented image template

# template_name = 'segmented'
# rx = r'050714_series(?P<series>.+)_cell(?P<cell_index>.+)_t(?P<timestep>.+)\.tif'
# reverse = '050714_series%d_cell%d_t%d.tif'

# E.image_templates.create(name=template_name, rx=rx, reverse=reverse)

### Segmented images

def region_ranges(cell_number, timestep):
  if cell_number==1: return 1
  elif cell_number==2:
    return 4 if timestep<=23 else 3
  elif cell_number==3:
    return 4 if timestep<=29 else 3
  elif cell_number==4: return 4
  elif cell_number==5: return 4

E.gather_segmented_images(region_ranges)

### Bounding boxes

bounding_boxes = {1:{'x':225,'y':307,'w':226,'h':205,},
                  2:{'x':123,'y':49,'w':176,'h':172,},
                  3:{'x':215,'y':60,'w':182,'h':167,},
                  4:{'x':300,'y':29,'w':173,'h':181,},
                  5:{'x':62,'y':0,'w':232,'h':97,},}

for cell in series.cells.all():
  d = bounding_boxes[cell.index]
  bb = BoundingBox(cell=cell, x=d['x'], y=d['y'], w=d['w'], h=d['h'])
  bb.save()

### Calculate
for cell_instance in CellInstance.objects.all():
  cell_instance.process_isolated()


#<<<050714 ######################################################################################

#>>>190714 ######################################################################################

#1. paths, scales, templates
#2. create experiment
#4. create regions
#5. for each series
#   - create cells
#   - cell bounding boxes
#   - set up region ranges for each cell
#6. gather input
#8. gather segmented
#9.

#<<<190714 ######################################################################################

