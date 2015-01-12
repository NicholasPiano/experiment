#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
PLOT_DIR = settings.PLOT_DIR

#local
from apps.image.models import SourceImage
from apps.cell.models import CellInstance, Cell, Extension
from apps.env.models import Region, Experiment
from apps.image.util.life.life import Life
from apps.image.util.life.rule import CoagulationsFillInVote
from apps.image.util.tools import get_surface_elements

#util
from scipy.ndimage import distance_transform_edt
from scipy.ndimage.measurements import center_of_mass
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import os
import math
from numpy.linalg import norm
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d
import scipy.optimize as optimization
from scipy.optimize import curve_fit
from scipy.misc import imread, imsave
from scipy.ndimage import binary_dilation as dilate
from matplotlib.ticker import NullFormatter
nullfmt   = NullFormatter()

# matplotlib.rc('font', **font)

class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(cell_instance, *args, **options):
    # get cell instance object
    cell_instance = CellInstance.objects.get(pk=747)

    #1. define edgle object
    class edgel():
      def __init__(self, index=0, x=0, y=0, d=0, a=0):
        self.index = index
        self.x = x
        self.y = y
        self.d = d
        self.a = a

    #2. resources
    #- image -> cell_instance.mask
    mask_array = cell_instance.mask_array()

    #3. center of mass and edge
    transform = distance_transform_edt(mask_array)
    cell_instance.cm = np.rint(center_of_mass(transform)).astype(int)
    transform[transform==0] = transform.max() #max all zeros equal to max
    edge = np.argwhere(transform==transform.min()) #edge is the min of the new transform image -> (n, 2) np array

    #4. get distances and angles from COM
    data = [edgel(i, e[0], e[1], math.sqrt((e[0]-cell_instance.cm[0])**2+(e[1]-cell_instance.cm[1])**2), math.atan2(e[0]-cell_instance.cm[0], e[1]-cell_instance.cm[1])) for (i,e) in enumerate(edge)]

    #5. trace along edge
    count = 0
    length = len(data)
    sorted_data = [data[0]] #index, x, y, length, angle

    while count<length-1:
      #get current point
      current_datum = sorted_data[count]

      #look for closest point to current that is not previous or current
      sorted_distance = sorted(data, key=lambda edg: math.sqrt((edg.x-current_datum.x)**2+(edg.y-current_datum.y)**2))
      min_list = filter(lambda edg: edg.index not in [d.index for d in sorted_data], sorted_distance)

      #add it to sorted_data
      sorted_data.append(min_list[0])

      count+=1

    peak_array = np.array([e.a for e in sorted_data])
    argmax = np.argmax(peak_array)
    sorted_data2 = np.roll(sorted_data, -argmax)

    final = list(sorted_data2[6:]) + list([sorted_data2[0]])

    x = [e.a*180.0/math.pi for e in final]
    y = [e.d*float(cell_instance.cell.experiment.x_microns_over_pixels) for e in final]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x,y)

    ax.xaxis.set_ticks([-180,-135,-90,-45,0,45,90,135,180])

    plt.xlabel(r'Angle, $\theta$ (degrees)')
    plt.ylabel('Distance from centre of cell ($\mu m$)')
    plt.title('Cell instance perimetre signal')

    plt.show()
