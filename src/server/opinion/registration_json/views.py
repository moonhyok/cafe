"""
Views which allow users to create and activate accounts.

"""

from django import forms
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string 
from django.utils.http import urlquote, base36_to_int, int_to_base36
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

from opinion.includes.jsonutils import *
from opinion.includes.queryutils import *
from opinion.includes.accountutils import *
from opinion.opinion_core.forms import UserDemographicsForm
from opinion.opinion_core.models import *
from opinion.includes.logutils import *

from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

from opinion.includes.profanityutils import *
from opinion.decorators import *

import random
import re
import time
import opinion.settings
import md5
import hashlib
from django.http import QueryDict
#import hashlib

def connect_visitor_to_user(request, user_id):
	visitor_id = request.session.get('visitor_id', False)
	if visitor_id:
		Visitor.objects.filter(id = visitor_id).update(user = user_id)

def activate(request, activation_key,
			 template_name='registration/activate.html',
			 extra_context=None):
	"""
	Activate a ``User``'s account from an activation key, if their key
	is valid and hasn't expired.
	
	By default, use the template ``registration/activate.html``; to
	change this, pass the name of a template as the keyword argument
	``template_name``.
	
	**Required arguments**
	
	``activation_key``
	   The activation key to validate and use for activating the
	   ``User``.
	
	**Optional arguments**
	   
	``extra_context``
		A dictionary of variables to add to the template context. Any
		callable object in this dictionary will be called to produce
		the end result which appears in the context.
	
	``template_name``
		A custom template to use.
	
	**Context:**
	
	``account``
		The ``User`` object corresponding to the account, if the
		activation was successful. ``False`` if the activation was not
		successful.
	
	``expiration_days``
		The number of days for which activation keys stay valid after
		registration.
	
	Any extra variables supplied in the ``extra_context`` argument
	(see above).
	
	**Template:**
	
	registration/activate.html or ``template_name`` keyword argument.
	
	"""
	activation_key = activation_key.lower() # Normalize before trying anything with it.
	account = RegistrationProfile.objects.activate_user(activation_key)
	
	if account:
		return json_success()
	else:
		return json_error('Invalid request.')


