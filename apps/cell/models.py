#django
from django.db import models

#local
from apps.env.models import Region, Experiment, Series, Timestep

#util


### Cell
class Cell(models.Model):

  #connections
  experiment = models.ForeignKey(Experiment, related_name='cells')
  series = models.ForeignKey(Series, related_name='cells')

  #properties


  #methods


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

  def parameters(self):
    pass
    #return a dictionary with paramters in it. These have been rescaled by the experiment factors

  #methods
  def run_calculations(self, ):
    #1. rescale model image to correct the great mistake
    self.mask = self.rescale_model_image()

    #2. position relative to top left corner of environment
    self.calculate_position()

    #3. extension lengths and angles
    self.calculate_extensions()

    #4. volume and surface area
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

    #resources
    #1. cell image
    segmented_image = self.image.get()
    #2. bounding box shape
    segmented_image_shape = self.cell.bounding_box.shape()

    #procedure
    #1. make a black figure the same size as the original image, but without axes or any markings
    black_mask_image = segmented_image.array_to_plot_to_image(np.zeros(segmented_image_shape), 'black_mask')
    black_mask_image.load()
    black_mask_array = imresize(black_mask_image.array, (480,640)) #rescale to match plot

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
    mask_image = segmented_image.modified.create(file_name=root+'_mask'+ext, input_path=segmented_image.input_path, series=self.series, timestep=self.timestep, description='mask')

    final_image = imresize(mask_array, segmented_image_shape)
    final_image[final_image>0]=1
    final_image.dtype = bool

    mask_image.array = final_image
    mask_image.save_array()
    return final_image

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
    segmented_image = self.mask

    #-self.cell.bounding_box
    bounding_box = self.cell.bounding_box

    #-self.cell.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0) #all focus
    focus_image_set = self.cell.series.experiment.images.filter(series=self.cell.series, timestep=self.timestep, channel=0):

    ### X and Y
    #1. rescale coords with bounding box
    self.position_x = self.cell.bounding_box.x + self.sub_center[0]
    self.position_y = self.cell.bounding_box.y + self.sub_center[1]

    ### Z
    #mask image set with self.image
    #1. loop through z at the correct timestep
    for focus_image in focus_image_set:
      focus_image.load()
      array = self.cell.bounding_box.cut(focus_image.array)
      masked_array = np.ma.array(array, mask=segmented_image)

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
    pass

  def calculate_volume_and_surface_area(self):
    pass

  def calculate_region(self):
    pass

### BoundingBox
class BoundingBox(models.Model):

  #connections
  cell = models.OneToOneField(Cell, related_name='bounding_box')

  #properties
  x = models.IntegerField(default=0)
  y = models.IntegerField(default=0)
  w = models.IntegerField(default=0)
  h = models.IntegerField(default=0)

  #methods
  def shape(self):
    return (self.h, self.w) #shape of the numpy array

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
