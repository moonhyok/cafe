#!/usr/bin/env python
import fileinput
import environ
import os
from opinion.opinion_core.models import *
import datetime
import time
import csv
import hashlib
import warnings
warnings.filterwarnings("ignore")

# Usage
# cat /var/log/apache2/access.log{,1} | grep -oP "GET /mobile/crcstats/\K([\w]+)" | uniq | sort | uniq |  python scripts/count_entrycode_renter.py

TIME_RANGE = datetime.date.today() - datetime.timedelta(days=2)

print ' '.join(["User ID", "User Email", "EntryCode", "Ratings Given By User Since We Sent Email", "Ratings Received (from Email Subject Line)"])

def received(user):
   return CommentAgreement.objects.filter(comment__in = DiscussionComment.objects.filter(user = user),is_current=True).count()

def given(u):
   return CommentAgreement.objects.filter(is_current=True,rater = u, created__gte = TIME_RANGE).count()

for line in fileinput.input():
   ec = line.strip()
   username = EntryCode.objects.filter(code=ec)[0].username if EntryCode.objects.filter(code=ec).exists() else None

   if username is not None:
      user = User.objects.get(username=username)
      to_print = map(str, (user.id, user.email, ec, given(user), received(user)))
      print ' '.join(to_print)


      
      
      
      
