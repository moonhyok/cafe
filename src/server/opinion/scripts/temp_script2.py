#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
import random

#p_begin_date=datetime.datetime(2014,1,16,0,0,0,0)
#print User.objects.filter(is_active=True,date_joined__lte = p_begin_date).count()*6

try:
    super_user = User.objects.get(pk = 1)
    super_user.set_password('C@Reportcard2')
    super_user.save()
except User.DoesNotExist:
    print 'Error: you must have a super user account in order to set up the database properly!'
    sys.exit()

