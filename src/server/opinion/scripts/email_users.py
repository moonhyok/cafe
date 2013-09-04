#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
from django.core.mail import EmailMessage
from numpy import *
import sys
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36

sure_check = raw_input('Are you sure you want to email all Opinion Space users? Type "YES" if you are: ')
if sure_check != 'YES':
    print 'Exiting script.'
    sys.exit()
	
# Set CHECK_EMAILS to True to not send any emails and just check if any emails are sent incorrectly
CHECK_EMAILS = True

# The range of ids to send emails to with the lower bound inclusive and upper bound not inclusive
startId = 2000
endIdNI = 5000

# List used to check if we're not spamming anyone
nonrecipients = []
recipients = []

shortbody = """
test:
{PASSWORD_RESET_LINK}
"""

subject = 'Opinion Space: Second Discussion Question'
from_email = Settings.objects.string('DEFAULT_FROM_EMAIL')
body = """Thank you for trying Opinion Space, a new approach to online discussions developed at the UC Berkeley Center for New Media. The first Opinion Space discussion was about the economy.  We now invite you to participate in our second discussion, on legalization of marijuana.

Just visit:

http://opinion.berkeley.edu
and sign in

If you don't remember your password, or never created one, click here to reset your password and create a new one:

{PASSWORD_RESET_LINK}

To see the new discussion question, sign in and click the large yellow point (ME) or the "Show My Opinions" button; then you can submit your response! Click on other points to read and rate their responses--note that people with similar opinions will have points close to yours. Larger points correspond to responses that other users have found most valuable.

Some reviews of Opinion Space are below, and at bottom is a link to unsubscribe (but we promise to contact you very rarely!).

"Opinion Space is quite pretty, mildly addictive, and full of rich possibilities for visualizing a community's opinions. Wired.com would love to have such a tool at its disposal..." Wired News.

"Linear lists are often dominated by extreme postings that can oversimplify and overshadow the rich variety of viewpoints," said Howard Rheingold, author of Smart Mobs.

"Massive collaboration is driven by passionate people with divergent viewpoints who come from all walks of life.  UC Berkeley's 'Opinion Space' is an exciting new visual model that helps people learn about and interact with each other. This kind of mutual awareness could have far-reaching implications."  - Jay Walsh, Head of Communications, Wikipedia.org

Thanks!

- the Opinion Space Team at UC Berkeley

We won't spam you, but if you don't want to receive any more emails from us, simply go to the settings page at http://opinion.berkeley.edu to opt out.
"""

total = 0
for user in User.objects.all():
    # Skip only if this user has chosen not to receive mail. Note this includes all users that haven't set a preference in settings
    user_settings = UserSettings.objects.filter(user = user, key = 'emailme')
    
    # Include len(user_settings) == 0 to exclude users that haven't set a preference for receiving email
	# This also excludes users not within the correct id range
    if (len(user_settings) > 0 and user_settings[0].value == '0') or user.id < startId or user.id >= endIdNI:
    	nonrecipients.append(user.email)
        continue

    recipients.append(user.email)

	# Create the password reset link - Remove this and put in a note about email us for a password reset link
    uid = int_to_base36(user.id)
    token = default_token_generator.make_token(user)
    url_root = settings.URL_ROOT
    password_reset_link = url_root + '/accounts/password/reset/route/' + uid + '-' + token + '/'
    userbody = body.replace('{PASSWORD_RESET_LINK}', password_reset_link)
    #tempbody = shortbody.replace('{PASSWORD_RESET_LINK}', password_reset_link)
	
    if CHECK_EMAILS:
		total += 1
		continue
    
    email = EmailMessage(subject = subject,
                         body = userbody,
                         from_email = from_email,
                         to = [user.email],
                         headers = {'Reply-To': Settings.objects.string('DEFAULT_FROM_EMAIL')})

    email.send()
    total += 1

if CHECK_EMAILS:
    for user in UserSettings.objects.filter(value = 0):
        u = User.objects.filter(id = user.user_id)
        if len(u) == 1:
            if u[0].id >= startId and u[0].id < endIdNI:
				if u[0].email not in nonrecipients or u[0].email in recipients:
					print u[0].email + " should not recieve an email. They currently are!"
        else:
            print "Error: for user " + user.user_id + ". There were multiple matching ids in the auth_user table"

if CHECK_EMAILS:
	print "Done checking emails."
	print "Email would be sent to %i recipients" % (total)
else:
	print "Email sent to %i recipients" % (total)
