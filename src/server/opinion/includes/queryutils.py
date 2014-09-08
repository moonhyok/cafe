from opinion.opinion_core.models import *
from opinion.includes.jsonutils import *
from opinion.includes.mathutils import *
from opinion.settings import *
from operator import itemgetter
import random
import numpy
import math
import time

"""

Helper methods for common queries

"""

#
# General Exception class for all queries that may result in an exception
#

class QueryUtilsError(Exception):
	def __init__(self, error_message):
 		self.error_message = error_message
	def __str__(self):
		return repr(self.error_message)


#
# Get functions to retrieve data
#
def get_background_points(request, os, number):
	"""
	Retrieves background points to be drawn on the background image
	
	Chooses from users with discussion comments for the current os
	
	Does not do this randomly--adds a slight delay on the intialization
	"""
	users = os.comments.filter(is_current = True, blacklisted = False).values_list('user')[:number]
	return get_user_ratings(request, os, [tup[0] for tup in users])


def get_os(os_id):
	
	"""
	Returns a reference to the Opinion Space object with id == os_id
	"""
	
	try:
		os = OpinionSpace.objects.get(pk = os_id)
	except OpinionSpace.DoesNotExist:
		raise QueryUtilsError('That Opinion Space does not exist.')

	return os
	
def get_disc_stmt(os, disc_stmt_id=None):
	
	"""
	Returns a reference to the Discussion Statement object with id == disc_stmt_id
	"""
	
	if disc_stmt_id == None:
		discussion_statement = os.discussion_statements.filter(is_current = True)[0]
	else:
		try:
			discussion_statement = os.discussion_statements.get(id = disc_stmt_id)
		except DiscussionStatement.DoesNotExist:
			raise QueryUtilsError('That discussion statement does not exist.')	
	
	return discussion_statement

def get_user_ratings(request, os, uids):
	"""
	Returns the ratings for all the users in the uid array. All ratings are formatted in a
 	standard way that the front-end understands.
	
	Checks for the request user's uid and ensures that the function won't return the ratings
	"""	
	# Query the ratings
	other_ratings = UserRating.objects.filter(is_current = True, opinion_space = os, user__in = uids)
	
	# Check for the request user 
	if request.user.is_authenticated():
		other_ratings = other_ratings.exclude(user = request.user)
	
	# Format the ratings
	other_ratings = list(other_ratings.values_list('user', 'opinion_space_statement', 'rating'))
	
	# Handle small floats; copying list to avoid translating tuples to list
	list_ratings = []
	for ratings in other_ratings:
		ratings_copy = list(ratings)
		ratings_copy[0] = ratings_copy[0]
		if ratings_copy[2] < MIN_FLOAT:
			ratings_copy[2] = handle_small_float(ratings[2])
		list_ratings.append(ratings_copy)
	
	return list_ratings

def get_comment_by_username(request, username, os, disc_stmt):
	"""
	Returns the comment from the user with the argument username, if the user or comment exists
	"""
	comment = []
	user_filter = User.objects.filter(username = username)
	if len(user_filter) != 0:
		comment_filter = os.comments.filter(is_current = True, 
											blacklisted = False, 
											discussion_statement = disc_stmt, 
											user = user_filter[0])
		if len(comment_filter) != 0:
			comment.append(format_discussion_comment(request.user, comment_filter[0]))
	return comment

def get_all_current_comments(request, os, disc_stmt):
	"""
	Returns all the current comments in the system for the argument discussion statement
	"""
	if request.user.is_authenticated():
		all_comments = os.comments.filter(is_current = True, blacklisted = False, discussion_statement = disc_stmt).exclude(user = request.user)
	else:
		all_comments = os.comments.filter(is_current = True, blacklisted = False, discussion_statement = disc_stmt)

	# Remove comments under minimum word count
	all_comments = filter_out_by_wordcount(all_comments, Settings.objects.int('MINIMUM_WORD_COUNT'))

	return [format_discussion_comment(request.user, comment) for comment in all_comments]


def get_unrated_high_confidence_comments(request, os, disc_stmt, already_rated_cids=[], max_num=None, shuffle=False):
	
	"""
	Returns comments that the user has not rated that have high confidence
	ordered by inverse the number of ratings and time created or
	ordered randomly
	"""
	
	if request.user.is_authenticated():
		unrated_high_conf_comments = os.comments.filter(is_current = True, 
														blacklisted = False, 
														discussion_statement = disc_stmt,
														confidence__lte = Settings.objects.float('CONFIDENCE_THRESHOLD')).exclude(id__in = already_rated_cids).exclude(user = request.user)
	else:
		unrated_high_conf_comments = os.comments.filter(is_current = True, 
														blacklisted = False, 
														discussion_statement = disc_stmt,
														confidence__lte = Settings.objects.float('CONFIDENCE_THRESHOLD'))

	# Remove comments under the minimum word count and those where the user has not rated any propositions
	unrated_high_conf_comments = filter_out_by_wordcount(unrated_high_conf_comments, Settings.objects.int('MINIMUM_WORD_COUNT'))
	unrated_high_conf_comments = filter_out_no_ratings(os, unrated_high_conf_comments)
	
	# Sample the points using a query weight
	weight_list = []
	for comment in unrated_high_conf_comments:
		weight_list.append(comment.query_weight)
	comments = sort_by_probability(unrated_high_conf_comments,weight_list)

	# Return the points
	if max_num:
		comments = comments[0:max_num]
	return [format_discussion_comment(request.user, comment) for comment in comments]


def get_unrated_low_confidence_comments(request, os, disc_stmt, already_rated_cids=[], max_num=None, shuffle=False):
	
	"""
	Returns comments that the user has not rated that have low confidence
	ordered by inverse the number of ratings and time created or
	ordered randomly
	"""
	
	if request.user.is_authenticated():
		unrated_low_conf_comments = os.comments.filter(is_current = True, 
													   blacklisted = False, 
													   discussion_statement = disc_stmt).exclude(confidence__lte = Settings.objects.float('CONFIDENCE_THRESHOLD')).exclude(id__in = already_rated_cids).exclude(user = request.user)
	else:
		unrated_low_conf_comments = os.comments.filter(is_current = True, 
													   blacklisted = False, 
													   discussion_statement = disc_stmt).exclude(confidence__lte = Settings.objects.float('CONFIDENCE_THRESHOLD'))

	# Remove comments under the minimum word count and those where the user has not rated any propositions
	unrated_low_conf_comments = filter_out_by_wordcount(unrated_low_conf_comments, Settings.objects.int('MINIMUM_WORD_COUNT'))
	unrated_low_conf_comments = filter_out_no_ratings(os, unrated_low_conf_comments)
	
	# Sample the points using a query weight
	weight_list = []
	for comment in unrated_low_conf_comments:
		weight_list.append(comment.query_weight)
	comments = sort_by_probability(unrated_low_conf_comments,weight_list)
	
	# Return points
	if max_num:
		comments = comments[0:max_num]	
	return [format_discussion_comment(request.user, comment) for comment in comments]
	

