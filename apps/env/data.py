#apps.env.data
#script stores prototype data for constructing experiment and region objects

#django

#local

#util
import os

### Classes

class Region():
  def __init__(self, name, index, description):
    self.name = name
    self.index = index
    self.description = description

class Experiment():
  def __init__(self, name, base_path, x_microns_over_pixels, y_microns_over_pixels, z_microns_over_pixels, time_per_frame):
    self.name = name
    self.base_path = base_path
    self.x_microns_over_pixels = x_microns_over_pixels
    self.y_microns_over_pixels = y_microns_over_pixels
    self.z_microns_over_pixels = z_microns_over_pixels
    self.time_per_frame = time_per_frame

class Template():
  def __init__(self, name, rx, reverse):
    self.name = name
    self.rx = rx
    self.reverse = reverse

### Data

regions = [
  Region(name='medium', index=1, description='Cells in the medium not connected to any endothelial cells or PDMS boundaries.'),
  Region(name='barrier_front', index=2, description='Cells immediately adjacent to the front edge of the barrier without any full contact with endothelial cells.'),
  Region(name='barrier_embedded', index=3, description='Cells fully embedded in the barrier. In contact with endothelial cells on all sides.'),
  Region(name='gel', index=4, description='Cells in the gel not connected to any endothelial cells or PDMS boundaries.'),
]

experiments = [
  Experiment(name='050714', base_path=os.path.join('/','Volumes','transport','data','confocal','050714'), x_microns_over_pixels=274.89/512.0, y_microns_over_pixels=274.89/512.0, z_microns_over_pixels=143.7/98.0, time_per_frame=600),
  Experiment(name='190714', base_path=os.path.join('/','Volumes','transport','data','confocal','190714'), x_microns_over_pixels=513.53/1024.0, y_microns_over_pixels=256.51/512.0, z_microns_over_pixels=1.482, time_per_frame=600),
  Experiment(name='260714', base_path=os.path.join('/','Volumes','transport','data','confocal','260714'), x_microns_over_pixels=0.5701647, y_microns_over_pixels=0.5696074, z_microns_over_pixels=1.482, time_per_frame=600),
]

templates = [
  Template(name='input', rx=r'^[0-9]{6}_s(?P<series>.+)_ch(?P<channel>.+)_t(?P<timestep>.+)_z(?P<focus>.+)\.tiff', reverse='_series%d_ch%d_t%d_z%d.tiff'),
  Template(name='segmented', rx=r'^[0-9]{6}_series(?P<series>.+)_cell(?P<cell_index>.+)_t(?P<timestep>.+)\.tif', reverse='_series%d_cell%d_t%d.tif')
]
