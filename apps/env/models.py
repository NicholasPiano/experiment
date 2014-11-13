#apps.env.models

#django
from django.db import models

#local
from apps.cell.data import access as cell_data_access

#util
import os
import re
from scipy.misc import imread, imsave

### Region
class Region(models.Model):

  #properties
  name = models.CharField(max_length=1)
  index = models.IntegerField(default=0)
  description = models.TextField(default='description')

### Experiment
class Experiment(models.Model):

  #properties
  name = models.CharField(max_length=255)

  #-paths
  base_path = models.CharField(max_length=255)
  input_path = models.CharField(default=os.path.join('backup','backup'), max_length=255) #appended to base_path
  segmented_path = models.CharField(default='segmented', max_length=255)
  mask_path = models.CharField(default='mask', max_length=255)
  modified_path = models.CharField(default='modified', max_length=255)
  plot_path = models.CharField(default='plot', max_length=255)

  #-scaling
  x_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  y_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)
  z_microns_over_pixels = models.DecimalField(default=0.0, decimal_places=4, max_digits=6)

  def volume(self, voxels): #returns microns cubed
    return voxels*float(self.x_microns_over_pixels*self.y_microns_over_pixels*self.z_microns_over_pixels)

  def area(self, pixels): #returns microns squared
    return pixels*float(self.x_microns_over_pixels*self.y_microns_over_pixels)

  time_per_frame = models.DecimalField(default=0.0, decimal_places=4, max_digits=10)

  def speed(self, pixels_per_timestep): #returns pixels per second
    return pixels_per_timestep*float(1.0/self.time_per_frame)

  #methods
  def create_images_from_input_directory(self):
    #1. get list of files
    input_path = os.path.join(self.base_path, self.input_path)
    file_list = [image_file_name for image_file_name in os.listdir(input_path) if re.search(r'\.ti[f]{1,2}$', image_file_name) is not None]
    template = self.image_templates.get(name='input')

    #2. extract details from each file_name and get or create objects
    for file_name in file_list:
      match = template.match(file_name)

      series, created = self.series.get_or_create(index=(int(match.group('series'))+1))
      timestep, created = self.timesteps.get_or_create(series=series, index=match.group('timestep'))
      channel = int(match.group('channel'))
      focus = int(match.group('focus'))

      image, created = self.images.get_or_create(file_name=file_name, input_path=input_path, series=series, timestep=timestep, channel=channel, focus=focus)
      print('processing input ... ' + file_name + (' (created)' if created else ''))

  def create_cells_from_segmented_directory(self):
    #1. get list of files
    input_path = os.path.join(self.base_path, self.segmented_path)
    file_list = [image_file_name for image_file_name in os.listdir(input_path) if re.search(r'\.ti[f]{1,2}$', image_file_name) is not None]
    template = self.image_templates.get(name='segmented')

    #2. extract details from each file_name and get or create objects
    for file_name in file_list:
      match = template.match(file_name)

      #these must exist or be created
      series = self.series.get(index=match.group('series')) #subtract one from series.
      timestep = self.timesteps.get(series=series, index=match.group('timestep'))
      cell, created = self.cells.get_or_create(series=series, index=match.group('cell_index'))
      bb = cell_data_access(self.name, series.index, cell.index).bounding_box
      bounding_box, created = cell.bounding_box.get_or_create(x=bb.x, y=bb.y, w=bb.w, h=bb.h)

      #might be zero
      region_index = cell_data_access(self.name, series.index, cell.index, timestep=timestep.index)

      if region_index != 0: #outside capture range

        #image might be blank
        open_image = imread(os.path.join(input_path, file_name))
        if open_image.max() != 0:

          #can now create image and cell_instance
          region = Region.objects.get(index=region_index)
          cell_instance, created = self.cell_instances.get_or_create(cell=cell, series=series, region=region, timestep=timestep)
          image, created = cell_instance.image.get_or_create(file_name=file_name, input_path=input_path, series=series, timestep=timestep)
          print('processing segmented ... ' + file_name + (' (created)' if created else ''))

        else:
          print('skipping %s, %d, %d: blank image'%(self.name, int(series.index), int(cell.index)))
      else:
        print('skipping %s, %d, %d: outside range'%(self.name, int(series.index), int(cell.index)))

### Series
class Series(models.Model):

  #connections
  experiment = models.ForeignKey(Experiment, related_name='series')

  #properties
  index = models.IntegerField(default=0)
  max_timestep = models.IntegerField(default=0)
  max_focus = models.IntegerField(default=0)

### Timestep
class Timestep(models.Model):

  #connections
  experiment = models.ForeignKey(Experiment, related_name='timesteps')
  series = models.ForeignKey(Series, related_name='timesteps')

  #properties
  index = models.IntegerField(default=0)
