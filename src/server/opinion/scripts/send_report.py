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
    username_display = user.id
    if user.email != '':
		email_display = '--'
    else:
		email_display = '--'
    table_row += time_joined_display + '\t' + username_display + '\t' + email_display + '\t' + str(score)
    if user_demographics != None:
        table_row += display_demographic(table_row, decode_to_unicode(user_demographics.location))
        table_row += display_demographic(table_row, decode_to_unicode(user_demographics.heard_about))
    return table_row
		
url_list = string.split(URL_ROOT,'/')
title = " " + url_list[len(url_list) - 1] + " "

# Subject
df_now = DateFormat(datetime.datetime.now())
report_subject = 'Citizen Report Card (on citizenreportcard.org) Acitivity Digest for ' + df_now.format('l, F jS, Y')

# From
#report_from = Settings.objects.string('DEFAULT_FROM_EMAIL')
report_from = 'messages@citizenreportcard.org'

# Recipients
if EMAIL_RECIPIENTS:
	report_recipients = EMAIL_RECIPIENTS

# Body
report_body = ''

## Header
report_header = report_subject + '\n'
report_body += report_header

## Feedback
feedbacks = Feedback.objects.filter(created__gte = datetime.date.today() - datetime.timedelta(days=1))
feedback_display = '\n'
feedback_display += 'Feedback:\n'
for feedback in feedbacks:
    feedback_line = ''
    if feedback.user != None:
        feedback_line += feedback.user.username + ' ' + feedback.user.email
    else:
        feedback_line += 'Anonymous'
    feedback_line += ' at ' + DateFormat(feedback.created).format('h:i:s A') + ': ' + decode_to_unicode(feedback.feedback)
    feedback_display += feedback_line + '\n'
report_body += feedback_display

## New users
table_body = ''

if Settings.objects.boolean('USE_ENTRY_CODES'):
	users = []
	users_objects = UserData.objects.filter(key = 'first_login', updated__gte = datetime.datetime.now())
	for ud in users_objects:
        	users.append(ud.user) 
else:
	users = User.objects.filter(date_joined__gte = datetime.datetime.now() - datetime.timedelta(days=1))

table_body += '\n' + 'New users that registered today:\n' + 'Format: Time Registered (PST), Username, Email, Reviewer Score, Location, Heard From (tab delimited)'
for user in users:
	table_row = ''
	table_row = create_table_row_user(user)
	table_body += '\n' + table_row 
report_body += table_body

## Daily Statistics
daily_statistics = '\n\n'
daily_statistics += 'Total new users: ' + str(len(users))
daily_statistics += '\n'
report_body += daily_statistics

## Top comments
OS_ID = 1
report_body += "\n"
report_body += "Top comments from the past week:\n" 

os = OpinionSpace.objects.get(pk = OS_ID)
discussion_statement_objects = os.discussion_statements.filter(is_current = True)
comments = DiscussionComment.objects.filter(is_current = True, discussion_statement = discussion_statement_objects[0], confidence__lte = .15, confidence__isnull = False).order_by('-normalized_score_sum')[0:20]
count = 1
for comment in comments:
	if comment.created.date() >= datetime.date.today() - datetime.timedelta(days=7):
		report_body += "\n"+str(count)+". Username: "+comment.user.username + "\nEmail: " + comment.user.email  + "\nComment:"  + decode_to_unicode(comment.comment) + "\nNormalized Score: " + str(comment.normalized_score_sum) + "\n"
		count+=1

## Flagged comments
report_body += "\n"
report_body += "Flagged comments:\n" 

flagged = FlaggedComment.objects.all().order_by('comment')
printed = []
for fcomment in flagged:
	if fcomment.comment.discussion_statement == discussion_statement_objects[0]:
		if fcomment.comment not in printed and not_admin_approved(fcomment.comment):
			report_body += 'Username: ' + fcomment.comment.user.username + '\nEmail: ' + fcomment.comment.user.email + "\nComment: " + decode_to_unicode(fcomment.comment.comment) + '\n'
			printed.append(fcomment.comment)

send_mail(report_subject, report_body, report_from, report_recipients)
