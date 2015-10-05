#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
import time

user_date = datetime.date(2015,8,26)
subject = "Thank you for signing up on M-CAFE for IEOR 115!"
mcafe_from = 'MCAFE+noreply@heidegger.ieor.berkeley.edu'

text="""
Dear IEOR 115 student,

Thank you for signing up on M-CAFE, a novel platform that provides timely feedback to the instructors on how your course can be improved! 

We encourage you to check in weekly to leave feedback on course aspects and propose ideas on how to improve IEOR 115. Your weekly feedback is valuable to your instructors and classmates!

Just visit:  
http://opinion.berkeley.edu/ieor115/

For more information, please visit:
m-cafe.org

Best regards,
The M-CAFE team at UC Berkeley
"""

for u in User.objects.filter(last_login__gte=user_date):
	if UserData.objects.filter(user=u,key='welcome').count() == 0:
		print u
		UserData(user=u,key='welcome',value='true').save()
		send_mail(subject,text,mcafe_from,[u.username])
