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
bins=[0,0.001,0.08,0.14,0.19,0.31,0.37,0.44,0.56,0.62,0.68,0.81,0.999,1]  
def median_index(median):
     if median<=1 and median>0.99:
        return 0
     if median<=0.99 and median>0.92:
        return 1
     if median<=0.92 and median>0.86:
        return 2
     if median<=0.86 and median>0.81:
        return 3
     if median<=0.81 and median>0.69:
        return 4
     if median<=0.69 and median>0.63:
        return 5
     if median<=0.63 and median>0.56:
        return 6
     if median<=0.56 and median>0.44:
        return 7
     if median<=0.44 and median>0.38:
        return 8
     if median<=0.38 and median>0.32:
        return 9
     if median<=0.32 and median>0.19:
        return 10
     if median<=0.19 and median>0.01:
        return 11
     if median<=0.01:
        return 12

'''change include skip'''
def rating_change():
	change_record=[]
	for s in statements:
		change_s={} #a dictionary where key is the number of change, value is total people
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

def rating_change_difference():
	'''see the difference between first rating and final rating. exclude final skip user'''
	rate_diff_record=[]
	for s in statements:
		rate_diff=[0]*25 # range_diff[0] means final=A+, initial=F range[24] means final=F, initial =A+
		for user in users:
			visitor=Visitor.objects.filter(user=user)
			if len(visitor)>0:
				s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains=str(s.id)).order_by('-created') #get issue skip log
				s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__startswith='slider_set '+str(s.id)).order_by('-created')
				if len(s_log_skip)==0:
					if len(s_log_rating)>1: # not skip user change rating
						grade_initial=median_index(1-float(s_log_rating[len(s_log_rating)-1].details.split()[2])) #get initial grade
						print grade_initial
						grade_final=median_index(1-float(s_log_rating[0].details.split()[2]))
						grade_diff=grade_final-grade_initial
						rate_diff[grade_diff+12]=rate_diff[grade_diff+12]+1
				else:
					if len(s_log_rating)>1:
						if s_log_skip[0].created<s_log_rating[0].created: # final rating
							grade_initial=median_index(1-float(s_log_rating[len(s_log_rating)-1].details.split()[2]))
							grade_final=median_index(1-float(s_log_rating[0].details.split()[2]))
							grade_diff=grade_final-grade_initial
							rate_diff[grade_diff+12]=rate_diff[grade_diff+12]+1
		rate_diff_record.append(rate_diff)
	for record in rate_diff_record:
		print record
						
					
				
#rating_change()			
rating_change_difference()
