#apps.cell.data
#script stores prototype data for constructing cell objects

#django

#local

#util
import bisect

### Classes

#cell
class Cell():
  def __init__(self, experiment, series, index, bounding_box, region_list):
    self.experiment = experiment
    self.series = series
    self.index = index
    self.bounding_box = bounding_box
    self.region_list = region_list

  def timestep(self, timestep):
    return self.region_list.query(timestep)

  def bounding_box(self):
    return tuple([self.bounding_box.x,self.bounding_box.y,self.bounding_box.w,self.bounding_box.h])

#bounding box
class BoundingBox():
  def __init__(self, x=0, y=0, w=0, h=0):
    self.x = x
    self.y = y
    self.w = w
    self.h = h

class RegionList():
  def __init__(self, range_dict):
    #input: range_dict = {0:0, 12:1, 17:2}
    self.range_tuple_list = sorted([(key, value) for key,value in range_dict.items()], key=lambda x: x[0])

  def query(self, timestep):
    keys = [key for key,value in self.range_tuple_list]
    bi = bisect.bisect_left(keys, timestep)
    index = bi-1 if bi!= 0 else 0
    return self.range_tuple_list[index][1]

### Data

cells = [
  Cell(experiment='050714', series=13, index=1, bounding_box=BoundingBox(x=225,y=307,w=226,h=205), region_list=RegionList(range_dict={0:1})),
  Cell(experiment='050714', series=13, index=2, bounding_box=BoundingBox(x=123,y=49,w=176,h=172), region_list=RegionList(range_dict={0:4, 24:3})),
  Cell(experiment='050714', series=13, index=3, bounding_box=BoundingBox(x=215,y=60,w=182,h=167), region_list=RegionList(range_dict={0:4, 29:3})),
  Cell(experiment='050714', series=13, index=4, bounding_box=BoundingBox(x=300,y=29,w=173,h=181), region_list=RegionList(range_dict={0:4})),
  Cell(experiment='050714', series=13, index=5, bounding_box=BoundingBox(x=62,y=0,w=232,h=97), region_list=RegionList(range_dict={0:4})),
  Cell(experiment='190714', series=12, index=1, bounding_box=BoundingBox(x=387,y=233,w=131,h=163), region_list=RegionList(range_dict={0:2})),
  Cell(experiment='190714', series=12, index=2, bounding_box=BoundingBox(x=384,y=162,w=128,h=191), region_list=RegionList(range_dict={0:2})),
  Cell(experiment='190714', series=12, index=3, bounding_box=BoundingBox(x=411,y=190,w=123,h=255), region_list=RegionList(range_dict={0:3})),
  Cell(experiment='190714', series=12, index=4, bounding_box=BoundingBox(x=427,y=45,w=109,h=228), region_list=RegionList(range_dict={0:1})),
  Cell(experiment='190714', series=13, index=1, bounding_box=BoundingBox(x=688,y=109,w=251,h=170), region_list=RegionList(range_dict={0:2})),
  Cell(experiment='190714', series=13, index=2, bounding_box=BoundingBox(x=417,y=323,w=158,h=170), region_list=RegionList(range_dict={0:2})),
  Cell(experiment='260714', series=12, index=1, bounding_box=BoundingBox(x=355,y=117,w=389,h=263), region_list=RegionList(range_dict={0:1, 21:2, 37:3, 78:0})),
  Cell(experiment='260714', series=12, index=2, bounding_box=BoundingBox(x=303,y=182,w=522,h=262), region_list=RegionList(range_dict={0:1, 21:2, 25:3, 30:4, 105:0})),
  Cell(experiment='260714', series=12, index=3, bounding_box=BoundingBox(x=488,y=140,w=305,h=368), region_list=RegionList(range_dict={0:1, 65:0})),
  Cell(experiment='260714', series=12, index=4, bounding_box=BoundingBox(x=278,y=20,w=485,h=267), region_list=RegionList(range_dict={0:1, 85:2, 89:3, 92:4})),
  Cell(experiment='260714', series=12, index=5, bounding_box=BoundingBox(x=581,y=55,w=378,h=293), region_list=RegionList(range_dict={0:1})),
  Cell(experiment='260714', series=12, index=6, bounding_box=BoundingBox(x=752,y=158,w=269,h=217), region_list=RegionList(range_dict={0:1, 60:0})),
  Cell(experiment='260714', series=12, index=7, bounding_box=BoundingBox(x=599,y=32,w=274,h=256), region_list=RegionList(range_dict={0:1, 116:2})),
  Cell(experiment='260714', series=13, index=1, bounding_box=BoundingBox(x=732,y=185,w=213,h=269), region_list=RegionList(range_dict={0:1, 96:0})),
  Cell(experiment='260714', series=13, index=2, bounding_box=BoundingBox(x=0,y=46,w=525,h=252), region_list=RegionList(range_dict={0:3, 27:4, 49:0})),
  Cell(experiment='260714', series=13, index=5, bounding_box=BoundingBox(x=229,y=18,w=436,h=257), region_list=RegionList(range_dict={0:0, 19:1, 23:2, 28:3})),
  Cell(experiment='260714', series=14, index=1, bounding_box=BoundingBox(x=0,y=43,w=762,h=413), region_list=RegionList(range_dict={0:1, 13:2, 20:3, 33:2, 42:3, 48:0})),
  Cell(experiment='260714', series=14, index=2, bounding_box=BoundingBox(x=173,y=61,w=480,h=447), region_list=RegionList(range_dict={0:1, 44:0})),
  Cell(experiment='260714', series=14, index=3, bounding_box=BoundingBox(x=295,y=189,w=528,h=288), region_list=RegionList(range_dict={0:1, 55:2, 91:3})),
  Cell(experiment='260714', series=14, index=4, bounding_box=BoundingBox(x=362,y=29,w=447,h=293), region_list=RegionList(range_dict={0:1, 83:2, 97:3})),
  Cell(experiment='260714', series=14, index=6, bounding_box=BoundingBox(x=454,y=56,w=343,h=455), region_list=RegionList(range_dict={0:1, 61:0})),
  Cell(experiment='260714', series=14, index=7, bounding_box=BoundingBox(x=157,y=127,w=358,h=280), region_list=RegionList(range_dict={0:0, 39:1, 69:2, 73:3, 109:4})),
  Cell(experiment='260714', series=15, index=2, bounding_box=BoundingBox(x=495,y=197,w=189,h=241), region_list=RegionList(range_dict={0:0, 39:2})),
  Cell(experiment='260714', series=15, index=4, bounding_box=BoundingBox(x=738,y=24,w=284,h=284), region_list=RegionList(range_dict={0:1, 68:0})),
  Cell(experiment='260714', series=15, index=7, bounding_box=BoundingBox(x=157,y=126,w=358,h=279), region_list=RegionList(range_dict={0:0, 35:4})),
  Cell(experiment='260714', series=15, index=8, bounding_box=BoundingBox(x=196,y=126,w=317,h=292), region_list=RegionList(range_dict={0:0, 35:4})),
  Cell(experiment='260714', series=15, index=10, bounding_box=BoundingBox(x=284,y=1,w=227,h=276), region_list=RegionList(range_dict={0:0, 48:3, 85:4, 105:0})),
]

### Access

def access(experiment_name, series_index, cell_index, timestep=None):
  global cells
#   print([experiment_name, int(series_index), int(cell_index)])
  f = filter(lambda x: (x.experiment==experiment_name and x.series==int(series_index) and x.index==int(cell_index)), cells)
  cell = f[0]
  if timestep is None:
    return cell
  else:
    return cell.timestep(timestep)

# cell = access('', 0, 0, timestep=13) #timestep specified. only returns region
# cell = access('', 0, 0) #returns entire cell object
