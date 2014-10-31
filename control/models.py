#control.models

#django
from django.db import models

#local

#util
import os
import re
import scipy
from scipy.ndimage import distance_transform_edt
from scipy.misc import imsave, imread, imresize
import numpy as np
import string
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math

def get_neighbour_image(image): #gets number of non-zero neighbours each cell has.
    #pad image with zeros
    big_image = np.zeros((image.shape[0]+2, image.shape[1]+2))
    big_image[1:-1,1:-1] = image
    image = big_image

    #get neighbours
    N = (
        image[  :-2,  :-2] + image[  :-2, 1:-1] + image[  :-2, 2:  ] +
        image[ 1:-1,  :-2]                      + image[ 1:-1, 2:  ] +
        image[ 2:  ,  :-2] + image[ 2:  , 1:-1] + image[ 2:  , 2:  ]
    )
    return N

# Create your models here.
class Experiment(models.Model): #contains everything about a certain experiment
  #sub: Series, Timestep,

  #properties
  name = models.CharField(default='name', max_length=255)

  #-paths
  base_path = models.CharField(default='base_path', max_length=255)
  input_path = models.CharField(default='input_path', max_length=255) #appended to base_path
  output_path = models.CharField(default='output_path', max_length=255)

  #-scaling
  x_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  y_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  z_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  time_per_frame = models.DecimalField(default=0.0, decimal_places=4, max_digits=10)

  #methods
  def gather_from_input(self):
    #get list of files
    input_path = os.path.join(self.base_path, self.input_path)
    file_list = [image_file_name for image_file_name in os.listdir(input_path) if re.search(r'\.ti[f]{1,2}$', image_file_name) is not None]
    template = self.image_templates.get(name='input')

    for file_name in file_list:
      #extract data from file name
      print('processing ... ' + file_name)
      match = re.match(template.rx, file_name)

      #unique coordinate -> create timesteps and series
      series, created = self.series.get_or_create(index=match.group('series'))
      timestep, created = self.timesteps.get_or_create(series=series, index=match.group('timestep'))
      channel = int(match.group('channel'))
      focus = int(match.group('focus'))

      self.images.create(file_name=file_name, input_path=input_path, series=series, timestep=timestep, channel=channel, focus=focus)

  def gather_segmented_images(self, data):
    #get list of files
    input_path = os.path.join(self.base_path, 'segmented')
    file_list = [image_file_name for image_file_name in os.listdir(input_path) if re.search(r'\.ti[f]{1,2}$', image_file_name) is not None]
    template = self.image_templates.get(name='segmented')

    for file_name in file_list:
      #extract data from file name
      print('processing segmented ... ' + file_name)
      match = re.match(template.rx, file_name)

      #get specific details from filename
      series = self.series.get(index=(int(match.group('series'))-1))
      cell, created = self.cells.get_or_create(series=series, index=match.group('cell_index'))
      timestep = self.timesteps.get(series=series, index=(int(match.group('timestep'))))
      region = self.regions.get(index=data[int(series.index)][int(cell.index)]['rr'][int(timestep.index)])

      cell_instance, created = self.cell_instances.get_or_create(cell=cell, series=series, region=region, timestep=timestep)
      image, created = cell_instance.image.get_or_create(file_name=file_name, input_path=input_path, series=series, timestep=timestep)

  def get_z0(self, region_id):
    avg_z0 = 0
    cell_instance_set = self.cell_instances.filter(region=self.regions.get(index=region_id))
    if cell_instance_set.count()>0:
      for cell_instance in cell_instance_set:
        avg_z0 += float(cell_instance.position_z)/cell_instance_set.count()

    return int(avg_z0)

class Series(models.Model):
  #sub:

  #properties
  experiment = models.ForeignKey(Experiment, related_name='series')
  index = models.IntegerField(default=0)

  #methods
  def get_z0(self, region_id):
    avg_z0 = 0
    cell_instance_set = self.cell_instances.filter(region=self.experiment.regions.get(index=region_id))
    if cell_instance_set.count()>0:
      for cell_instance in cell_instance_set:
        avg_z0 += float(cell_instance.position_z)/cell_instance_set.count()

    return int(avg_z0)

