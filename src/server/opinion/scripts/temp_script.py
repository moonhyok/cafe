#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

comments = DiscussionComment.objects.filter(is_current=True)
print comments.count()
count = 0
for c in comments:
	if CommentRating.objects.filter(comment = c,is_current=True).count() >= 5:
		count = count + 1
		print CommentRating.objects.filter(comment = c).order_by("created")[4].created - c.created 
print count
