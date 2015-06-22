try:
    import oauth2
    import twitter
except:
    pass
import urlparse
import urllib
try:
    import json
except ImportError:
    import simplejson as json
import string
from django.contrib.auth.models import User
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
from opinion.includes.logutils import *
from opinion.registration_json.views import connect_visitor_to_user
from django.template.loader import get_template
from django.template import RequestContext

def manual_login(request, user):
	connect_visitor_to_user(request, user.id)
	request.session['user_id'] = user.id
	request.session['_auth_user_id'] = user.id
	request.session['_auth_user_backend'] = 'opinion.email-auth.EmailOrUsernameModelBackend'

def facebook_register(request, allow_login=False):
	if request.method == 'GET':
		code = request.REQUEST.get('code','')
		t = get_template('applicationreturn.html')
		create_user_event_log(request,{'log_type' : 9, 'details' : 'Facebook register'})	
		error_des = request.REQUEST.get('error_description','')
		
		if len(error_des) != 0:
			request.session['social_errors'] = 'Facebook says: ' + error_des
			return t.render(RequestContext(request, {'os_id':'1'}))
		
		if len(code) == 0:
			request.session['social_errors'] = 'Improper Redirect From Facebook, Please Check Popup-Blocker Settings'
			return t.render(RequestContext(request, {'os_id':'1'}))
		create_user_event_log(request,{'log_type' : 9, 'details' : 'Facebook redirect OK'})	
		redirect_uri =''
		if URL_ROOT.find('localhost') > -1:
			redirect_uri = 'http://dev.hybridwisdom.com/qa/accountsjson/facebook/'
		elif allow_login:
			redirect_uri = FB_REDIRECT_URI + "registerorlogin/"
		else:
			redirect_uri = FB_REDIRECT_URI + "register/"
			
		query = {'code': code, 'client_secret': FB_SECRET_KEY, 'client_id': FB_APP_ID, 'redirect_uri' : redirect_uri}
		uh = urllib.urlopen('https://graph.facebook.com/oauth/access_token?%s' % (urllib.urlencode(query)))
		result = ''
		line = uh.readline()
		while line != '':
			result = result + line
			line = uh.readline()
		params = {}
		
		#try:
		params = dict([part.split('=') for part in result.split('&')])
		#except ValueError:
		#	request.session['social_errors'] = 'Unable to parse result from graph.facebook.com'
		#	return t.render(RequestContext(request, {'os_id':'1'}))
			
		if not params.has_key('access_token'):
			request.session['social_errors'] = 'Neccessary access was not granted from Facebook'
			return t.render(RequestContext(request, {'os_id':'1'}))
		
		uh = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % (params['access_token']))
		
		result = ''
		line = uh.readline()
		while line != '':
			result = result + line
			line = uh.readline()
		result_dict = json.loads(result)
		
		first_name = ''
		last_name = ''
		id = ''
		
		attr_list = ['birthday', 'religion', 'gender', 'political', 'email', 'timezone', 'id', 'updated']
		if result_dict.has_key('first_name'):
			first_name = result_dict['first_name']
		
		if result_dict.has_key('last_name'):
			last_name = result_dict['last_name']
			
		if result_dict.has_key('id'):
			id = result_dict['id']
		
		if first_name == '' or id == '':
			request.session['social_errors'] = 'Unable to retrieve enough data to create an account'
			return t.render(RequestContext(request, {'os_id':'1'}))
		create_user_event_log(request,{'log_type' : 9, 'details' : 'Facebook data fetch OK'})	
		arriving_user = ForeignCredential.objects.filter(foreignid = id + "_facebook")
		password = ''
		if len(arriving_user) == 0:
			password = User.objects.make_random_password(24)
			arriving_user = User.objects.create_user(get_next_available_name(first_name.lower() + last_name.lower(),0) ,  '' , password)
			arriving_user.save()
			foreign_cred = ForeignCredential(user = arriving_user, foreignid = id + "_facebook")
			foreign_cred.save()
			for attr in attr_list:
				if result_dict.has_key(attr):
					value = result_dict[attr]
					data = UserData(key = attr, value = value, user = arriving_user)
					data.save()
			data = UserData(key = 'first_name', value = first_name, user = arriving_user) 
			data.save()
			data = UserData(key = 'last_name', value = last_name, user = arriving_user) 
			data.save()
			create_user_event_log(request,{'log_type' : 9, 'details' : 'Facebook account created'})	
		elif allow_login:
			arriving_user = arriving_user[0].user
		else:
			request.session['social_errors'] = 'This user already has an account, please click Sign In instead'
			return t.render(RequestContext(request, {'os_id':'1'}))
		create_user_event_log(request,{'log_type' : 9, 'details' : 'OS Login'})	
		manual_login(request,arriving_user)
		return t.render(RequestContext(request, {'os_id':'1'}))
	else:
		request.session['social_errors'] = 'Bad redirect from facebook'
		return t.render(RequestContext(request, {'os_id':'1'}))

