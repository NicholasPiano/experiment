#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance, Cell, Extension
from apps.env.models import Region

#util
import matplotlib.pyplot as plt
import numpy as np
import math
from numpy.linalg import norm
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
      '''
      ### PLOT 1

      Description: Volume and surface area scatter plot, colored by region
      X: Surface area
      Y: Volume
      Resources: cell instance list for each region
      Method: extract volume and surface area from each cell instance

      '''



#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
