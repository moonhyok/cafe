#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import time

#exclude_list=['nonnecke@berkeley.edu','goldberg@eecs.berkeley.edu','angelaslin@berkeley.edu','matti@example.com','patel24jay@gmail.com','ccrittenden@berkeley.edu','alisoncliff@berkeley.edu','alisoncliff@berkeley.edu','hunallen@berkeley.edu']
alluser=User.objects.all().order_by('id')

for user in alluser:
    entrycode=EntryCode.objects.filter(username=user.username)
    
    if len(entrycode)>0:
        subject = "Evaluate CS169.1x on M-CAFE"
        email_list = [user.username]
        message = render_to_string('registration/mcafe-6th-regrade.txt',
                                   {'entrycode': '',
                                   })
        email = EmailMessage(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'),email_list, headers = {'Reply-To': 'cafe.mooc@gmail.com'})
    try:
	print user.username
        email.send()

        time.sleep(0.1)
    except:
        pass

