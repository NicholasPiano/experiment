# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# local
from apps.img.models import *

# util

### Command
# https://docs.djangoproject.com/en/1.7/howto/custom-management-commands/
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    # 1. for each experiment, fetch images
    if len(args)==0:
      for experiment in Experiment.objects.all():
        experiment.input_cells()
    else:
      for arg in args:
        experiment = Experiment.objects.get(name=arg)
        experiment.input_cells()
