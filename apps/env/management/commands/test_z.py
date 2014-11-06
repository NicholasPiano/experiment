#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.cell.models import CellInstance
from apps.image.models import SourceImage

#util
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.misc import imsave

class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):



#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