def facebook_login(request):
	if request.method == 'GET':
		code = request.REQUEST.get('code','')		
		t = get_template('applicationreturn.html')
		create_user_event_log(request,{'log_type' : 9, 'details' : 'Facebook login'})
		error_des = request.REQUEST.get('error_description','')
		
		if len(error_des) != 0:
			request.session['social_errors'] = 'Facebook says: ' + error_des
			return t.render(RequestContext(request, {'os_id':'1'}))
		
		if len(code) == 0:
			request.session['social_errors'] = 'Improper Redirect From Facebook, Please Check Popup-Blocker Settings'
			return t.render(RequestContext(request, {'os_id':'1'}))
		create_user_event_log(request,{'log_type' : 9, 'details' : 'Facebook redirect OK'})
		redirect_uri =''
		if URL_ROOT.find('localhost') > -1:
			redirect_uri = 'http://dev.hybridwisdom.com/qa/accountsjson/facebook/'
		else:
			redirect_uri = FB_REDIRECT_URI
			
		query = {'code': code, 'client_secret': FB_SECRET_KEY, 'client_id': FB_APP_ID, 'redirect_uri' : redirect_uri}
		uh = urllib.urlopen('https://graph.facebook.com/oauth/access_token?%s' % (urllib.urlencode(query)))
		result = ''
		line = uh.readline()
		while line != '':
			result = result + line
			line = uh.readline()
		params = {}
		
		try:
			params = dict([part.split('=') for part in result.split('&')])
		except ValueError:
			request.session['social_errors'] = 'Unable to parse result from graph.facebook.com'
			return t.render(RequestContext(request, {'os_id':'1'}))
			
		if not params.has_key('access_token'):
			request.session['social_errors'] = 'Neccessary access was not granted from Facebook'
			return t.render(RequestContext(request, {'os_id':'1'}))
		
		uh = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % (params['access_token']))
		
		result = ''
		line = uh.readline()
		while line != '':
			result = result + line
			line = uh.readline()
		result_dict = json.loads(result)
		
		first_name = ''
		last_name = ''
		id = ''
		
		attr_list = ['birthday', 'religion', 'gender', 'political', 'email', 'timezone', 'id', 'updated']
		if result_dict.has_key('first_name'):
			first_name = result_dict['first_name']
		
		if result_dict.has_key('last_name'):
			last_name = result_dict['last_name']
			
		if result_dict.has_key('id'):
			id = result_dict['id']
		
		if first_name == '' or id == '':
			request.session['social_errors'] = 'Unable to retrieve enough data to create an account'
			return t.render(RequestContext(request, {'os_id':'1'}))
		create_user_event_log(request,{'log_type' : 9, 'details' : 'Facebook data OK'})
		arriving_user = ForeignCredential.objects.filter(foreignid = id + "_facebook")
		password = ''
		if len(arriving_user) == 0:
			request.session['social_errors'] = 'There is no user tied to this social media account, please click First Time instead'
			return t.render(RequestContext(request, {'os_id':'1'}))
		else: #update information and login
			arriving_user = arriving_user[0].user
			for attr in attr_list:
				if result_dict.has_key(attr):
					value = result_dict[attr]
					search = UserData.objects.filter(key = attr, user = arriving_user)
					if len(search) > 0:
						search[0].value = value
						search[0].save()
					else:
						data = UserData(key = attr, value = value, user = arriving_user)
						data.save()
		create_user_event_log(request,{'log_type' : 9, 'details' : 'OS Login'})		
		manual_login(request,arriving_user)
		return t.render(RequestContext(request, {'os_id':'1'}))
	else:
		request.session['social_errors'] = 'Bad redirect from facebook'
		return t.render(RequestContext(request, {'os_id':'1'}))