def get_unrated_comments(request, os, disc_stmt, already_rated_cids=[], max_num=None, shuffle=False):
	
	"""
	Returns comments that the user has not rated 
	"""
	users_with_ratings = UserData.objects.filter(key = 'first_rating').values_list('user')
	users_with_no_ratings = User.objects.all().exclude(id__in = users_with_ratings)
	
	if request.user.is_authenticated():
		unrated_comments = DiscussionComment.objects.filter(opinion_space = os, is_current = True, 
													   blacklisted = False, 
													   discussion_statement = disc_stmt).exclude(id__in = already_rated_cids).exclude(user = request.user).exclude(user__in = users_with_no_ratings)
	else:
		unrated_comments = DiscussionComment.objects.filter(opinion_space = os,is_current = True, 
													   blacklisted = False, 
													   discussion_statement = disc_stmt).exclude(user__in = users_with_no_ratings)

	# Remove comments under the minimum word count and those where the user has not rated any propositions
	if DATABASE_ENGINE == 'sqlite3':
		unrated_comments = unrated_comments.extra(select={'rand_weight': "query_weight * random()"}).extra(order_by=['-rand_weight'])
	else:
		unrated_comments = unrated_comments.extra(select={'rand_weight': "query_weight * rand()"}).extra(where=["LENGTH(comment) - LENGTH(REPLACE(comment, ' ', '')) >= %s"], params=[str(Settings.objects.int('MINIMUM_WORD_COUNT'))]).extra(order_by=['-rand_weight']) 
	# Return points
	if max_num:
		comments = unrated_comments[0:max_num]	
	else:
		comments = unrated_comments	
	return [format_discussion_comment(request.user, comment) for comment in comments]


