#apps.cell.models

#django
from django.db import models

#local
from apps.env.models import Region, Experiment, Series, Timestep
from apps.image.util.life.life import Life
from apps.image.util.life.rule import *
from apps.image.util.tools import get_surface_elements

#util
import os
import re
import scipy
from scipy.ndimage import distance_transform_edt
from scipy.misc import imsave, imread, imresize
from scipy.ndimage.measurements import center_of_mass
from scipy.signal import find_peaks_cwt
from scipy.ndimage.morphology import binary_dilation as dilate
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
    first_timestep_index = min([c.timestep.index for c in cell_instance_set])

    #2. for each instance, calculate the time difference from the previous instance
    for i, cell_instance in enumerate(cell_instance_set_sorted):
      if cell_instance.timestep.index!=first_timestep_index:
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
        first_cell_instance = cell_instance_set.get(timestep__index=first_timestep_index)

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
      self.barrier_crossing_timestep = min([c.timestep.index for c in cell_instance_set.filter(region__index=2)])
      self.save()
    else:
      self.barrier_crossing_timestep = -1
      self.save()

  def create_bounding_box(self, x=0, y=0, w=0, h=0):
    self.bounding_box = BoundingBox(x=x, y=y, w=w, h=h)
    self.save()

### CellInstance
class CellInstance(models.Model):

  def __str__(self):
    return '%s series %d, cell %d, t-%d' % (self.experiment.name, self.series.index, self.cell.index, self.timestep.index)

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

  def position(self, factor=None):
    factor = np.array([self.experiment.x_microns_over_pixels, self.experiment.y_microns_over_pixels, self.experiment.z_microns_over_pixels], dtype=float) if factor is None else factor
    return factor*np.array([self.position_x, self.position_y, self.position_z], dtype=float)

  velocity_x = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
  velocity_y = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
  velocity_z = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)

  def velocity(self):
    return np.array([self.experiment.x_microns_over_pixels, self.experiment.y_microns_over_pixels], dtype=float)*np.array([self.velocity_x, self.velocity_y], dtype=float)/float(self.experiment.time_per_frame)

  displacement_x = models.IntegerField(default=0)
  displacement_y = models.IntegerField(default=0)
  displacement_z = models.IntegerField(default=0)

  def displacement(self, factor=1):
    return factor*np.array([self.displacement_x, self.displacement_y, self.displacement_z], dtype=int)

  #-volume and surface area
  volume = models.IntegerField(default=0)
  surface_area = models.IntegerField(default=0)

  def area(self):
    return float(self.experiment.x_microns_over_pixels*self.experiment.y_microns_over_pixels)*self.surface_area

  #-extensions
  max_extension_length = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
  max_extension_angle = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)

  def parameters(self):
    pass
    #return a dictionary with paramters in it. These have been rescaled by the experiment factors

  #methods
  def run_calculations(self):

    '''
    Combining calculations into one method now that the mask is done.

    Tasks:
    1. Volume
    2. Surface area
    3. Extensions

    '''
    if self.volume==0:
      self.position_volume_surface_area()

    ext = False
    print('Extensions...'),
    if self.extensions.count()==0: #there is no way to get previously created extensions uniquely.
      ext = True
      self.calculate_extensions()

    print('done.' if ext else 'not calculated.')

  def position_volume_surface_area(self):
    #1. resources
    #- mask
    mask = np.array(np.invert(self.mask_array()), dtype=bool)

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
    self.surface_area = array_3D_binary[self.position_z].sum() #area of the middle slice

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
    mask_array = self.mask_array()

    #3. center of mass and edge
    transform = distance_transform_edt(mask_array)
    self.cm = np.rint(center_of_mass(transform)).astype(int)
    transform[transform==0] = transform.max() #max all zeros equal to max
    edge = np.argwhere(transform==transform.min()) #edge is the min of the new transform image -> (n, 2) np array

    #4. get distances and angles from COM
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

    #save
    self.save()

  def mask_array(self):
    image = self.image.get()
    image.load()
    return image.array

  def reconstruction_3D(self, ones=False):
    #1. resources
    #- mask
    mask = np.array(np.invert(self.mask_array()), dtype=bool)

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
      if i<self.position_z-5 or i>self.position_z+5:
        life.update_cycle() #again

      array_3D_binary[i] = life.array

    #5. mask 3D array
    array_3D_masked = np.ma.array(array_3D, mask=np.invert(np.array(array_3D_binary), dtype=bool), fill_value=0)
    array_3D_masked = array_3D_masked.filled()

    #6. set all nonzero to one
    if ones:
      array_3D_masked[array_3D_masked>0] = 1

    #7. insert mask outline into top and bottom layers of 3D array

    return array_3D_masked

  def reconstruction_3D_reduced(self):
    ''' On each level, only the 10 furthest pixels from the center of the cell are accepted. '''
    #1. resources
    #- mask
    mask = np.array(np.invert(self.mask_array()), dtype=bool)

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

    #6. set all nonzero to one
    if ones:
      array_3D_masked[array_3D_masked>0] = 1

    #7. insert mask outline into top and bottom layers of 3D array

    return array_3D_masked

  def reconstruction_mask_outline(self, top_and_bottom=False):
    ''' Basically the same as the 3D reconstruction, but with the mask outline on the top and bottom of the field '''
    #1. resources
    #- mask
    mask = np.array(np.invert(self.mask_array()), dtype=bool)

    #- number of images in stack
    number_of_stack_images = self.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0).count()

    #2. make blank array
    mask_3D = np.zeros((number_of_stack_images, mask.shape[0], mask.shape[1]))

    #3. dilate mask and subtract to get edge
    dilated_mask = dilate(mask)
    mask = dilated_mask - mask

    #4. set top and bottom of 3D
    mask_3D[0] = mask
    mask_3D[:-1] = mask

    return mask_3D

  def display_model(self):
    ''' Brings up matplotlib window with the model in its field. '''
    pass

  def display_model_in_environment(self):
    ''' Displays the model and field outlines in the original brightfield image. '''
    pass

  def volume_test(self, radius_estimate=7): #microns
    ''' On each level, only the 10 furthest pixels from the center of the cell are accepted. '''
    #1. resources
    #- mask
    mask = np.array(np.invert(self.mask_array()), dtype=bool)

    #- bounding box
    bounding_box = self.cell.bounding_box.get()
