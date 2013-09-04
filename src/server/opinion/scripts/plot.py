#!/usr/bin/env python
import sys, os
import environ
from opinion.opinion_core.models import *
from django.contrib.auth.models import User
from opinion.settings_local import ASSETS_LOCAL

import numpy as np
from matplotlib import pyplot as plt
import itertools, datetime, heapq
import pickle

import string
import array
from django.core.mail import send_mail
from django.utils.dateformat import DateFormat
from opinion.includes.queryutils import *

from opinion.includes.plotutils import *

from opinion.settings_local import CONFIGURABLES
import time

start_date = Settings.objects.filter(key='START_DATE')
end_date = Settings.objects.filter(key='END_DATE')
if len(start_date)>0:
    start_date = start_date[0].value
else:
    start_date = CONFIGURABLES['START_DATE']['default']

if len(end_date)>0:
    end_date = end_date[0].value
else:
    end_date = CONFIGURABLES['END_DATE']['default']

start_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(start_date, "%Y-%m-%d")))
end_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(end_date, "%Y-%m-%d")))

timer_start = datetime.datetime.now()

endDate = datetime.datetime.now()
if endDate > end_date:
    endDate = end_date

startdates = [[start_date, 'alltime'],
              [endDate - datetime.timedelta(days=30), '1month'],
              [endDate - datetime.timedelta(days=90), '3months']]

result = {}

