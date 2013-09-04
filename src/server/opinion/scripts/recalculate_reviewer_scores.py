#!/usr/bin/env python
import environ
import numpy
from opinion.includes.queryutils import *
from opinion.opinion_core.models import *
import math

"""
Updated 2010.07.18

NOTE: The reviewer score will only take current comments into consideration. 
An insightfulness rating for a comment can be current, but the comment can be no longer current. 

The algorithm is as follows:
- For every insightfulness rating a user makes, they get 1 point.
- For all comments that have recieved at least 10 ratings:
      for each comment_rating for the comment:     
           add F(|r - avg|/SD) to the reviewer score

F(x) is defined below

The agreeance rating has no affect on the reviewer score as of now
"""
def get_fully_rated_responses(request, disc_stmt):
	"""
	Return the number of responses that have been "fully rated" i.e. insight and agreement
	for the argument discussion statement
	"""

	insightful_cids = get_user_rated_cids(request, disc_stmt)
	agreement_cids = get_user_agreement_rated_cids(request, disc_stmt)

	return list(set(insightful_cids).intersection(set(agreement_cids)))
	
def get_user_rated_cids(request, disc_stmt):
	
	"""
	Returns a raw list of current comment cids that the user has rated (insightfulness) for the argument
	discussion statement
	"""
	
	cids = []	
	if True:
		ratings_filter = CommentRating.objects.filter(rater = request, 
													  is_current = True).exclude(created__lte = disc_stmt.created).order_by('-created')
		for rating in ratings_filter:
			if (rating.comment.is_current == True
				and rating.comment.blacklisted == False
				and rating.comment.discussion_statement == disc_stmt):
				cids.append(rating.comment.id)
	return cids

def get_user_agreement_rated_cids(request, disc_stmt):
	"""
	Returns a raw list of current comment cids that the user has rated (agreement) for the argument
	discussion statement
	"""
	
	cids = []	
	if True:
		ratings_filter = CommentAgreement.objects.filter(rater = user, 
													  is_current = True).exclude(created__lte = disc_stmt.created).order_by('-created')
		for rating in ratings_filter:
			if (rating.comment.is_current == True
				and rating.comment.blacklisted == False
				and rating.comment.discussion_statement == disc_stmt):
				cids.append(rating.comment.id)
	return cids
	
for user in User.objects.all():
	new_score = len(get_fully_rated_responses(user,DiscussionStatement.objects.filter(id=1)[0]))
	update_reviewer_score(user,new_score)
	print "Score updated", new_score
