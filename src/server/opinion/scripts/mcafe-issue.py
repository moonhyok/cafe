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
datapath= settings.MEDIA_ROOT + "/mobile/stats_data/"

#calculate grade distribution for each question

statements = OpinionSpaceStatement.objects.all().order_by('id')
exclude_list=['goldberg@berkeley.edu','nonnecke@citris-uc.org','nonnecke@berkeley.edu','sanjay@eecs.berkeley.edu','goldberg@eecs.berkeley.edu','angelaslin@berkeley.edu','matti@example.com','patel24jay@gmail.com','ccrittenden@berkeley.edu','alisoncliff@berkeley.edu','alisoncliff@berkeley.edu','hunallen@gmail.com','hunallen@berkeley.edu']
user=User.objects.exclude(username__in=exclude_list).filter(is_active=True).order_by('id')


active_users = user[11:]
bins=[0,0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1]

for s in statements:
    s_rating_list=[0]*len(active_users)
    s_skip=0
    for i in range(len(active_users)):
        user_s_rating=UserRating.objects.filter(opinion_space_statement=s,user=user[i]).order_by('created')
        visitor=Visitor.objects.filter(user=user[i])
        if len(visitor)>0:
            s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    rating=s_log_rating[0].details.split()
                    s_rating_list[i]=float(rating[len(rating)-1])
                else: #not click on skip, not move slider s, => skip
                    s_skip=s_skip+1
                    s_rating_list[i]=-1
            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    s_skip=s_skip+1
                    s_rating_list[i]=-1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        s_skip=s_skip+1
                        s_rating_list[i]=-1
                    else:
                        rating=s_log_rating[0].details.split()
                        s_rating_list[i]=float(rating[len(rating)-1])
        else:
            if(len(user_s_rating))>0:
                s_rating_list[i]=(user_s_rating[0].rating)

        if len(user_s_rating)>1: #rate more than 1 time, get user log info
            s_log_skip=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    rating=s_log_rating[0].details.split()
                    if s_rating_list[i]==-1:
                        s_skip=s_skip-1
                    s_rating_list[i]=float(rating[len(rating)-1])

            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    if s_rating_list[i]!=-1:
                        s_skip=s_skip+1
                    s_rating_list[i]=-1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        if s_rating_list[i]!=-1:
                            s_skip=s_skip+1
                        s_rating_list[i]=-1
                    else:
                        if s_rating_list[i]==-1:
                            s_skip=s_skip-1
                        rating=s_log_rating[0].details.split()
                        s_rating_list[i]=float(rating[len(rating)-1])
                

    s_rating_list=[x for x in s_rating_list if x>-1]
    if len(s_rating_list)>0:
        ofile  = open(settings.MEDIA_ROOT + "/mobile/stats_data/"+"issue"+str(s.id)+"_r.csv", "wb")
        writer=csv.writer(ofile,delimiter=',')
        title=['score','total']
        writer.writerow(title)
        
        hist,bin_edges = np.histogram(s_rating_list,bins=11,range=(0,1),normed=False)
        value = np.median(s_rating_list)
        skip=np.array([s_skip])
        hist=np.concatenate((hist,skip), axis=1)
        print hist
        for i in range(len(hist)-1):
            row=[i,hist[i]]
            writer.writerow(row)
        writer.writerow(["Skip",hist[len(hist)-1]])


