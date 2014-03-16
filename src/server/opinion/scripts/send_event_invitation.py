'''send March 20 invitation'''
#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
import time
import csv
import hashlib

ofile  = open('send_event_invitation.csv', "wb")
writer=csv.writer(ofile,delimiter=',')
title=["UserId","username","email","comment","received","entrycode"]
writer.writerow(title)

user_active=User.objects.filter(is_active=True)
duplicated_email=['hunallen@gmail.com','patel.jay@berkeley.edu','ccrittenden@berkeley.edu','nonnecke@citris-uc.org','nonnecke@berkeley.edu','tanja.aitamurto@gmail.com','sanjaykrishn@gmail.com','goldberg@berkeley.edu']
user_email=[]
for email in duplicated_email:
    entrycode=hashlib.sha224(email).hexdigest()[0:7]
    candidate=EntryCode.objects.filter(code__exact=entrycode).order_by('id')
    user = User.objects.filter(username__exact=candidate[len(candidate)-1].username).order_by('id')
    user= user[len(user)-1]
    comment=DiscussionComment.objects.filter(user = user,is_current=True)
    if len(comment)>0
       user_email.append(user)


for user in user_active:
   if len(user.email)>0 and user.email not in duplicated_email:
       comment=DiscussionComment.objects.filter(user = user,is_current=True)
       if len(comment)>0:
          user_email.append(user)

for user in user_email:
    entrycode=EntryCode.objects.filter(username=user.username)
    row=[user.id]
    row.append(user.username)
    row.append(user.email)
    row.append(DiscussionComment.objects.filter(user = user,is_current=True)[0].comment)
    row.append(CommentAgreement.objects.filter(comment__in = DiscussionComment.objects.filter(user = user),is_current=True).count())
    if len(entrycode)>0:
        row.append(entrycode[0].code)
        received = CommentAgreement.objects.filter(comment__in = DiscussionComment.objects.filter(user = user),is_current=True).count()
        subject = str(received)+" people have graded your suggestion: Updates on the California Report Card"
        email_list = [user.email]
        comment=DiscussionComment.objects.filter(user = user,is_current=True)
        message = render_to_string('registration/crc_event_invitation.txt',
                                  {'entrycode': entrycode[0].code,
                                   'received': received,
                                   'comment': comment[0].comment,
                                    })
        
        try:
           #send_mail(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'), email_list)
           time.sleep(0.3)
        except:
           pass
    else:
        row.append("NA")
    writer.writerow(row)


