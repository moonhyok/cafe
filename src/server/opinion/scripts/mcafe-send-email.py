#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import time

today_date=datetime.datetime.today()-datetime.timedelta(days=1)
user_today=User.objects.filter(date_joined__gte=today_date)


for user in user_today:
    entrycode=EntryCode.objects.filter(username=user.username)
    
    if len(entrycode)>0:
        subject = "Your unique link to the CS169.2x MCAFE"
        email_list = [user.username]
        message = render_to_string('registration/mcafe-confirmation.txt',
                                   {'entrycode': entrycode[0].code,
                                   })
        email = EmailMessage(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'),
                    email_list, headers = {'Reply-To': 'cafe.mooc@gmail.com'})
    try:
        email.send()
        print user.username
        time.sleep(0.3)
    except:
        pass
