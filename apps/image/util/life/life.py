#django

#local
from apps.image.util.life.rule import *
from apps.image.util.tools import get_neighbour_array

#util
import numpy as np

### CLASSES
class Life(object):

  def __init__(self, array, ruleset=VoteInfinite()):
    self.array = array
    self.ruleset = ruleset

  def update(self, index=1):
    #get rule
    rule = self.ruleset.get_rule(index)

    #get neighbours with mask
    N = get_neighbour_array(self.array)

    #get binary array from rule
    #birth
    birth = np.zeros(N.shape, bool)

    for n in rule.born:
        birth = birth | ((self.array[1:-1,1:-1]==0) & (N==n))

    survive = np.zeros(N.shape, bool)

    for n in rule.survive:
        survive = survive | ((self.array[1:-1,1:-1]==1) & (N==n))

    #set grid
    self.array[...] = 0
    self.array[1:-1,1:-1][birth | survive] = 1 #need a better way of doing this able to support multiple states.

class Composite(object): #contains original images and processed images
  #the idea behind this is each iteration of a particular process contains information that can be used.
  #I want an ndarray that can store many things about the array of images.
  pass
