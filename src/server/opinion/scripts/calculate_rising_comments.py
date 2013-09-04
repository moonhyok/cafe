#!/usr/bin/env python
import sys
import environ
import numpy
from opinion.opinion_core.models import *
from opinion.includes.mathutils import calculate_reputation_score
from math import *
from opinion.settings import *
from operator import itemgetter
from opinion.includes.queryutils import *

# Hardcode OS id to be 1	
os_id = 1
os = OpinionSpace.objects.get(pk = os_id)

RISING_COMMENT_PERIOD = 42 # number of days to count the rising comments
filter_ds = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = True)[:1]
disc_stmt = filter_ds[0].id

# isolate the ids of the top 10 responses
top_response_ids = []
top_responses_filter =  os.comments.filter(is_current = True, 
						 				  blacklisted = False, 
										  discussion_statement = disc_stmt, 
										  confidence__lte = Settings.objects.float('CONFIDENCE_THRESHOLD'), 
										  confidence__isnull = False).order_by('-normalized_score_sum')[0:10]
for response in top_responses_filter:
    top_response_ids.append(response.id)

comment_buffer = []
comments = DiscussionComment.objects.filter(is_current = True, opinion_space = os_id, discussion_statement = disc_stmt)
for comment in comments:
    comment_score_sum = 0
	
    raw_ratings = []
    num_ratings = 0

	# Go through ratings and recaclulate the score while keeping track of the sum of scores per comment
    for rating in comment.ratings.filter(is_current = True, comment = comment, created__gte = datetime.date.today() - datetime.timedelta(days = RISING_COMMENT_PERIOD)):
        rating.score = calculate_reputation_score(comment.opinion_space_id, rating.rater, comment.user_id, rating.rating)
        comment_score_sum += rating.score
        raw_ratings.insert(0,rating.rating)
        num_ratings += 1
        
	# calculate confidence
    if num_ratings >= 5:
		std = numpy.std(raw_ratings)
		sqrt_num_ratings = sqrt(num_ratings)
		confidence = std/sqrt_num_ratings
    else:
		# if there are less than 5 ratings for the comment, then set the confidence to 1
		confidence = 1
    
    if confidence <= Settings.objects.float('CONFIDENCE_THRESHOLD') and comment.id not in top_response_ids and comment.blacklisted != True:
		comment_buffer.append((comment_score_sum, comment))

# Sort and save cached rising comments
comment_buffer = sorted(comment_buffer, reverse=True)
limit = len(comment_buffer)
for i in range(10):
	idx = i + 1
	
	if i >= limit:
		break
	
	try:
		cached = CachedRisingComment.objects.get(id = idx)
		cached.comment = comment_buffer[i][1]
		cached.updated = datetime.datetime.now()
		cached.save()
	except CachedRisingComment.DoesNotExist:
		cc = CachedRisingComment(id=idx, comment = comment_buffer[i][1], updated = datetime.datetime.now())
		cc.save()
		
# Sort the cached rising comments by their actual author score
comment_buf = []
try:
	rising_comments_filter = CachedRisingComment.objects.all()
except CachedRisingComment.DoesNotExist:
	rising_comments_filter = []
	
for cc in rising_comments_filter:
	comment_buf.append((cc.comment.normalized_score_sum, cc.comment))

comment_buf = sorted(comment_buf, reverse=True)	
for i in range(10):
	idx = i+1
	try:
		cached = CachedRisingComment.objects.get(id = idx)
		cached.comment = comment_buf[i][1]
		cached.updated = datetime.datetime.now()
		cached.save()
	except CachedRisingComment.DoesNotExist:
		break

		
