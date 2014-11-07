#apps.cell.models

#django
from django.db import models

#local
from apps.env.models import Region, Experiment, Series, Timestep

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
  def calculation_instance_velocities(self):
    pass

  def calculate_barrier_crossing_timestep(self):
    pass

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

  velocity_x = models.IntegerField(default=0)
  velocity_y = models.IntegerField(default=0)
  velocity_z = models.IntegerField(default=0)

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
    #1. rescale model image to correct the great mistake
    if self.image.get().modified.count()==0: #only run processing if modified images do not already exist
      self.rescale_model_image()

    #3. position relative to top left corner of environment
    self.calculate_position()

    #4. extension lengths and angles
    if self.extensions.count()==0: #there is no way to get previously created extensions uniquely.
      self.calculate_extensions()

    #5. volume and surface area
    self.calculate_volume_and_surface_area()

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
    black_mask_image.delete()

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
    mask_image = segmented_image.modified.create(file_name=root+'_mask'+ext, input_path=self.experiment.mask_path, series=self.series, timestep=self.timestep, description='mask')

    final_image = imresize(mask_array, segmented_image_shape)
    final_image[final_image>0]=1
    final_image.dtype = bool

    mask_image.array = final_image
    mask_image.save_array()

  def calculate_position(self):
    '''
    There are two different approaches necessary for x,y and z. x,y is a simple translation. z requires searching through the
    GFP. This method still needs to be investigated.

    Basically, the idea is that the maximum GFP intensity will occur at the center of the cell. This has been tested briefly,
    but is not 100% backed up by empirical knowledge of the cell. The GFP binds to the DNA in the cytoplasm, not in the
    nucleus, so there should be a dip in the GFP in the center of the cell. This is sort of observed, but I would have to test it
    with more cells. I have only looked at one.

    '''

    #resources
    #-self.image
    segmented_image = self.mask_image()

    #-self.cell.bounding_box
    bounding_box = self.cell.bounding_box.get()

    #-self.cell.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0) #all focus
    focus_image_set = self.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0) #gfp only

    ### X and Y
    self.cm = self.find_center_of_mass()

    #1. rescale coords with bounding box
    self.position_x = self.cell.bounding_box.get().x + self.cm[0]
    self.position_y = self.cell.bounding_box.get().y + self.cm[1]

    print(focus_image_set.count())

    ### Z
    mean_list = []
    for image in focus_image_set.order_by('focus'):
      #load
      image.load()

      #cut to bounding box
      cut_image = bounding_box.cut(image.array)

      #apply mask
      masked_image = np.ma.array(cut_image, mask=segmented_image, fill_value=0)

      mean_list.append(masked_image.mean())

    self.position_z = np.argmax(mean_list)

    ### Save
    self.save()

  def find_center_of_mass(self):
    segmented_image = self.mask_image()
    transform = distance_transform_edt(segmented_image)
    return np.rint(center_of_mass(transform)).astype(int)

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

  def calculate_volume_and_surface_area(self):
    pass

  def mask_image(self):
    segmented_image = self.image.get().modified.get(description='mask')
    segmented_image.load()
    return segmented_image.array

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
    return (self.y, self.x) #column, row

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
