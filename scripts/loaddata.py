import logging
import os
import sys

import django
from django.conf import settings
from django.core.management import call_command

sys.path.insert(0, 'src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skeleton.settings')

django.setup()

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

call_command('loaddata', 'users')
call_command('loaddata', 'clients')
