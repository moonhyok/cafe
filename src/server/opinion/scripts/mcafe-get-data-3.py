#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
try:
    import json
except ImportError:
    import simplejson as json
import numpy as np
from opinion.includes.queryutils import *
import csv
import scipy.io
import datetime

exclude_list=['goldberg@berkeley.edu','nonnecke@citris-uc.org','nonnecke@berkeley.edu','sanjay@eecs.berkeley.edu','goldberg@eecs.berkeley.edu','angelaslin@berkeley.edu','matti@example.com','patel24jay@gmail.com','ccrittenden@berkeley.edu','alisoncliff@berkeley.edu','hunallen@gmail.com','hunallen@berkeley.edu']
user=User.objects.exclude(username__in=exclude_list).filter(is_active=True).order_by('id')
user=user[51:]

statements = OpinionSpaceStatement.objects.all().order_by('id')

#rating date
rate_1st_date=datetime.datetime(2014,6,4,7,0,0)
rate_2nd_date=datetime.datetime(2014,6,19,7,0,0)
rate_3rd_date=datetime.datetime(2014,6,26,9,0,0)
rate_4th_date=datetime.datetime(2014,7,3,10,0,0)
rate_5th_date=datetime.datetime(2014,7,10,10,0,0)
rate_6th_date=datetime.datetime(2014,7,17,10,0,0)
rate_7th_date=datetime.datetime(2014,7,24,10,0,0)
rate_end_date=datetime.datetime(2014,8,21,0,0,0)


visitors_1=Visitor.objects.filter(created__gte=rate_1st_date,created__lt=rate_2nd_date)
grade_week1_v=np.zeros(len(visitors_1))
for i in range(len(grade_week1_v)):
    s_log=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_1[i].id,log_type=11).filter(created__gte=rate_1st_date,created__lt=rate_2nd_date)
    if len(s_log)>0:
        grade_week1_v[i]=1


#get 1st week visitor grades(not registed as user)
baseline_issues_1st_v=-1*np.ones((len(visitors_1),5))
for s in statements:
    for i in range(len(visitors_1)):
        s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_1[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__lt=rate_2nd_date).order_by('-created')
        s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_1[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__lt=rate_2nd_date).order_by('-created')
        if len(s_log_skip)==0: #no skip
            if len(s_log_rating)>0:
                rating=s_log_rating[0].details.split()
                baseline_issues_1st_v[i,s.id-1]=float(rating[len(rating)-1])
            else: #not click on skip, not move slider s, => skip
                baseline_issues_1st_v[i,s.id-1]=-1
        else:
            if len(s_log_rating)==0:  #click skip, not move slider s => skip
                baseline_issues_1st_v[i,s.id-1]=-1
            else:
                if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                    baseline_issues_1st_v[i,s.id-1]=-1
                else:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_1st_v[i,s.id-1]=float(rating[len(rating)-1])


visitors_2=Visitor.objects.filter(created__gte=rate_2nd_date,created__lt=rate_3rd_date)

grade_week2_v=np.zeros(len(visitors_2))
for i in range(len(grade_week2_v)):
    s_log=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_2[i].id,log_type=11).filter(created__gte=rate_2nd_date,created__lt=rate_3rd_date)
    if len(s_log)>0:
        grade_week2_v[i]=1

#get 2nd week visitor grades(not registed as user)
baseline_issues_2nd_v=-1*np.ones((len(visitors_2),5))
for s in statements:
    for i in range(len(visitors_2)):
        s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_2[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_2nd_date,created__lt=rate_3rd_date).order_by('-created')
        s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_2[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_2nd_date,created__lt=rate_3rd_date).order_by('-created')
        if len(s_log_skip)==0: #no skip
            if len(s_log_rating)>0:
                rating=s_log_rating[0].details.split()
                baseline_issues_2nd_v[i,s.id-1]=float(rating[len(rating)-1])
            else: #not click on skip, not move slider s, => skip
                baseline_issues_2nd_v[i,s.id-1]=-1
        else:
            if len(s_log_rating)==0:  #click skip, not move slider s => skip
                baseline_issues_2nd_v[i,s.id-1]=-1
            else:
                if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                    baseline_issues_2nd_v[i,s.id-1]=-1
                else:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_2nd_v[i,s.id-1]=float(rating[len(rating)-1])


