#apps.cell.models

#django
from django.db import models

#local
from apps.env.models import Region, Experiment, Series, Timestep
from apps.image.util.life.life import Life
from apps.image.util.life.rule import CoagulationsFillInVote
from apps.image.util.tools import get_surface_elements

#util
import os
import re
import scipy
from scipy.ndimage import distance_transform_edt
from scipy.misc import imsave, imread, imresize
from scipy.ndimage.measurements import center_of_mass
from scipy.signal import find_peaks_cwt
import numpy as np
import string
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math

### Cell
class Cell(models.Model):

  #connections
  experiment = models.ForeignKey(Experiment, related_name='cells')
  series = models.ForeignKey(Series, related_name='cells')

  #properties
  index = models.IntegerField(default=0)
  barrier_crossing_timestep = models.IntegerField(default=0)

  #methods
  def run_calculations(self):
    # velocity, displacement, crossing time
    print('calculate instance velocities...'),
    self.calculate_instance_velocities()
    print('done.')
    print('calculate barrier crossing timestep...'),
    self.calculate_barrier_crossing_timestep()
    print('done.')

  def calculate_instance_velocities(self):
    #1. resources
    #- cell_instance set -> order by timestep
    cell_instance_set = self.cell_instances.all()
    cell_instance_set_sorted = sorted(cell_instance_set, key=lambda x: x.timestep.index)

    #2. for each instance, calculate the time difference from the previous instance
    for i, cell_instance in enumerate(cell_instance_set_sorted):
      print('cell instance %d: %d'%(i, cell_instance.timestep.index))
      if cell_instance.timestep.index!=min([c.timestep.index for c in cell_instance_set]):
        #search for next timestep below
        previous_timestep_index = cell_instance.timestep.index-1
        while cell_instance_set.filter(timestep__index=previous_timestep_index).count()==0:
          previous_timestep_index -= 1

        #get cell_instance
        previous_cell_instance = cell_instance_set.get(timestep__index=previous_timestep_index)
        time_difference = cell_instance.timestep.index - previous_timestep_index

        #spatial differences
        difference_x = cell_instance.position_x - previous_cell_instance.position_x
        difference_y = cell_instance.position_y - previous_cell_instance.position_y
        difference_z = cell_instance.position_z - previous_cell_instance.position_z

        #velocity
        cell_instance.velocity_x = float(difference_x)/float(time_difference)
        cell_instance.velocity_y = float(difference_y)/float(time_difference)
        cell_instance.velocity_z = float(difference_z)/float(time_difference)

        #displacement
        first_cell_instance = cell_instance_set.get(timestep__index=min([cell_instance.timestep.index for cell_instance in cell_instance_set]))

        cell_instance.displacement_x = cell_instance.position_x - first_cell_instance.position_x
        cell_instance.displacement_y = cell_instance.position_y - first_cell_instance.position_y
        cell_instance.displacement_z = cell_instance.position_z - first_cell_instance.position_z

      else:
        (cell_instance.velocity_x, cell_instance.velocity_y, cell_instance.velocity_z) = (0,0,0)
        (cell_instance.displacement_x, cell_instance.displacement_y, cell_instance.displacement_z) = (0,0,0)

      #save
      cell_instance.save()

  def calculate_barrier_crossing_timestep(self):
    #1. resources
    #- cell_instance set
    cell_instance_set = self.cell_instances.order_by('timestep')

    #find crossing time -> earliest time when cell is in region 2
    if cell_instance_set.filter(region__index=2).count()!=0:
      self.barrier_crossing_timestep = min([cell_instance.timestep.index for cell_instance in cell_instance_set.filter(region__index=2)])
      self.save()
    else:
      self.barrier_crossing_timestep = -1
      self.save()

