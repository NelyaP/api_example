import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

GROUPS = ['GUEST', 'SALES', 'REPORTER', ]
MODELS = [
    'user', 
    'report', 
    'order', 
    ]
PERMISSIONS = ['view', 'add', 'change', ] 

class Command(BaseCommand):
    help = "Creates default group and permissions"

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    codename = '{}_{}'.format(permission, model)
                    try:
                        model_add_perm = Permission.objects.get(codename=codename)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)        
        self.stdout.write(self.style.SUCCESS("Created default groups and permissions."))