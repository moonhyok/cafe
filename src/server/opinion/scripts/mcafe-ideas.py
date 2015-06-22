#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import simplejson as json


import numpy as np
from opinion.includes.queryutils import *
import csv
import datetime
datapath= settings.MEDIA_ROOT + "/mobile/js/mcafe-ideas-r.json"
testpath= settings.MEDIA_ROOT + "/mobile/js/mcafe-ideas-detail.csv"
comments=DiscussionComment.objects.all()
commentratings=np.zeros(len(comments))

rate_1st_date=datetime.datetime(2014,6,4,7,0,0)
rate_2nd_date=datetime.datetime(2014,6,19,7,0,0)
rate_3rd_date=datetime.datetime(2014,6,26,9,0,0)
rate_4th_date=datetime.datetime(2014,7,3,10,0,0)
rate_5th_date=datetime.datetime(2014,7,10,10,0,0)
rate_6th_date=datetime.datetime(2014,7,17,10,0,0)
rate_7th_date=datetime.datetime(2014,7,24,10,0,0)

for i in range(len(comments)):
    rating_c=CommentAgreement.objects.filter(comment=comments[i])
    ratings=np.array(rating_c.values_list('agreement', flat=True))
#rating formula mean - 1.96*sqrt((var+1/13)/N)
    if len(ratings)==1:
        commentratings[i]=ratings[0]
    if len(ratings)>1:
        sum=0
        for j in range(len(ratings)):
            sum=sum+(ratings[j]-np.mean(ratings))*(ratings[j]-np.mean(ratings))
        var=float(sum)/(len(ratings)-1)
        commentratings[i]=np.mean(ratings)-1.96*np.sqrt((var+float(1)/13)/len(ratings))

index=np.argsort(commentratings)
commentratings=np.sort(commentratings)
commentratings=commentratings[::-1]
index=index[::-1] # from highest to lowest
data=[]
for i in range(10):
    data.append({"ranking":str(i+1),"ideas":comments[index[i]].comment,"date":str(comments[index[i]].created.month)+"/"+str(comments[index[i]].created.day)})

outfile = open(datapath, "w")
json.dump(data,outfile)
outfile.close()

ofile  = open(testpath, "wb")
writer=csv.writer(ofile,delimiter=',')
title=['ID','Rank','Comment','Number of rating','Score','Date','Week']
writer.writerow(title)
for i in range(len(comments)):
    rating_c=CommentAgreement.objects.filter(comment=comments[index[i]])
    join_week=0
    if comments[index[i]].created<rate_2nd_date:
        join_week=1
    elif comments[index[i]].created>=rate_2nd_date and comments[index[i]].created<rate_3rd_date:
        join_week=2
    elif comments[index[i]].created>=rate_3rd_date and comments[index[i]].created<rate_4th_date:
        join_week=3
    elif comments[index[i]].created>=rate_4th_date and comments[index[i]].created<rate_5th_date:
        join_week=4
    elif comments[index[i]].created>=rate_5th_date and comments[index[i]].created<rate_6th_date:
        join_week=5
    elif comments[index[i]].created>=rate_6th_date and comments[index[i]].created<rate_7th_date:
        join_week=6
    else:
        join_week=7
    writer.writerow([str(comments[index[i]].id),str(i),smart_str(comments[index[i]].comment),str(len(rating_c)),str(commentratings[i]),str(comments[index[i]].created.month)+"/"+str(comments[index[i]].created.day),str(join_week)])

