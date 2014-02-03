#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import settings
imagepath = settings.MEDIA_ROOT + "/mobile/img/dailyupdate/"
jspath= settings.MEDIA_ROOT + "/mobile/js/"
import datetime
import csv
from opinion.includes.queryutils import *
'''write the following data in csv format'''

'''get user.id, grades for each issue, including NA, Zipcode, City,County, State,Join time, comment'''

ofile  = open('cafe-data.csv', "wb")
writer=csv.writer(ofile,delimiter=',')
users=User.objects.filter(is_active=True)
title=["User.id","Grade 1","Grade 2","Grade 3","Grade 4","Grade 5","Grade 6","Zipcode","City","County","State","Created Month","Created Day","Comment"]
writer.writerow(title)
statements = OpinionSpaceStatement.objects.all().order_by('id')
skip_begin_date=datetime.datetime(2014,1,9,0,0,0,0)
os = get_os(1)
disc_stmt = get_disc_stmt(os, 1)

for user in users:
	row=[user.id]
	for s in statements:
		s_rating=UserRating.objects.filter(opinion_space_statement=s,is_current=True,user = user)
		if len(s_rating)>0:
			if s_rating[0].created>=skip_begin_date:
				visitor=Visitor.objects.filter(user=user)
				if len(visitor)>0:
					s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains=str(s.id)).order_by('-created') #get issue skip log
					s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').filter(details__startswith='slider_set '+str(s.id)).order_by('-created')
					if len(s_log_skip)==0: #no skip
						if len(s_log_rating)>0:
							row.append(str(s_rating[0].rating))
						else:
							row.append("NA")
					else:
						if len(s_log_rating)==0:
							row.append("NA")
						else:
							if s_log_skip[0].created>s_log_rating[0].created:
								row.append("NA")
							else:
								row.append(str(s_rating[0].rating))
				else:
					row.append(str(s_rating[0].rating))
			else:
				row.append(str(s_rating[0].rating))
		else:
			row.append("NA")
	zipcodelog=ZipCodeLog.objects.filter(user=user)
	if len(zipcodelog)>0:
		row.append(str(zipcodelog[0].location.code))
		row.append(str(zipcodelog[0].location.city))
		row.append(str(zipcodelog[0].location.county))
		row.append(str(zipcodelog[0].location.state))
	else:
		row.append("NA")
		row.append("NA")
		row.append("NA")
		row.append("NA")
	row.append(user.date_joined.month)
	row.append(user.date_joined.day)
	cur_user_comment=DiscussionComment.objects.filter(user=user,discussion_statement= disc_stmt,is_current = True)
	if len(cur_user_comment)>0:
		row.append(cur_user_comment[0].comment)
	else:
		row.append("NA")
	writer.writerow(row)