#     bounding_box.y = bounding_box.y - 30

    #- focus image set
    focus_image_set = self.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0) #only gfp

    #2. first loop:
    #- load images
    #- cut to bounding box
    #- mask with segmented image
    #- get mean list
    mean_list = []
    above_mean_list = []
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
      above_mean_list.append((focus_image.array>focus_image.mean).sum())
      #3D
      array_3D.append(focus_image.array.filled())
      focus_image.unload()

    global_mean = np.sum(mean_list)/float(len(mean_list))
    array_3D = np.array(array_3D)

    #radius estimate
    max_pos = np.argmax(mean_list)
    microns_area_radius_squared = (self.surface_area*float(self.experiment.x_microns_over_pixels)**2)/math.pi
    level_delta = int(((radius_estimate**3)/microns_area_radius_squared)/float(self.experiment.z_microns_over_pixels)) + 1

    #3. second loop
    #- threshold
    array_3D_binary = np.zeros(array_3D.shape)
    array_3D_binary[array_3D>global_mean] = 1

    above_global_mean_list = []

    #- run life
    for i in range(max_pos-level_delta if max_pos-level_delta >= 0 else 0, max_pos+level_delta+1 if max_pos+level_delta+1 < array_3D.shape[0] else array_3D.shape[0]-1):
      array_original = array_3D[i]
      above_global_mean_list.append((array_original>global_mean).sum())
      array_binary = array_3D_binary[i]

      life = Life(array_binary)
      life.ruleset = CoagulationsFillInVote()
      life.ruleset.timestamps = [2,4,4]
      life.update_cycle()

      array_3D_binary[i] = life.array

    #4. cut outside range
    array_3D[:max_pos-level_delta-1] = 0
    array_3D[max_pos+level_delta+1:] = 0

    #5. mask 3D array
    array_3D_masked = np.ma.array(array_3D, mask=np.invert(np.array(array_3D_binary), dtype=bool), fill_value=0)
    array_3D_masked = array_3D_masked.filled()

    #7. insert mask outline into top and bottom layers of 3D array

    return (array_3D_masked, mean_list, above_mean_list, global_mean, above_global_mean_list)

  def brightfield_3D_array(self):
    #- bounding box
    bounding_box = self.cell.bounding_box.get()

    #- focus image set
    focus_image_set = self.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=1).order_by('focus') #only bf

    #compile
    brightfield_3D = []

    for im in focus_image_set:
      im.load()
      cut_image = bounding_box.cut(im.array)
      brightfield_3D.append(cut_image)
      im.unload()
    brightfield_3D = np.array(brightfield_3D)

    return brightfield_3D

  def gfp_3D_array(self):
    #- bounding box
    bounding_box = self.cell.bounding_box.get()

    #- focus image set
    focus_image_set = self.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0).order_by('focus') #only gfp

    gfp_3D = []

    for im in focus_image_set:
      im.load()
      cut_image = bounding_box.cut(im.array)
      gfp_3D.append(cut_image)
      im.unload()

    gfp_3D = np.array(gfp_3D)

    return gfp_3D

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

  def m_length(self):
    return float(self.cell.experiment.x_microns_over_pixels*self.length)

  angle = models.DecimalField(default=0.0, decimal_places=4, max_digits=8)
