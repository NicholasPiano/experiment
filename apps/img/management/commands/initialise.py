# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# local
from apps.img.data import *
from apps.img.models import *

# util
import os

# vars
base_path = settings.DATA_DIR

### Command
# https://docs.djangoproject.com/en/1.7/howto/custom-management-commands/
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    # 1. create new experiments
    for experiment in experiments:
      e, e_created = Experiment.objects.get_or_create(name=experiment.name)
      if e_created:
        print('creating experiment %s...'%e.name)
        e.rmop = experiment.rmop
        e.cmop = experiment.cmop
        e.zmop = experiment.zmop
        e.tpf = experiment.tpf
        e.save()
      else:
        print('experiment %s already exists, skipping...'%e.name)

      #create paths
      if not os.path.exists(os.path.join(base_path, e.name)):
        os.mkdir(os.path.join(base_path, e.name))
      if not os.path.exists(os.path.join(base_path, e.name, 'img')):
        os.mkdir(os.path.join(base_path, e.name, 'img'))
      if not os.path.exists(os.path.join(base_path, e.name, 'plots')):
        os.mkdir(os.path.join(base_path, e.name, 'plots'))

    # 2. create new series
    for srs in series:
      experiment = Experiment.objects.get(name=srs.experiment_name)
      s, s_created = Series.objects.get_or_create(experiment=experiment, index=srs.index)
      if s_created:
        print('creating series %s/%d...'%(s.experiment.name,s.index))
      else:
        print('series %s/%d already exists, skipping...'%(s.experiment.name,s.index))

      #create paths
      if not os.path.exists(os.path.join(base_path, experiment.name, str(s.index))):
        os.mkdir(os.path.join(base_path, experiment.name, str(s.index)))
      if not os.path.exists(os.path.join(base_path, experiment.name, str(s.index), 'ij')):
        os.mkdir(os.path.join(base_path, experiment.name, str(s.index), 'ij'))
      if not os.path.exists(os.path.join(base_path, experiment.name, str(s.index), 'ij', 'in')):
        os.mkdir(os.path.join(base_path, experiment.name, str(s.index), 'ij', 'in'))
      if not os.path.exists(os.path.join(base_path, experiment.name, str(s.index), 'ij', 'out')):
        os.mkdir(os.path.join(base_path, experiment.name, str(s.index), 'ij', 'out'))
      if not os.path.exists(os.path.join(base_path, experiment.name, str(s.index), 'cp')):
        os.mkdir(os.path.join(base_path, experiment.name, str(s.index), 'cp'))
      if not os.path.exists(os.path.join(base_path, experiment.name, str(s.index), 'cp', 'in')):
        os.mkdir(os.path.join(base_path, experiment.name, str(s.index), 'cp', 'in'))
      if not os.path.exists(os.path.join(base_path, experiment.name, str(s.index), 'cp', 'out')):
        os.mkdir(os.path.join(base_path, experiment.name, str(s.index), 'cp', 'out'))
      if not os.path.exists(os.path.join(base_path, experiment.name, str(s.index), 'plots')):
        os.mkdir(os.path.join(base_path, experiment.name, str(s.index), 'plots'))

    # 3. create new regions
    for region in regions:
      r, r_created = Region.objects.get_or_create(index=region.index)
      if r_created:
        print('creating region %d...'%r.index)
        r.name = region.name
        r.description = region.description
        r.save()
      else:
        print('region %d already exists, skipping...'%r.index)

    # 4. templates
    for experiment in Experiment.objects.all():
      print('templates for experiment %s'%experiment.name)
      for template in templates:
        t, t_created = experiment.image_templates.get_or_create(name=template.name)
        if t_created:
          print('creating template "%s" for experiment %s...'%(t.name, experiment.name))
          t.rx = template.rx
          t.reverse = template.reverse
          t.save()
        else:
          print('template "%s" already exists for experiment %s, skipping...'%(t.name, experiment.name))
