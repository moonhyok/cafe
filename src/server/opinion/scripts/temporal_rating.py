'''this script is used to analyze rating change behavior'''

#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
try:
    import json
except ImportError:
    import simplejson as json
import numpy
from opinion.includes.queryutils import *

os.environ['MPLCONFIGDIR'] = "/tmp"

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import settings
imagepath = settings.MEDIA_ROOT + "/mobile/img/dailyupdate/"
jspath= settings.MEDIA_ROOT + "/mobile/js/"
import datetime

'''1st question for each issue, how many people change their rating
output is a histogram. horizontal axis is times of change'''
''' log information begin at 2014 01 09'''
skip_begin_date=datetime.datetime(2014,1,9,0,0,0,0)
statements = OpinionSpaceStatement.objects.all().order_by('id')
users = User.objects.filter(is_active=True,date_joined__gte=skip_begin_date)
change_record=[]
'''change include skip'''
def rating_change():
	for s in statements:
		change_s={}
		for user in users:
			visitor=Visitor.objects.filter(user=user)
			if len(visitor)>0:
				s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains=str(s.id)).order_by('-created') #get issue skip log
				s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').filter(details__startswith='slider_set '+str(s.id)).order_by('-created')
				if len(s_log_skip)+len(s_log_rating)==0: #skip
					if 1 in change_s:
						change_s[0]=change_s[0]+1
					else:
						change_s[0]=1
				else:
					if len(s_log_skip)+len(s_log_rating) in change_s:
						change_s[len(s_log_skip)+len(s_log_rating)]=change_s[len(s_log_skip)+len(s_log_rating)]+1
					else:
						change_s[len(s_log_skip)+len(s_log_rating)]=1
		change_record.append(change_s)
	for i in range(0,len(change_record)):
		print "Issue",i," ",change_record[i]
	
rating_change()			
