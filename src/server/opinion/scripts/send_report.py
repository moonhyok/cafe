#!/usr/bin/env python
import environ
import string
from opinion.opinion_core.models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.dateformat import DateFormat
from opinion.includes.queryutils import *


## Functions
# Utility for displaying demographics
def display_demographic(line, demographic):
    if demographic != None and demographic != '':
        return '\t' + demographic
    else:
        return '\t' + '--'

# Table row function
def create_table_row_user(user):
    table_row = ''
    try:
        user_demographics = UserDemographics.objects.get(user = user)
    except UserDemographics.DoesNotExist:
        user_demographics = None
    try:
		reviewer_score = ReviewerScore.objects.get(user = user)
		score = reviewer_score.reviewer_score
    except ReviewerScore.DoesNotExist:
		score = 0
    time_joined_display = DateFormat(user.date_joined).format('h:i:s A')
    user_data_login = UserData.objects.filter(user = user, key = 'first_login')
    if len(user_data_login) > 0:
        time_joined_display = DateFormat(datetime.datetime.fromtimestamp(float(user_data_login[0].value))).format('h:i:s A')
    username_display = user.username
    if user.email != '':
		email_display = '--'
    else:
		email_display = '--'
    table_row += time_joined_display + '\t' + username_display + '\t' + email_display + '\t' + str(score)
    # if user_demographics != None:
    #     table_row += display_demographic(table_row, decode_to_unicode(user_demographics.location))
    #     table_row += display_demographic(table_row, decode_to_unicode(user_demographics.heard_about))
    zip_qs = ZipCodeLog.objects.filter(user=user)
    zip_code = str(zip_qs[0].location.city) if zip_qs else ''
    table_row += display_demographic(table_row, zip_code)

    ## Did they leave a comment?
    # TODO: make sure it is the current discussion questions
    commented = DiscussionComment.objects.filter(user = user).exists()
    table_row += "\tyes" if commented else "\tno"
    
    return table_row
		
url_list = string.split(URL_ROOT,'/')
title = " " + url_list[len(url_list) - 1] + " "

# Subject
df_now = DateFormat(datetime.datetime.now())
report_subject = '[California Report Card] Activity Digest for ' + df_now.format('l, F jS, Y')

# From
#report_from = Settings.objects.string('DEFAULT_FROM_EMAIL')
report_from = 'messages@californiareportcard.org'

# Recipients
if EMAIL_RECIPIENTS:
	report_recipients = EMAIL_RECIPIENTS

# Body
report_body = ''

## Header
report_header = report_subject
report_body += "<h2>%s</h2>" % report_header
report_body += "californiareportcard.org"

## Quick stats
report_body += "<h3>Number of users so far: %s</h3>" % User.objects.filter(id__gte = 310).count()

# TODO: add number of users who gave us their email?

# We aren't collecting feedback now (12/26)
"""
### Feedback
feedbacks = Feedback.objects.filter(created__gte = datetime.date.today() - datetime.timedelta(days=1))
feedback_display = ''
feedback_display += '<h3>Feedback:</h3>'
for feedback in feedbacks:
    feedback_line = ''
    if feedback.user != None:
        feedback_line += feedback.user.username + ' ' + feedback.user.email
    else:
        feedback_line += 'Anonymous'
    feedback_line += ' at ' + DateFormat(feedback.created).format('h:i:s A') + ': ' + decode_to_unicode(feedback.feedback)
    feedback_display += feedback_line + '\n'
report_body += feedback_display
"""

## New users
table_body = ''

if Settings.objects.boolean('USE_ENTRY_CODES'):
	users = []
	users_objects = UserData.objects.filter(key = 'first_login', updated__gte = datetime.datetime.now())
	for ud in users_objects:
        	users.append(ud.user) 
else:
	users = User.objects.filter(date_joined__gte = datetime.datetime.now() - datetime.timedelta(days=1))

table_body += '<h3>New users that registered today:</h3>'

table_body += '<table border="1">'
table_body += "<tr><td>Time Registered (PST)</td><td>User ID</td><td>Email</td><td>Reviewer Score</td><td>Location</td><td>Left a comment?</td></tr>"

for user in users:
	table_row = '<tr>'
        row_data = create_table_row_user(user).split("\t")
        print row_data
        row_data = map(lambda x: "<td>" + x + "</td>", row_data)
	table_row += "".join(row_data)
        table_row += "</tr>"
        table_body += table_row
table_body += "</table>"
report_body += table_body

## Daily Statistics
daily_statistics = ""
daily_statistics += '<h3>Total new users: ' + str(len(users)) + '</h3>'
report_body += daily_statistics

## Top comments
OS_ID = 1
report_body += "<h3>Top comments from the past week:</h3>" 

os = OpinionSpace.objects.get(pk = OS_ID)
discussion_statement_objects = os.discussion_statements.filter(is_current = True)
comments = DiscussionComment.objects.filter(is_current = True, discussion_statement = discussion_statement_objects[0], confidence__lte = .15, confidence__isnull = False).order_by('-normalized_score_sum')[0:20]
count = 1
for comment in comments:
	if comment.created.date() >= datetime.date.today() - datetime.timedelta(days=7):
		report_body += "\n"+str(count)+". Username: "+comment.user.username + "\nEmail: " + comment.user.email  + "\nComment:"  + decode_to_unicode(comment.comment) + "\nNormalized Score: " + str(comment.normalized_score_sum) + "\n"
		count+=1

## Flagged comments
report_body += ""
report_body += "<h3>Flagged comments:</h3>" 

flagged = FlaggedComment.objects.all().order_by('comment')
printed = []
for fcomment in flagged:
    if fcomment.created.date() >= datetime.date.today() - datetime.timedelta(days=7):
	if fcomment.comment.discussion_statement == discussion_statement_objects[0]:
		if fcomment.comment not in printed and not_admin_approved(fcomment.comment):
			report_body += 'Username: ' + fcomment.comment.user.username + '\nEmail: ' \
                            + fcomment.comment.user.email + "\nComment: " + decode_to_unicode(fcomment.comment.comment) + '\n\n'
			printed.append(fcomment.comment)

#send_mail(report_subject, report_body, report_from, report_recipients)

from django.core.mail import EmailMultiAlternatives
msg = EmailMultiAlternatives(report_subject, report_body, report_from, report_recipients)
html_content = report_body.replace("\n", "<br>")
msg.attach_alternative(html_content, "text/html")
msg.send()

