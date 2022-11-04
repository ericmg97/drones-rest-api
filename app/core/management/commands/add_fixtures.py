"""
Django command to add fixtures if the database is empty.
"""
from django.core.management.commands import loaddata
from core.models import User


class Command(loaddata.Command):
    def handle(self, *args, **options):
        if len(User.objects.all()) == 0:
            args = list(args)
            for file_name in args:
                super().handle(file_name, **options)
