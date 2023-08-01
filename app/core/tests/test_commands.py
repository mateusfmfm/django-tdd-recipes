"""Test custom Django management commands"""

from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2OpError


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):

    """Test waiting for DB if DB is ready"""
    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])


    """Test waiting for DB when getting OperationalError"""
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        patched_check.side_effect = [Psycopg2OpError] * 2 \
        + [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
