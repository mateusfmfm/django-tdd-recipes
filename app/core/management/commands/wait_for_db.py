"""""
Django command to wait for the DB
"""

import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError

"""Django command to wait for DB"""
class Command(BaseCommand):
    
    """Entrypoint"""
    def handle(self, *args, **options):
        self.stdout.write('Waiting4DB')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('DB unavailable...waiting...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('DB Available'))



