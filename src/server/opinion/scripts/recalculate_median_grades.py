#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

active_users = list(User.objects.filter(is_active=True))
skip_begin_date=datetime.datetime(2014,1,9,0,0,0,0)

for s in OpinionSpaceStatement.objects.all():
    ratings = UserRating.objects.filter(is_current=True,opinion_space_statement = s, user__in = active_users)
    skip_logs = LogUserEvents.objects.filter(is_visitor=True, log_type=11,details__contains='slider_set',created__gte = skip_begin_date)
    users_with_grades = []
    for skip_log in skip_logs:
        slider_set_args = skip_log.details[10:].lstrip()
        visitor = Visitor.objects.filter(id = skip_log.logger_id)
	if len(visitor) > 0:
          visitor = visitor[0]
          if visitor.user != None and visitor.user.is_active and int(slider_set_args[0]) == s.id:
            users_with_grades.append(visitor.user)

    cache = StatementMedians.objects.filter(statement = s)
    value = np.median(ratings.filter(user__in = users_with_grades).values_list('rating'))
    if cache.count() == 0:
        StatementMedians(statement = s, rating = value).save()
    else:
        cache[0].rating = value
        cache[0].save()

    print s.id, value
