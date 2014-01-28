#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
import numpy

today_date=datetime.datetime(2014,1,28,0,0,0,0)
user_today=User.objects.filter(date_joined__gte=today_date)
active_users = list(User.objects.filter(is_active=True)) 
statements = OpinionSpaceStatement.objects.all().order_by('id')

for s in statements:
   ratings = UserRating.objects.filter(is_current=True,opinion_space_statement = s, user__in = active_users,created__gte=today_date)
   skip_logs = LogUserEvents.objects.filter(is_visitor=True, log_type=11,details__contains='slider_set',created__gte = today_date)
   users_with_grades = []
   for skip_log in skip_logs:
       slider_set_args = skip_log.details[10:].lstrip()
       visitor = Visitor.objects.filter(id = skip_log.logger_id)
       if len(visitor) > 0:
          visitor = visitor[0]
       if visitor.user != None and visitor.user.is_active and int(slider_set_args[0]) == s.id:
          users_with_grades.append(visitor.user)
       
   s_rating_list=[]        
   for rating in ratings.filter(user__in = users_with_grades):
      s_rating_list.append(rating.rating)
    
   bins=[0,0.001,0.08,0.14,0.19,0.31,0.37,0.44,0.56,0.62,0.68,0.81,0.999,1]  

   hist,bin_edges = numpy.histogram(s_rating_list,bins,normed=False)
   print sum(hist)
   
   mode=numpy.argmax(hist)
   grade=''
   if mode==0:
      grade='A+'
   elif mode==1:
      grade='A'
   elif mode==2:
      grade='A-'
   elif mode==3:
      grade='B+'
   elif mode==4:
      grade='B'
   elif mode==5:
      grade='B-'
   elif mode==6:
      grade='C+'
   elif mode==7:
      grade='C'
   elif mode==8:
      grade='C-'
   elif mode==9:
      grade='D+'
   elif mode==10:
      grade='D'
   elif mode==11:
      grade='D-'
   else:
      grade='F'
   print s.statement, " mode:",grade