visitors_3=Visitor.objects.filter(created__gte=rate_3rd_date,created__lt=rate_4th_date)
grade_week3_v=np.zeros(len(visitors_3))
for i in range(len(grade_week3_v)):
    s_log=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_3[i].id,log_type=11).filter(created__gte=rate_3rd_date,created__lt=rate_4th_date)
    if len(s_log)>0:
        grade_week3_v[i]=1

#get 3rd week visitor grades(not registed as user)
baseline_issues_3rd_v=-1*np.ones((len(visitors_3),5))
for s in statements:
    for i in range(len(visitors_3)):
        s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_3[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_3rd_date,created__lt=rate_4th_date).order_by('-created')
        s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_3[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_3rd_date,created__lt=rate_4th_date).order_by('-created')
        if len(s_log_skip)==0: #no skip
            if len(s_log_rating)>0:
                rating=s_log_rating[0].details.split()
                baseline_issues_3rd_v[i,s.id-1]=float(rating[len(rating)-1])
            else: #not click on skip, not move slider s, => skip
                baseline_issues_2nd_v[i,s.id-1]=-1
        else:
            if len(s_log_rating)==0:  #click skip, not move slider s => skip
                baseline_issues_3rd_v[i,s.id-1]=-1
            else:
                if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                    baseline_issues_3rd_v[i,s.id-1]=-1
                else:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_3rd_v[i,s.id-1]=float(rating[len(rating)-1])

visitors_4=Visitor.objects.filter(created__gte=rate_4th_date,created__lt=rate_5th_date)
#get 4th week visitor grades(not registed as user)
grade_week4_v=np.zeros(len(visitors_4))
for i in range(len(grade_week4_v)):
    s_log=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_4[i].id,log_type=11).filter(created__gte=rate_4th_date,created__lt=rate_5th_date)
    if len(s_log)>0:
        grade_week4_v[i]=1

baseline_issues_4th_v=-1*np.ones((len(visitors_4),5))
for s in statements:
    for i in range(len(visitors_4)):
        s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_4[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('-created')
        s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_4[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('-created')
        if len(s_log_skip)==0: #no skip
            if len(s_log_rating)>0:
                rating=s_log_rating[0].details.split()
                baseline_issues_4th_v[i,s.id-1]=float(rating[len(rating)-1])
            else: #not click on skip, not move slider s, => skip
                baseline_issues_4th_v[i,s.id-1]=-1
        else:
            if len(s_log_rating)==0:  #click skip, not move slider s => skip
                baseline_issues_4th_v[i,s.id-1]=-1
            else:
                if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                    baseline_issues_4th_v[i,s.id-1]=-1
                else:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_4th_v[i,s.id-1]=float(rating[len(rating)-1])

#get 5th week visitor grades(not registed as user)
visitors_5=Visitor.objects.filter(created__gte=rate_5th_date,created__lt=rate_6th_date)
grade_week5_v=np.zeros(len(visitors_5))
for i in range(len(grade_week5_v)):
    s_log=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_5[i].id,log_type=11).filter(created__gte=rate_5th_date,created__lt=rate_6th_date)
    if len(s_log)>0:
        grade_week5_v[i]=1

baseline_issues_5th_v=-1*np.ones((len(visitors_5),5))
for s in statements:
    for i in range(len(visitors_5)):
        s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_5[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_5th_date,created__lt=rate_6th_date).order_by('-created')
        s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_5[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_5th_date,created__lt=rate_6th_date).order_by('-created')
        if len(s_log_skip)==0: #no skip
            if len(s_log_rating)>0:
                rating=s_log_rating[0].details.split()
                baseline_issues_5th_v[i,s.id-1]=float(rating[len(rating)-1])
            else: #not click on skip, not move slider s, => skip
                baseline_issues_5th_v[i,s.id-1]=-1
        else:
            if len(s_log_rating)==0:  #click skip, not move slider s => skip
                baseline_issues_5th_v[i,s.id-1]=-1
            else:
                if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                    baseline_issues_5th_v[i,s.id-1]=-1
                else:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_5th_v[i,s.id-1]=float(rating[len(rating)-1])


#get 6th week visitor grades(not registed as user)
visitors_6=Visitor.objects.filter(created__gte=rate_6th_date,created__lt=rate_7th_date)
grade_week6_v=np.zeros(len(visitors_6))
for i in range(len(grade_week6_v)):
    s_log=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_6[i].id,log_type=11).filter(created__gte=rate_6th_date,created__lt=rate_7th_date)
    if len(s_log)>0:
        grade_week6_v[i]=1

