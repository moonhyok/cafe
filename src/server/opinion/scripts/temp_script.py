#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

for u in User.objects.filter(id__lte = 361):
	comment = DiscussionComment.objects.filter(is_current =True, user = u)
	if len(comment) > 0:
		comment[0].blacklisted = True
		comment[0].save()
		print "Pruned negative comment"

