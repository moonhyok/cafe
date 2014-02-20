'''this script will plot stacked histogram for each issue on a single plot'''
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

os.environ['MPLCONFIGDIR'] = "/tmp"

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import settings
imagepath = settings.MEDIA_ROOT + "/mobile/img/dailyupdate/"
jspath= settings.MEDIA_ROOT + "/mobile/js/"
import datetime

def issues_stack_hist():
   """produce histogram for each issue"""
   statements = OpinionSpaceStatement.objects.all().order_by('id')
   #bins=[0,0.01,0.19,0.32,0.38,0.44,0.56,0.63,0.69,0.81,0.86,0.92,0.99,1]
   bins=[0,0.001,0.08,0.14,0.19,0.31,0.37,0.44,0.56,0.62,0.68,0.81,0.999,1]  
          #A+   A   A-   B+   B    B-   C+   C    C-   D+   D    D-    F
   N=6 # six issue
   ind=np.arange(N)
   width=0.5
   hist_all=np.zeros((6,14))
   
   active_users = list(User.objects.filter(is_active=True)) 
   skip_begin_date=datetime.datetime(2014,1,9,0,0,0,0)
   for s in statements:
       s_rating=UserRating.objects.filter(opinion_space_statement=s,is_current=True,user__in = active_users)
       s_rating_list=[]
       s_skip=0
       for rating in s_rating:
          if rating.created>=skip_begin_date:
                visitor=Visitor.objects.filter(user=rating.user)  #get the visitor of the user
                if len(visitor)>0:
                   s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains=str(s.id)).order_by('-created') #get issue skip log
                   s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').filter(details__startswith='slider_set '+str(s.id)).order_by('-created')
                   if len(s_log_skip)==0: #no skip
                      if len(s_log_rating)>0:
                         s_rating_list.append(rating.rating)
                      else: #not click on skip, not move slider s, => skip
                         s_skip=s_skip+1
                   else:
                      if len(s_log_rating)==0:  #click skip, not move slider s => skip
                         s_skip=s_skip+1
                      else:
                         if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                            s_skip=s_skip+1
                         else:
                            s_rating_list.append(rating.rating)
                else: 
                   s_rating_list.append(rating.rating)
          else:
                s_rating_list.append(rating.rating)       
       
       if len(s_rating_list)>0:
          hist,bin_edges = np.histogram(s_rating_list,bins,normed=False)
          skip=np.array([s_skip])
          hist=np.concatenate((hist,skip), axis=1)
          hist_in_percent=(100*hist/float(sum(hist)))
       hist_all[s.id-1]=hist_in_percent
   
   hist_all=np.transpose(hist_all)
   
   fig, ax = plt.subplots()
   ax.set_ylim([0, 100])
   plt.subplots_adjust(left=0.13, right=0.83, top=0.95, bottom=0.18)
   
   fig.patch.set_facecolor('#74b9b7')
   
   p1 = ax.bar(ind, hist_all[13],   width, color='#0b294f', align='center',edgecolor = "none")
   p2 = ax.bar(ind, hist_all[12], width, color='#7d625f', bottom=hist_all[13], align='center',edgecolor = "none")
   p3 = ax.bar(ind, hist_all[11], width, color='#c3c3c3', bottom=hist_all[13]+hist_all[12], align='center',edgecolor = "none")
   p4 = ax.bar(ind, hist_all[10], width, color='#4E2E75', bottom=hist_all[13]+hist_all[12]+hist_all[11], align='center',edgecolor = "none")
   p5 = ax.bar(ind, hist_all[9], width, color='#A186C1', bottom=hist_all[13]+hist_all[12]+hist_all[11]+hist_all[10], align='center',edgecolor = "none")
   p6 = ax.bar(ind, hist_all[8], width, color='#003A70', bottom=hist_all[13]+hist_all[12]+hist_all[11]+hist_all[10]+hist_all[9], align='center',edgecolor = "none")
   p7 = ax.bar(ind, hist_all[7], width, color='#80D2F4', bottom=hist_all[13]+hist_all[12]+hist_all[11]+hist_all[10]+hist_all[9]+hist_all[8], align='center',edgecolor = "none")
   p8 = ax.bar(ind, hist_all[6], width, color='#61b392', bottom=hist_all[13]+hist_all[12]+hist_all[11]+hist_all[10]+hist_all[9]+hist_all[8]+hist_all[7], align='center',edgecolor = "none")
   p9 = ax.bar(ind, hist_all[5], width, color='#c1e9a3', bottom=hist_all[13]+hist_all[12]+hist_all[11]+hist_all[10]+hist_all[9]+hist_all[8]+hist_all[7]
                                                                 +hist_all[6], align='center',edgecolor = "none")
   p10 = ax.bar(ind, hist_all[4], width, color='#fef391', bottom=hist_all[13]+hist_all[12]+hist_all[11]+hist_all[10]+hist_all[9]+hist_all[8]+hist_all[7]
                                                                 +hist_all[6]+hist_all[5], align='center',edgecolor = "none")
   p11 = ax.bar(ind, hist_all[3], width, color='#fbbd88', bottom=hist_all[13]+hist_all[12]+hist_all[11]+hist_all[10]+hist_all[9]+hist_all[8]+hist_all[7]
                                                                 +hist_all[6]+hist_all[5]+hist_all[4], align='center',edgecolor = "none")
   p12 = ax.bar(ind, hist_all[2], width, color='#ff8ba1', bottom=hist_all[13]+hist_all[12]+hist_all[11]+hist_all[10]+hist_all[9]+hist_all[8]+hist_all[7]
                                                                 +hist_all[6]+hist_all[5]+hist_all[4]+hist_all[3], align='center',edgecolor = "none")
   p13 = ax.bar(ind, hist_all[1], width, color='#e05e75', bottom=hist_all[13]+hist_all[12]+hist_all[11]+hist_all[10]+hist_all[9]+hist_all[8]+hist_all[7]
                                                                 +hist_all[6]+hist_all[5]+hist_all[4]+hist_all[3]+hist_all[2], align='center',edgecolor = "none")
   p14 = plt.bar(ind, hist_all[0], width, color='#bc3160', bottom=hist_all[13]+hist_all[12]+hist_all[11]+hist_all[10]+hist_all[9]+hist_all[8]+hist_all[7]
                                                                 +hist_all[6]+hist_all[5]+hist_all[4]+hist_all[3]+hist_all[2]+hist_all[1], align='center',edgecolor = "none")
   
   ax.set_xticks(ind)
   ax.set_xticklabels( ('Obamacare', 'K12 Funding', 'College Funding', 'Immigrant', 'Marijuana','Same-sex') )
   plt.setp(ax.get_xticklabels(), fontsize=18,rotation=30)
   plt.setp(ax.get_yticklabels(), fontsize=20)
   legend=plt.legend( (p14[0], p13[0],p12[0],p11[0],p10[0],p9[0],p8[0],p7[0],p6[0],p5[0],p4[0],p3[0],p2[0],p1[0]), ('A+', 'A', 'A-', 'B+', 'B','B-','C+','C','C-','D+','D','D-','F','Skip'),bbox_to_anchor=(1.25, 1))
   for label in legend.get_texts():
       label.set_fontsize('18')
   fig.set_size_inches(8,8)
   
   plt.ylabel('Percentage',fontsize=24)
   plt.savefig(imagepath+'stacked.png',edgecolor='none',dpi=100,format='png')

issues_stack_hist()
