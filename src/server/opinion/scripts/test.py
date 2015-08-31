#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *

for u in UserData.objects.filter(key="year"):
	print u.value