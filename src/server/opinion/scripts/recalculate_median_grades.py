#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

active_users = list(User.objects.filter(is_active=True))
skip_begin_date=datetime.datetime(2014,1,9,0,0,0,0)

for s in OpinionSpaceStatement.objects.all():

    s_rating=UserRating.objects.filter(opinion_space_statement=s,is_current=True,user__in = active_users)
    s_rating_list=[]
    for rating in s_rating:
        if rating.created>=skip_begin_date:
           visitor=Visitor.objects.filter(user=rating.user)  #get the visitor of the user
           if len(visitor)>0:
              s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains=str(s.id)).order_by('-created') #get issue skip log
              s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').filter(details__startswith='slider_set '+str(s.id)).order_by('-created')
              if len(s_log_skip)==0: #no skip
                  if len(s_log_rating)>0:
                     s_rating_list.append(rating.rating)
              else:
                  if len(s_log_rating)>0:  #click skip, not move slider s => skip
                     if s_log_skip[0].created<=s_log_rating[0].created: #final decision is skip
                        s_rating_list.append(rating.rating)
           else: 
              s_rating_list.append(rating.rating)
        else:
           s_rating_list.append(rating.rating)
    
    cache = StatementMedians.objects.filter(statement = s)
    value = np.median(s_rating_list)
    if cache.count() == 0:
        StatementMedians(statement = s, rating = value).save()
    else:
	cache.update(rating = value)

    print s.id, value, len(s_rating_list)
