#create experiments with base path

import os
from control.models import Experiment

#1. 050714

name = '050714'

### Initial
# base_path = os.path.join('/','Volumes','Nick\'s Stuff','Segmentation','img','050714')
# input_path = os.path.join('backup','backup')
# output_path = os.path.join('output')

# x_microns_over_pixels = 274.89/512.0
# y_microns_over_pixels = 274.89/512.0
# z_microns_over_pixels = 143.7/98.0

# Experiment.objects.create(name=name,
#                           base_path=base_path,
#                           input_path=input_path,
#                           output_path=output_path,
#                           x_microns_over_pixels=x_microns_over_pixels,
#                           y_microns_over_pixels=y_microns_over_pixels,
#                           z_microns_over_pixels=z_microns_over_pixels)

E = Experiment.objects.get(name=name)

