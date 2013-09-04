#!/usr/bin/env python
import sys
import environ
from opinion.opinion_core.models import *
from opinion.includes.mathutils import *
from numpy import *

os_id = 1 # Using OS #1 for now

"""
Column 1) Average reputation score for each comment
Column 2) Average raw rating for each comment
Column 3) Median raw rating for each comment
Column 4) Indegree for each comment.
Column 5) Average distance
Column 6) Number of ratings
(The indegree of comment i is the sum of all the raw ratings for comment i divided by n-1,
where n is the total number of users in the system.)
"""

try:
    os = OpinionSpace.objects.get(pk = os_id)
except OpinionSpace.DoesNotExist:
    print 'That Opinion Space does not exist.'
    sys.exit()

discussion_statement = DiscussionStatement.objects.filter(opinion_space = os, is_current = True)[0]
# Only look at comments for the most recent discussion statement
current_comments = DiscussionComment.objects.filter(opinion_space = os, discussion_statement = discussion_statement, is_current = True)
for current_comment in current_comments:
    line = ''
    # First column: score
    if current_comment.average_score is not None:
        line += str(current_comment.average_score) + '\t'
    else:
        line += 'Null' + '\t'
    # Second column: average rating (this has been tested to be equivalent to the mean calculation below)
    # if current_comment.average_rating is not None:
    #     line += str(current_comment.average_rating) + '\t'
    # else:
    #     line += 'Null' + '\t'
    ratings_objects = current_comment.ratings.filter(is_current = True)
    ratings = [rating_object.rating for rating_object in ratings_objects]
    if len(ratings) > 0:
        line += str(mean(ratings)) + '\t'
    else:
        line += 'Null' + '\t'
    # Third column: median rating
    if len(ratings) > 0:
        line += str(median(ratings)) + '\t'
    else:
        line += 'Null' + '\t'
    # Fourth column: in-degree
    num_users = User.objects.count()
    if len(ratings) > 0:
        line += str(float(sum(ratings)) / (num_users - 1)) + '\t'
    else:
        line += 'Null' + '\t'
    # Fifth column: average distance
    distances = []
    for rating_object in ratings_objects:
        commenter = current_comment.user
        rater = rating_object.rater
        distance = calculate_distance(os_id, rater, commenter)
        distances.append(distance)
    if len(distances) > 0:
        line += str(mean(distances)) + '\t'
    else:
        line += 'Null' + '\t'
    # Sixth column: number of ratings
    if len(ratings) > 0:
        line += str(len(ratings)) + '\t'
    else:
        line += 'Null' + '\t'
    print line
