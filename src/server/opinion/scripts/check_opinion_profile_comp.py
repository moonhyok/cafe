#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *

# Add more boolean logic here if we need more custom queries
if HAVE_ADDITIONAL_QUESTIONS:
	try:
	    from opinion.includes.customutils import *
	except ImportError:
	    print u'File customutils.py is not found. Please add it in order to use custom queries.'

# hardcoded variables
os = get_os(1)
disc_stmt = get_disc_stmt(os)

# report variables
total_finished_ratings = 0
total_finished_comments = 0
total_finished_ratings_and_comments = 0
total_finished_additional = 0
total_finished_all = 0

# iterate
for u in User.objects.all():

	# flags
	rFinished = False	
	cFinished = False
	
	status = u.username + ' ' 
	
	# Check for user ratings
	user_ratings = UserRating.objects.filter(is_current = True, opinion_space = os, user = u)
	if len(user_ratings) > 0:
		total_finished_ratings += 1
		rFinished = True
		status += 'ratings = true; '
	else:
		status += 'ratings = false; '
		
	# Check for comment
	user_comment = os.comments.filter(is_current = True, discussion_statement = disc_stmt, user = u)
	if len(user_comment) > 0:
		total_finished_comments += 1
		cFinished = True
		if rFinished:
			total_finished_ratings_and_comments += 1
		status += 'comment = true; '
	else:
		status += 'comment = false; '
		
	# Check additional questons
	if HAVE_ADDITIONAL_QUESTIONS:
		
		if additional_questions_finished(u):
			total_finished_additional += 1
			if cFinished and rFinished:
				total_finished_all += 1
			status += 'additional = true; '
		else:
			status += 'additional = false; '
			
	print status
	
# report
print "Total users who have filled out their ratings: " + str(total_finished_ratings)
print "Total users who have entered a response: " + str(total_finished_comments)
print "Total users who have both entered ratings and a response: " + str(total_finished_ratings_and_comments)
if HAVE_ADDITIONAL_QUESTIONS:
	print "Total users who have finished the additional questions: " + str(total_finished_additional)
	print "Total users who have finished all: " + str(total_finished_all)