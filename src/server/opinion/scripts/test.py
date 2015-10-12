#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *



print InstructorUser.objects.all()
for u in AdminPanelUser.objects.all():
	print "I "
	print u.value