def register(request, success_url=None,
			 form_class=RegistrationFormUniqueEmail, profile_callback=None,
			 template_name='registration/registration_form.html',
			 extra_context=None):
	"""
	Allow a new user to register an account.
	
	Following successful registration, issue a redirect; by default,
	this will be whatever URL corresponds to the named URL pattern
	``registration_complete``, which will be
	``/accounts/register/complete/`` if using the included URLConf. To
	change this, point that named pattern at another URL, or pass your
	preferred URL as the keyword argument ``success_url``.
	
	By default, ``registration.forms.RegistrationFormUniqueEmail`` will be used
	as the registration form; to change this, pass a different form
	class as the ``form_class`` keyword argument. The form class you
	specify must have a method ``save`` which will create and return
	the new ``User``, and that method must accept the keyword argument
	``profile_callback`` (see below).
	
	To enable creation of a site-specific user profile object for the
	new user, pass a function which will create the profile object as
	the keyword argument ``profile_callback``. See
	``RegistrationManager.create_inactive_user`` in the file
	``models.py`` for details on how to write this function.
	
	By default, use the template
	``registration/registration_form.html``; to change this, pass the
	name of a template as the keyword argument ``template_name``.
	
	**Required arguments**
	
	None.
	
	**Optional arguments**
	
	``form_class``
		The form class to use for registration.
	
	``extra_context``
		A dictionary of variables to add to the template context. Any
		callable object in this dictionary will be called to produce
		the end result which appears in the context.
	
	``profile_callback``
		A function which will be used to create a site-specific
		profile instance for the new ``User``.
	
	``success_url``
		The URL to redirect to on successful registration.
	
	``template_name``
		A custom template to use.
	
	**Context:**
	
	``form``
		The registration form.
	
	Any extra variables supplied in the ``extra_context`` argument
	(see above).
	
	**Template:**
	
	registration/registration_form.html or ``template_name`` keyword
	argument.
	
	"""
	request.session['first_time_data'] = '' #clear the first_time cookie based logs
	if request.method == 'POST':
		request_post_copy = request.POST.copy()

		# Usernames will be saved in lowercase - this is because iexact doesn't work properly
		# with a specific collation (utf8_bin)
		formatted_username = request_post_copy.get('username', '')
		request_post_copy['username'] = formatted_username.lower() # Username saved as lowercase

		form = form_class(data=request_post_copy, files=request.FILES)
		print "printing"
		print request_post_copy['username']
		print request_post_copy['year']
		print request_post_copy['regdesign']

		data_demog={'username': request_post_copy['username'], 'password':request_post_copy['username'],'password1':request_post_copy['username'],'password2':request_post_copy['username'],'email':request_post_copy['username'],'zipcode':request_post_copy['username']}

					# 'year':request_post_copy['year'],
					# 'numCoursesTaken':request_post_copy['regdesign'],
					# 'interest':request_post_copy['interests'],
					# 'reason':request_post_copy['reason'],
					# 'major':request_post_copy['major']
					
		
		demog_qdict = QueryDict('')
		demog_qdict = demog_qdict.copy()
		demog_qdict.update(data_demog)
		
		demog = UserDemographicsForm(data=demog_qdict)
		#demog = UserDemographicsForm(data=request_post_copy)

		if form.is_valid() and demog.is_valid():
			new_user = form.save(profile_callback=profile_callback)

			ud = UserData(user = new_user, key='demographics',value=request_post_copy.urlencode())
			ud.save()
			print request_post_copy.urlencode()
			
			# Save the original formatting of the username
			username_setting = UserSettings(user = new_user, key = 'username_format', value = formatted_username)
			username_setting.save()
			
			# Extract the URL
			if request_post_copy.has_key('url') and request_post_copy['url'] != '':
				url_setting = UserSettings(user = new_user, key = 'url', value = request_post_copy['url'])
				url_setting.save()

			# Extract answer and question
			if request_post_copy.has_key('question') and request_post_copy.has_key('answer') and request_post_copy['question'] != '' and request_post_copy['answer'] != '':
				q_setting = UserSettings(user = new_user, key = 'question', value = request_post_copy['question'])
				q_setting.save()
				a_setting = UserSettings(user = new_user, key = 'answer', value = request_post_copy['answer'])
				a_setting.save()			
			
			# Save demographics
			request_post_copy_again = request_post_copy.copy()
			request_post_copy_again['user'] = new_user.id
			demog = UserDemographicsForm(data=request_post_copy_again)
			demog.save()

			# Create a zip code log entry for this user
			z = ZipCode.objects.filter(code=request_post_copy['zipcode'])
			if len(z) > 0:
				c = ZipCodeLog(user=new_user, location=z[0])
				c.save()

			#save additional informaiton of this user in UserDate
			#if the user didn't type age or reason, the value will be -1
			if request_post_copy.has_key('major'):
				country=UserData(user=new_user,key='major',value=request_post_copy['major'])
				country.save()

			if request_post_copy.has_key('year'):
				gender=UserData(user=new_user,key='year',value=request_post_copy['year'])
				gender.save()

			if request_post_copy.has_key('regdesign'):
				age=UserData(user=new_user,key='regdesign',value=request_post_copy['regdesign'])
				age.save()
			
			if request_post_copy.has_key('interests'):
				trainingYears=UserData(user=new_user,key='interests',value=request_post_copy['interests'])
				trainingYears.save()

			if request_post_copy.has_key('reason'):
				reason=UserData(user=new_user,key='reason',value=request_post_copy['reason'])
				reason.save()
			
			# Create EntryCode
			#print "Hamerican"
			entrycode = hashlib.sha224(request_post_copy['username']).hexdigest()[0:7]
			#print entrycode
			ECobject=EntryCode(username=request_post_copy['username'],code=entrycode, first_login=False)
			#print request_post_copy['username']
			ECobject.save()
			#print len(EntryCode.objects.filter(username__icontains=''))
			# Create visit times
			visittimes=UserData(user=new_user,key='visitTimes',value=str(1))
			visittimes.save()
			# If this was a visitor, connect to a user
			connect_visitor_to_user(request, new_user.id)
			
			# Check the username for profanity
			profanity_result = check_bad_words(formatted_username)
			if profanity_result[0]:
				pfu = ProfanityFlaggedUsername(user = new_user, profanity = profanity_result[1])
				pfu.save()
			
			#return json_result({'success':True, 'username': user_name_arg})
			return json_success()
		else:
			# Combine errors from the user form and demographics form and send back as JSON
			form.errors.update(demog.errors)
			return json_result({'form_errors': errors_to_dict(form.errors)})
	else:
		return json_error('Invalid request.')

## This was taken from django.contrib.auth.forms, and then extended to support a max_length of 75

