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

#rating date
rate_2nd_date=datetime.datetime(2014,6,19,7,0,0)
rate_3rd_date=datetime.datetime(2014,6,26,9,0,0)
rate_4th_date=datetime.datetime(2014,7,3,10,0,0)
rate_5th_date=datetime.datetime(2014,7,10,10,0,0)
rate_6th_date=datetime.datetime(2014,7,17,10,0,0)
rate_7th_date=datetime.datetime(2014,7,24,10,0,0)
rate_end_date=datetime.datetime(2014,8,21,0,0,0)

exclude_list=['goldberg@berkeley.edu','nonnecke@citris-uc.org','nonnecke@berkeley.edu','sanjay@eecs.berkeley.edu','goldberg@eecs.berkeley.edu','angelaslin@berkeley.edu','matti@example.com','patel24jay@gmail.com','ccrittenden@berkeley.edu','alisoncliff@berkeley.edu','hunallen@gmail.com','hunallen@berkeley.edu']
user=User.objects.exclude(username__in=exclude_list).filter(is_active=True).filter(date_joined__lt=rate_end_date).order_by('id')
user=user[51:]

statements = OpinionSpaceStatement.objects.all().order_by('id')

#1st week and 1st time rating baseline issues user's grade

baseline_issues_1st=-1*np.ones((len(user),5))
for s in statements:
    for i in range(len(user)):
        user_s_rating=UserRating.objects.filter(opinion_space_statement=s,user=user[i],created__lt=rate_2nd_date).order_by('created')
        visitor=Visitor.objects.filter(user=user[i])
        if len(visitor)>0:
            s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__lt=rate_2nd_date).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__lt=rate_2nd_date).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_1st[i,s.id-1]=float(rating[len(rating)-1])
                else: #not click on skip, not move slider s, => skip
                    baseline_issues_1st[i,s.id-1]=-1
            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    baseline_issues_1st[i,s.id-1]=-1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        baseline_issues_1st[i,s.id-1]=-1
                    else:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_1st[i,s.id-1]=float(rating[len(rating)-1])
        else:
            if len(user_s_rating)>0:
                baseline_issues_1st[i,s.id-1]=user_s_rating[0].rating