def generate_twitter_url(request):	
	register = request.REQUEST.get('register','False') #some weirdness with encoding
	register_or_login = request.REQUEST.get('registerorlogin', 'False')
	
	if string.lower(register) == 'true':
		register = "register/"
	elif string.lower(register_or_login) == 'true':
		register = "registerorlogin/"
	else:
		register = ""

	consumer = oauth2.Consumer(TWITTER_KEY,TWITTER_SECRET)
	client = oauth2.Client(consumer)
	resp, content = client.request(twitter.REQUEST_TOKEN_URL, "POST", body=urllib.urlencode({'oauth_callback':URL_ROOT + "/accountsjson/twitter/" + register}))
	if resp['status'] != '200':
		return "Twitter Error"
	request_token = dict(urlparse.parse_qsl(content))
	auth_url = 'https://api.twitter.com/oauth/authenticate?oauth_token=%s' % (request_token['oauth_token'])
	#cache the data below since the client leaves the view
	request.session['oauth_token'] = request_token['oauth_token']
	request.session['oauth_token_secret'] = request_token['oauth_token_secret']
	create_user_event_log(request,{'log_type' : 9, 'details' : 'Twitter URL Sent'})
	return auth_url

def twitter_register(request, allow_login=False):
	t = get_template('applicationreturn.html')		
	consumer = oauth2.Consumer(TWITTER_KEY,TWITTER_SECRET)
	verifier = request.REQUEST.get('oauth_verifier','')
	if verifier == '':
		request.session['social_errors'] = 'Twitter Error: The user closed the sign-in dialog or clicked CANCEL'
		return t.render(RequestContext(request, {'os_id':'1'}))
	create_user_event_log(request,{'log_type' : 9, 'details' : 'Twitter Register'})
	oa_init_token = request.session.get('oauth_token','')
	oa_init_secret = request.session.get('oauth_token_secret','')
	
	if len(oa_init_token) == 0 or len(oa_init_secret) == 0:
		request.session['social_errors'] = 'Session Error: Authentication could not proceed due to a session error'
		return t.render(RequestContext(request, {'os_id':'1'}))
	
	token = oauth2.Token(oa_init_token, oa_init_secret)
	token.set_verifier(verifier)
	oauth_client  = oauth2.Client(consumer, token)
	resp, content = oauth_client.request(twitter.ACCESS_TOKEN_URL, method='POST', body='oauth_verifier=%s' % verifier)
	if resp['status'] != '200':
		request.session['social_errors'] = 'Twitter Server Error: Error acquiring data from twitter, most probably an issue on their end'
		return t.render(RequestContext(request, {'os_id':'1'}))
	
	access_token  = dict(urlparse.parse_qsl(content))
	
	if not access_token.has_key('user_id'):
		request.session['social_errors'] = 'Twitter User Error: Error acquiring data from twitter, could indicate a problem with your account'
		return t.render(RequestContext(request, {'os_id':'1'}))
	create_user_event_log(request,{'log_type' : 9, 'details' : 'Twitter data OK'})
	id = access_token['user_id'];
	arriving_user = ForeignCredential.objects.filter(foreignid = id + "_twitter" )
	twitter_user = twitter.Api(TWITTER_KEY,TWITTER_SECRET,access_token['oauth_token'], access_token['oauth_token_secret']).VerifyCredentials()
	
	if len(arriving_user) == 0:
		password = User.objects.make_random_password(24)
		arriving_user = User.objects.create_user(get_next_available_name(decode_to_unicode(access_token['screen_name']).lower(),0) ,  '' , password)
		arriving_user.save()
		foreign_cred = ForeignCredential(user = arriving_user, foreignid = id + "_twitter")
		foreign_cred.save()
		create_user_event_log(request,{'log_type' : 9, 'details' : 'Twitter register'})
		if not twitter_user.GetName() == None and not twitter_user.GetName() == '':
			data = UserData(key = 'name', value = twitter_user.GetName(), user = arriving_user)
			data.save()
		
		if not twitter_user.GetScreenName() == None and not twitter_user.GetScreenName() == '':
			data = UserData(key = 'screename', value = twitter_user.GetScreenName(), user = arriving_user)
			data.save()
		
		if not twitter_user.GetLocation() == None and not twitter_user.GetLocation() == '':
			data = UserData(key = 'location', value = twitter_user.GetLocation(), user = arriving_user)
			data.save()
		
		if not twitter_user.GetDescription() == None and not twitter_user.GetDescription()== '':
			data = UserData(key = 'description', value = twitter_user.GetDescription(), user = arriving_user)
			data.save()
		
		if not twitter_user.GetFollowersCount() == None and not twitter_user.GetFollowersCount()== '':
			data = UserData(key = 'followers_count', value = twitter_user.GetFollowersCount(), user = arriving_user)
			data.save()
	elif allow_login:
		arriving_user = arriving_user[0].user
	else:
		request.session['social_errors'] = 'This user already has an account, please click Sign In instead'
		return t.render(RequestContext(request, {'os_id':'1'}))
	create_user_event_log(request,{'log_type' : 9, 'details' : 'Twitter OS login'})	
	manual_login(request,arriving_user)
	return t.render(RequestContext(request, {'os_id':'1'}))

	
