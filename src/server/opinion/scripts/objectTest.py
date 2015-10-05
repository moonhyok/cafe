#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *


print User
for u in User.objects.all():
	print u

print data