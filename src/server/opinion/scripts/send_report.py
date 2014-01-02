#!/usr/bin/env python
import environ
import string
from opinion.opinion_core.models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.dateformat import DateFormat
from opinion.includes.queryutils import *

def list_to_td(L):
    row_data = map(lambda x: "<td>" + x + "</td>", L)
    return  "".join(row_data)

TIME_FRAME = datetime.date.today() - datetime.timedelta(days=1)		
url_list = string.split(URL_ROOT,'/')
title = " " + url_list[len(url_list) - 1] + " "

# Subject
df_now = DateFormat(datetime.datetime.now())
report_subject = '[California Report Card] Activity Digest for ' + df_now.format('l, F jS, Y')

# From
report_from = 'CRC-Daily-Activity-Summary@citizenreportcard.org'

# Recipients
if EMAIL_RECIPIENTS:
	report_recipients = EMAIL_RECIPIENTS
else:
	error_sub = "Error sending nightly report"
        error_body = "%s\nEMAIL_RECIPIENTS not set in settings_local.py\n%s" % (error_sub, URL_ROOT)
	send_mail(error_sub, error_body, report_from, TROUBLESHOOT_EMAIL_RECIPIENTS)        

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

if Settings.objects.boolean('USE_ENTRY_CODES'):
	users = []
	users_objects = UserData.objects.filter(key = 'first_login', updated__gte = datetime.datetime.now())
	for ud in users_objects:
        	users.append(ud.user) 
else:
	users = User.objects.filter(date_joined__gte = datetime.datetime.now() - datetime.timedelta(days=1))


# Participation Statistics
participation_legend = {
	1 : 'visited the site, pressed "Begin"', 
	2 : 'submitted grades',
	3 : 'submitted zip code',
	4 : 'submitted CA zip code',
	5 : 'rated at least 2 other participant\'s ideas',
	6 : 'submitted a valid idea',
	7 : 'submitted email address',
	8 : 'submitted valid email address',
	9 : 'returns using unique URL',
	10 : '9+ rates'
}

participation_reached = { 
	1 : LogUserEvents.objects.filter(details='first time',log_type=7, created__gte=TIME_FRAME).count(),
	2 : LogUserEvents.objects.filter(details='sliders finished',log_type=5, created__gte=TIME_FRAME).count(),
	3 : len(users),
	4 : len(filter(lambda u: u.location.state == 'CA', users)), 
	5 : sum([CommentRating.objects.filter(user = u).count() >= 2 for u in users]),
	6 : sum([DiscussionComment.objects.filter(user = u).exists() for u in users]),
	7 : sum([bool(u.email) for u in users]),
	8 : sum([bool(u.email) for u in users]),
	9 : 'under construction',
	10 : 'under construction', 
}

pr = participation_reached

participation_stopped = {
	1 : pr[1] - pr[2],
	2 : pr[2] - (pr[3] + pr[4]),
	3 : pr[3] - pr[5],
	4 : pr[4] - pr[5],
	5 : pr[5] - pr[6],
	6 : pr[6] - (pr[7] + pr[8]),
	7 : pr[7],
	8 : pr[8],
	9 : '--',
	10 : '--'
}

participation_table = "<h3>Participation Summary:</h3>"
participation_table += "<table border='1'><tr><td>Level</td><td>Actions</td><td># Who Reached Level</td><td># Who Stopped At Level</td></tr>"
for p in sorted(participation_legend.keys()):
	r = list_to_td([str(p), participation_legend[p], str(participation_reached[p]), str(participation_stopped[p])])
	line = "<tr>" + r + "</tr>"
	participation_table += line

participation_table += "</table>"
report_body += participation_table

## New users
table_body = ''

table_body += '<h3>New users that registered today:</h3>'

table_body += '<table border="1">'

header_cols = ['Time Registered (PST)', 'User ID', 'Zip Code', 'Location', '# Ideas Rated', 'Submitted Idea?', 'Email address']
header_row = "<tr>%s</tr>" % list_to_td(header_cols)
table_body += header_row

for user in users:
	table_row = '<tr>'
        row_data = create_table_row_user(user).split("\t")
        print row_data
	table_row += list_to_td(row_data)
	#row_data = map(lambda x: "<td>" + x + "</td>", row_data)
	#table_row += "".join(row_data)
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
    
    time_joined_display = DateFormat(user.date_joined).format('h:i:s A')
    user_data_login = UserData.objects.filter(user = user, key = 'first_login')
    if len(user_data_login) > 0:
        time_joined_display = DateFormat(datetime.datetime.fromtimestamp(float(user_data_login[0].value))).format('h:i:s A')

    username_display = user.username
    if user.email != '':
		email_display = '--'
    else:
		email_display = '--'

    zip_qs = ZipCodeLog.objects.filter(user=user)
    if zip_qs:
	    zipcode, location = zip_qs[0].location.code, zip_qs[0].location.city + ", " + zip_qs[0].location.state
    else:
	    zipcode, location = "--", "--"

    num_ideas_rated = CommentRating.objects.filter(user = user).count()
    
    ## Did they leave a comment?
    # TODO: make sure it is the current discussion questions
    commented = "yes" if DiscussionComment.objects.filter(user = user).exists() else no

    return "\t".join([time_joined_display, username_display, zipcode, location, num_ideas_ratied, commented])

