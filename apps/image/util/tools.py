#apps.image.util.tools

#django

#local

#util
import os
import numpy as np
from scipy.ndimage.filters import convolve
from scipy import io as sio

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

def array_to_vmd_xyz(array, path, filename): #expects 3D array
  ''' For each element of the array, print out its coordinates and its value to a file. '''

  rows, columns, levels = array.shape

  with open(os.path.join(path, filename), 'w') as xyz_file:

    #loop over array
    counter = 0
    xyz_file.write('%d\n'%((array>0).sum()-1))
    for row in range(rows):
      for column in range(columns):
        for level in range(levels):
          if array[row,column,level]>0:
            value = array[row,column,level]
            xyz_file.write('Pixel%d %d %d %d %d\n'%(counter, row, column, level, value))
            counter+=1

def array_to_matlab_script(array, path, filename):
  sio.savemat(os.path.join(path, filename), {'array':array})

def array_to_vmd_vtf(array, path, filename):
  with open(os.path.join(path, filename), 'w') as vtf_file:

    rows, columns, levels = array.shape

    #define atoms with radii
    counter = 0
    point_dict_list = []
    mx = array.max()
    for row in range(rows):
      for column in range(columns):
        for level in range(levels):
          if array[row,column,level]>0:
            value = array[row,column,level]
            point_dict_list.append({'index':counter, 'row':row, 'column':column, 'level':level})

            vtf_file.write('atom %d radius %f\n'%(counter, float(value)/float(mx)))
            counter += 1

    #give atom positions
    vtf_file.write('\ntimestep indexed\n')
    for point_dict in point_dict_list:
      vtf_file.write('%d %d %d %d\n'%(point_dict['index'],point_dict['row'],point_dict['column'],point_dict['level']))

def get_bins(data, mod=2):
  #get interquartile range
  q75, q25 = np.percentile(data, [75,25])
  iqr = q75 - q25

  #number of bins
  data_range = np.max(data)-np.min(data)
  n_bins = data_range*(len(data)**(1/3.0))/(iqr*mod)
  return n_bins

def index_to_letter(index):
  pass
