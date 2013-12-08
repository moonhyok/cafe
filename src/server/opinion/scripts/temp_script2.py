#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

"""
comments = DiscussionComment.objects.all()  
for c in comments:
	if len(c.comment.split()) < 20:
		print c.comment 
		c.blacklisted = True
		c.save()
"""

for u in UserRating.objects.all():
	u.rating = max(u.rating -.1,0)
	print u.rating
	u.save()

