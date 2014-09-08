#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
from opinion.includes.queryutils import *
import json
from django.db.models import Q

try:
    super_user = User.objects.get(pk = 1)
    super_user.set_password('admin')
    super_user.save()
except User.DoesNotExist:
    print 'Error: you must have a super user account in order to set up the database properly!'
    sys.exit()

