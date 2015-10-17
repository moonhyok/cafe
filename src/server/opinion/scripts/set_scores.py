#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
import csv
import settings

users = User.objects.all()
agreement = {}
max = 0
for u in users:	
	comment = DiscussionComment.objects.filter(is_current=True,user=u)
	if len(comment) > 0 and len(CommentAgreement.objects.filter(is_current=True,comment = comment[0])) > 4: 
		agreement[u] = np.mean(CommentAgreement.objects.filter(is_current=True,comment = comment[0]).values_list('agreement'))
		if agreement[u] > max:
			max = agreement[u]
	else:
		agreement[u] = 0 

for u in users:
	comment = DiscussionComment.objects.filter(is_current=True,user=u)
	if len(comment) > 0:
		score = 0
		if comment[0].normalized_score_sum != None:
			score = .5*comment[0].normalized_score_sum
		score = score + agreement[u]*.5
		comment[0].confidence = score
		comment[0].save()
		print comment[0].id,score

