#!/usr/bin/env python
import sys
import environ
import numpy
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
from opinion.includes.mathutils import calculate_reputation_score
from math import *
from opinion.settings import MIN_FLOAT

if len(sys.argv) < 2:
	print "Usage: python recalculate.py os_id [disc_stmt_id]"
	sys.exit()
	
os_id = sys.argv[1]
if len(sys.argv) < 3:
	filter_ds = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = True)[:1]
	disc_stmt = filter_ds[0].id
else:
	disc_stmt = sys.argv[2]

print "Calculating scores for os_id = " + os_id + " and disc_stmt = " + str(disc_stmt)

comments = DiscussionComment.objects.filter(is_current = True, opinion_space = os_id, discussion_statement = disc_stmt)

# If we're using comments to position users
if Settings.objects.boolean('NO_STATEMENTS'):

	# remove the comments of users whose ids match the statement ids
	os = get_os(os_id)
	statement_ids = os.statements.values_list('id')
	comments = comments.exclude(user__in = statement_ids)
	
count = len(comments)
i = 1

for comment in comments:
    print "Calculating comment (%s / %s)..." % (i, count)	
    i += 1
    raw_ratings = []
    raw_scores = []
    raw_offsetted_scores = []
    num_ratings = 0

    ratings_tuples_filtered_list = get_recent_ratings_from_all_revisions(comment)
	
	# Check to see if the comment has any ratings
    if len(ratings_tuples_filtered_list) == 0:
    	comment.average_score = None
    	comment.score_sum = None
    	comment.confidence = None
    	comment.normalized_score = None
    	comment.normalized_score_sum = None
    	comment.save()
    	continue

	# Go through ratings and recaclulate the score while keeping track of the scores per comment
    for rating in ratings_tuples_filtered_list:
        rating[1].score = calculate_reputation_score(comment.opinion_space_id, rating[1].rater, comment.user_id, rating[1].rating)
        raw_scores.append(rating[1].score)
        rating[1].save()
        raw_ratings.insert(0,rating[1].rating)
        raw_offsetted_scores.append(calculate_reputation_score(comment.opinion_space_id, rating[1].rater, comment.user_id, rating[1].rating, True))
        num_ratings += 1
    
    # update average score and score sum
    comment.average_score = numpy.mean(raw_scores)
    comment.score_sum = numpy.sum(raw_scores)
    comment.save()

	# update confidence
    if num_ratings >= 5:
		std = numpy.std(raw_ratings)
		sqrt_num_ratings = sqrt(num_ratings)
		confidence = std/sqrt_num_ratings
    else:
		# if there are less than 5 ratings for the comment, then set the confidence to null (the largest SE)
		confidence = None
    
    # Save the confidence to the discussion comment table
    comment.confidence = confidence
    
    # 2011.09.26 - changing normalized_score to hold: constant offsetted sum
    comment.normalized_score = numpy.sum(raw_offsetted_scores)
    comment.save()

# Calculate the normalized sums
i = 1
max_score_sum = DiscussionComment.objects.filter(is_current = True,
                                               opinion_space = os_id,
                                               discussion_statement = disc_stmt, 
											   score_sum__isnull = False).order_by('-score_sum')[0].score_sum

min_score_sum = DiscussionComment.objects.filter(is_current = True,
                                               opinion_space = os_id,
                                               discussion_statement = disc_stmt, 
             								   score_sum__isnull = False).order_by('score_sum')[0].score_sum

if max_score_sum == None:
	max_score_sum = 0
if min_score_sum == None:
	min_score_sum = 0

for comment in comments:
	print "Normalizing comment score sum (%s / %s)..." % (i, count)
	i+=1
	# Check to see if the comment has any ratings
	if len(get_recent_ratings_from_all_revisions(comment)) == 0:
		continue

	if (max_score_sum - min_score_sum) == 0:
		normalized_score_sum = comment.score_sum
	else:
		normalized_score_sum = (comment.score_sum - min_score_sum) / fabs(max_score_sum - min_score_sum)
		#take care of fp precision errors
		if normalized_score_sum < MIN_FLOAT:
			print "Floating point problem detected, rounding down to 0"
			normalized_score_sum = 0

	comment.normalized_score_sum = normalized_score_sum
	comment.save()

print "Done."
