'''Ask participant to return the site'''
#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
import time

user_active=User.objects.filter(is_active=True)
launch_day=datetime.datetime(2014,01,28,0,0,0,0)
f=open('send_grade_email_test.txt','w')
user_email=[]
for user in user_active:
    if len(user.email)>0:
       comment=DiscussionComment.objects.filter(user = user,is_current=True)
       if len(comment)>0:
          user_email.append(user)
          

for user in user_email:
    entrycode=EntryCode.objects.filter(username=user.username)
    f.write(str(user.email)+'\n')
    if len(entrycode)>0:
        subject = "Your grades are ready to view at the California Report Card!"
        received = 2*CommentAgreement.objects.filter(comment__in = DiscussionComment.objects.filter(user = user),is_current=True).count()
        email_list = [user.email]
        comment=DiscussionComment.objects.filter(user = user,is_current=True)
        f.write(str(entrycode[0].code)+'\n')
        f.write(str(comment[0].comment)+'\n')
        f.write(str(received/2)+'\n')
        message = render_to_string('registration/crc_grade_ready.txt',
                                  {'entrycode': entrycode[0].code,
                                   'received': received/2,
                                   'comment': comment[0].comment,
                                   'newParticipant': User.objects.filter(date_joined__gte=launch_day).count()
                                    })
        
        try:
           #send_mail(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'), email_list)
           time.sleep(0.3)
        except:
           pass
