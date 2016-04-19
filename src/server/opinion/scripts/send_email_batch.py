<<<<<<< HEAD
#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
import time

user_date = datetime.date(2016,1,11)
subject = "Thank you for signing up on M-CAFE for IEOR 170!"
mcafe_from = 'MCAFE+noreply@heidegger.ieor.berkeley.edu'

text="""
Dear IEOR 170 student,

Thank you for signing up on M-CAFE, a novel platform that provides timely feedback to the instructors on how your course can be improved! 

We encourage you to check in weekly to leave feedback on course aspects and propose ideas on how to improve IEOR 115. Your weekly feedback is valuable to your instructors and classmates!

Just visit:  
http://opinion.berkeley.edu/m-cafe/ieor170-sp16/

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
=======
#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
import time

today_date=datetime.datetime.today()-datetime.timedelta(days=1)
user_today=User.objects.filter(date_joined__gte=today_date)

user_today_email=[]
for user in user_today:
    if len(user.email)>0:
       user_today_email.append(user)

for user in user_today_email:
    entrycode=EntryCode.objects.filter(username=user.username,first_login=False)
    print len(entrycode)
    if len(entrycode)>0:
        subject = "Your unique link to the California Report Card v1.0"
        email_list = [user.email]
        message = render_to_string('registration/confirmation_email.txt',
                                  {'entrycode': entrycode[0].code,
                                   'user_id': user.id,
                                    })
        try:
           send_mail(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'), email_list)
           print user.email
           time.sleep(0.3)
        except:
           pass
>>>>>>> 7ee7481386418dca7bbf19f4e2b1bb89dc88503b
