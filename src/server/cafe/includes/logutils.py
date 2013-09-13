import string

from cafe.cafe_core.models import *
from cafe.includes.jsonutils import *
from cafe.settings import OS_ID_DEFAULT

def create_visitor(request):
    # See if we need to create a visitor here
    if not request.user.is_authenticated() and not request.session.get('visitor_id', False):
        visitor = Visitor()
        visitor.save()
        request.session['visitor_id'] = visitor.id

def get_logger_info(request):
    # Decide whether to log as visitor or user
    create_visitor(request)
    logger_id = request.session.get('visitor_id', False)
    is_visitor = True
    if request.user.is_authenticated():
        logger_id = request.user.id
        is_visitor = False
    
    return logger_id, is_visitor


def create_http_error_log(request, extra = {}):
	logger_id, is_visitor = get_logger_info(request)
	
	args = request.REQUEST
		
	url = args.get('url', '') #URL cannot be blank
	if url == '':
		return
	
	try:
		os_id = int(args.get('os_id', ''))
	except ValueError:
		os_id = OS_ID_DEFAULT #use default
	
	try:
		os = OpinionSpace.objects.get(id = os_id)
	except OpinionSpace.DoesNotExist:
		return
	
	message = args.get('message', None)
	error_type = int(args.get('error_type', '0'))
	
	error_log = LogHTTPErrors(logger_id = logger_id, is_visitor = is_visitor, opinion_space = os, url = url, error_type = error_type, message = message)
	error_log.save()
	
	return json_success()

def create_user_event_log(request, extra = {}):
	logger_id, is_visitor = get_logger_info(request)
	args = request.REQUEST
	
	try:
		os_id = int(extract_info(args, extra, 'os_id', ''))
	except ValueError:
		os_id = OS_ID_DEFAULT #use default
		
	try:
		os = OpinionSpace.objects.get(id = os_id)
	except OpinionSpace.DoesNotExist:
		return json_error('That opinion space does not exist')

	try:
	 	log_type = int(extract_info(args, extra, 'log_type', ''))
	except ValueError:
		return json_error('Invalid log type')
	
	details = extract_info(args, extra, 'details', None)
	
	if log_type == 8 and not is_visitor: #ViewNotifications Event
		user = User.objects.filter(id = logger_id)
		if user.count() == 1:
			lastNotificationCache = list(UserData.objects.filter(user = user[0], key='last_notification_query'))
			if len(lastNotificationCache) > 0: #wierd evaluation bug..., remove the forced evaluation and replace len with count to check it out
				lastNotificationCache[0].value = details
				lastNotificationCache[0].save()
			else:
				user = User.objects.filter(id = logger_id)
				user = user[0]
				lastNotificationCache = UserData(user = user, key='last_notification_query', value=details)
				lastNotificationCache.save()
		
	user_event_log = LogUserEvents(logger_id = logger_id, is_visitor = is_visitor, opinion_space = os, log_type = log_type, details = details)
	user_event_log.save()

	return json_success()

def create_comment_view_log(request, extra = {}):
	logger_id, is_visitor = get_logger_info(request)
	args = request.REQUEST
	
	try:
		comment_id = int(args.get('comment_id', ''))
	except ValueError:
		return json_error('Invalid params')

	try:
		comment = DiscussionComment.objects.get(id = comment_id)
	except DiscussionComment.DoesNotExist:
		return json_error('That comment does not exist')

	comment_log = LogCommentView(logger_id = logger_id, is_visitor = is_visitor, comment = comment)
	comment_log.save()

	return json_success()

def create_comments_returned_log(request, os, returned_comments, query_type):
	
	logger_id, is_visitor = get_logger_info(request)
	comments_list = string.join([str(comment['cid']) for comment in returned_comments], ' ')
	
	comments_returned_log = LogCommentsReturned(logger_id = logger_id, is_visitor = is_visitor, opinion_space = os, query_type = query_type, comments_list = comments_list)
	comments_returned_log.save()

def extract_info(args, extra, key, default):
	"""
	Checks for the key in args and then extra,
	
	Returns default if not found
	
	** must check that value == default, cannot do just an if statement because
	** if the value is 0 (login for log_type for user_events), the if will not
	** be true
	"""	
	value = args.get(key, default)
	if value == default:
		value = extra.get(key, default)

	return value
