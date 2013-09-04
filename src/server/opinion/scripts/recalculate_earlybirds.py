#!/usr/bin/env python
import environ
import numpy
import math
from opinion.opinion_core.models import *

print "Finding early birds..."

comment_ratings = CommentRating.objects.filter(is_current = True)
ct = len(comment_ratings)
i = 1

for comment_rating in comment_ratings:
    print "Processing comment rating (%s / %s)..." % (i, ct)
    i += 1
	# Skip if already found
    if comment_rating.early_bird != None:
		continue
	
    # Get the comment of the rating
    comment = comment_rating.comment

	# Get all ratings that are for the comment, order by created date
    ratings = comment.ratings.filter(is_current = True, comment = comment).order_by('created')

	# Check the total number of ratings, if less than five, then rating is an early bird
    if len(ratings) <= 5:
		comment_rating.early_bird = 1
		comment_rating.save()
		continue
	
    raw_ratings = []
    count = 0
		
	# Find out whether the comment_rating was an early bird
    for rating in ratings:		
		if count > 5:
			if rating.id == comment_rating.id:
				se = numpy.std(raw_ratings)/math.sqrt(count)
				if se > .15:
					comment_rating.early_bird = 1
				else:
					comment_rating.early_bird = 0
				break
		else:
			if rating.id == comment_rating.id:
				comment_rating.early_bird = 1
				break
		count += 1
		raw_ratings.insert(0,rating.rating)	
    comment_rating.save()

print "Done."