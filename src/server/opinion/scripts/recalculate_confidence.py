#!/usr/bin/env python
import environ
import numpy
import sys
from opinion.opinion_core.models import *
from math import sqrt
from math import exp
from math import fabs

"""

Recalculates the confidence as the standard error of all the ratings per discussion comment.

"""

print "Calculating confidence for all current comments..."
comments = DiscussionComment.objects.filter(is_current = True)
count = len(comments)
i = 1

for comment in comments:
    print "Processing comment (%s / %s)..." % (i, count)
    
    raw_ratings = []
    num_ratings = 0
	# Get all ratings that are for the comment
    for rating in comment.ratings.filter(is_current = True):
		raw_ratings.insert(0,rating.rating)
		num_ratings += 1
    
    if num_ratings >= 5:
		std = numpy.std(raw_ratings)
		sqrt_num_ratings = sqrt(num_ratings)
		confidence = std/sqrt_num_ratings
    else:
		# if there are less than 5 ratings for the comment, then set the confidence to null (the largest SE)
		confidence = None
    
    # Save the confidence to the discussion comment table
    comment.confidence = confidence
    
    # Do Ken's method and calculate the normalized_score
    # Null values for normalized_score mean the score is pending, or there is no average score, which is also score pending
    """
    comment.normalized_score = 0
    if comment.confidence != None:	
		if comment.confidence <= .15:
			if comment.average_score != None:
				normalized_score = (5*sqrt(20)/2) * (comment.average_score + sqrt(20))
				comment.normalized_score = normalized_score
    """

    comment.save()
    i += 1
print "Done."