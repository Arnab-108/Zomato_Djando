from .settings import *
from django.db import connections
import mongoengine
# Disconnect all existing database connections
connections.close_all()

# Override specific settings for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',  # Use a dummy engine for testing
        'NAME': 'test_db',
    }
}

# Use the same MongoDB Atlas URI for testing
MONGO_DBNAME = 'test_zomato_db'
MONGO_URI = f'mongodb+srv://arnabadhikary007:arnabadhikary@cluster0.xrv0a3m.mongodb.net/test_zomato_db?retryWrites=true&w=majority'

# Use the custom test runner
TEST_RUNNER = 'ZomatoChronicles.test_runner.NoDbTestRunner'


# Use mongoengine connection for testing
mongoengine.connect(host=MONGO_URI, db=MONGO_DBNAME)

# Specify any other test-specific settings if needed
