from django.test.runner import DiscoverRunner
from django.db import connections
import os
import sys
from django.conf import settings

class NoDbTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        # Disable database setup
        pass

    def teardown_databases(self, old_config, **kwargs):
        # Disconnect all existing database connections
        for conn in connections.all():
            conn.close()

# Disconnect all existing database connections before running tests
connections.close_all()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZomatoChronicles.test_settings')

# Initialize Django
import django
django.setup()

# Run the tests using the custom test runner
test_runner = NoDbTestRunner(verbosity=2)
failures = test_runner.run_tests(['zomato'])  # Run tests for the 'zomato' app

if failures:
    sys.exit(1)  # If there are test failures, exit with a non-zero status code