### CellInstance
class CellInstance(models.Model):

  #connections
  region = models.ForeignKey(Region, related_name='cell_instances')
  experiment = models.ForeignKey(Experiment, related_name='cell_instances')
  series = models.ForeignKey(Series, related_name='cell_instances')
  cell = models.ForeignKey(Cell, related_name='cell_instances')
  timestep = models.ForeignKey(Timestep, related_name='cell_instances')

  #properties
  #-position and velocity
  position_x = models.IntegerField(default=0)
  position_y = models.IntegerField(default=0)
  position_z = models.IntegerField(default=0)

  def position(self, factor=1):
    return factor*np.array([self.position_x, self.position_y, self.position_z], dtype=int)

  velocity_x = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
  velocity_y = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
  velocity_z = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)

  def velocity(self, factor=1):
    return factor*np.array([self.velocity_x, self.velocity_y, self.velocity_z], dtype=int)

  displacement_x = models.IntegerField(default=0)
  displacement_y = models.IntegerField(default=0)
  displacement_z = models.IntegerField(default=0)

  def displacement(self, factor=1):
    return factor*np.array([self.displacement_x, self.displacement_y, self.displacement_z], dtype=int)

  #-volume and surface area
  volume = models.IntegerField(default=0)
  surface_area = models.IntegerField(default=0)

  #-extensions
  max_extension_length = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
  max_extension_angle = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)

  def parameters(self):
    pass
    #return a dictionary with paramters in it. These have been rescaled by the experiment factors

  #methods
  def run_calculations(self):
    '''
    #### STAGE 1: Rescaling
    This first part must be done to accurately locate the image in the larger environment.
    '''
    #1. rescale model image to correct the great mistake
    rescaled = False
    print('Image rescaling...'),
    if self.image.get().modified.count()==0: #only run processing if modified images do not already exist
      rescaled = True
      self.rescale_model_image()

    print('done.' if rescaled else 'image not rescaled.')

    '''
    #### STAGE 2: Localisation -> loading focus images
    With the image rescaled, it now needs to be applied to the stack of focus images. This needs to be done as
    few times as possible.

    '''

    self.position_volume_and_surface_area()

    '''
    #### STAGE 3: Extensions -> using model only
    This stage does not require the focus images to be loaded.

    '''
    ext = False
    print('Extensions...'),
    if self.extensions.count()==0: #there is no way to get previously created extensions uniquely.
      ext = True
      self.calculate_extensions()

    print('done.' if ext else 'not calculated.')

  def rescale_model_image(self):
    '''
    The great mistake:

      When originally making the images to be segmented, I wanted to annotate the image with the cell number and
      timestep. This meant that I had to plot the image. When plotting the image, matplotlib encases the image in
      a plot window that usually has a size of (480, 640). This is independent of the size of the image, so the
      original scaling of the image is lost.

    The solution:

      My solution is to plot and save an image of the same size as the original image (the bounding box). This can
      then be used to find the extent of the image in the plot and provide values to cut the segmented plot with.
      It is a serious hack that is truly abominable. The mistake should never have been made initially. This solution
      will only be used as long as I am still working with these segmented images.

    '''

    ###CHECK
    # we will be creating an image named <root>_mask.<ext> from a file named <root>.<ext>.
    # Check if one already exists in the mask path, and if it does, make a mask image from it.

    #resources
    #1. cell image
    segmented_image = self.image.get()
    #2. bounding box shape
    segmented_image_shape = self.cell.bounding_box.get().shape()

    #procedure
    #1. make a black figure the same size as the original image, but without axes or any markings
    black_mask_image = segmented_image.array_to_plot_to_image(np.zeros(segmented_image_shape), 'black_mask')
    black_mask_image.load()
    black_mask_array = imresize(black_mask_image.array, (480,640)) #rescale to match plot
