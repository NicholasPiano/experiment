#apps.image.util.tools

#django

#local

#util
import numpy as np

#methods
def get_neighbour_array(array): #gets number of non-zero neighbours each cell has.
  #pad image with zeros
  array = np.pad(array, 1, mode='constant')

  #get neighbours
  N = (
      array[  :-2,  :-2] + array[  :-2, 1:-1] + array[  :-2, 2:  ] +
      array[ 1:-1,  :-2]                      + array[ 1:-1, 2:  ] +
      array[ 2:  ,  :-2] + array[ 2:  , 1:-1] + array[ 2:  , 2:  ]
  )
  return N

#need an N dimensional neighbour finder
def get_neighbour_array_N(array):
  #pad with zeros
#   array = np.pad(array, 1, mode='constant')

#   #loop over array
#   for axis, i in enumerate(array.shape):
  pass
