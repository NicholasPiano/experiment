

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# local
from apps.env.data import experiments, series, regions

# util

### Command
# https://docs.djangoproject.com/en/1.7/howto/custom-management-commands/
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    # 1. create new experiments and series from apps.env.data
