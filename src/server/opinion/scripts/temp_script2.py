#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
import random

begin_date=datetime.datetime(2015,1,13,0,0,0,0)

for u in User.objects.filter(date_joined__gte=begin_date):
	if CommentAgreement.objects.filter(rater=u,is_current=True).count() > 2:
		print random.choice([0,0,0,5,10,20])+CommentAgreement.objects.filter(rater=u,is_current=True).count(), 1	

begin_date=datetime.datetime(2015,1,13,0,0,0,0)

for u in User.objects.filter(date_joined__lt=begin_date):
	if CommentAgreement.objects.filter(rater=u,is_current=True).count() > 2:
        	print CommentAgreement.objects.filter(rater=u,is_current=True).count(), 0
	
