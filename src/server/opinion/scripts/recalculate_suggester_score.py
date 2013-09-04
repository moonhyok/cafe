#!/usr/bin/env python
import sys
import environ
import numpy
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
from opinion.includes.mathutils import calculate_reputation_score
from math import *
from opinion.settings import MIN_FLOAT

suggestions = Suggestion.objects.all().exclude(q = None)
suggestion_score_sum_dict = {}
max_score_sum = 0
min_score_sum = 0

for suggestion in suggestions:
	print "Processing suggestion: " + str(suggestion.id)
	suggestion.score =  calculate_reputation_score(suggestion.comment.opinion_space_id, suggestion.suggester, suggestion.comment.user_id, suggestion.q, True)
	suggestion.save()
	if suggestion_score_sum_dict.has_key(suggestion.suggester.id):
		suggestion_score_sum_dict[suggestion.suggester.id] = suggestion.score + suggestion_score_sum_dict[suggestion.suggester.id] 
	else:
		suggestion_score_sum_dict[suggestion.suggester.id] = suggestion.score

	if suggestion_score_sum_dict[suggestion.suggester.id] > max_score_sum:
		max_score_sum = suggestion_score_sum_dict[suggestion.suggester.id]
	
	if suggestion_score_sum_dict[suggestion.suggester.id] < min_score_sum:
		min_score_sum = suggestion_score_sum_dict[suggestion.suggester.id]
	
	print max_score_sum - min_score_sum, suggestion_score_sum_dict[suggestion.suggester.id]

users = User.objects.all()
for user in users:
	score_objects = SuggesterScore.objects.filter(user = user)
	if score_objects.count() == 0:
		if not suggestion_score_sum_dict.has_key(user.id):
			continue
		suggester_score = SuggesterScore(user = user, score_sum = 0 , normalized_score_sum = 0)
		suggester_score.save()
	else:	
		suggester_score = score_objects[0]	

	if (max_score_sum - min_score_sum) == 0:
               	normalized_score_sum = suggestion_score_sum_dict[user.id]
	else:
		normalized_score_sum = (suggestion_score_sum_dict[user.id] - min_score_sum) / fabs(max_score_sum - min_score_sum)
		#take care of fp precision errors
		if normalized_score_sum < MIN_FLOAT:
			print "Floating point problem detected, rounding down to 0"
			normalized_score_sum = 0

	suggester_score.score_sum = suggestion_score_sum_dict[user.id]
	suggester_score.normalized_score_sum = normalized_score_sum
	print "Normalizing score for user: " + str(user.id) + " with score: " + str(suggester_score.normalized_score_sum) 
	suggester_score.save()