#2nd week rating user's grade
baseline_issues_2nd=-1*np.ones((len(user),5))
for s in statements:
    for i in range(len(user)):
        if user[i].date_joined>=rate_2nd_date and user[i].date_joined<=rate_3rd_date: #user join second week, get their first rating
            user_s_rating=UserRating.objects.filter(opinion_space_statement=s,user=user[i],created__gte=rate_2nd_date,created__lt=rate_3rd_date).order_by('created')
            visitor=Visitor.objects.filter(user=user[i])
            if len(visitor)>0:
                s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_2nd_date,created__lt=rate_3rd_date).order_by('-created')
                s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_2nd_date,created__lt=rate_3rd_date).order_by('-created')
                if len(s_log_skip)==0: #no skip
                    if len(s_log_rating)>0:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_2nd[i,s.id-1]=float(rating[len(rating)-1])
                    else: #not click on skip, not move slider s, => skip
                        baseline_issues_2nd[i,s.id-1]=-1
                else:
                    if len(s_log_rating)==0:  #click skip, not move slider s => skip
                        baseline_issues_2nd[i,s.id-1]=-1
                    else:
                        if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                            baseline_issues_2nd[i,s.id-1]=-1
                        else:
                            rating=s_log_rating[0].details.split()
                            baseline_issues_2nd[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(user_s_rating)>0:
                    baseline_issues_2nd[i,s.id-1]=user_s_rating[0].rating
        
        else: #user join before second week, check if they regrade
            s_log_skip=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_2nd_date,created__lt=rate_3rd_date).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_2nd_date,created__lt=rate_3rd_date).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_2nd[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    baseline_issues_2nd[i,s.id-1]=-1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        baseline_issues_2nd[i,s.id-1]=-1
                    else:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_2nd[i,s.id-1]=float(rating[len(rating)-1])

#grade 2nd week
grade_week2=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_2nd_date and user[i].date_joined<rate_3rd_date:
        grade_week2[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).filter(created__gte=rate_2nd_date,created__lt=rate_3rd_date)
        if len(s_log)>0:
            grade_week2[i]=1

#appear 2nd week
appear_week2=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_2nd_date and user[i].date_joined<rate_3rd_date:
        appear_week2[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id).filter(created__gte=rate_2nd_date,created__lt=rate_3rd_date)
        if len(s_log)>0:
            appear_week2[i]=1

#number of submit ideas in the 2nd week
submit_week2=np.zeros(len(user))
for i in range(len(user)):
    comments=DiscussionComment.objects.filter(user=user[i],created__gte=rate_2nd_date,created__lt=rate_3rd_date)
    submit_week2[i]=len(comments)

#number of rated ideas in the 2nd week
rate_week2=np.zeros(len(user))
for i in range(len(user)):
    ratings=CommentAgreement.objects.filter(rater=user[i],created__gte=rate_2nd_date,created__lt=rate_3rd_date)
    rate_week2[i]=len(ratings)

#3rd week grade
baseline_issues_3rd=-1*np.ones((len(user),5))
for s in statements:
    for i in range(len(user)):
        if user[i].date_joined>=rate_3rd_date and user[i].date_joined<rate_4th_date: #user join 3rd week, get their first rating
            user_s_rating=UserRating.objects.filter(opinion_space_statement=s,user=user[i],created__gte=rate_3rd_date,created__lt=rate_4th_date).order_by('created')
            visitor=Visitor.objects.filter(user=user[i])
            if len(visitor)>0:
                s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_3rd_date,created__lt=rate_4th_date).order_by('-created')
                s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_3rd_date,created__lt=rate_4th_date).order_by('-created')
                if len(s_log_skip)==0: #no skip
                    if len(s_log_rating)>0:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_3rd[i,s.id-1]=float(rating[len(rating)-1])
                    else: #not click on skip, not move slider s, => skip
                        baseline_issues_3rd[i,s.id-1]=-1
                else:
                    if len(s_log_rating)==0:  #click skip, not move slider s => skip
                        baseline_issues_3rd[i,s.id-1]=-1
                    else:
                        if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                            baseline_issues_3rd[i,s.id-1]=-1
                        else:
                            rating=s_log_rating[0].details.split()
                            baseline_issues_3rd[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(user_s_rating)>0:
                    baseline_issues_3rd[i,s.id-1]=user_s_rating[0].rating
        
        else: #user join before 3rd week, check if they regrade
            s_log_skip=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_3rd_date,created__lt=rate_4th_date).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_3rd_date,created__lt=rate_4th_date).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_3rd[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    baseline_issues_3rd[i,s.id-1]=-1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        baseline_issues_3rd[i,s.id-1]=-1
                    else:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_3rd[i,s.id-1]=float(rating[len(rating)-1])

#appear 3rd week
appear_week3=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_3rd_date and user[i].date_joined<rate_4th_date:
        appear_week3[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id).filter(created__gte=rate_3rd_date,created__lt=rate_4th_date)
        if len(s_log)>0:
            appear_week3[i]=1

#grade 3rd week
grade_week3=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_3rd_date and user[i].date_joined<rate_4th_date:
        grade_week3[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).filter(created__gte=rate_3rd_date,created__lt=rate_4th_date)
        if len(s_log)>0:
            grade_week3[i]=1


#number of submit ideas in the 3rd week
submit_week3=np.zeros(len(user))
for i in range(len(user)):
    comments=DiscussionComment.objects.filter(user=user[i],created__gte=rate_3rd_date,created__lt=rate_4th_date)
    submit_week3[i]=len(comments)

#number of rated ideas in the 3rd week
rate_week3=np.zeros(len(user))
for i in range(len(user)):
    ratings=CommentAgreement.objects.filter(rater=user[i],created__gte=rate_3rd_date,created__lt=rate_4th_date)
    rate_week3[i]=len(ratings)


#4th week grade
baseline_issues_4th=-1*np.ones((len(user),5))
for s in statements:
    for i in range(len(user)):
        if user[i].date_joined>=rate_4th_date and user[i].date_joined<rate_5th_date: #user join 4th week, get their first rating
            user_s_rating=UserRating.objects.filter(opinion_space_statement=s,user=user[i],created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('created')
            visitor=Visitor.objects.filter(user=user[i])
            if len(visitor)>0:
                s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('-created')
                s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('-created')
                if len(s_log_skip)==0: #no skip
                    if len(s_log_rating)>0:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_4th[i,s.id-1]=float(rating[len(rating)-1])
                    else: #not click on skip, not move slider s, => skip
                        baseline_issues_4th[i,s.id-1]=-1
                else:
                    if len(s_log_rating)==0:  #click skip, not move slider s => skip
                        baseline_issues_4th[i,s.id-1]=-1
                    else:
                        if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                            baseline_issues_4th[i,s.id-1]=-1
                        else:
                            rating=s_log_rating[0].details.split()
                            baseline_issues_4th[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(user_s_rating)>0:
                    baseline_issues_4th[i,s.id-1]=user_s_rating[0].rating
        
        else: #user join before 3rd week, check if they regrade
            s_log_skip=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_4th[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    baseline_issues_4th[i,s.id-1]=-1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        baseline_issues_4th[i,s.id-1]=-1
                    else:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_4th[i,s.id-1]=float(rating[len(rating)-1])


#appear 4th week
appear_week4=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_4th_date and user[i].date_joined<rate_5th_date:
        appear_week4[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id).filter(created__gte=rate_4th_date,created__lt=rate_5th_date)
        if len(s_log)>0:
            appear_week4[i]=1

#grade 4th week
grade_week4=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_4th_date and user[i].date_joined<rate_5th_date:
        grade_week4[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).filter(created__gte=rate_4th_date,created__lt=rate_5th_date)
        if len(s_log)>0:
            grade_week4[i]=1


#number of submit ideas in the 4th week
submit_week4=np.zeros(len(user))
for i in range(len(user)):
    comments=DiscussionComment.objects.filter(user=user[i],created__gte=rate_4th_date,created__lt=rate_5th_date)
    submit_week4[i]=len(comments)

#number of rated ideas in the 4th week
rate_week4=np.zeros(len(user))
for i in range(len(user)):
    ratings=CommentAgreement.objects.filter(rater=user[i],created__gte=rate_4th_date,created__lt=rate_5th_date)
    rate_week4[i]=len(ratings)


#5th week grade
baseline_issues_5th=-1*np.ones((len(user),5))
for s in statements:
    for i in range(len(user)):
        if user[i].date_joined>=rate_5th_date and user[i].date_joined<rate_6th_date: #user join 5th week, get their first rating
            user_s_rating=UserRating.objects.filter(opinion_space_statement=s,user=user[i],created__gte=rate_5th_date,created__lt=rate_6th_date).order_by('created')
            visitor=Visitor.objects.filter(user=user[i])
            if len(visitor)>0:
                s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_5th_date,created__lt=rate_6th_date).order_by('-created')
                s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_5th_date,created__lt=rate_6th_date).order_by('-created')
                if len(s_log_skip)==0: #no skip
                    if len(s_log_rating)>0:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_5th[i,s.id-1]=float(rating[len(rating)-1])
                    else: #not click on skip, not move slider s, => skip
                        baseline_issues_5th[i,s.id-1]=-1
                else:
                    if len(s_log_rating)==0:  #click skip, not move slider s => skip
                        baseline_issues_5th[i,s.id-1]=-1
                    else:
                        if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                            baseline_issues_5th[i,s.id-1]=-1
                        else:
                            rating=s_log_rating[0].details.split()
                            baseline_issues_5th[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(user_s_rating)>0:
                    baseline_issues_5th[i,s.id-1]=user_s_rating[0].rating
        
        else: #user join before 3rd week, check if they regrade
            s_log_skip=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_5th_date,created__lt=rate_6th_date).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_5th_date,created__lt=rate_6th_date).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_5th[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    baseline_issues_5th[i,s.id-1]=-1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        baseline_issues_5th[i,s.id-1]=-1
                    else:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_5th[i,s.id-1]=float(rating[len(rating)-1])


#6th week grade
baseline_issues_6th=-1*np.ones((len(user),5))
for s in statements:
    for i in range(len(user)):
        if user[i].date_joined>=rate_6th_date and user[i].date_joined<rate_7th_date: #user join 5th week, get their first rating
            user_s_rating=UserRating.objects.filter(opinion_space_statement=s,user=user[i],created__gte=rate_6th_date,created__lt=rate_7th_date).order_by('created')
            visitor=Visitor.objects.filter(user=user[i])
            if len(visitor)>0:
                s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_6th_date,created__lt=rate_7th_date).order_by('-created')
                s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_6th_date,created__lt=rate_7th_date).order_by('-created')
                if len(s_log_skip)==0: #no skip
                    if len(s_log_rating)>0:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_6th[i,s.id-1]=float(rating[len(rating)-1])
                    else: #not click on skip, not move slider s, => skip
                        baseline_issues_6th[i,s.id-1]=-1
                else:
                    if len(s_log_rating)==0:  #click skip, not move slider s => skip
                        baseline_issues_6th[i,s.id-1]=-1
                    else:
                        if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                            baseline_issues_6th[i,s.id-1]=-1
                        else:
                            rating=s_log_rating[0].details.split()
                            baseline_issues_6th[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(user_s_rating)>0:
                    baseline_issues_6th[i,s.id-1]=user_s_rating[0].rating
        
        else: #user join before 3rd week, check if they regrade
            s_log_skip=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_6th_date,created__lt=rate_7th_date).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_6th_date,created__lt=rate_7th_date).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_6th[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    baseline_issues_6th[i,s.id-1]=-1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        baseline_issues_6th[i,s.id-1]=-1
                    else:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_6th[i,s.id-1]=float(rating[len(rating)-1])

#7th week grade
baseline_issues_7th=-1*np.ones((len(user),5))
for s in statements:
    for i in range(len(user)):
        if user[i].date_joined>=rate_7th_date and user[i].date_joined<rate_end_date: #user join 5th week, get their first rating
            user_s_rating=UserRating.objects.filter(opinion_space_statement=s,user=user[i],created__gte=rate_7th_date,created__lt=rate_end_date).order_by('created')
            visitor=Visitor.objects.filter(user=user[i])
            if len(visitor)>0:
                s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_7th_date,created__lt=rate_end_date).order_by('-created')
                s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_7th_date,created__lt=rate_end_date).order_by('-created')
                if len(s_log_skip)==0: #no skip
                    if len(s_log_rating)>0:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_7th[i,s.id-1]=float(rating[len(rating)-1])
                    else: #not click on skip, not move slider s, => skip
                        baseline_issues_7th[i,s.id-1]=-1
                else:
                    if len(s_log_rating)==0:  #click skip, not move slider s => skip
                        baseline_issues_7th[i,s.id-1]=-1
                    else:
                        if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                            baseline_issues_7th[i,s.id-1]=-1
                        else:
                            rating=s_log_rating[0].details.split()
                            baseline_issues_7th[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(user_s_rating)>0:
                    baseline_issues_7th[i,s.id-1]=user_s_rating[0].rating
        
        else: #user join before 7th week, check if they regrade
            s_log_skip=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_7th_date,created__lt=rate_end_date).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_7th_date,created__lt=rate_end_date).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_7th[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    baseline_issues_7th[i,s.id-1]=-1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        baseline_issues_7th[i,s.id-1]=-1
                    else:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_7th[i,s.id-1]=float(rating[len(rating)-1])

#appear 5th week
appear_week5=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_5th_date and user[i].date_joined<rate_6th_date:
        appear_week5[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id).filter(created__gte=rate_5th_date,created__lt=rate_6th_date)
        if len(s_log)>0:
            appear_week5[i]=1

#grade 5th week
grade_week5=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_5th_date and user[i].date_joined<rate_6th_date:
        grade_week5[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).filter(created__gte=rate_5th_date,created__lt=rate_6th_date)
        if len(s_log)>0:
            grade_week5[i]=1


#number of submit ideas in the 5th week
submit_week5=np.zeros(len(user))
for i in range(len(user)):
    comments=DiscussionComment.objects.filter(user=user[i],created__gte=rate_5th_date,created__lt=rate_6th_date)
    submit_week5[i]=len(comments)

#number of rated ideas in the 5th week
rate_week5=np.zeros(len(user))
for i in range(len(user)):
    ratings=CommentAgreement.objects.filter(rater=user[i],created__gte=rate_5th_date,created__lt=rate_6th_date)
    rate_week5[i]=len(ratings)

#appear 6th week
appear_week6=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_6th_date and user[i].date_joined<rate_7th_date:
        appear_week6[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id).filter(created__gte=rate_6th_date,created__lt=rate_7th_date)
        if len(s_log)>0:
            appear_week6[i]=1

#grade 6th week
grade_week6=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_6th_date and user[i].date_joined<rate_7th_date:
        grade_week6[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).filter(created__gte=rate_6th_date,created__lt=rate_7th_date)
        if len(s_log)>0:
            grade_week6[i]=1


#number of submit ideas in the 6th week
submit_week6=np.zeros(len(user))
for i in range(len(user)):
    comments=DiscussionComment.objects.filter(user=user[i],created__gte=rate_6th_date,created__lt=rate_7th_date)
    submit_week6[i]=len(comments)

#number of rated ideas in the 6th week
rate_week6=np.zeros(len(user))
for i in range(len(user)):
    ratings=CommentAgreement.objects.filter(rater=user[i],created__gte=rate_6th_date,created__lt=rate_7th_date)
    rate_week6[i]=len(ratings)

#appear 7th week
appear_week7=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_7th_date and user[i].date_joined<rate_end_date:
        appear_week7[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id).filter(created__gte=rate_7th_date,created__lt=rate_end_date)
        if len(s_log)>0:
            appear_week7[i]=1

#grade 7th week
grade_week7=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_7th_date and user[i].date_joined<rate_end_date:
        grade_week7[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).filter(created__gte=rate_7th_date,created__lt=rate_end_date)
        if len(s_log)>0:
            grade_week7[i]=1


#number of submit ideas in the 7th week
submit_week7=np.zeros(len(user))
for i in range(len(user)):
    comments=DiscussionComment.objects.filter(user=user[i],created__gte=rate_7th_date,created__lt=rate_end_date)
    submit_week7[i]=len(comments)

#number of rated ideas in the 7th week
rate_week7=np.zeros(len(user))
for i in range(len(user)):
    ratings=CommentAgreement.objects.filter(rater=user[i],created__gte=rate_7th_date,created__lt=rate_end_date)
    rate_week7[i]=len(ratings)




#join week
join_week=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined<rate_2nd_date:
        join_week[i]=1
    elif user[i].date_joined>=rate_2nd_date and user[i].date_joined<rate_3rd_date:
        join_week[i]=2
    elif user[i].date_joined>=rate_3rd_date and user[i].date_joined<rate_4th_date:
        join_week[i]=3
    elif user[i].date_joined>=rate_4th_date and user[i].date_joined<rate_5th_date:
        join_week[i]=4
    elif user[i].date_joined>=rate_5th_date and user[i].date_joined<rate_6th_date:
        join_week[i]=5
    elif user[i].date_joined>=rate_6th_date and user[i].date_joined<rate_7th_date:
        join_week[i]=6
    else:
        join_week[i]=7

#number of submit ideas in the 1st week
submit_week1=np.zeros(len(user))
for i in range(len(user)):
    comments=DiscussionComment.objects.filter(user=user[i],created__lte=rate_2nd_date)
    submit_week1[i]=len(comments)

#number of rated ideas in the 1st week
rate_week1=np.zeros(len(user))
for i in range(len(user)):
    ratings=CommentAgreement.objects.filter(rater=user[i],created__lte=rate_2nd_date)
    rate_week1[i]=len(ratings)

scipy.io.savemat('mcafe_data_2.mat',dict(baseline_issues_4th=baseline_issues_4th,appear_week4=appear_week4,grade_week4=grade_week4,rate_week4=rate_week4,submit_week4=submit_week4,baseline_issues_3rd=baseline_issues_3rd,appear_week3=appear_week3,grade_week3=grade_week3,submit_week3=submit_week3,rate_week3=rate_week3,appear_week2=appear_week2,rate_week2=rate_week2,submit_week2=submit_week2,grade_week2=grade_week2,baseline_issues_2nd=baseline_issues_2nd,baseline_issues_1st=baseline_issues_1st,join_week=join_week,submit_week1=submit_week1,rate_week1=rate_week1,baseline_issues_5th=baseline_issues_5th,appear_week5=appear_week5,grade_week5=grade_week5,rate_week5=rate_week5,submit_week5=submit_week5,appear_week6=appear_week6,grade_week6=grade_week6,rate_week6=rate_week6,submit_week6=submit_week6,appear_week7=appear_week7,grade_week7=grade_week7,rate_week7=rate_week7,submit_week7=submit_week7,baseline_issues_6th=baseline_issues_6th,baseline_issues_7th=baseline_issues_7th))
