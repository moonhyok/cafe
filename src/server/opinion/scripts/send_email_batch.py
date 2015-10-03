#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
import time

today_date=datetime.datetime.today()-datetime.timedelta(days=1)
user_today=User.objects.filter(date_joined__gte=today_date)

user_today_email=[]
for user in user_today:
    if len(user.email)>0:
       user_today_email.append(user)

for user in user_today_email:
    entrycode=EntryCode.objects.filter(username=user.username,first_login=False)
    print len(entrycode)
    if len(entrycode)>0:
        subject = "Your unique link to the California Report Card v1.0"
        email_list = [user.email]
        message = render_to_string('registration/confirmation_email.txt',
                                  {'entrycode': entrycode[0].code,
                                   'user_id': user.id,
                                    })
        try:
           send_mail(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'), email_list)
           print user.email
           time.sleep(0.3)
        except:
           pass
