#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
import random

comments = DiscussionComment.objects.all()  
for c in comments:
	if  c.id <= comments.count() - 3:
		print c.comment 
		c.blacklisted = True
		c.save()

#user = User.objects.filter(id__gte = 300)
#for u in user:
#	print u.username
#	for r in UserRating.objects.filter(user = u):
#		r.rating = .5*random.random() 
#		r.save()


