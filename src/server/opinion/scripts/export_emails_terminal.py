#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
from numpy import *

os_id = 1 # Using OS #1 for now

try:
    os = OpinionSpace.objects.get(pk = os_id)
except OpinionSpace.DoesNotExist:
    print 'That Opinion Space does not exist.'
    sys.exit()

for user in User.objects.all():
    print user.email