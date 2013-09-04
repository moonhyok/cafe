#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
from django.core.mail import EmailMessage
import sys
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36

if len(sys.argv) < 3:
	print "Usage: python send_password_reset.py username email"
	sys.exit()
	
username = str(sys.argv[1]).lower()
email = sys.argv[2]

subject = 'Hybrid Wisdom: Password Reset'
from_email = Settings.objects.string('DEFAULT_FROM_EMAIL')
body = """You are receiving this email becase you have indicated that you would like to reset your password.

To reset your password, click here and create a new one:

{PASSWORD_RESET_LINK}

If you did not request a password reset, please disregard this message.

- The Hybrid Wisdom Team
"""

user = User.objects.get(username = username)

# Create the password reset link
uid = int_to_base36(user.id)
token = default_token_generator.make_token(user)
url_root = settings.URL_ROOT
password_reset_link = url_root + '/accountsjson/password/reset/confirm/' + uid + '-' + token + '/'
userbody = body.replace('{PASSWORD_RESET_LINK}', password_reset_link)
  
email = EmailMessage(subject = subject,
                     body = userbody,
                     from_email = from_email,
                     to = [email],
                     headers = {'Reply-To': Settings.objects.string('DEFAULT_FROM_EMAIL')})

email.send()