baseline_issues_6th_v=-1*np.ones((len(visitors_6),5))
for s in statements:
    for i in range(len(visitors_6)):
        s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_6[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_6th_date,created__lt=rate_7th_date).order_by('-created')
        s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_6[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_6th_date,created__lt=rate_7th_date).order_by('-created')
        if len(s_log_skip)==0: #no skip
            if len(s_log_rating)>0:
                rating=s_log_rating[0].details.split()
                baseline_issues_6th_v[i,s.id-1]=float(rating[len(rating)-1])
            else: #not click on skip, not move slider s, => skip
                baseline_issues_6th_v[i,s.id-1]=-1
        else:
            if len(s_log_rating)==0:  #click skip, not move slider s => skip
                baseline_issues_6th_v[i,s.id-1]=-1
            else:
                if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                    baseline_issues_6th_v[i,s.id-1]=-1
                else:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_6th_v[i,s.id-1]=float(rating[len(rating)-1])

#get 7th week visitor grades(not registed as user)
visitors_7=Visitor.objects.filter(created__gte=rate_7th_date,created__lt=rate_end_date)
grade_week7_v=np.zeros(len(visitors_7))
for i in range(len(grade_week7_v)):
    s_log=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_7[i].id,log_type=11).filter(created__gte=rate_7th_date,created__lt=rate_end_date)
    if len(s_log)>0:
        grade_week7_v[i]=1

baseline_issues_7th_v=-1*np.ones((len(visitors_7),5))
for s in statements:
    for i in range(len(visitors_7)):
        s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_7[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_7th_date,created__lt=rate_end_date).order_by('-created')
        s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors_7[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_7th_date,created__lt=rate_end_date).order_by('-created')
        if len(s_log_skip)==0: #no skip
            if len(s_log_rating)>0:
                rating=s_log_rating[0].details.split()
                baseline_issues_7th_v[i,s.id-1]=float(rating[len(rating)-1])
            else: #not click on skip, not move slider s, => skip
                baseline_issues_7th_v[i,s.id-1]=-1
        else:
            if len(s_log_rating)==0:  #click skip, not move slider s => skip
                baseline_issues_7th_v[i,s.id-1]=-1
            else:
                if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                    baseline_issues_7th_v[i,s.id-1]=-1
                else:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_7th_v[i,s.id-1]=float(rating[len(rating)-1])

visitor_number=[len(visitors_1),len(visitors_2),len(visitors_3),len(visitors_4),len(visitors_5),len(visitors_6),len(visitors_7)]

scipy.io.savemat('mcafe_data_3.mat', dict(baseline_issues_1st_v=baseline_issues_1st_v,baseline_issues_2nd_v=baseline_issues_2nd_v,baseline_issues_3rd_v=baseline_issues_3rd_v,baseline_issues_4th_v=baseline_issues_4th_v,baseline_issues_5th_v=baseline_issues_5th_v,visitor_number=visitor_number,grade_week1_v=grade_week1_v,grade_week2_v=grade_week2_v,grade_week3_v=grade_week3_v,grade_week4_v=grade_week4_v,grade_week5_v=grade_week5_v,baseline_issues_6th_v=baseline_issues_6th_v,baseline_issues_7th_v=baseline_issues_7th_v,grade_week6_v=grade_week6_v,grade_week7_v=grade_week7_v))

