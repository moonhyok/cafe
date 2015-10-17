# Loads the environment with the Django project's settings file

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Path to the project directory

from django.core.management import setup_environ
import settings
setup_environ(settings)
