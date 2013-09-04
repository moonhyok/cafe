#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
import random
import settings

f = open('booking_users.csv', 'r')

line = f.readline()
i = 0
while line != "":
	components = line.split(',')
	username = "Participant" + str(i+9000)
	email = components[5]
	entry_code = '%030x' % random.randrange(256**15)
	entry_code = entry_code[:10]
	if len(email) == 0:
		break;
	
	user = User.objects.create_user(username, email, entry_code)
	user.save()	
	
	entrycode = EntryCode(username = username, code = entry_code, first_login = True)
	entrycode.save()
		
	print username,email,settings.URL_ROOT +'/' + entry_code
	
	i = i + 1
	line = f.readline()

