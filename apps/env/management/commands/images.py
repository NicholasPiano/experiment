#django
from django.core.management.base import BaseCommand, CommandError

#local

#util

#command
class Command(BaseCommand):
    args = '<none>'
    help = ''

    def handle(self, *args, **options):