class Timestep(models.Model):
  #sub:

  #properties
  experiment = models.ForeignKey(Experiment, related_name='timesteps')
  series = models.ForeignKey(Series, related_name='timesteps')
  index = models.IntegerField(default=0)

  #methods

class Region(models.Model): #a single region of the experiment. Changes with time
  #sub:

  #properties
  experiment = models.ForeignKey(Experiment, related_name='regions', default=None)
  description = models.TextField(default='region')
  index = models.IntegerField(default=0)

  #methods

class Cell(models.Model): #contains all information about a single cell
  #sub: CellInstance, Extension

  #properties
  experiment = models.ForeignKey(Experiment, related_name='cells')
  series = models.ForeignKey(Series, related_name='cells')
  index = models.IntegerField(default=0)

  #methods
  def calculate_instance_velocities(self): #also displacement
    displacement = np.zeros((3))
    previous_position = np.zeros((3))

    for cell_instance in self.cell_instances.order_by('timestep'):

      #current position
      current_position = np.array((cell_instance.position_x, cell_instance.position_y, cell_instance.position_z))
      if previous_position.max()==0:
        previous_position = current_position

      #cell velocity
      (cell_instance.velocity_x, cell_instance.velocity_y, cell_instance.velocity_z) = tuple(current_position-previous_position)

      #displacement
      displacement += current_position-previous_position
      (cell_instance.displacement_x, cell_instance.displacement_y, cell_instance.displacement_z) = tuple(displacement)

      #previous position
      previous_position = current_position

      #save
      cell_instance.save()


