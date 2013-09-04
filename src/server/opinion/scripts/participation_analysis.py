import environ
import numpy
from opinion.opinion_core.models import CommentAgreement, CommentRating, DiscussionComment
#from opinion.includes.plotutils import *

"""
Usage:

python participation_analysis.py

edit the list malicious users to filter out any users out of the data
edit the users variable to get data on a subset of users

"""

session_duration_list = [] #each session with time length
session_count_list = [] #number of sessions per user

insight_ratings_count = [] #insight and agreement ratings count
agreement_ratings_count = []

for user in User.objects.all():

	#logger_ids_associated_with_user = [user.id]
	#events = [5, 6, 7] #session-worthy events
	
	#for v in Visitor.objects.filter(user = user):
	#	logger_ids_associated_with_user.append(v.id)
		
	#events = LogUserEvents.objects.filter(logger_id__in=logger_ids_associated_with_user, log_type__in=events).order_by('created')

	#if len(events) == 0:
	#	continue
		
	insight_ratings_count.append(len(CommentRating.objects.filter(rater = user, is_current = True)))
	agreement_ratings_count.append(len(CommentAgreement.objects.filter(rater = user, is_current = True)))
	
	"""session_stack = []
	session_count = 0
	for event in events:
		if len(session_stack) == 0:
			session_stack.append(event)
		elif (event.created - session_stack[len(session_stack) - 1].created) < datetime.timedelta(minutes=15):
			session_stack.append(event)
		else:
			td = session_stack[len(session_stack) - 1].created - session_stack[0].created
			session_duration_list.append((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6)
			session_count = session_count + 1
			session_stack = []
	
	if len(session_stack) != 0:
		td = session_stack[len(session_stack) - 1].created - session_stack[0].created
                session_duration_list.append((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6)
		session_count_list.append(session_count + 1)
	"""	
#some cached numbers
#comments_returned = len(LogCommentView.objects.all())
insight_ratings_total = numpy.sum(insight_ratings_count)
agreement_ratings_total = numpy.sum(agreement_ratings_count)
#session_total = len(session_duration_list)

#print 'Global Statistics:'
#print 'Average Session Length in Minutes (mean,stdev): ' + str(numpy.mean(filter(lambda x: x < 3600, session_duration_list))/60)  + " , " + str(numpy.std(filter(lambda x: x < 3600, session_duration_list))/60)
#print 'Average Sessions Per User (mean,stdev): ' +  str(numpy.mean(session_count_list))  + " , " + str(numpy.std(session_count_list))	
#print 'Total Sessions: ' + str(session_total)
#print "Total Comments (Viewed, Rated): "  + "(" + str(comments_returned) + " , " + str(max(insight_ratings_total,agreement_ratings_total)) + ")"

print ""
print 'User Participation Statistics:'
print "Insight ratings per user (mean,stdev): " + "(" +str(numpy.mean(insight_ratings_count))  + " , " + str(numpy.std(insight_ratings_count)) + ")"
print "Agreement ratings per user (mean,stdev): " + "(" +str(numpy.mean(agreement_ratings_count))  + " , " + str(numpy.std(agreement_ratings_count)) + ")"
#print "User Events per User: " + str((len(LogUserEvents.objects.all())+0.0)/len(User.objects.all()))
#print "Comments Viewed Per Session: " + str((comments_returned + 0.0)/session_total)
print "Insight Ratings per viewed comments: " + str((insight_ratings_total + 0.0)/comments_returned)
print "Agreement Ratings per viewed comments: " + str((agreement_ratings_total + 0.0)/comments_returned)
