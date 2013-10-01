#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

for u in User.objects.all():
	u.username = 'user' + str(u.id)
	us = UserSettings.objects.filter(user = u)
        if len(us) > 0:
		us[0].delete()
	u.save()
