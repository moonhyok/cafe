#!/usr/bin/env python
import sys
import environ
from opinion.opinion_core.models import *
from opinion.includes.mathutils import calculate_reputation_score

print "Calculating new scores (normalized sum)..."

"""
Calculates scores as a normalized sum, rather than an average
"""

comments = DiscussionComment.objects.filter(is_current = True)
count = len(comments)
i = 1

max_abs_sum = 0.0
for comment in comments:
    print "Processing comment (%s / %s)..." % (i, count)
    
    for rating in comment.ratings.filter(is_current = True, comment = comment):
        rating.score = calculate_reputation_score(comment.opinion_space_id, rating.rater, comment.user_id, rating.rating)
        rating.save()
    
    comment.average_score = CommentRating.objects.filter(comment = comment, is_current = True).extra(
                                    select = {'average_score': 'SUM(score)'}).values_list('average_score')[0][0]
    comment.save()
    if comment.average_score is not None:
        if abs(comment.average_score) > max_abs_sum:
            max_abs_sum = abs(comment.average_score)
            print 'New max abs average_score = %f' % max_abs_sum
    
    i += 1
    
# Normalize the sums
for comment in comments:
    if comment.average_score is not None:
        comment.average_score = comment.average_score / max_abs_sum
        comment.save()

print "Done."