for sd in startdates:

  startDate = sd[0]
  if startDate < start_date: 
    startDate = start_date
  print startDate 
  rate_count = {}
  view_count = {}
      
  for ratings in CommentRating.objects.filter(is_current = True, created__gte=startDate, created__lte=endDate).values('rater', 'comment__discussion_statement', 'comment__user').distinct().iterator():
      if (ratings['comment__user'], ratings['comment__discussion_statement']) in rate_count: 
          rate_count[(ratings['comment__user'],ratings['comment__discussion_statement'])] += 1
      else:
          rate_count[(ratings['comment__user'],ratings['comment__discussion_statement'])] = 1
  
  for log in LogCommentView.objects.filter(created__gte=startDate, created__lte=endDate).values('comment__discussion_statement', 'comment__user').iterator():
      if (log['comment__user'], log['comment__discussion_statement']) in view_count:
          view_count[(log['comment__user'],log['comment__discussion_statement'])] += 1
      else:
          view_count[(log['comment__user'],log['comment__discussion_statement'])] = 1
  
  rate_count = [rate_count[key] for key in rate_count if rate_count[key]<150]
  view_count = [view_count[key] for key in view_count if view_count[key]<150]  
  

  idle_duration = datetime.timedelta(minutes=15)
  visit_gap = datetime.timedelta(hours=1)
  minimum_session_length = 1 #datetime.timedelta(minutes=1
  maximum_no_visit_length = 15
  events = [5, 6, 7] #session-worthy events
       
  avg_session_length = []
  avg_session_gap = []
  user_visit_counts = []
  session_count=[]

  userid_lst = []
  agreement_ratings= []
  agreement_ratings_count = []
  insight_ratings= []
  insight_ratings_count = []

  for r in CommentAgreement.objects.filter(is_current = True, created__gte=startDate, created__lte=endDate):
    agreement_ratings.append(r.agreement)
  for r in  CommentRating.objects.filter(is_current = True, created__gte=startDate, created__lte=endDate):
    insight_ratings.append(r.rating)


  for u in User.objects.all():

          userid_lst.append(u.id)

          c = CommentAgreement.objects.filter(is_current=True, created__gte=startDate, created__lte=endDate, rater = u).values('comment__discussion_statement', 'comment__user').distinct()
          agreement_ratings_count.append(c.count())
          i = CommentRating.objects.filter(is_current=True, created__gte=startDate, created__lte=endDate, rater = u).values('comment__discussion_statement', 'comment__user').distinct()
          insight_ratings_count.append(i.count())

          id_lst = [u.id]
          for v in Visitor.objects.filter(user=u):
                  id_lst.append(v.id)
          log = list(LogUserEvents.objects.filter(created__gte=startDate, created__lte=endDate)\
          .filter(logger_id__in=id_lst, log_type__in=events).order_by('created') )
          if len(log) < 2:
                  continue

          session_last_log_date= log[0].created
          session_end_at_end_of_log = False
          session_duration = []
          session_gap = []

          visit_count = 0

          for i in range(0, len(log)-1):
                  diff = log[i+1].created - log[i].created
                  if (diff > idle_duration):
                          if(i == len(log)-2):
                                  session_at_end_of_log = True
                          mins = find_seconds((log[i].created - session_last_log_date)) / 60
                          if mins > minimum_session_length and mins < 60*5:
                                  session_duration.append(mins)
                                  next_session_start = log[i+1].created
                                  session_last_log_date = next_session_start
                                  days = find_seconds(diff)/(24*3600)
                                  session_gap.append(days)
                                  if(diff > visit_gap):
                                          visit_count = visit_count + 1

          if not session_end_at_end_of_log:
                          mins = find_seconds((log[-1].created - session_last_log_date)) / 60
                          if mins > minimum_session_length and mins < 60*5:
                                  session_duration.append(mins)

          if session_duration:
                  session_count.append(len(session_duration))
                  m = np.mean(session_duration)
                  avg_session_length.append(m)

          if session_gap:
                  avg_session_gap.append(np.mean(session_gap))

          if visit_count:
                  user_visit_counts.append(visit_count)
  x = []
  y = []
  y2 = []

  oneDay = datetime.timedelta(days=1)

  start = startDate.date()
  end = start + oneDay

  idle_duration = datetime.timedelta(minutes=15)
  session_at_end_of_log = False

  loop = True
  xcoord = 0

  unique_visitors = []

  while loop:
          total_session_counts = 0
          visitorcount = 0
          for elem in userid_lst:
            log = list(LogUserEvents.objects.filter(logger_id=elem, created__gte=start, created__lt=end, is_visitor=False).order_by('created'))
            #log2 = list(LogCommentView.objects.filter(created__gte=start, created__lt=end).order_by('created'))
            #log = sorted(log+log2, key=lambda d: d.created) 
            session_counts = 0
            for i in range(0, len(log)-1):
                    diff = log[i+1].created - log[i].created
                    if (diff > idle_duration):
                            if(i == len(log)-2):
                                    session_at_end_of_log = True
                            session_counts += 1
            total_session_counts += session_counts
          
            log = list(LogCommentsReturned.objects.filter(logger_id=elem, created__gte=start, created__lt=end, is_visitor=False))
            if log:
              visitorcount += 1

          unique_visitors.append(visitorcount)
          y.append(total_session_counts)
          x.append(xcoord)
          y2.append(CommentRating.objects.filter(created__gte=start, created__lte=end, is_current=True).count())
          xcoord += 1

          start += oneDay
          end += oneDay
          if start > endDate.date():
                  loop = False

  disp = {}

  for l in LogCommentsReturned.objects.filter(created__gte=startDate, created__lte=endDate, query_type=LogCommentsReturned.unrated):
          comments = l.comments_list.split()
          for c in comments:
                  if c in disp:
                          disp[c] += 1
                  else:
                          disp[c] = 1

  x3 = []
  y3= []

  for k in disp.keys():
          x3.append(int(k))
          y3.append(int(disp[k]))


  dic = { 
          'ratings_per_comment': rate_count,
          'views_per_comment': view_count,
          'sessions_per_user': session_count,
          'session_duration': avg_session_length,
          'session_gap': avg_session_gap,
          'stats_per_day': [x, y, y2, unique_visitors],
          'comments_returned': [x3,y3],
          'agreement_ratings_count': agreement_ratings_count,
          'insight_ratings_count': insight_ratings_count,        
          'agreement_ratings': agreement_ratings,
          'insight_rating': insight_ratings,
          'last_updated': datetime.datetime.now(),
          'start_date': startDate,
          'end_date': endDate,
        }

  result[sd[1]] = dic
  


path=ASSETS_LOCAL+'statistics/data.pkl'
pickle.dump(result, open(path, "w"))

timer_end = datetime.datetime.now()
print "Done. Displaying graph. (time = %s seconds)" % str((timer_end-timer_start).seconds)




