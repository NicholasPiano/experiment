#apps.image.util.tools

#django

#local

#util
import os
import numpy as np
from scipy.ndimage.filters import convolve

#methods
def get_neighbour_array(array): #gets number of non-zero neighbours each cell has.
  #get neighbours
  N = (
      array[  :-2,  :-2] + array[  :-2, 1:-1] + array[  :-2, 2:  ] +
      array[ 1:-1,  :-2]                      + array[ 1:-1, 2:  ] +
      array[ 2:  ,  :-2] + array[ 2:  , 1:-1] + array[ 2:  , 2:  ]
  )
  return N

#need an N dimensional neighbour finder
def get_surface_elements(array):
  #weights
  weights = np.zeros((3,3,3))
  weights[0,1,1] = 1
  weights[2,1,1] = 1
  weights[1,1,1] = 10
  weights[1,1,0] = 1
  weights[1,0,1] = 1
  weights[1,1,2] = 1
  weights[1,2,1] = 1 #star shape with 10 in the centre -> only nearest neighbours

  #convolve
  c = convolve(array, weights, mode='constant')
  return c

def cartesian(arrays, out=None):
    """
    Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out

def array_to_vmd_xyz(array, path, filename):
  ''' For each element of the array, print out its coordinates and its value to a file. '''

  with open(os.path.join(path, filename)) as xyz_file:

