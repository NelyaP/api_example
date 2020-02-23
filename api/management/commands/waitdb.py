import time
import socket

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Waits for database to be available"

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = connections['default']
        connected = None
        while not connected:
            try:
                c = db_conn.cursor()
                connected = True
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))