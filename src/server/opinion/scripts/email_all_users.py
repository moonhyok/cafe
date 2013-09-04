#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
from django.core.mail import EmailMessage
from django.utils.http import int_to_base36
import hashlib
import datetime

subject = 'Hybrid Wisdom: Update'
from_email = Settings.objects.string('DEFAULT_FROM_EMAIL')
body = """Hello {USERNAME},

  Some text goes here

- the Hybrid Wisdom Team

To unsubscribe to future notifications: {UNSUBSCRIBE_LINK}
"""

def createUnsubscribeLink(user):
    uid = int_to_base36(user.id)
    url_root = settings.URL_ROOT
    hasher = hashlib.md5()
    hasher.update(user.email)
    token = hasher.hexdigest()
    return url_root + '/accountsjson/unsubscribe/notifications/' + uid + '-' + token + '/'

users = User.objects.all()
emails = set()
twitter_set = set()

for u in users:
  email = u.email
  if email:
    emails.add((u,email))
  else:
    email_objects = UserData.objects.filter(user = u, key = 'email')
    if len(email_objects) != 0:
      emails.add((u,email_objects[0].value))
    else:
      foreign_creds = ForeignCredential.objects.filter(user = u)
      if len(foreign_creds) != 0:
         if 'twitter' in foreign_creds[0].foreignid:
            screenname = UserData.objects.filter(user = u, key = 'screename')
            if len(screenname) > 0:
               twitter_set.add((u,screenname[0].value))

import twitter
#HWL account details
ck = "7ZgGeudviRlKQFpIKozYeA"
cs = "NXyt7wzm35shKjeAet26emRv8ZkeLwDOutdYyors"
at = "461801199-3cNjhyHzMbInG7O57nBO6jtZrPesCXTF6sH9mOEu"
ats = "A8BZXxIrGDql4XAIpTYergoMW1ESBM6GnHn2k5a6c"
#api = twitter.Api(consumer_key=ck,consumer_secret=cs,access_token_key=at,access_token_secret=ats)

for e in emails:
  ud = UserData.objects.filter(user = e[0], key='unsubscribe_notification_updates')
  if len(ud) != 0:
    continue
  new_body = body.replace("{USERNAME}",e[0].username).replace("{UNSUBSCRIBE_LINK}",createUnsubscribeLink(e[0]))
  print e[1]
"""
        email = EmailMessage(subject = subject,
                         body = new_body,
                         from_email = from_email,
                         to = [e[1]],
                         headers = {'Reply-To': Settings.objects.string('DEFAULT_FROM_EMAIL')})
        email.send()
"""

for t in twitter_set:
  ud = UserData.objects.filter(user = t[0], key='unsubscribe_notification_updates')
  if len(ud) != 0:
    continue
  new_body = body.replace("{USERNAME}",t[0].username).replace("{UNSUBSCRIBE_LINK}",createUnsubscribeLink(t[0]))
  print t[1]
  #api.PostDirectMessage(t[1],new_body)
