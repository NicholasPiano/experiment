#apps.image.util

#django

#local

#util
import numpy as np

#methods

def get_neighbour_image(image): #gets number of non-zero neighbours each cell has.
  #pad image with zeros
  big_image = np.zeros((image.shape[0]+2, image.shape[1]+2))
  big_image[1:-1,1:-1] = image
  image = big_image

  #get neighbours
  N = (
      image[  :-2,  :-2] + image[  :-2, 1:-1] + image[  :-2, 2:  ] +
      image[ 1:-1,  :-2]                      + image[ 1:-1, 2:  ] +
      image[ 2:  ,  :-2] + image[ 2:  , 1:-1] + image[ 2:  , 2:  ]
  )
  return N
