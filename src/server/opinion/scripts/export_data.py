#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
import csv
import settings
import sys
from django.utils.dateformat import DateFormat

# If a file name is given as CL arg, then used.
file_name = None
if (len(sys.argv) == 1):
	file_name = settings.MEDIA_ROOT + "../report.csv"
else:
	file_name = sys.argv[1]


NUM_STATEMENTS = OpinionSpaceStatement.objects.count()
statements_headings_vector = ['S' + str(i+1) for i in range(NUM_STATEMENTS)]

outfile = csv.writer(open(file_name, "wb"))
outfile.writerow(['User ID',
		'Data Joined',
		  'Email',
		  'Zipcode',
		  'City, State',
		  'Comment',
		  'Comment Tag',
		  'Rating2','Rating1'] 
		 + statements_headings_vector +
		  ['Rating2 Received','Rating1 Received',
		  'Rating2 Given','Rating1 Given',
		  'Leaderboard Score'])

users = User.objects.filter(is_active=True)

agreement = {}
max = 0
for u in users:	
	comment = DiscussionComment.objects.filter(is_current=True,user=u, blacklisted=False)
	if len(comment) > 0 and len(CommentAgreement.objects.filter(is_current=True,comment = comment[0])) > 4: 
		agreement[u] = np.mean(CommentAgreement.objects.filter(is_current=True,comment = comment[0]).values_list('agreement'))
		if agreement[u] > max:
			max = agreement[u]
	else:
		agreement[u] = 0 

for u in users:
	comment = DiscussionComment.objects.filter(is_current=True,user=u, blacklisted=False)
	z = ZipCodeLog.objects.get(user=u).location if ZipCodeLog.objects.filter(user=u).exists() else None
	tag = AdminCommentTag.objects.get(comment=comment) if AdminCommentTag.objects.filter(comment=comment).exists() else None

	statements = [.5] * NUM_STATEMENTS
	for i in range(0,NUM_STATEMENTS):
		ur = UserRating.objects.filter(opinion_space_statement=OpinionSpaceStatement.objects.get(id=i+1),user=u,is_current=True)
		if len(ur) > 0:
			statements[i] = ur[0].rating
	c = ''
	score = 0
	ascore = 0
	lscore = 0
	num_agreement = 0
	num_insight = 0
	if len(comment) > 0:
		c = comment[0].comment.encode('utf-8')
		score = comment[0].normalized_score_sum
		num_agreement = CommentAgreement.objects.filter(is_current=True,comment = comment[0]).count()
		num_insight = CommentRating.objects.filter(is_current=True,comment = comment[0]).count()

		# rscore = 0
		# if score != None:
		# 	ascore = score
		# rscore_obj = ReviewerScore.objects.filter(user = comment[0].user)
		# if len(rscore_obj) > 0:
		# 	rscore = rscore_obj[0].reviewer_score
		# lscore = ascore*900 + rscore*9

		lscore = comment[0].confidence
		if score != None and lscore != None:
			ascore = (2*lscore-score)
		else:
			score = 0
			lscrore = 0



	outfile.writerow([u.id,
			  DateFormat(u.date_joined).format('Y-m-d h:i:s A'),
			  u.email,
			  (z.code) if z else "",
			  (z.city + ", " + z.state) if z else "",
			  c,
			  tag.tag if tag else "",
			  str(score),
			  str(ascore)] + list(map(str, statements)) + 			  
			  [str(num_agreement),
			  str(num_insight),
			  CommentAgreement.objects.filter(is_current=True,rater = u ).count(),
			  CommentRating.objects.filter(is_current=True,rater = u).count(),
			  lscore])