class AuthenticationFormLargeUsername(AuthenticationForm):
	"""
	Base class for authenticating users. Extend this to get a form that accepts
	username/password logins.
	"""
	username = forms.CharField(label=_("Username"), max_length=75)
	password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

	def __init__(self, request=None, *args, **kwargs):
		"""
		If request is passed in, the form will validate that cookies are
		enabled. Note that the request (a HttpRequest object) must have set a
		cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
		running this validation.
		"""
		self.request = request
		self.user_cache = None
		super(AuthenticationForm, self).__init__(*args, **kwargs)

####################################
## From django.contrib.auth.views ##
####################################

def login(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
	if TEMP_DEBUG_LOGGING:
		TEMP_DEBUG_FILE = open('/tmp/os-debug.log','a')
		TEMP_DEBUG_FILE.write("\nLogin:" + str(datetime.datetime.now()) + "\n")
	
	"Displays the login form and handles the login action."
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		from django.contrib.auth import login
		if form.is_valid():
			user = form.get_user()

			# Check if the user is banned
			user_ob = User.objects.filter(username = user)
			if len(user_ob) != 0:
				if len(BanishedUser.objects.filter(user = user_ob[0])) != 0:
					return json_result({'form_errors': {"__all__":["User is banned"]}})

			login(request, user)
			
			# If this was a visitor, connect to a user
			connect_visitor_to_user(request, user.id)
			
			# Log the login
			create_user_event_log(request, {"log_type": LogUserEvents.login})

			if TEMP_DEBUG_LOGGING:
				TEMP_DEBUG_FILE.write("Login results is user_authenticated?" + str(request.user.is_authenticated()))
				TEMP_DEBUG_FILE.close()
			return json_result({'success' : True, 'sms_can_change_password': get_sms_can_change_password(request.user)})#json_success()
		else:
			if Settings.objects.boolean('SOFT_ENTRY_CODES'):
				c = request.POST.get('entrycode','')
				code_object = EntryCode.objects.filter(code = c)
				if len(code_object) <= 0:
					return json_error('Invalid Entry Code')

				u = User.objects.filter(username = code_object[0].username)

				if len(u) <= 0:
					return json_error('Entry code and user do not match')
					
				if code_object[0].first_login:
					first_login_time = UserData(user = u[0], key = 'first_login', value = time.time())
					first_login_time.save()
					
				code_object[0].first_login = False
				code_object[0].save()
				connect_visitor_to_user(request, u[0].id)
				request.session['user_id'] = u[0].id
				request.session['_auth_user_id'] = u[0].id
				request.session['_auth_user_backend'] = 'opinion.email-auth.EmailOrUsernameModelBackend'
				return json_success()
			# Invalid login
			if TEMP_DEBUG_LOGGING:
				TEMP_DEBUG_FILE.write(json_result({'form_errors': errors_to_dict(form.errors)}).content)
				TEMP_DEBUG_FILE.close()
			return json_result({'form_errors': errors_to_dict(form.errors)})
	else:
		return json_error('Invalid request.')

login = never_cache(login)

def get_auth_state(request):
	if request.user.is_authenticated():
		return json_success()
	else:
		error_dict = request.session.get('social_errors','')
		if error_dict == '':
			return json_result({})
		else:
			return json_result({'social_errors': error_dict})
		
def clear_auth_err(request):
	request.session['social_errors'] = ''
	return json_success()

def get_entry_code(request):
	if request.method == "POST":
		query = request.POST
		entrycode = query.__getitem__("entrycode")
		codeobject = EntryCode.objects.filter(code = entrycode)
		
		if len(entrycode) == 0 or len(codeobject) == 0:
			return json_error('Incorrect parameters')

		users = User.objects.filter(username=codeobject[0].username)

		# return username and/or formatted username
		if len(users) > 0:
			usetting = UserSettings.objects.filter(user = users[0], key = 'username_format')
			if len(usetting) > 0:
				return json_result({'username': codeobject[0].username,
									'username_format': usetting[0].value})
			else:
				return json_result({'username': codeobject[0].username})
		else:
			return json_error('Invalid Entry Code')
	else:
		return json_error('Invalid request')

def get_entry_code_first_login(request):
	if request.method == "GET":
		query = request.GET
		entrycode = query.__getitem__("entrycode")
		codeobject = EntryCode.objects.filter(code = entrycode)

		if len(codeobject) == 0:
			return json_error('Incorrect Parameters')

		login_status = codeobject[0].first_login
		
		return json_result({'first_time': login_status})

@auth_required
def update_user_data_field(request):
	if request.method == "POST": 
		user = request.user
		field = request.POST.get('field','')
		if not (field == ''):
			new_value = request.POST.get('new_value','')
			new_value = new_value.strip()
			if not (new_value == '') or not (new_value == None):
				if field == 'heard_about':
					return heard_about_update(user,new_value)
				elif field == 'location':
					return location_update(user,new_value)
				elif field == 'password':
	
					# Check for flag or if the user is an sms user
					if Settings.objects.boolean('ALLOW_PASSWORD_CHANGE') or get_sms_can_change_password(request.user):
						return password_update(user,new_value)
					else:
						return json_error('Invalid request')

				elif field == 'username':
					
					# Check for flag or if the user is an sms user
					if Settings.objects.boolean('ALLOW_USERNAME_CHANGE') or get_sms_can_change_password(request.user):
						return username_update(user,new_value)
					else:
						return json_error('Invalid request')

				elif field == 'user_data':
					return userdata_update(request)
				else:
					return json_error('Specified field not available for update')
			else:
				return json_error('A new value must be specified')
		else:
			return json_error('A field must be specified')
	else:
		return json_error('Invalid request')

def logout(request, next_page=None, template_name='registration/logged_out.html'):
	"Logs out the user"
	if TEMP_DEBUG_LOGGING:
		TEMP_DEBUG_FILE = open('/tmp/os-debug.log','a')
		TEMP_DEBUG_FILE.write("\nLogin:" + str(datetime.datetime.now()) + "\n")
	visitor_id = request.session.get('visitor_id', False)
	from django.contrib.auth import logout
		
	create_user_event_log(request, {"log_type": LogUserEvents.logout})

	application_close_helper(request)

	logout(request)
	request.session.flush()
#	if visitor_id:
#		request.session['visitor_id'] = visitor_id

	if TEMP_DEBUG_LOGGING:
		TEMP_DEBUG_FILE.write("Logout results is user_authenticated?" + str(request.user.is_authenticated()))
		TEMP_DEBUG_FILE.close()

	return json_success()

# 4 views for password reset:
# - password_reset sends the mail
# - password_reset_done shows a success message for the above
# - password_reset_confirm checks the link the user clicked and 
#   prompts for a new password
# - password_reset_complete shows a success message for the above

def password_reset(request, is_admin_site=False, template_name='registration/password_reset_form.html',
		email_template_name='registration/password_reset_email.html',
		password_reset_form=PasswordResetForm, token_generator=default_token_generator,
		post_reset_redirect=None):
	if request.method == "POST":
		form = password_reset_form(request.POST)
		if form.is_valid():
			opts = {}
			opts['use_https'] = request.is_secure()
			opts['token_generator'] = token_generator
			if is_admin_site:
				opts['domain_override'] = request.META['HTTP_HOST']
			else:
				opts['email_template_name'] = email_template_name
				if not Site._meta.installed:
					opts['domain_override'] = RequestSite(request).domain
			form.save(**opts)
			return json_success()
		else:
			return json_result({'form_errors': errors_to_dict(form.errors)})
	else:
		return json_error('Invalid request.')
		
def password_reset2(request):
	if request.method == "GET":
		link = request.GET.get('link','')
		ud = UserData.objects.filter(key = 'prlink',value=link)
		
		context_instance = RequestContext(request)
		context_instance['link'] = link
		if link == "" or len(ud) == 0:
			context_instance['validlink'] = False
			context_instance['username'] = ''
		else:
			context_instance['validlink'] = True
			user = ud[0].user
			context_instance['username'] = user.username
		
		return render_to_response('registration/password_reset_confirm.html', context_instance=context_instance)
	else:
		link = request.POST.get('link','')
		print link
		ud = UserData.objects.filter(key = 'prlink',value=link)
		if len(ud) > 0:
			user = ud[0].user
			user.set_password(request.POST.get('password',''))
			user.save()
			ud[0].delete()
			return render_to_response('registration/password_change_done.html')
		else:
			return json_error('Invalid request.')

@auth_required
def password_create(request, token_generator=default_token_generator, send_email=True):
	if request.method == "POST":
		if send_email:
			from django.core.mail import send_mail 
			current_site = Site.objects.get_current() 
		
			subject = render_to_string('registration/password_create_email_subject.txt') 
			# Email subject *must not* contain newlines 
			subject = ''.join(subject.splitlines()) 
			user = request.user
			email_list = [user.email]
			message = render_to_string('registration/password_create_email.txt', 
									   { 'site': current_site, 
										 'url_root': settings.URL_ROOT, 
										 'uid': int_to_base36(user.id), 
										 'user': user, 
										 'token': token_generator.make_token(user) })               
			send_mail(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'), email_list)
		return json_success()
	else:
		return json_error('Invalid request.')

# Changed to no longer be a JSON method - for the password reset link
def password_reset_confirm(request, uidb36=None, token=None, template_name='registration/password_reset_confirm.html',
						   token_generator=default_token_generator, set_password_form=SetPasswordForm,
						   post_reset_redirect=None):
	"""
	View that checks the hash in a password reset link and presents a
	form for entering a new password.
	"""
	assert uidb36 is not None and token is not None # checked by URLconf
	
	if post_reset_redirect is None:
		post_reset_redirect = reverse('django.contrib.auth.views.password_reset_complete')

	try:
		uid_int = base36_to_int(uidb36)
	except ValueError:
		raise Http404

	try:
		user = User.objects.get(id=uid_int)
	except User.DoesNotExist:
		raise Http404

	context_instance = RequestContext(request)

	if token_generator.check_token(user, token):
		context_instance['validlink'] = True
		if request.method == 'POST':
			form = set_password_form(user, request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(post_reset_redirect)
		else:
			form = set_password_form(None)
	else:
		context_instance['validlink'] =  False
		form = None
	context_instance['form'] = form
	return render_to_response(template_name, context_instance=context_instance)

@auth_required
def password_change(request, template_name='registration/password_change_form.html',
					post_change_redirect=None):
	if request.method == "POST":
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			return json_success()
		else:
			return json_result({'form_errors': errors_to_dict(form.errors)})
	else:
		return json_error('Invalid request.')

def wording_change(str):
	return str.replace('username', 'email')

def username_suggest(request):
	if request.method == "GET":
		query = request.GET
		name = query.__getitem__("name")    
		if re.search(r'^\w+$',name):
			return json_result('name: ' + get_next_available_name(name,0))
		else:
			return json_error('Invalid username')
	else:
		return json_error('Invalid request.');                                 

def phrase_change(str):
	return str.replace('Please enter a correct username and password.', 'Please enter a correct password.').replace('Note that both fields are case-sensitive.', 'Note that the password field is case-sensitive.')

# Returns a serializable dictionary of form fields mapping to lists of their errors.
def errors_to_dict(errors):
	if Settings.objects.boolean('USE_ENTRY_CODES'):
		ret_val = dict([(k, [unicode(phrase_change(e)) for e in v]) for k,v in errors.items()])
	else:
		ret_val = dict([(k, [unicode(e) for e in v]) for k,v in errors.items()]) 
	return ret_val

def upload_file(request):
	if request.method == 'POST':
		#form = UploadFileForm(request.POST, request.FILES)
		#if form.is_valid():
		return json_result('url: ' +handle_uploaded_file(request.FILES['Filedata']))
	else:
		return json_error('Invalid request')


def handle_uploaded_file(f):
	m = md5.md5()
	m.update(str(random.random()))
	numericalcode = m.hexdigest() 
	destination = open(ASSETS_LOCAL+numericalcode + f.name, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()

	import Image
	imageFile = ASSETS_LOCAL + numericalcode + f.name
	im1 = Image.open(imageFile)
	im1_size = im1.size

	if im1_size[0] > im1_size[1]:
		width = IMAGE_WIDTH
		height = IMAGE_WIDTH*(im1_size[1]+0.0)/im1_size[0]
	else:
		width = IMAGE_HEIGHT*(im1_size[0]+0.0)/im1_size[1]
		height = IMAGE_HEIGHT

	im2 = im1.resize((width, height), Image.ANTIALIAS)
	im2.save(ASSETS_LOCAL+numericalcode + f.name + '.jpg')
	
	return ASSETS_URL+numericalcode + f.name + '.jpg'

def unsubscribe_notifications(request, uidb36=None, token=None):

	assert uidb36 is not None and token is not None # checked by URLconf
	
	# ensure working uid
	try:
		uid_int = base36_to_int(uidb36)
	except ValueError:
		raise Http404
	
	# ensure user with uid exists
	try:
		user = User.objects.get(id=uid_int)
	except User.DoesNotExist:
		raise Http404
	
	# check email hash matches   
	hasher = ""#hashlib.md5() TODO
	hasher.update(user.email)
	if(token != hasher.hexdigest()):
		raise Http404
   
	# add unsubscribe row if there isn't one in UserData   
	user_data_cache = UserData.objects.filter(user=user, key = 'unsubscribe_notification_updates')
	if user_data_cache.count() == 0:
		user_data_cache = UserData(user=user, key = 'unsubscribe_notification_updates', value='')
		user_data_cache.save()
	
	return render_to_response("unsubscribe.html", context_instance=None)
