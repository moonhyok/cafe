#!/usr/bin/env python
from opinion.opinion_core.models import *
import numpy as np
from opinion.includes.queryutils import *
import random

email_users = User.objects.filter(is_active=True).exclude(email__contains="example").exclude(email = None).exclude(email = "")
#print email_users.count()
def get_participation_score(user):
	return (100*CommentRating.objects.filter(rater = user, is_current=True).count())#, user.email)

def get_author_score(user):
	result = (0, None)
	for c in DiscussionComment.objects.filter(user = user, is_current=True):
		if CommentRating.objects.filter(is_current=True,comment=c).count() > 0:	
			rating_mean = 1- np.mean(CommentRating.objects.filter(is_current=True,comment=c).values_list('rating'))
			rating_se = 1.96*np.std(CommentRating.objects.filter(is_current=True,comment=c).values_list('rating'))/np.sqrt(CommentRating.objects.filter(is_current=True,comment=c).count())
			result = (rating_mean - rating_se, c.comment)
	return result[0]

# total = []
# for u in email_users:
# 	total.append(get_author_score(u))

# total.sort(reverse=True)

# for t in total[:10]:
# 	print t

# ptotal = []
# for u in email_users:
# 	ptotal.append(get_participation_score(u))

# ptotal.sort(reverse=True)

# for p in ptotal[:10]:
# 	print p

