#!/usr/bin/env python
import environ
import string
from opinion.opinion_core.models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.dateformat import DateFormat
from opinion.includes.queryutils import *
from prettytable import *


url_list = string.split(URL_ROOT,'/')
title = " " + url_list[len(url_list) - 1] + " "


# From
report_from = 'CRC-Daily-Activity-Summary@citizenreportcard.org'

# Recipients
if EMAIL_RECIPIENTS:
	report_recipients = EMAIL_RECIPIENTS
else:
	error_sub = "Error sending nightly report"
        error_body = "%s\nEMAIL_RECIPIENTS not set in settings_local.py\n%s" % (error_sub, URL_ROOT)
	send_mail(error_sub, error_body, report_from, TROUBLESHOOT_EMAIL_RECIPIENTS)        


report_information = format_pretty_nightly_statistics_table() # format pretty table
report_subject = report_information['report_subject']
report_body_text = report_information['report_body_text']
report_body_html = report_information['report_body_html']

from django.core.mail import EmailMultiAlternatives
msg = EmailMultiAlternatives("test: " + report_subject, report_body_text, report_from, report_recipients)
msg.attach_alternative(report_body_html, "text/html")
msg.send()