#     black_mask_image.delete()

    #2. get edge columns and rows
    bw = np.dot(black_mask_array[...,:3], [0.299, 0.587, 0.144]) #greyscale image. Unnecessary.

    b = (bw!=0)
    columns = np.all(b, axis=0)
    rows = np.all(b, axis=1)

    firstcol = columns.argmin()
    firstrow = rows.argmin()

    lastcol = len(columns) - columns[::-1].argmin()
    lastrow = len(rows) - rows[::-1].argmin()

    #3. apply to self.image.get() -> crop
    segmented_image.load()
    mask_array = segmented_image.array[firstrow:lastrow,firstcol:lastcol]

    #4. save as another ModifiedImage
    root, ext = os.path.splitext(segmented_image.file_name)
    mask_image = segmented_image.modified.create(file_name=root+'_mask'+ext, input_path=os.path.join(self.experiment.base_path, self.experiment.mask_path), series=self.series, timestep=self.timestep, description='mask')

    final_image = imresize(mask_array, segmented_image_shape)
    final_image[final_image>0]=1
    final_image.dtype = bool

    mask_image.array = final_image
    mask_image.save_array()

  def position_volume_and_surface_area(self):
    #1. resources
    #- segmented image and mask
    segmented_image = self.mask_image()
    mask = np.array(np.invert(segmented_image), dtype=bool) #true values are ignored

    #- bounding box
    bounding_box = self.cell.bounding_box.get()

    #- focus image set
    focus_image_set = self.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0) #only gfp

    #2. first loop:
    #- load images
    #- cut to bounding box
    #- mask with segmented image
    #- get mean list
    mean_list = []
    array_3D = []
    for focus_image in focus_image_set.order_by('focus'):
      #load
      focus_image.load()
      #cut
      cut_image = bounding_box.cut(focus_image.array)
      #mask
      focus_image.array = np.ma.array(cut_image, mask=mask, fill_value=0)
      #mean
      mean_list.append(focus_image.array.mean()) # <<< mean list
      focus_image.mean = focus_image.array.mean()
      focus_image.save()
      #3D
      array_3D.append(focus_image.array.filled())
      focus_image.unload()

    global_mean = np.sum(mean_list)/float(len(mean_list))
    array_3D = np.array(array_3D)

    #3. second loop
    #- threshold
    array_3D_binary = np.zeros(array_3D.shape)
    array_3D_binary[array_3D>global_mean] = 1

    #- run life
    for i in range(array_3D.shape[0]):
      array_binary = array_3D_binary[i]

      life = Life(array_binary)
      life.ruleset = CoagulationsFillInVote()
      life.ruleset.timestamps = [2,4,4]
      life.update_cycle()

      array_3D_binary[i] = life.array

    #5. mask 3D array
    array_3D_masked = np.ma.array(array_3D, mask=np.invert(np.array(array_3D_binary), dtype=bool), fill_value=0)
    array_3D_masked = array_3D_masked.filled()

    #5. calculate values
    #- position -> centre of mass of 3D array
    (self.position_z, self.position_y, self.position_x) = tuple(np.rint(center_of_mass(array_3D_masked)).astype(int)+bounding_box.location())

    #- volume
    self.volume = array_3D_binary.sum()

    #- surface area
    array_3D_neighbours = get_surface_elements(array_3D_binary)
    array_3D_neighbours[array_3D_neighbours>9] = 0
    self.surface_area = array_3D_neighbours.sum()

    #save
    self.save()

  def calculate_extensions(self):
    '''
    This is done by finding all points on the edge of the model and measuring their angles and distances from the COM

    '''

    #1. define edgle object
    class edgel():
      def __init__(self, index=0, x=0, y=0, d=0, a=0):
        self.index = index
        self.x = x
        self.y = y
        self.d = d
        self.a = a

    #2. resources
    #- image -> self.mask
    segmented_image = self.mask_image()

    #3. get edge
    transform = distance_transform_edt(segmented_image)
    transform[transform==0] = transform.max() #max all zeros equal to max
    edge = np.argwhere(transform==transform.min()) #edge is the min of the new transform image -> (n, 2) np array

    #4. get distances and angles from COM
    self.cm = self.find_center_of_mass()
    data = [edgel(i, e[0], e[1], math.sqrt((e[0]-self.cm[0])**2+(e[1]-self.cm[1])**2), math.atan2(e[0]-self.cm[0], e[1]-self.cm[1])) for (i,e) in enumerate(edge)]

    #5. trace along edge
    count = 0
    length = len(data)
    sorted_data = [data[0]] #index, x, y, length, angle

    while count<length-1:
      #get current point
      current_datum = sorted_data[count]

      #look for closest point to current that is not previous or current
      sorted_distance = sorted(data, key=lambda edg: math.sqrt((edg.x-current_datum.x)**2+(edg.y-current_datum.y)**2))
      min_list = filter(lambda edg: edg.index not in [d.index for d in sorted_data], sorted_distance)

      #add it to sorted_data
      sorted_data.append(min_list[0])

      count+=1

    #reposition by the minimum value to ensure all peaks are not on the edge
    peak_array = np.array([e.d for e in sorted_data])
    argmin = np.argmin(peak_array)
    peak_array2 = np.roll(peak_array, -argmin)

    #reposition indices
    peak_size = np.arange(10,20)
    peak_indices = np.array(find_peaks_cwt(peak_array2, peak_size)) + argmin
    peak_indices[peak_indices>length] -= length

    #get values at indices
    peak_list = [sorted_data[i if i<length else i-1] for i in peak_indices] #actual list of peaks. Make extension objects from these.

    #6. create extension objects
    for peak in peak_list:
      self.extensions.create(region=self.region, cell=self.cell, length=peak.d, angle=peak.a)

    #7. find max
    max_extension = max(self.extensions.all(), key=lambda x: x.length)
    self.max_extension_length = max_extension.length
    self.max_extension_angle = max_extension.angle

  def mask_image(self):
    segmented_image = self.image.get().modified.get(description='mask')
    segmented_image.load()
    return segmented_image.array

  def find_center_of_mass(self):
    segmented_image = self.mask_image()
    transform = distance_transform_edt(segmented_image)
    return np.rint(center_of_mass(transform)).astype(int)

### BoundingBox
class BoundingBox(models.Model):

  #connections
  cell = models.ForeignKey(Cell, related_name='bounding_box')

  #properties
  x = models.IntegerField(default=0)
  y = models.IntegerField(default=0)
  w = models.IntegerField(default=0)
  h = models.IntegerField(default=0)

  #methods
  def shape(self):
    return (self.h, self.w) #shape of the numpy array

  def location(self):
    return np.array((0, self.y, self.x)) #column, row

  def all(self):
    return (self.x, self.y, self.w, self.h) #standard format

  def cut(self, array):
    return array[self.y:self.y+self.h,self.x:self.x+self.w]

### Extension
class Extension(models.Model):

  #connections
  region = models.ForeignKey(Region, related_name='extensions')
  cell = models.ForeignKey(Cell, related_name='extensions')
  cell_instance = models.ForeignKey(CellInstance, related_name='extensions')

  #properties
  length = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
  angle = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