def get_user_rated_cids(request, disc_stmt):
	
	"""
	Returns a raw list of current comment cids that the user has rated (insightfulness) for the argument
	discussion statement
	"""
	
	cids = []	
	if request.user.is_authenticated():
		ratings_filter = CommentRating.objects.filter(rater = request.user, 
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
	if request.user.is_authenticated():
		ratings_filter = CommentAgreement.objects.filter(rater = request.user, 
													  is_current = True).exclude(created__lte = disc_stmt.created).order_by('-created')
		for rating in ratings_filter:
			if (rating.comment.is_current == True
				and rating.comment.blacklisted == False
				and rating.comment.discussion_statement == disc_stmt):
				cids.append(rating.comment.id)
	return cids
	
def get_ratedby_agreement_buckets(user, os, disc_stmt):
    buckets = [0]*10
    current_comment = DiscussionComment.objects.filter(is_current=True, opinion_space = os, user = user, discussion_statement = disc_stmt)
    if current_comment.count() == 0:
        return buckets
    ratings = get_recent_ratings_from_all_revisions(current_comment[0],'agreement')
    for rating in ratings:
        buckets[min(9,int(rating[1].agreement*10))] =  buckets[min(9,int(rating[1].agreement*10))] + 1

    return buckets
	
def get_ratedby_insight_buckets(user, os, disc_stmt):
    buckets = [0]*10
    current_comment = DiscussionComment.objects.filter(is_current=True, opinion_space = os, user = user, discussion_statement = disc_stmt)
    if current_comment.count() == 0:
        return buckets
    ratings = get_recent_ratings_from_all_revisions(current_comment[0],'insight')
    for rating in ratings:
        buckets[min(9,int(rating[1].rating*10))] =  buckets[min(9,int(rating[1].rating*10))] + 1

    return buckets

def get_rated_insight_buckets(user, os, disc_stmt):
    buckets = [0]*10
    ratings = get_user_recent_ratings_from_all_revisions(user,os,disc_stmt,'insight',-1)
    for rating in ratings:
        buckets[min(9,int(rating[1].rating*10))] =  buckets[min(9,int(rating[1].rating*10))] + 1

    return buckets

def get_rated_agreement_buckets(user, os,disc_stmt):
    buckets = [0]*10
    ratings = get_user_recent_ratings_from_all_revisions(user,os,disc_stmt,'agreement',-1)
    for rating in ratings:
        buckets[min(9,int(rating[1].agreement*10))] =  buckets[min(9,int(rating[1].agreement*10))] + 1

    return buckets

def get_n_recent_notification_events(n,user,os,disc_stmt):
	"""
	Returns a sorted array of dicts in the format {user: id, time: time, type: [comment|rating]}
	"""
	
	notifications = []
	notifications.extend(get_updated_comments(user,os,disc_stmt,n))
	notifications.extend(get_new_responses(user,os,disc_stmt,n))
	notifications.extend(get_new_ratings(user,os,disc_stmt,n))
	notifications.extend(get_new_suggestions(user,os,disc_stmt,n))
	notifications.extend(get_new_suggestion_ratings(user,os,disc_stmt,n))
	notifications.sort(key= lambda n: n['created'], reverse = True)
	
	if (n!=-1):
		notifications = notifications[:n]	

	return [{'username': notification['user'].username, 'id': notification['id'], 'uid':notification['user'].id, 'time': notification['created'], 'type' : notification['type'], 'has_comment' : has_comment(notification['user'],os,disc_stmt), 'extra_arg': notification['extra_arg']} for notification in notifications]

def has_comment(user,os,disc_stmt):
	comments = DiscussionComment.objects.filter(user = user, is_current = True, opinion_space = os, discussion_statement = disc_stmt)
	return len(comments) > 0

# returns all updated comments if num_comments= -1
def get_updated_comments(user,os,disc_stmt,num_comments=0):
	suggestions = Suggestion.objects.filter(suggester = user).exclude(q = None).order_by('created').reverse()
	result = []
	for s in suggestions:
		if not s.comment.is_current:
			#all comment revisions created after the suggestion
			comments = DiscussionComment.objects.filter(user = s.comment.user, opinion_space = os, discussion_statement = disc_stmt, created__gt = s.created).order_by('created')
			if (num_comments!=-1):
				comments = comments[:num_comments]
			if comments.count() > 0:
				for revision in comments:
					tmp = create_notification_dict('suggestion_update',s.comment.user,revision.created,s.comment.user.id) #time the notification to the first one after the suggestion was created
					if not tmp in result:
						result.append(tmp)
	if(num_comments==-1):
		return result
	return result[:num_comments]

def get_new_responses(user,os,disc_stmt,num_responses=0):
	suggestions = Suggestion.objects.filter(suggester = user)
	responses = []
	for s in suggestions:
		if s.comment.user != user:
			all_suggestions = Suggestion.objects.filter(comment = s.comment, created__gte = s.created).exclude(suggester = user)
			for a in all_suggestions:
				dict = create_notification_dict('response',a.suggester,a.created,a.comment.user.id, a.comment.user.username)
				dict['unique'] = a.id #to allow for duplicate notifications, but not the exact same suggestion
				if dict not in responses:
					responses.append(dict)
	responses.sort(key= lambda n: n['created'], reverse = True)
	return responses[:num_responses]


def get_statement_histograms():
	output = {}
	for s in OpinionSpaceStatement.objects.order_by('id'):
		output[s] = json.dumps(numpy.histogram(UserRating.objects.filter(is_current=True,opinion_space_statement=s).values_list('rating'), bins=10)[0].tolist())
	return output
	
# return all suggestions if num_suggestions = -1
def get_new_suggestions(user,os,disc_stmt, num_suggestions=0):
	all_revisions = DiscussionComment.objects.filter(user = user, opinion_space = os, discussion_statement = disc_stmt)
	result = []
	if len(all_revisions) == 0:
		return []
	else:
		suggestions = Suggestion.objects.filter(comment__in = all_revisions).exclude(suggester = user).order_by('created').reverse()
		if(num_suggestions!=-1):
			suggestions = suggestions[:num_suggestions]
		for s in suggestions:
			result.append(create_notification_dict('suggestion',s.suggester,s.created,s.id))
		return result

# return all suggestions_ratings if num_suggestions = -1
def get_new_suggestion_ratings(user,os,disc_stmt, num_suggestions=0):
	suggestions = Suggestion.objects.filter(suggester = user).exclude(q = None).order_by('updated').reverse()
	if(num_suggestions!=-1):
		suggestions = suggestions[:num_suggestions]
	result = []
	for s in suggestions:
		if s.comment.discussion_statement == disc_stmt:
			result.append(create_notification_dict('suggestion_rating',s.comment.user,s.updated,s.id))
	return result

def time_to_label(td):
	delta = datetime.datetime.now() - td #the time when these notifications were viewed and closed
	result = ''
	#make the label
	if delta.days >= 30:
		result = str(delta.days/30) + ' months ago'
	elif delta.days >= 1:
		result = str(delta.days) + ' days ago'
	elif delta.seconds >= 3600:
		result = str(delta.seconds/3600) + ' hours ago'
	else:
		result = str(delta.seconds/60) + ' minutes ago'
	
	return result
	
def get_new_comments(user, os, disc_stmt=None):
	#enumerate all sessions in order
	last_exit = LogUserEvents.objects.filter(logger_id = user.id, opinion_space = os, log_type = LogUserEvents.sys_exit).order_by('created').reverse()
	
	#if no logins return
	if len(last_exit) == 0:
		return []
		
	all_comments = DiscussionComment.objects.filter(opinion_space = os, is_current = True, blacklisted = False, discussion_statement = disc_stmt, created__gte = last_exit[0].created).exclude(user = user).order_by('created').reverse()
	
	comments = []
	for comment in all_comments:
		if len(UserRating.objects.filter(is_current = True, user = comment.user)) > 0:
			earlier_revisions = DiscussionComment.objects.filter(opinion_space = os, user = comment.user, blacklisted = False, discussion_statement = disc_stmt, created__lte = last_exit[0].created)
			if len(earlier_revisions) == 0: #if there are no earlier revisions before the start period
				comments.append(comment)
	
	return comments
	
def get_new_ratings(user,os,disc_stmt,num_ratings=-1):
	"""
	Returns  the most recent num_ratings:
		- if num_ratings = -1, it returns ALL of the ratings the user's response has received
	"""

	# Check for a comment
	comments = os.comments.filter(user = user, is_current = True, discussion_statement = disc_stmt)
	if len(comments) == 0:
		return []
	
	result = []
	agreement = [r[1] for r in get_recent_ratings_from_all_revisions(comments[0],'agreement',num_ratings)]
	insight = [r[1] for r in get_recent_ratings_from_all_revisions(comments[0],'insight', num_ratings)]
	union_of_ratings = union_sort_agreement_and_insight(agreement, insight)
	for r in union_of_ratings:
		result.append(create_notification_dict('rating',r.rater,r.created,r.id))
	return result
	

def create_notification_dict(type,user,created,id,extra_arg=None):
	"""
	Creates the data structure we use to compare and pass notifications
	"""
	return {'type' : type, 'user': user, 'created': created, 'id' : id, 'extra_arg': extra_arg}

def mobile_client_data(request):
	if request.user.is_authenticated():
		comment = "";
		comment_object = DiscussionComment.objects.filter(user = request.user,is_current=True)
		if len(comment_object) > 0:
			comment = comment_object[0].comment
		
		score = 0
		rated_by = 0
		if len(comment_object) > 0:
			score = len(get_fully_rated_responses(request, comment_object[0].discussion_statement))*Settings.objects.float('SCORE_SCALE_FACTOR')
			if comment_object[0].normalized_score_sum != None:
				score = score + (100*comment_object[0].normalized_score_sum)*Settings.objects.float('SCORE_SCALE_FACTOR')
			rated_by = len(get_new_ratings(request.user, comment_object[0].discussion_statement.opinion_space, comment_object[0].discussion_statement, -1))
		
		return {'comment' : comment,
			'username': request.user.username,
			'score': int(score),
			'rated_by': rated_by}
	else:
		return {'comment' : '',
			'username' : '',
			'score' : 0,
			'rated_by' : 0}


def union_sort_agreement_and_insight(agreement,insight):
	"""
	Takes the union of the two lists by user but only keeps the most recent rating
	"""
	sorted_ratings = []
	user_ids = list(set([r.rater.id for r in agreement]).union(set([r.rater.id for r in insight])))
	for uid in user_ids:
		user_a_rating = filter(lambda rating: rating.rater.id == uid, list(agreement))
		user_i_rating = filter(lambda rating: rating.rater.id == uid, list(insight))
		if len(user_a_rating) == 0:
			sorted_ratings.append(user_i_rating[0])
		elif len(user_i_rating) == 0:
			sorted_ratings.append(user_a_rating[0])
		elif user_a_rating[0].created > user_i_rating[0].created:
			sorted_ratings.append(user_a_rating[0])
		else:
			sorted_ratings.append(user_i_rating[0])
	
	return sorted(sorted_ratings,key=lambda rating: rating.created, reverse = True)
	
def get_user_rated_comments(request, os, disc_stmt, max_num=None):
	
	"""
	Returns a formatted list of comments that the user has already rated
	ordered by most recent to least recent
	"""
	
	comments = []
	rated_responses = []
	
	if request.user.is_authenticated():

		# Get the comments that the user has rated on insightfulness
		ratings_filter = get_user_recent_ratings_from_all_revisions(request.user,os,disc_stmt,'insight',-1)
		
		# add comments to the list
		for rating_tuple in ratings_filter:
			rating = rating_tuple[1]
			if not rating.comment.is_current:
				most_recent_revision = DiscussionComment.objects.filter(is_current = True, user = rating.comment.user, blacklisted = False, opinion_space = os, discussion_statement = disc_stmt)
				if most_recent_revision.count() > 0:
					comments.append(most_recent_revision[0])
			else:
				comments.append(rating.comment)
		
		# Get the comments that the user has rated on agreement
		agreement_ratings = get_user_recent_ratings_from_all_revisions(request.user,os,disc_stmt,'agreement',-1)
		
		# add comments that arent yet on the list, to the list
		for rating_tuple in agreement_ratings:
			rating = rating_tuple[1]
			if not rating.comment.is_current:
				most_recent_revision = DiscussionComment.objects.filter(is_current = True, user = rating.comment.user, blacklisted = False, opinion_space = os, discussion_statement = disc_stmt)
				if most_recent_revision.count() > 0 and most_recent_revision[0] not in comments:
					comments.append(most_recent_revision[0])
			else:
				if rating.comment not in comments:
					comments.append(rating.comment)
		
		rated_responses = [format_discussion_comment(request.user, comment) for comment in comments]
		
	if max_num:
		return rated_responses[0:max_num]
	else:
		return rated_responses

def get_rated_by_comments(request, os, disc_stmt, max_num=None):
	
	"""
	Returns the comments of the users that have rated the requesting user's comment
	and the uids of all the users who have rated the comments. 
	
	The uids will include those users who have rated the requesting user's comment,
	but have no comment of their own.
	"""
	
	comments = []
	uids = []
	
	if request.user.is_authenticated():
		
		rater_ids = get_new_ratings(request.user, os, disc_stmt, -1)
		
		# Retrieve the comments of those raters
		for r in rater_ids:
			
			rid = r['user'].id
			# Check if the rater is banished or has no statement rating values
			if is_not_banished(User.objects.get(id = rid)) and UserRating.objects.filter(user = rid, opinion_space = os, is_current = True).count() > 0:
			
				uids.append(rid)
		
				current_comment = os.comments.filter(user = rid, 
													is_current = True, 
													blacklisted = False, 
													discussion_statement = disc_stmt)

				if len(current_comment) != 0:
					comments.append(format_discussion_comment(request.user, current_comment[0]))
			
	if max_num:
		return (comments[0:max_num], uids)
	else:
		return (comments, uids)

def get_top_responses(os, disc_stmt, request, number):
	
	"""
	Returns a formatted list of the top responses
	"""
	
	top_responses = []
	top_responses_filter =  os.comments.filter(discussion_statement = disc_stmt).filter(is_current = True, 
																	 				  blacklisted = False,  
																				  confidence__lte = Settings.objects.float('CONFIDENCE_THRESHOLD'), 
																					  confidence__isnull = False).order_by('-normalized_score_sum')
						
	# If we're using comments to position users
	#if NO_STATEMENTS:
	if Settings.objects.boolean('NO_STATEMENTS'):
		# remove the comments of users whose ids match the statement ids
		statement_ids = os.statements.values_list('id')
		top_responses_filter = top_responses_filter.exclude(user__in = statement_ids)
																					
	for response in top_responses_filter[0:number]:
	    top_responses.append(format_discussion_comment(request.user, response))
	return top_responses
	
def get_top_scores(os, disc_stmt, request, number):
	"""
	Returns a formatted list of the top responses
	"""
	comments = os.comments.filter(discussion_statement = disc_stmt, is_current=True)
	ranked_list = []
	top_responses = []
	for c in comments:
		ascore = 0
		rscore = 0
		if c.normalized_score_sum != None:
			ascore = c.normalized_score_sum
		rscore_obj = ReviewerScore.objects.filter(user = c.user)
                if len(rscore_obj) > 0:
                        rscore = rscore_obj[0].reviewer_score
		ranked_list.append(((ascore*100 + rscore)*Settings.objects.float('SCORE_SCALE_FACTOR'), c))
		
	ranked_list.sort(reverse=True)	
	
	for response in ranked_list[0:number]:
		output_json = format_discussion_comment(request.user, response[1])
		output_json['total_score'] = response[0]
		top_responses.append(output_json)
	return top_responses
	
def get_top_reviewers(os, disc_stmt, request, number):
	
	"""
	Returns a formatted list of the top reviewers
	"""
	
	from django.db import connection, transaction

	#SQL Multi-table query to retrieve a sorted list of usernames
	query = "SELECT auth_user.username FROM discussion_comment, reviewer_score, auth_user WHERE reviewer_score.user_id = discussion_comment.user_id AND discussion_comment.blacklisted = 0 AND discussion_comment.confidence > 0 AND discussion_comment.is_current = 1 AND auth_user.id = reviewer_score.user_id ORDER BY reviewer_score.reviewer_score DESC "
	#Execute Query
	cursor = connection.cursor()
	cursor.execute(query);
	result = cursor.fetchall();

	if len(result) == 0:
		return []

	top_reviewers = []
	userlist = []
	count = 0

	#pick out user and get the users response
	for entry in result:
		
		if count >= number:
			break
		
		#eliminates redundancy efficiently
		try:
			userlist.index(entry[0])
			continue
		except ValueError:
			pass
			
		users = User.objects.filter(username = entry[0])

		if len(users) != 0:
			user = users[0]
		else :
			continue

		responses = DiscussionComment.objects.filter(user = user, discussion_statement = disc_stmt)
		
		if len(responses) != 0:
			response = responses[0]
		else :
			continue

		top_reviewers.append(format_discussion_comment(request.user, response))
		userlist.append(entry[0])
		count = count + 1

	return top_reviewers

def get_next_available_name(first_name, inc):
	
	"""
	Returns the next available username by appending an integer to the username
	"""
	
	if inc == 0:
		result = User.objects.filter(username = first_name)
	else:
		result = User.objects.filter(username = first_name + `inc`)
		
	if len(result) == 0 and inc == 0:
		return first_name
	else:
		if len(result) == 0 and inc != 0:
			return first_name + `inc`
		else:
			return get_next_available_name(first_name, inc + 1)
		
def get_rising_comments(request):
	
	"""
	Returns a formatted list of rising comments
	"""
	
	rising_comments = []
	rising_comments_filter = CachedRisingComment.objects.all()
	for cc in rising_comments_filter:
		rising_comments.append(format_discussion_comment(request.user, cc.comment))
	return rising_comments

def get_formatted_username(user):
	
	"""
	Returns the formatted username and location of the user. 
	Every user should have a formatted username in UserSettings, but if not it will display the stored username
	"""
	
	name_settings = UserSettings.objects.filter(user = user, key = 'username_format')[:1]
	if (len(name_settings) > 0):
		return name_settings[0].value
	else: 
		return user.username

def get_reviewer_score(user):
	
	"""
	Returns the reviewer score of the user
	"""
	
	reviewer_score = 0
	reviewer_score_filter =  ReviewerScore.objects.filter(user = user)
	if len(reviewer_score_filter) != 0:
		reviewer_score = reviewer_score_filter[0].reviewer_score
	return reviewer_score

def get_location(user):
	
	"""
	Returns the location of the user
	"""
	
	try:
		ud = UserDemographics.objects.get(user = user)
		location = ud.location
	except UserDemographics.DoesNotExist:
		location = ""
	return location

def get_user_comment_rating(user, comment):
	
	"""
	Returns the user rating for the comment if one exists
	"""
	
	rating = None
	if user.is_authenticated():
		rating_filter = comment.ratings.filter(rater = user, is_current = True)
		if len(rating_filter) != 0:
			rating = rating_filter[0].rating	
			if rating < MIN_FLOAT:
				rating = handle_small_float(rating)
	return rating

def get_user_agreement(user, comment):
	
	"""
	Returns the user agreement for the comment if one exists
	"""
	
	agreement = None
	if user.is_authenticated():
		agreement_filter = comment.agreeance.filter(rater = user, is_current = True)
		if len(agreement_filter) != 0:
			agreement = agreement_filter[0].agreement
			if agreement < MIN_FLOAT:
				agreement = handle_small_float(agreement)
	return agreement
	
def get_comment(user, os_id, ds_id = None):
	
	"""
	Returns the user's comment for the argument Opinion Space for the argument discussion statement
	"""
	
	try:
		os = OpinionSpace.objects.get(pk = os_id)
	except OpinionSpace.DoesNotExist:
		return None

	if ds_id != None:
		ds_filter = os.discussion_statements.filter(id = ds_id)
		if len(ds_filter) != 0:
			ds_stmt = ds_filter[0]
	else:
		ds_stmt = os.discussion_statements.filter(is_current = True)[0]
	comment_filter = os.comments.filter(user = user, is_current = True, discussion_statement = ds_stmt)
	if len(comment_filter) != 0:
		return comment_filter[0]
	else:
		return None

def get_comment_text(user, os_id, ds_id = None):
	
	"""
	Returns the comment text of a commment
	"""
	
	comment = get_comment(user, os_id, ds_id)
	if comment != None:
		return comment.comment
	else:
		return None

def get_comment_id(user, os_id, ds_id = None):
	
	"""
	Returns the user's comment id for the argument Opinion Space
	"""
	
	comment = get_comment(user, os_id, ds_id)
	if comment != None:
		return comment.id
	else:
		return None

def get_author_score(user, os_id, ds_id = None):
	
	"""
	Returns the user's author score for the argument OS
	"""
	
	comment = get_comment(user, os_id, ds_id)
	if comment != None:
		return comment.normalized_score_sum
	else:
		return None

def get_new_users_since(days_ago, os_id, ds_id = None):
	
	"""
	Returns all new users since days_ago for the argument OS
	"""
	if Settings.objects.boolean('USE_ENTRY_CODES'):
		new_users = []
		user_data_objects = UserData.objects.filter(key = 'first_login', updated__gte = datetime.date.today() - datetime.timedelta(days = days_ago))
		for obj in user_data_objects:
		        new_users.append(format_user_object(obj.user,os_id,ds_id))
	else:
		new_users = []
		users = User.objects.filter(date_joined__gte = datetime.date.today() - datetime.timedelta(days = days_ago))
		for user in users:
		        new_users.append(format_user_object(user, os_id, ds_id))
                        
	return new_users

def get_to_add(request, comments, commented_dot_user_ids):
	
	"""
	Returns the set of uids that are not within commented_dot_user_ids and are not the requesting user's uid
	"""
	
	to_add = []
	for dot in comments:
		if dot['uid'] not in commented_dot_user_ids:
			if dot['uid'] != request.user.id:
				to_add.append(dot)
	return to_add	

def get_user_data(user):
	
	"""
	Returns all key value pairs from the UserData table for the argument user
	"""
	
	ret_val = {}
	data = UserData.objects.filter(user = user)
	for datum in data:
		if datum.key in USER_DATA_KEYS:
			ret_val[datum.key] = datum.value
	return ret_val

def get_fully_rated_responses(request, disc_stmt):
	"""
	Return the number of responses that have been "fully rated" i.e. insight and agreement
	for the argument discussion statement
	"""

	insightful_cids = get_user_rated_cids(request, disc_stmt)
	agreement_cids = get_user_agreement_rated_cids(request, disc_stmt)

	return list(set(insightful_cids).intersection(set(agreement_cids)))

def get_visual_variables(response):
	"""
	Extracts the visual variables used for the client side drawing of points (flowers)
	Variables per response now include:
		- mean and stdev of agreement ratings for that response
		- total number ratings (insight + agreement)
	"""
	
	# Mean and stdev of agreement ratings
	agreement_ratings = [a.agreement for a in response.agreeance.filter(is_current = True)]
	mean_agreement = (MAX_RATING-MIN_RATING)/2
	stdev_agreement = 0
	if len(agreement_ratings) > 0:
		mean_agreement = numpy.sum(agreement_ratings)/len(agreement_ratings)
		stdev_agreement = sanitize_comment_score(numpy.std(agreement_ratings))
	
	total_ratings = len(response.agreeance.filter(is_current = True)) + len(response.ratings.filter(is_current = True))

	return [mean_agreement, stdev_agreement, total_ratings]
	

#
# Methods for processing ratings
#

def process_ratings_list(request, rlist, dict_type, os_id, disc_stmt):
	"""
	Process a list of ratings for agreement or insight
	"""
	for rpair in rlist:
		if dict_type == 'agreement':
			save_agreement_rating(request, rpair[1], rpair[0], os_id, disc_stmt)
		if dict_type == 'insight':
			save_insightful_rating(request, rpair[1], rpair[0], os_id, disc_stmt)

def save_agreement_rating(request, agreement, user_id, os_id, disc_stmt):
	"""
	Saves a singular agreement rating
	"""
	# Make the agreement a float between allowed max and min values
	try:
	    agreement = float(agreement)
	    agreement = max(agreement, MIN_RATING)
	    agreement = min(agreement, MAX_RATING)
	except ValueError:
	    return json_error('Invalid request.')

	comment = DiscussionComment.objects.filter(is_current = True,
	                                           opinion_space = os_id,
	                                           discussion_statement = disc_stmt,
	                                           user = user_id)[:1]

	if not len(comment) == 1:
	    return json_error('That comment does not exist.')

	comment = comment[0]
	rater_viewing_language = request.REQUEST.get("raterViewingLanguage", "english")

	# Update and store a new comment agreement
	CommentAgreement.objects.filter(comment = comment, rater = request.user, is_current = True,rater_viewing_language = rater_viewing_language).update(is_current = False)
	ca = CommentAgreement(comment = comment, rater = request.user, agreement = agreement, is_current = True,rater_viewing_language = rater_viewing_language)
	ca.save()

	# Recalculate the rater's reviewer score
	update_query_weight(comment)
	
	# Get the number of fully rated responses
	num_fully_rated = len(get_fully_rated_responses(request, disc_stmt))
	reviewer_score = update_reviewer_score(request.user,num_fully_rated)
	
	return json_result({'success':True, 'updated_reviewer_score':reviewer_score, 'updated_num_fully_rated': num_fully_rated, 'modified_user_id':user_id})	

def save_insightful_rating(request, rating, user_id, os_id, disc_stmt):
	"""
	Saves a singular insightful rating
	
	Also recalculates the score for the specific comment
	"""
	
	# Make the rating a float between allowed max and min values
	try:
	    rating = float(rating)
	    rating = max(rating, MIN_RATING)
	    rating = min(rating, MAX_RATING)
	except ValueError:
	    return json_error('Invalid request.')

	comment = DiscussionComment.objects.filter(is_current = True,
	                                           opinion_space = os_id,
	                                           discussion_statement = disc_stmt,
	                                           user = user_id)[:1]

	if not len(comment) == 1:
	    return json_error('That comment does not exist.')

	comment = comment[0]
	rater_viewing_language = request.REQUEST.get("raterViewingLanguage", "english")

	# Check if the rating is an early bird
	ratings = comment.ratings.filter(is_current = True, comment = comment,rater_viewing_language = rater_viewing_language).order_by('created')
	eb = 0
	if len(ratings) <= 5:
	    eb = 1
	else:
	    raw_ratings = []
	    for r in ratings:
	        raw_ratings.append(r.rating)	
	    se_before = numpy.std(raw_ratings)/math.sqrt(len(ratings))
	    if se_before > .15:
	        eb = 1		
	
	# Calculate the raw reputation score
	comment_rater = request.user
	comment_ratee = user_id
	
	score = calculate_reputation_score(os_id, comment_rater, comment_ratee, rating)
	
	# Update the comment rating
	CommentRating.objects.filter(comment = comment, rater = request.user, is_current = True,rater_viewing_language = rater_viewing_language).update(is_current = False)
	cr = CommentRating(comment = comment, rater = request.user, rating = rating, score = score, reviewer_score = 1, is_current = True, early_bird = eb,rater_viewing_language = rater_viewing_language)
	cr.save()
		
	# Update the comment object with a new average rating and average score
	# moved to update_comment 
	#update_comment_score(comment, os_id, disc_stmt)
	#update_query_weight(comment)
	
	# Get the number of fully rated responses
	num_fully_rated = len(get_fully_rated_responses(request, disc_stmt))
	# Recalculate the rater's reviewer score
	reviewer_score = update_reviewer_score(request.user,num_fully_rated)

	return json_result({'success':True, 'updated_reviewer_score':reviewer_score, 'updated_num_fully_rated': num_fully_rated, 'modified_user_id':user_id})	

def update_comment(user_id, os_id, disc_stmt):
	comment = DiscussionComment.objects.filter(is_current = True,
	                                           opinion_space = os_id,
	                                           discussion_statement = disc_stmt,
	                                           user = user_id)[:1]

	if not len(comment) == 1:
	    return json_error('That comment does not exist.')

	comment = comment[0]
	update_comment_score(comment, os_id, disc_stmt)
	update_query_weight(comment)
	return json_result({'success':True})
	

def update_reviewer_score(user,val=0):
	"""
	Recalculates the user's reviewer score
	"""	
	# TODO: fix here to actually calculate the contribution of the agreement ratings
	# to the reviewer score
	sum = val

	reviewer_score = ReviewerScore.objects.filter(user = user)
	if len(reviewer_score) != 0:
		ReviewerScore.objects.filter(user = user).update(reviewer_score = sum) # Update the reviewer score
	else:
		review = ReviewerScore(user = user, reviewer_score = sum) # otherwise create a new row in the db
		review.save()
	
	return sum
	
def update_comment_score(comment, os_id, disc_stmt):
	"""
	Recalculates the comment's score on several different metrics
		- average rating and average score
		- 
	"""
	ratings_tuples_filtered =  get_recent_ratings_from_all_revisions(comment)

	raw_scores = []
	raw_ratings = []
	raw_offsetted_scores = []
	
	for tuple in ratings_tuples_filtered:
		raw_ratings.append(tuple[1].rating)
		raw_scores.append(tuple[1].score)
		raw_offsetted_scores.append(calculate_reputation_score(comment.opinion_space_id, tuple[1].rater, comment.user_id, tuple[1].rating, True))

	comment.average_rating = numpy.mean(raw_ratings)
	comment.average_score = numpy.mean(raw_scores)
	comment.save() 

	# update the normalized score and confidence		
	if len(raw_ratings) >= 5:
		std = numpy.std(raw_ratings)
		sqrt_num_ratings = sqrt(len(raw_ratings))
		confidence = std/sqrt_num_ratings
	else:
		# if there are less than 5 ratings for the comment, then set the confidence to null (the largest SE)
		confidence = None

	# Save the confidence to the discussion comment table
	comment.confidence = confidence

	# 2011.09.26 - changing normalized_score to hold: constant offsetted sum
	comment.normalized_score = numpy.sum(raw_offsetted_scores)

	comment.save()

	# Calculate the score sum 
	score_sum = numpy.sum(raw_scores)
	comment.score_sum = score_sum
	comment.save()

	# Calculate the normalized score sum
	max_score_sum = DiscussionComment.objects.filter(is_current = True,
	                                            	opinion_space = os_id,
	                                            	discussion_statement = disc_stmt,
													score_sum__isnull = False).order_by('-score_sum')[0].score_sum

	min_score_sum = DiscussionComment.objects.filter(is_current = True,
	                                            	opinion_space = os_id,
	                                            	discussion_statement = disc_stmt,
													score_sum__isnull = False).order_by('score_sum')[0].score_sum

	if max_score_sum == None:
		max_score_sum = 0
	if min_score_sum == None:
		min_score_sum = 0

	# In the case that there is one discussion comment in the space, or by some miracle the max == min
	# we will normalize by 1, because all score_sums are the same
	if (max_score_sum - min_score_sum) == 0:
		normalized_score_sum = score_sum
	else:
		normalized_score_sum = (score_sum - min_score_sum) / math.fabs(max_score_sum - min_score_sum)
		#take care of fp precision errors
		if normalized_score_sum < MIN_FLOAT:
			normalized_score_sum = 0
			
	comment.normalized_score_sum = normalized_score_sum
	comment.save()	

def get_revisions(user, os, disc_stmt):
	comment_list = DiscussionComment.objects.filter(user = user, is_current = False, discussion_statement = disc_stmt, opinion_space = os).order_by('created').reverse()
	return [(c.comment, c.created.strftime("%B %d, %Y")) for c in comment_list]
	
def get_revisions_and_suggestions(user, os, disc_stmt,reverse=True):
	#get all comments
	comment_list = DiscussionComment.objects.filter(user = user, discussion_statement = disc_stmt, opinion_space = os)
	
	#get a list of all revisions and suggestions
	complete_list = []
	if SEND_REVISIONS:
		complete_list.extend(comment_list)
	complete_list.extend(Suggestion.objects.filter(comment__in = comment_list))
	
	#sort and reverse
	complete_list = sorted(complete_list, key=lambda obj: obj.created)
	if reverse:
		complete_list.reverse()
	
	#create the formatted tuple
	tuple_list = []
	for x in complete_list:
		if isinstance(x, DiscussionComment):
			if not x.is_current:
				tuple_list.append((x.comment, x.created.strftime("%B %d, %Y"), 'comment',x.user.username))
		else:
			tuple_list.append((x.suggestion, x.created.strftime("%B %d, %Y"), 'suggestion',x.suggester.username))
	
	return tuple_list

#
# Formatting functions to package data in a standard way
#

def format_discussion_comment(request_user, response):
	
	"""
	Formats a data structure holding the information for a disucssion comment
	with relation to a user (request_user)
	"""
	#print len(response.comment.split()) > 3, response.query_weight
	
	return {'uid': response.user.id,
			'username': get_formatted_username(response.user),
			#'location': get_location(response.user),
			'cid': response.id,
			'disc_id': response.discussion_statement.id,
			'rating': get_user_comment_rating(request_user, response),
			'agreeance': get_user_agreement(request_user, response),
			'confidence': sanitize_comment_confidence(response.confidence),
			'norm_score': sanitize_comment_score(response.normalized_score_sum),
			'comment': response.comment,
			'spanish_comment': response.spanish_comment,
			'rev_score': get_reviewer_score(response.user),
			'vis_vars': [0,0,0]}
			#'prev_comments': get_revisions_and_suggestions(response.user, response.opinion_space, response.discussion_statement,False) }

def format_general_discussion_comment(response):
	
	"""
	Formats a data structure holding the information for a disucssion comment
	with no relation to a user
	"""
	tag, z = "", None
	zipcode=""
	city_state=""
	if ZipCodeLog.objects.filter(user=response.user).exists():
		ZipCodeLog.objects.get(user=response.user).location

	if AdminCommentTag.objects.filter(comment=response).exists():
		tag = AdminCommentTag.objects.get(comment=response).tag
	if z:
		zipcode = z.code
		city_state = (z.city + ", " + z.state)


	return {'uid': response.user.id,
		'username': get_formatted_username(response.user),
		'email' : response.user.email,
		'location': get_location(response.user),
		'cid': response.id,
		'confidence': sanitize_comment_confidence(response.confidence),
		'norm_score': sanitize_comment_score(response.normalized_score_sum),
		'comment': response.comment,
		'spanish_comment': response.spanish_comment,
		'original_language': response.original_language,
		'rev_score': get_reviewer_score(response.user),
		'vis_vars': get_visual_variables(response),
		'zipcode' : zipcode,
		'city_state' : city_state,
		'tag' : tag,
		}

def format_user_object(user, os_id, ds_id = None):
	
	"""
	Formats users objects
	"""
	
	return {'uid':user.id,
			'username': get_formatted_username(user),
			'location': get_location(user),
			'email': user.email,
			'comment': get_comment_text(user, os_id, ds_id),
			'cid': get_comment_id(user, os_id, ds_id),
			'author_score': get_author_score(user, os_id, ds_id),
			'reviewer_score': get_reviewer_score(user),
			'reset_link': create_pw_reset_link(user)
		   }

def create_pw_reset_link(user):
	import hashlib
	time = datetime.datetime.now().isoformat()
	plain = time
	token = hashlib.sha1(plain)
	token = token.hexdigest()[:10]
	udl = UserData.objects.filter(user = user, key='prlink')
	if len(udl) > 0:
		return URL_ROOT + '/accountsjson/password/reset/?link='+udl[0].value
	else:
		udl = UserData(user=user,key='prlink',value=token)
		udl.save()
		return URL_ROOT + '/accountsjson/password/reset/?link='+token

#
# General helper functions
#

def filter_out_by_wordcount(comments, minimum):
	"""
	
	Returns a set of comments where the number of words in the response
	is greater than the minimum number of words required
	
	"""
	filtered_list = []
	for comment in comments:
		if len(comment.comment.split()) >= minimum:
			filtered_list.append(comment)
	return filtered_list

def filter_out_no_ratings(os, comments):
	"""
	
	Returns a set of comments where the users who wrote the comments have
	rated at least one of the initial propositions, ie have at least
	one row in the UserRating table where is_current = True
	
	"""
	
	filtered_list = []
	for comment in comments:
		if UserData.objects.filter(user = comment.user, key = 'first_rating').count() != 0:
			filtered_list.append(comment)
	return filtered_list

def sort_by_inverse_num_ratings_and_time(comments):
	
	"""
	Sorts by inverse number of ratings and for all ties, by 
	"""
	
	data = []
	for comment in comments:
		data.append((comment, len(comment.ratings.filter(is_current = True)), comment.created))
	
	# Since python sorts are stable, we sort by descending time then sort
	# by ascending number of ratings
	data = sorted(data, key=itemgetter(2), reverse=True)
	data = sorted(data, key=itemgetter(1))
	return [d[0] for d in data]

def sort_shuffle(comments):
	"""
	Sorts the comments pseudo-randomly
	
	Add more functionality here to make the sort more sophisticated
	"""
	data = [comment for comment in comments] # translate to array from queryset
	random.shuffle(data)
	return data
	
def sort_by_response_score(formatted_comments):
	"""
	Sorts the set of FORMATTED comments by comment score

	Returns a sorted set of pairs (uid, normailzed_score_sum) from smallest to largest
	based on score
	"""
	data = [(comment['uid'], comment['norm_score']) for comment in formatted_comments]
	data = sorted(data, key=itemgetter(1))
	return data

def sort_by_avg_agreement(formatted_comments):
	"""
	Sorts the set of FORMATTED comments by average agreement

	Returns a sorted set of pairs (uid, normailzed_score_sum) from smallest to largest
	based on score
	"""
	data = [(comment['uid'], comment['vis_vars'][0]) for comment in formatted_comments]
	data = sorted(data, key=itemgetter(1))
	return data

def sort_by_probability(comments, probability_list):
        """
        Sorts based on an array of weights that determine how frequently
        a comment appear near the top.
        """
        i = 0 #initial index
        data = [] #empty list
        for comment in comments:
                data.append((comment,random.random()*probability_list[i]))
                i = i + 1 #increment i
        data = sorted(data,key=itemgetter(1),reverse=True)
        return [d[0] for d in data]

def partition_points(left, high_num, low_num):
	
	"""
	Partition the number of high and low confidence points
	"""
	
	high_portion = 0
	low_portion = 0
	if high_num + low_num > left:
		if high_num < left/2 or low_num < left/2:
			if high_num < left/2:
				high_portion = high_num
				low_portion = left - high_num
			else:
				high_portion = left - low_num
				low_portion = low_num
		else:
			high_portion = left/2
			low_portion = left/2
	else:
		high_portion = high_num
		low_portion = low_num
	return (high_portion, low_portion)


def sanitize_comment_confidence(confidence):
	
	"""
	For null confidence, return 1, the maximum SE possible
	"""
	
	if confidence is None:
		return 1
	else:
		return confidence

def sanitize_comment_score(score):
	
	"""
	For null scores (without any ratings) return 0, the lowest score	
	"""
	
	if score is None:
		return 0
	else:
		if score < MIN_FLOAT:
			score = handle_small_float(score)
		return score
		
def decode_to_unicode(text, encoding='utf-16'):
	
	"""
	Decode early - translate comments to unicode using utf-8 encoding
	"""
	
	if not isinstance(text, unicode):
		text = unicode(text, encoding)
	return text

def handle_small_float(number):
	"""
	Utility function that for now rounds the number to zero
	
	This function can also transform from scientific notation to decimal if precision needed
	"""
	return 0

#
# Commonly used boolean queries
#

def not_admin_approved(comment):
	"""
	Admin panel helper methods
	"""
	return len(AdminApprovedComment.objects.filter(comment = comment)) == 0

def is_not_banished(user):
	"""
	Returns if a user is banished or not
	"""
	return len(BanishedUser.objects.filter(user = user)) == 0

def update_query_weight(comment):
    if comment.query_weight == -1:#comment was just created	
        if len(DiscussionComment.objects.filter(is_current = True, opinion_space = comment.opinion_space, discussion_statement = comment.discussion_statement)) == 0:
            comment.query_weight = 0 #automatically the max as you are the only one in the space
        else:
            comment.query_weight = DiscussionComment.objects.filter(is_current = True, opinion_space = comment.opinion_space, discussion_statement = comment.discussion_statement).order_by('query_weight').reverse()[0].query_weight
			
    elif comment.query_weight != 0:#if the query_weight is already the max then do nothing wait for the cron to fix this, o/w decrement
        comment.query_weight = comment.query_weight - 1
	
    comment.save()
	
def get_formated_comments_from_user_list(request_user,user_list, os, disc_stmt,max_num):
	
	"""
	Returns the comments of the users from a list of users
	"""
	
	comments = []
	uids = []
	for uid in user_list:
		
		#check to see if the user exists first
		user = User.objects.filter(id = uid)
		
		if len(user) == 0:
			continue
		
		user = user[0]
		
		# Check if the rater is banished or has no statement rating values
		if is_not_banished(User.objects.get(id = user.id)) and len(UserRating.objects.filter(user = user, opinion_space = os, is_current = True)) > 0:
			
			uids.append(user.id)
		
			current_comment = os.comments.filter(user = user, 
													is_current = True, 
													blacklisted = False, 
													discussion_statement = disc_stmt)

			if len(current_comment) != 0:
				comments.append(format_discussion_comment(request_user, current_comment[0]))
			
	if max_num:
		return (comments[0:max_num], uids)
	else:
		return (comments, uids)
	
def get_sms_can_change_password(user):
	fkey = ForeignCredential.objects.filter(user = user)
	if len(fkey) == 1:#if there is 1 foreignid
		tup = fkey[0].foreignid.partition('_') #if it follows our _ syntax
		if tup[2] == 'sms' and user.username == tup[0]: #if there is data after the _
			return True
	return False

def get_recent_ratings_from_all_revisions(comment,type='insight',slice=-1):
	"""
	Returns a tuple of rater.id and rating object, of all the ratings that matter for a given comment
	"""
	all_revisions = DiscussionComment.objects.filter(user = comment.user, opinion_space = comment.opinion_space, discussion_statement = comment.discussion_statement)
	#list of tuples of all current ratings for a user in all revisions of the comment, sorted most recent first
	if type == 'insight':
		if slice == -1:
			ratings_tuples = [(r.rater.id, r) for r in CommentRating.objects.filter(is_current = True, comment__in = all_revisions).order_by('created').reverse()]
		else:
			ratings_tuples = [(r.rater.id, r) for r in CommentRating.objects.filter(is_current = True, comment__in = all_revisions).order_by('created').reverse()[:slice]]
	else:
		if slice == -1:
			ratings_tuples = [(r.rater.id, r) for r in CommentAgreement.objects.filter(is_current = True, comment__in = all_revisions).order_by('created').reverse()]
		else:
			ratings_tuples = [(r.rater.id, r) for r in CommentAgreement.objects.filter(is_current = True, comment__in = all_revisions).order_by('created').reverse()[:slice]]
	
	#remove ratings with duplicate users while preserving order
	ratings_tuples_filtered_list = []
	for t in ratings_tuples:
		if not t[0] in [y[0] for y in ratings_tuples_filtered_list]:
			ratings_tuples_filtered_list.append(t)
	
	return ratings_tuples_filtered_list

def get_user_recent_ratings_from_all_revisions(user,os,disc_stmt,type='insight',slice=-1):
	"""
	Returns a tuple of rater.id and rating object, of all the ratings that matter made by a given user
	"""
	
	if type == 'insight':
		if slice == -1:
			ratings_tuples = [(r.comment.user.id,r) for r in CommentRating.objects.filter(is_current=True, rater = user).order_by('created').reverse()]
		else:
			ratings_tuples = [(r.comment.user.id,r) for r in CommentRating.objects.filter(is_current=True, rater = user).order_by('created').reverse()[:slice]]
	else:
		if slice == -1:
			ratings_tuples = [(r.comment.user.id, r) for r in CommentAgreement.objects.filter(is_current=True, rater = user).order_by('created').reverse()]
		else:
			ratings_tuples = [(r.comment.user.id,r) for r in CommentAgreement.objects.filter(is_current=True, rater = user).order_by('created').reverse()[:slice]]
		
	#remove ratings with duplicate users while preserving order
	ratings_tuples_filtered_list = []
	for t in ratings_tuples:
		if not t[0] in [y[0] for y in ratings_tuples_filtered_list]:
			if t[1].comment.opinion_space == os and not t[1].comment.blacklisted and t[1].comment.discussion_statement == disc_stmt:
				ratings_tuples_filtered_list.append(t)
	
	return ratings_tuples_filtered_list

def ratings_2_vector(user):
    result_vector = {}
    for u in UserRating.objects.filter(user = user, is_current=True):
        result_vector[u.opinion_space_statement.id] = u.rating
    return result_vector

def user_2_user_dist(vector1,vector2):
    dist = 0
    for k in vector1:
        if k in vector2:
            dist = dist + abs(vector1[k] - vector2[k])

    for k in vector2:
        if k in vector2 and k not in vector1:
            dist = dist + abs(vector2[k])

    return dist
	
def get_never_seen_comments(user,os,disc_stmt,max_num=None,efficient_count=False, no_statements=False):
  users_with_ratings = UserData.objects.filter(key = 'first_rating').values_list('user')
  users_with_no_ratings = User.objects.all().exclude(id__in = users_with_ratings)

  rated_users = set()
	
  if user.is_authenticated():
        insight_rated_comments = CommentRating.objects.filter(rater = user, is_current=True)
        agreement_rated_comments = CommentAgreement.objects.filter(rater = user, is_current=True)
        my_ratings = ratings_2_vector(user)
		
        if NEVER_SEEN_TIGHT_BOUND: # a single rating counts as seeing the user
            for i in insight_rated_comments:
                if i.comment.discussion_statement == disc_stmt:
                    rated_users.add(i.comment.user)
            for a in agreement_rated_comments:
                if a.comment.discussion_statement == disc_stmt:
                   rated_users.add(a.comment.user)
        else:
            insight_rated_users = set([c.comment.user for c in insight_rated_comments if c.comment.discussion_statement == disc_stmt])
            agreement_rated_users = set([c.comment.user for c in agreement_rated_comments if c.comment.discussion_statement == disc_stmt])
            rated_users = insight_rated_users.intersection(agreement_rated_users)

        rated_users.add(user) #exlude self too
		
  current_comments = DiscussionComment.objects.filter(is_current = True, blacklisted = False, opinion_space = os, discussion_statement = disc_stmt).exclude(user__in = list(rated_users)).exclude(user__in = users_with_no_ratings)
		
  if DATABASE_ENGINE == 'sqlite3':
     current_comments =  current_comments.extra(select={'rand_weight': "query_weight * random()"}).extra(order_by=['-rand_weight'])
  else:
     current_comments =  current_comments.extra(select={'rand_weight': "query_weight * rand()"}).extra(where=["LENGTH(comment) - LENGTH(REPLACE(comment, ' ', '')) >= %s"], params=[str(2)]).extra(order_by=['-rand_weight'])
		
	#print users_with_no_ratings
  if max_num != None:
    current_comments = current_comments[:max_num]
	
  if efficient_count:
    return current_comments.count()
  else:
    return [format_discussion_comment(user, current_comment) for current_comment in current_comments]

def get_rated_updated_comments(user,os,disc_stmt,max_num=None):
	agreement_ratings = get_user_recent_ratings_from_all_revisions(user,os,disc_stmt,'agreement') #get most recent agreement ratings
	insight_ratings = get_user_recent_ratings_from_all_revisions(user,os,disc_stmt,'insight')#get most recent insight ratings
	"""
	logic below is trick so here is it in english:
	get the most recent insight ratings over all revisions for all rated users
	get the most recent agreement ratings over all revisions for all rated users
	create a set of users who recieved those ratings, exluding users that have current comment
	you are left with a set of users who you have rated either agreement or insight but haven't rated the current comment
	"""
	rated_users = set()
	current_users = set()
	for i in insight_ratings:
		if i[1].comment.is_current:
			current_users.add(i[1].comment.user)
		rated_users.add(i[1].comment.user)
	for a in agreement_ratings:
		if a[1].comment.is_current:
			current_users.add(a[1].comment.user)
		rated_users.add(a[1].comment.user)
	
	rated_users = rated_users.difference(current_users)
	
	comments = []
	for rated_user in rated_users:
		most_recent_revision = DiscussionComment.objects.filter(is_current = True, user = rated_user, blacklisted = False, opinion_space = os, discussion_statement = disc_stmt)
		if most_recent_revision.count() > 0:
			comments.append(most_recent_revision[0])
	
	weight_list = []
	for comment in comments:
		weight_list.append(comment.query_weight)
	comments = sort_by_probability(comments,weight_list)
	
	if max_num != None:
		comments = comments[:max_num]
	
	return [format_discussion_comment(user, c) for c in comments]

def update_suggestion_score(suggestion): 
	suggestion.score = calculate_reputation_score(suggestion.comment.opinion_space_id, suggestion.suggester, suggestion.comment.user_id, suggestion.q, True)
	suggestion.save()
	
	score_objects = SuggesterScore.objects.filter(user = suggestion.suggester)
	if score_objects.count() == 0:
		suggestion_score = SuggesterScore(user = suggestion.suggester, score_sum = 0, normalized_score_sum = 0)
		suggestion_score.save()
	else:	
		suggestion_score = score_objects[0]
	
	all_suggestions = Suggestion.objects.filter(suggester = suggestion.suggester).exclude(q = None)
	score_sum = 0
	for s in all_suggestions:
		score_sum = s.score + score_sum  

	suggestion_score.score_sum = score_sum
	suggestion_score.save()
	
	#should always have > 0 count
	max_score_sum = SuggesterScore.objects.all().order_by('score_sum').reverse()[0].score_sum
	min_score_sum = SuggesterScore.objects.all().order_by('score_sum')[0].score_sum
	
	if (max_score_sum - min_score_sum) == 0:
		normalized_score_sum = suggestion_score.score_sum
	else:
		normalized_score_sum = (suggestion_score.score_sum - min_score_sum) / math.fabs(max_score_sum - min_score_sum)
		if normalized_score_sum < MIN_FLOAT:
			normalized_score_sum = 0

	suggestion_score.normalized_score_sum = normalized_score_sum
	suggestion_score.save()

def score_to_grade(score1):
  score = 100 - score1;

  if score == 100:
    return 'A+'
  elif score > 92:
    return 'A'
  elif score > 86:
    return 'A-'
  elif score > 81:
    return 'B+'
  elif score > 69 :
    return 'B'
  elif score > 63 :
    return 'B-'
  elif score > 56:
    return 'C+'
  elif score > 44:
    return 'C'
  elif score > 38:
    return 'C-'
  elif score > 32:
    return 'D+'
  elif score > 19 :
    return 'D'
  elif score == 0 :
    return 'F'
  else:
    return 'D-'

def score_to_int(score1):
  score = 100 - score1;

  if score == 100:
    return 12
  elif score > 92:
    return 11
  elif score > 86:
    return 10
  elif score > 81:
    return 9
  elif score > 69 :
    return 8
  elif score > 63 :
    return 7
  elif score > 56:
    return 6
  elif score > 44:
    return 5
  elif score > 38:
    return 4
  elif score > 32:
    return 3
  elif score > 19 :
    return 2
  elif score == 0 :
    return 0
  else:
    return 1

def user_author_score(user):
  current_comment = DiscussionComment.objects.filter(user = user)
  if len(current_comment) == 0:
     return 0
  else:
     score = 0
     for a in CommentAgreement.objects.filter(comment = current_comment[0]):
         score = score + score_to_int(100*a.agreement)*100
     return score

def translate_to_english(comment):
	import goslate
	googleTranslate = goslate.Goslate()
	return googleTranslate.translate(comment,'en')

def translate_to_spanish(comment):
	import goslate
	googleTranslate = goslate.Goslate()
	return googleTranslate.translate(comment,'es')

def translate_all_comments():
	import goslate
	googleTranslate = goslate.Goslate()

	for comment in DiscussionComment.objects.all():
		try:
			spanComment = translate_to_spanish(comment.comment)
		except BaseException:
			print("there was an error in translating: " + comment.comment)
        
		if len(spanComment) > 1024:
			comment.spanish_comment = spanComment[0:1023]
		else:
			comment.spanish_comment = spanComment

		comment.save()
