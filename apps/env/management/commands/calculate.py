#django
from django.core.management.base import BaseCommand, CommandError

#local


#util

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = ''

    def handle(self, *args, **options):
      pass

#error: raise CommandError('Poll "%s" does not exist' % poll_id)
#write to terminal: self.stdout.write('Successfully closed poll "%s"' % poll_id)
#self.stdout.write("Unterminated line", ending='')
