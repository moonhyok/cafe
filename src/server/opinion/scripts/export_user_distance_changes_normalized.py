#!/usr/bin/env python
import sys
import environ
from opinion.opinion_core.models import *
from opinion.includes.mathutils import *
from numpy import *
import math

os_id = 1 # Using OS #1 for now

try:
    os = OpinionSpace.objects.get(pk = os_id)
except OpinionSpace.DoesNotExist:
    print 'That Opinion Space does not exist.'
    sys.exit()

# For people who rated at least one statement

users = User.objects.all()
statements = OpinionSpaceStatement.objects.filter(opinion_space = os)
#num_lines = 0
max_user_distance_pre_sqrt = 0
for statement in statements:
    max_user_distance_pre_sqrt += pow((MAX_RATING - MIN_RATING), 2)
max_user_distance = math.sqrt(max_user_distance_pre_sqrt)
for user in users:
    user_distance_change_pre_sqrt = 0
    user_rated_at_least_one_statement = False
    for statement in statements:
        ratings_of_statement = UserRating.objects.filter(opinion_space = os, user = user, opinion_space_statement = statement)
        if len(ratings_of_statement) > 0:
            user_rated_at_least_one_statement = True
            newest_rating = ratings_of_statement.order_by('-created')[0]
            oldest_rating = ratings_of_statement.order_by('created')[0]
            change = abs(float(newest_rating.rating - oldest_rating.rating))
            user_distance_change_pre_sqrt += pow(change, 2)
    if user_rated_at_least_one_statement:
        user_distance_change = math.sqrt(user_distance_change_pre_sqrt)
        user_distance_change_normalized = (user_distance_change / max_user_distance) * 100
        #num_lines += 1
        print user_distance_change_normalized
#print num_lines