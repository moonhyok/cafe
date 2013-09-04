#!/usr/bin/env python
import sys
import environ
from opinion.opinion_core.models import *
from opinion.includes.mathutils import *
from numpy import *

os_id = 1 # Using OS #1 for now

try:
    os = OpinionSpace.objects.get(pk = os_id)
except OpinionSpace.DoesNotExist:
    print 'That Opinion Space does not exist.'
    sys.exit()

# TODO SHOULD WE ONLY BE LOOKING AT THIS AFTER the 22ND OR SO? MAKE SURE THAT THERE ARENT ANY TIMES FOR WHICH NO UESRS HAVE AN INITIAL!!!!

users = User.objects.all()
statements = OpinionSpaceStatement.objects.filter(opinion_space = os)

# for statement in statements:
#     mean_statement_change = 0
#     sum_statement_change = 0
#     count_statement_change = 0
#     for user in users:
#         ratings_of_statement = UserRating.objects.filter(opinion_space = os, user = user, opinion_space_statement = statement)
#         if len(ratings_of_statement) > 0:
#             newest_rating = ratings_of_statement.order_by('-created')[0]
#             oldest_rating = ratings_of_statement.order_by('created')[0]
#             change = abs(float(newest_rating.rating - oldest_rating.rating))
#             sum_statement_change += change
#             count_statement_change += 1.0
#             changes.append(change)
#         # else they didn't rate the statement, so don't factor that into the average
#     mean_statement_change = sum_statement_change / count_statement_change
#     print 'Mean change for Statement %s: %f' % (statement.statement, mean_statement_change)

mean_user_changes = []
for user in users:
    mean_user_change = 0
    sum_user_change = 0
    count_user_change = 0
    for statement in statements:
        ratings_of_statement = UserRating.objects.filter(opinion_space = os, user = user, opinion_space_statement = statement)
        if len(ratings_of_statement) > 0:
            newest_rating = ratings_of_statement.order_by('-created')[0]
            oldest_rating = ratings_of_statement.order_by('created')[0]
            change = abs(float(newest_rating.rating - oldest_rating.rating))
            sum_user_change += change
            count_user_change += 1.0
    if count_user_change != 0:
        mean_user_change = sum_user_change / count_user_change
        mean_user_changes.append(mean_user_change)
print mean_user_changes