class CellInstance(models.Model): #describes single cell at a particular timestep
  #sub:

  #properties
  experiment = models.ForeignKey(Experiment, related_name='cell_instances')
  series = models.ForeignKey(Series, related_name='cell_instances')
  cell = models.ForeignKey(Cell, related_name='cell_instances')
  region = models.ForeignKey(Region, related_name='cell_instances')
  second_region = models.CharField(max_length=1, default='')
  timestep = models.ForeignKey(Timestep, related_name='cell_instances')

  #-position and velocity
  position_x = models.IntegerField(default=0)
  position_y = models.IntegerField(default=0)
  position_z = models.IntegerField(default=0)

  velocity_x = models.IntegerField(default=0)
  velocity_y = models.IntegerField(default=0)
  velocity_z = models.IntegerField(default=0)

  displacement_x = models.IntegerField(default=0)
  displacement_y = models.IntegerField(default=0)
  displacement_z = models.IntegerField(default=0)

  #volume and surface area
  volume = models.IntegerField(default=0)
  surface_area = models.IntegerField(default=0)

  #methods
  def process_isolated(self):
    #1. rescale image so that it lines up pixel for pixel with original image set
    self.mask_array = self.rescale_model_image()

    #2. find cell center in rescaled image
    self.sub_center = self.center()

    #3. find position in x,y,z
    self.calculate_position()

    #4. find all extensions
    self.calculate_extensions()

    #5. volume and surface area
    self.calculate_volume_and_surface_area()

    #6. second region
    self.calculate_second_region()

    print('%d done...'%self.pk)

  def calculate_second_region(self):
    #based on region and position, assign second region
    total_z = self.experiment.images.filter(series=self.series, timestep=self.timestep, channel=0).count()
    top = self.experiment.get_z0() + int(60.0/float(self.experiment.z_microns_over_pixels))
    bottom = self.experiment.get_z0()

    if self.region.index == 1:
      self.second_region = 'a'
    elif self.region.index == 2 or self.region.index == 3:
      if self.position_z > bottom and self.position_z < top: #middle of environment
        self.second_region = 'e'
      else: #top or bottom
        self.second_region = 'd'
    elif self.region.index == 4:
      if self.position_z > bottom and self.position_z < top: #middle of environment
        self.second_region = 'c'
      else: #top or bottom
        self.second_region = 'b'

    #save
    print('%d done...'%self.pk)
    self.save()

  def calculate_volume_and_surface_area(self):
    #find min and max intensity focus
    max_intensity = 0
    min_intensity = 0
    for focus_image in self.cell.series.experiment.images.filter(series=self.series, timestep=self.timestep, channel=0):
      focus_image.load()
      array = self.cell.bounding_box.cut(focus_image.array)
      masked_array = np.ma.array(array, mask=self.mask_array)

      #max
      if masked_array.sum() > max_intensity:
        max_intensity = masked_array.sum()

      #min
      if min_intensity==0 or masked_array.sum()<min_intensity:
        min_intensity = masked_array.sum()

    #set max level to area of mask, set min level to 0
    #rescale intensities to fit this range
    #perimeter of object with area A is sqrt(A), multiply by 1 for z -> surface area
    neighbours = get_neighbour_image(self.mask_array)
    perimeter = (self.mask_array!=0).sum() - (neighbours!=8).sum() #number of perimeter pixels
    area = (self.mask_array!=0).sum()

    volume = 0 #number of pixels that lie within the model
    surface_area = 0 #number of pixels that lie on the edge of the model

    for focus_image in self.cell.series.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0):
      focus_image.load()
      array = self.cell.bounding_box.cut(focus_image.array)
      masked_array = np.ma.array(array, mask=self.mask_array)

      #volume
      focus_area = int(float(masked_array.sum()-min_intensity)*area/float(max_intensity-min_intensity))
      volume += focus_area

      #surface_area -> erode binary mask to have the same number of pixels as the scaled area
      eroded_mask_array = self.mask_array
      while eroded_mask_array.sum() > focus_area:
        eroded_mask_array = scipy.ndimage.binary_erosion(eroded_mask_array).astype(self.mask_array.dtype)

      #now eroded
      eroded_neighbours = get_neighbour_image(eroded_mask_array)
      eroded_perimeter = (eroded_mask_array!=0).sum() - (eroded_neighbours!=8).sum() #number of perimeter pixels
      surface_area += eroded_perimeter

    #save
    self.volume = volume
    self.surface_area = surface_area

    self.save()

  def calculate_position(self):
    #resources
    #-self.image
    #-self.cell.bounding_box
    #-self.cell.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0) #all focus

    ### X and Y
    #1. rescale coords with bounding box
    self.position_x = self.cell.bounding_box.x + self.sub_center[0]
    self.position_y = self.cell.bounding_box.y + self.sub_center[1]

    ### Z
    #mask image set with self.image
    #1. loop through z at the correct timestep
    max_intensity = 0
    for focus_image in self.cell.series.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0):
      focus_image.load()
      array = self.cell.bounding_box.cut(focus_image.array)
      masked_array = np.ma.array(array, mask=self.mask_array)
      if masked_array.sum() > max_intensity:
        max_intensity = masked_array.sum()
        self.position_z = focus_image.focus

    ### Min and Max Z
#     cropped_z_image = z_image[bb[1]:bb[1]+bb[3],bb[0]:bb[0]+bb[2]]
#     masked_z_image = np.ma.array(cropped_z_image, mask=np.invert(mask))
#     mean = masked_z_image.mean()
#     int_list.append(masked_z_image.sum())
#     masked_z_image -= mean
#     if masked_z_image.max()==255:
#       print(z)
#     mean_difference_list.append(masked_z_image.sum())

    ### Save
    self.save()

  def calculate_extensions(self):
    #resources
    #-self.image

    #calculate extensions
    #1. get edges
    if self.mask_array.max()>0:
      neighbours = get_neighbour_image(self.mask_array)
      neighbours[neighbours==8] = 0

      #edges
      edge = np.where(neighbours!=0)
      edge_list = [(x,y) for (x,y) in zip(edge[0],edge[1])]

      #angles
      polar_edge_list = [(x-self.sub_center[0], y-self.sub_center[1]) for (x,y) in edge_list]
      angle_list = [math.atan2(x,y) for (x,y) in polar_edge_list]

      #histogram
      hist,bins = np.histogram(angle_list, bins=360)
      center = (bins[:-1]+bins[1:])/2.0
      width = 0.7 * (bins[1] - bins[0])

      #distances
