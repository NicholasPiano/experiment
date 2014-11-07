#apps.image.util.tools

#django

#local

#util
import numpy as np

#methods
def get_neighbour_array(array): #gets number of non-zero neighbours each cell has.
  #pad image with zeros
  big_array = np.zeros((array.shape[0]+2, array.shape[1]+2))
  big_array[1:-1,1:-1] = array
  array = big_array

  #get neighbours
  N = (
      array[  :-2,  :-2] + array[  :-2, 1:-1] + array[  :-2, 2:  ] +
      array[ 1:-1,  :-2]                      + array[ 1:-1, 2:  ] +
      array[ 2:  ,  :-2] + array[ 2:  , 1:-1] + array[ 2:  , 2:  ]
  )
  return N
