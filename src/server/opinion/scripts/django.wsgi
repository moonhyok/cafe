import os
import sys

os.environ['HOME'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = 'opinion.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
site_path = '/var/www/opinionspace/instances/%NAME%/src/server/'
opinion_path = '/var/www/opinionspace/instances/%NAME%/src/server/opinion/'
sys.path.append(site_path)
sys.path.append(opinion_path)