#       print(zip(list(tuple(self.sub_center))*len(edge_list), edge_list))
      distances = [math.sqrt(x**2 + y**2) for (x,y) in [tuple(a-np.array(b)) for (a,b) in zip([self.sub_center]*len(edge_list), edge_list)]]
      xy = zip(angle_list, distances)
      xy_sorted = sorted(xy, key=lambda x: x[0])
      data = zip(*xy_sorted)
      x, y = np.array(data[0]), np.array(data[1]) #angle, distance

      #only take evenly spaced values, maybe histogram
      indexes = np.digitize(x, bins)

      max_list = {} #contains only the max value in each bin
      for a,b,i in zip(x,y,indexes):
        if i in max_list:
          if max_list[i][0] < a:
            max_list[i] = (a,b)
        else:
          max_list[i] = (a,b)

      max_data = tuple(max_list.values())
      x,y = zip(*max_data)

      #detect triplets (low-high-low)
      peaks = []
      for i in range(len(y)):
        sample = y[i:i+3]
        x_sample = x[i:i+3]
        if len(sample)>2 and sample[0] < sample[1] and sample[2] < sample[1]:
          peaks.append((sample[1], x_sample[1]))

      #peaks is the array I want from each image
      mean = np.mean([p for p,q in peaks])
      peaks = [(p,q) for p,q in peaks if p>mean]

      #make one extension for each number that passes the filter
      for length,angle in peaks:
        self.extensions.create(experiment=self.experiment, length=length, angle=angle)

  def rescale_model_image(self):
    #resources
    #-self.image.get()
    image = self.image.get()
    #-self.cell.bounding_box
    bounding_box = self.cell.bounding_box

    #procedure
    #1. make a black figure the same size as the bounding box
    shape = (bounding_box.h, bounding_box.w)
    black_mask = np.zeros(shape)

    #2. save figure as an image wrapped by ModifiedImage
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(black_mask, cmap=cm.Greys_r)
    ax.axis('off')

    root, ext = os.path.splitext(image.file_name)
    black_mask_image = image.modified.create(file_name=root+'_black_mask'+ext, input_path=image.input_path, series=image.series, timestep=image.timestep, description='black_mask')
    plt.savefig(os.path.join(black_mask_image.input_path, black_mask_image.file_name))
    plt.close()

    #3. reload image
    black_mask_image.load()
    black_mask_array = imresize(black_mask_image.array, (480,640))

    #4. get edge columns and rows
    bw = np.dot(black_mask_array[...,:3], [0.299, 0.587, 0.144])

    b = (bw!=0)
    columns = np.all(b, axis=0)
    rows = np.all(b, axis=1)

    firstcol = columns.argmin()
    firstrow = rows.argmin()

    lastcol = len(columns) - columns[::-1].argmin()
    lastrow = len(rows) - rows[::-1].argmin()

    #5. apply to self.image.get() -> crop
    image.load()
    mask_array = image.array[firstrow:lastrow,firstcol:lastcol]

    #6. save as another ModifiedImage
    root, ext = os.path.splitext(image.file_name)
    mask_image = image.modified.create(file_name=root+'_mask'+ext, input_path=image.input_path, series=image.series, timestep=image.timestep, description='mask')

    final_image = imresize(mask_array, shape)
    final_image[final_image>0]=1
    final_image.dtype = bool

    mask_image.array = final_image
    mask_image.save_array()
    return final_image

  def center(self):
    transform = distance_transform_edt(self.mask_array)
    where = np.where(transform==np.max(transform))
    return np.array((where[0][0], where[1][0]))

  def get_position_in_microns(self):
    #scale x,y,z in pixels to microns
    return np.array([self.experiment.x_microns_over_pixels, self.experiment.y_microns_over_pixels, self.experiment.z_microns_over_pixels])*np.array([self.position_x, self.position_y, self.position_z])

  def get_velocity_in_microns(self):
    #scale x,y,z in pixels to microns
    return np.array([self.experiment.x_microns_over_pixels, self.experiment.y_microns_over_pixels, self.experiment.z_microns_over_pixels])*np.array([self.position_x, self.position_y, self.position_z])

class Extension(models.Model): #contains a single cell protrusion length
  #sub:

  #properties
  experiment = models.ForeignKey(Experiment, related_name='extensions')
  cell_instance = models.ForeignKey(CellInstance, related_name='extensions')

  length = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
  angle = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)

  #methods
