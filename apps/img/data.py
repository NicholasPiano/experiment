#apps.image.data
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
  def __init__(self, name, base_path, rmop, cmop, zmop, tpf):
    self.name = name
    self.base_path = base_path
    self.rmop = rmop
    self.cmop = cmop
    self.zmop = zmop
    self.tpf = tpf

class Series():
  def __init__(self, experiment_name, index):
    self.experiment_name = experiment_name
    self.index = index

class Template():
  def __init__(self, name, rx, reverse):
    self.name = name
    self.rx = rx
    self.reverse = reverse

### Data
regions = [
  Region(name='medium', index=1, description='Cells in the medium not connected to any endothelial cells or PDMS boundaries.'),
  Region(name='barrier_boundary', index=2, description='Cells immediately adjacent to the front edge of the barrier without any full contact with endothelial cells.'),
  Region(name='barrier_embedded', index=3, description='Cells fully embedded in the barrier. In contact with endothelial cells on all sides.'),
  Region(name='gel', index=4, description='Cells in the gel not connected to any endothelial cells or PDMS boundaries.'),
]

experiments = [
  Experiment(name='050714', base_path=os.path.join('/','Volumes','transport','data','confocal','050714'), rmop=0.5369, cmop=0.5369, zmop=1.482, tpf=10.7003),
  Experiment(name='190714', base_path=os.path.join('/','Volumes','transport','data','confocal','190714'), rmop=0.501, cmop=0.5015, zmop=1.482, tpf=9.7408),
  Experiment(name='260714', base_path=os.path.join('/','Volumes','transport','data','confocal','260714'), rmop=0.5696074, cmop=0.5701647, zmop=1.482, tpf=7.6807),
]

series = [
  # 050714
  Series(experiment_name='050714', index=14),

  # 190714
  Series(experiment_name='190714', index=13),

  # 260714
  Series(experiment_name='260714', index=13),
  Series(experiment_name='260714', index=14),
  Series(experiment_name='260714', index=15),
  Series(experiment_name='260714', index=16),
]

templates = [
  Template(name='input', rx=r'^[0-9]{6}_s(?P<series>.+)_ch(?P<channel>.+)_t(?P<frame>.+)_z(?P<level>.+)\.tiff', reverse=r'_series%d_ch%d_t%d_z%d.tiff'),
]
