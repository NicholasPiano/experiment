#apps.image.util.tools

#django

#local

#util
import numpy as np

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
def get_neighbour_array_3D(array):
  N = np.zeros(array.shape)

  r = [0,1,2]
  h = [-2,-1,0]
  ind = zip(r,h)

  for x0,x1 in ind:
    for y0,y1 in ind:
      print([x0,x1,y0,y1])
      print(array[x0:x1,y0:y1])
#       N += array[x0:x1,y0:y1]
#   print(N)

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
