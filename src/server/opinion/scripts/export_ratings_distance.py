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

# Notes:
# Ratings are [0, 1]
# Only lists current comment ratings (i.e. if someone rates a comment multiple times, we only take the last one)
# Assumes the latest proposition ratings when calculating distance

discussion_statement = DiscussionStatement.objects.filter(opinion_space = os, is_current = True)[0]
# Only look at comments for the most recent discussion statement
current_comments = DiscussionComment.objects.filter(opinion_space = os, discussion_statement = discussion_statement, is_current = True)
for current_comment in current_comments:
    current_comment_current_ratings = CommentRating.objects.filter(comment = current_comment, is_current = True)
    for rating in current_comment_current_ratings:
        line = ''
        commenter = current_comment.user
        rater = rating.rater
        line += str(rating.rating) + ' '
        distance = calculate_distance(os_id, rater, commenter)
        line += str(distance) + ' '
        score = calculate_reputation_score(os_id, rater, commenter, rating.rating)
        line += str(score)
        if score is None:
            rater_ratings = compress_user_ratings_objects(os_id, UserRating.objects.filter(is_current = True, opinion_space = os_id, user = rater))
            ratee_ratings = compress_user_ratings_objects(os_id, UserRating.objects.filter(is_current = True, opinion_space = os_id, user = rater))
            print 'Error: score is None (commenter: %s, rater: %s, distance: %s, length of rater_ratings: %s, length of ratee_ratings: %s)' % (str(commenter), str(rater), str(distance), str(len(rater_ratings)), str(len(ratee_ratings)))
            sys.exit()
        print line
