import os
import sys
import site

# site.addsitedir('/opt/os_venv/lib/python2.7/site-packages')
os.environ['HOME'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = 'opinion.settings'

# activate_env=("/opt/os_venv/bin/activate_this.py")
# execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi

site_path = '/var/www/opinion/opinion.berkeley.edu/landing/m-cafe/ieor115-fa15/src/server/'
opinion_path = '/var/www/opinion/opinion.berkeley.edu/landing/m-cafe/ieor115-fa15/src/server/opinion'
sys.path.append(site_path)
sys.path.append(opinion_path)

application = django.core.handlers.wsgi.WSGIHandler()