def twitter_login(request):
	t = get_template('applicationreturn.html')		
	consumer = oauth2.Consumer(TWITTER_KEY,TWITTER_SECRET)
	verifier = request.REQUEST.get('oauth_verifier','')
	if verifier == '':
		request.session['social_errors'] = 'Twitter Error: The user closed the sign-in dialog or clicked CANCEL'
		return t.render(RequestContext(request, {'os_id':'1'}))
	
	oa_init_token = request.session.get('oauth_token','')
	oa_init_secret = request.session.get('oauth_token_secret','')
	
	if len(oa_init_token) == 0 or len(oa_init_secret) == 0:
		request.session['social_errors'] = 'Session Error: Authentication could not proceed due to a session error'
		return t.render(RequestContext(request, {'os_id':'1'}))
	
	token = oauth2.Token(oa_init_token, oa_init_secret)
	token.set_verifier(verifier)
	oauth_client  = oauth2.Client(consumer, token)
	resp, content = oauth_client.request(twitter.ACCESS_TOKEN_URL, method='POST', body='oauth_verifier=%s' % verifier)
	if resp['status'] != '200':
		request.session['social_errors'] = 'Twitter Server Error: Error acquiring data from twitter, most probably an issue on their end'
		return t.render(RequestContext(request, {'os_id':'1'}))
	
	access_token  = dict(urlparse.parse_qsl(content))
	
	if not access_token.has_key('user_id'):
		request.session['social_errors'] = 'Twitter User Error: Error acquiring data from twitter, could indicate a problem with your account'
		return t.render(RequestContext(request, {'os_id':'1'}))
	create_user_event_log(request,{'log_type' : 9, 'details' : 'Twitter data OK'})	
	id = access_token['user_id'];
	arriving_user = ForeignCredential.objects.filter(foreignid = id + "_twitter" )
	twitter_user = twitter.Api(TWITTER_KEY,TWITTER_SECRET,access_token['oauth_token'], access_token['oauth_token_secret']).VerifyCredentials()
	
	if len(arriving_user) == 0:
		request.session['social_errors'] = 'There is no user tied to this social media account, please click First Time instead'
		return t.render(RequestContext(request, {'os_id':'1'}))
	else:
		arriving_user = arriving_user[0].user
	create_user_event_log(request,{'log_type' : 9, 'details' : 'Twitter OS login'})		
	manual_login(request,arriving_user)
	return t.render(RequestContext(request, {'os_id':'1'}))
