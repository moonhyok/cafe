#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
import random

#p_begin_date=datetime.datetime(2014,1,16,0,0,0,0)
#print User.objects.filter(is_active=True,date_joined__lte = p_begin_date).count()*6

for l in LogUserEvents.objects.filter(log_type=11,details__contains="slider_set").exclude(details__contains="skip"):
	print l.details.split()[1], l.logger_id
