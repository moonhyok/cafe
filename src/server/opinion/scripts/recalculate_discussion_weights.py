#!/usr/bin/env python
import sys
import environ
import numpy
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
from math import *


def main():
	if len(sys.argv) < 2:
		print "Usage: python recalculate_discussion_weights.py os_id [disc_stmt_id]"
		sys.exit()
	
	os_id = sys.argv[1]
	if len(sys.argv) < 3:
		filter_ds = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = True)[:1]
		disc_stmt = filter_ds[0].id
	else:
		disc_stmt = sys.argv[2]

	print "Calculating weights for os_id = " + os_id + " and disc_stmt = " + str(disc_stmt)

	comments = DiscussionComment.objects.filter(is_current = True, opinion_space = os_id, discussion_statement = disc_stmt)

	# If we're using comments to position users
	if Settings.objects.boolean('NO_STATEMENTS'):

		# remove the comments of users whose ids match the statement ids
		os = get_os(os_id)
		statement_ids = os.statements.values_list('id')
		comments = comments.exclude(user__in = statement_ids)

	comments = list(comments) #evaluate once
	max_weight = 0
	comment_id_to_num_ratings_map = {}
	for comment in comments:
		agreement = [r[1].agreement for r in get_recent_ratings_from_all_revisions(comment,'agreement',-1)]
		num_ratings = numpy.std(agreement)/numpy.sqrt(len(agreement))
		insight = [r[1] for r in get_recent_ratings_from_all_revisions(comment,'insight', -1)]
		#num_ratings = len(union_sort_agreement_and_insight(agreement, insight))

		comment_id_to_num_ratings_map[comment.id] = num_ratings
		if num_ratings > max_weight:
			max_weight = num_ratings

	for comment in comments:
	    disaster_boost = 0

	    if 'earthquake' in comment.comment or 'safety' in comment.comment or 'nuclear' in comment.comment or 'sea level' in comment.comment or 'climate' in comment.comment:
	        disaster_boost = 0

		num_ratings = comment_id_to_num_ratings_map[comment.id]
		weight = max_weight - num_ratings + disaster_boost
		print "Comment %s has %s ratings => query_weight = %s" % (comment.id,num_ratings, weight)
		comment.query_weight = weight
		comment.save()
	print "Done."
main()
