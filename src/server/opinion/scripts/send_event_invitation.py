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

user_active=User.objects.filter(is_active=True)
duplicated_email=['hunallen@gmail.com','patel.jay@berkeley.edu','ccrittenden@berkeley.edu','nonnecke@citris-uc.org','nonnecke@berkeley.edu','tanja.aitamurto@gmail.com']
user_email=[]

for user in user_active:
   if len(user.email)>0 and user.email not in duplicated_email:
       comment=DiscussionComment.objects.filter(user = user,is_current=True)
       if len(comment)>0:
          user_email.append(user)

for email in duplicated_email:
    entrycode=hashlib.sha224(email).hexdigest()[0:7]   
    candidate=EntryCode.objects.filter(code__exact=entrycode).order_by('id')
    if len(candidate)>0:
       user = User.objects.filter(username__exact=candidate[len(candidate)-1].username).order_by('id')
       if len(user)>0:
          user= user[len(user)-1]
          comment=DiscussionComment.objects.filter(user = user,is_current=True)
          if len(comment)>0:
             user_email.append(user)

email_ken='goldberg@berkeley.edu'
entrycode=hashlib.sha224(email_ken).hexdigest()[0:7]   
candidate=EntryCode.objects.filter(code__exact=entrycode).order_by('id')
if len(candidate)>0:
   user = User.objects.filter(username__exact=candidate[len(candidate)-2].username).order_by('id')
   if len(user)>0:
      user= user[len(user)-1]
      received = CommentAgreement.objects.filter(comment__in = DiscussionComment.objects.filter(user = user),is_current=True).count()
      subject = str(received)+" people have graded your suggestion: Updates on the California Report Card"
      email_list = [user.email]
      comment=DiscussionComment.objects.filter(user = user,is_current=True)
      message = render_to_string('registration/crc_event_invitation.txt',
                                  {'entrycode': entrycode,
                                   'received': received,
                                   'comment': comment[0].comment,
                                    })
      try:
         #send_mail(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'), email_list)
         time.sleep(0.3)
      except:
         pass

'''
for user in user_email:
    entrycode=EntryCode.objects.filter(username=user.username)
    if len(entrycode)>0:
        received = CommentAgreement.objects.filter(comment__in = DiscussionComment.objects.filter(user = user),is_current=True).count()
        subject = str(received)+" people have graded your suggestion: Updates on the California Report Card"
        email_list = [user.email]
        comment=DiscussionComment.objects.filter(user = user,is_current=True)
        message = render_to_string('registration/crc_event_invitation.txt',
                                  {'entrycode': entrycode[0].code,
                                   'received': received,
                                   'comment': comment[0].comment,
                                    })
        print subject
        print message
        try:
           #send_mail(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'), email_list)
           time.sleep(0.3)
        except:
           pass'''


