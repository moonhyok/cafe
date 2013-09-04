#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
from django.contrib.auth.models import User
from random import *
from opinion.includes.mathutils import *

first_os = OpinionSpace.objects.get(pk = 1)
users = User.objects.all()
for u in users:
	ratings = UserRating.objects.filter(user = u, is_current = True, opinion_space = first_os)
	if ratings.count() > 0:
		udc = UserData.objects.filter(user = u, key = 'first_rating')
		if udc.count() == 0:
			udc = UserData(user = u, key = 'first_rating', value = '')
			udc.save()
			print 'UD saved'