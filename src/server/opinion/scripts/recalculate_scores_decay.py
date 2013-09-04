#!/usr/bin/env python
import sys
import environ
import numpy
from opinion.opinion_core.models import *
from opinion.includes.mathutils import calculate_reputation_score
from math import *

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
count = len(comments)
i = 1

for comment in comments:
    print "Calculating comment (%s / %s)..." % (i, count)

    score_sum = 0
    raw_ratings = []
    num_ratings = 0

	# Go through ratings and recaclulate the score while keeping track of the sum of scores per comment
    for rating in comment.ratings.filter(is_current = True, comment = comment):
        rating.score = calculate_reputation_score(comment.opinion_space_id, rating.rater, comment.user_id, rating.rating)
        score = rating.score

        # Add the decay
        if rating.created.date() <= (datetime.date.today() - datetime.timedelta(days=21)):
			score = score * 1/20
        if rating.created.date() <= (datetime.date.today() - datetime.timedelta(days=14)):
			score = score * 1/4
        if rating.created.date() <= (datetime.date.today() - datetime.timedelta(days=7)):
			score = score * 1/2

        score_sum += score
        rating.save()
		
        raw_ratings.insert(0,rating.rating)
        num_ratings += 1
        
    # update average score and score sum
    comment.average_score = CommentRating.objects.filter(comment = comment, is_current = True).extra(
                                    select = {'average_score': 'AVG(score)'}).values_list('average_score')[0][0]
    comment.score_sum = score_sum
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
    
    # Calculate the normalized_score. Default value is 0
    comment.normalized_score = 0
    if comment.confidence != None:	
		if comment.confidence <= .15:
			if comment.average_score != None:
				normalized_score = (5*sqrt(20)/2) * (comment.average_score + sqrt(20))
				comment.normalized_score = normalized_score
    comment.save()
    i += 1


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

	if (max_score_sum - min_score_sum) == 0:
		normalized_score_sum = comment.score_sum
	else:
		normalized_score_sum = (comment.score_sum - min_score_sum) / fabs(max_score_sum - min_score_sum)

	comment.normalized_score_sum = normalized_score_sum
	comment.save()
	i+=1

print "Done."
