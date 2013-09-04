#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import time
import datetime

# Get the first OS
fs = ForeignCredential.objects.all()
["01-18","18-25","26-33","33-50","50+"]
for f in fs:
	keys = UserData.objects.filter(user = f.user)
	for k in keys:
		if k.key == 'birthday':
			years = (datetime.datetime.now() - datetime.datetime.strptime(k.value, "%m/%d/%Y")).days / 365.25
			if years < 18:
				age= "01-18"
			elif years > 18 and years < 26:
				age="18-25"
			elif years > 26 and years < 34:
				age="26-33"
			elif years > 34 and years < 50:
				age="33-50"
			else:
				age="50+"
			if UserData.objects.filter(user= f.user,key='age').count() == 0:
				UserData(user= f.user,key='age',value=age).save()
				print UserData.objects.filter(user= f.user,key='age').count()
			else:
				print UserData.objects.filter(user= f.user,key='age')[0].value