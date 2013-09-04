from django import forms
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.template.loader import render_to_string 
from django.utils.http import urlquote, base36_to_int, int_to_base36
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

from opinion.includes.jsonutils import *
from opinion.includes.queryutils import *
from opinion.includes.logutils import *
from opinion.opinion_core.forms import UserDemographicsForm
from opinion.opinion_core.models import *

from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

from opinion.includes.profanityutils import *

import random
import re
import opinion.settings

def password_update(user_to_update,password):
    if len(password) > 0:
        user_to_update.set_password(password)
        user_to_update.save()
        return json_success()
    else:
        return json_error('Blank password not permitted')
            

def location_update(user_to_update,location):
    ud = UserDemographics.objects.filter(user = user_to_update)

    if len(ud) == 0:
        ud = UserDemographics(user = user_to_update)
        ud.location = location
        ud.save()
    else:
        ud[0].location = location
        ud[0].save()

    return json_success()

def heard_about_update(user_to_update,heard_about):
    ud = UserDemographics.objects.filter(user = user_to_update)

    if len(ud) == 0:
        ud = UserDemographics(user = user_to_update)
        ud.heard_about = heard_about
        ud.save()
    else:
        ud[0].heard_about = heard_about
        ud[0].save()

    return json_success()

def username_update(user_to_update, sn):        
    u = user_to_update

    if len(sn.lower()) < MIN_USERNAME_LENGTH or len(sn.lower()) > 30:
        return json_error('Username must be between 3 and 30 characters')

    if not re.search(r'^\w+$',sn):
        return json_error('Invalid Username')

    collisions = User.objects.filter(username = sn.lower())
        
    if len(collisions) > 0 and not sn.lower() == u.username:
        return json_error('Username is taken')            

    code_object = EntryCode.objects.filter(username = u.username)
    
    if len(code_object) > 0:
        code_object[0].username = sn.lower()
        code_object[0].save()
        
    u.username = sn.lower()
    u.save()

    user_settings = UserSettings.objects.filter(user = u, key = 'username_format')

    if len(user_settings) == 0:
        user_settings = UserSettings(user = u, key = 'username_format', value = sn)
    else:
        user_settings = user_settings[0]
        user_settings.value = sn
            
    user_settings.save()

    user_demographics = UserDemographics.objects.filter(user = u)
    
    if len(user_demographics) == 0:
        user_demographics = UserDemographics(user = u)
        user_demographics.save()
            
    return json_success()

def userdata_update(request):
    query = request.POST
    u = request.user
    keys = opinion.settings.USER_DATA_KEYS.keys()

    # Make sure client side sends all values or this breaks
    for k in keys:
        v = query.get(k,'')
        v = v.strip()
        userdata = UserData.objects.filter(user = u, key = k)

        if len(userdata) == 0:
            userdata = UserData(user = u, key = k, value = v)
        else:
            userdata = userdata[0]
            userdata.value = v

        if len(v) > 0:
            userdata.save()
        
    return json_success()

def application_close_helper(request):

	# log end of session
	create_user_event_log(request,{'log_type' : LogUserEvents.sys_exit, 'details' : 'session end'})
	
	# check if view notifications log entry needed
	time_of_last_view_notifications = LogUserEvents.objects.filter(logger_id = request.user.id, log_type = 5, details = 'notificationButton').order_by('created').reverse()
	
	if time_of_last_view_notifications.count() > 0: # tests to see if notifications is open but not closed.
		notifications_properly_closed = LogUserEvents.objects.filter(logger_id = request.user.id, log_type = 5, details = LogUserEvents.notification_detail, created__gte = time_of_last_view_notifications[0].created).count()
		
		if notifications_properly_closed == 0:
			create_user_event_log(request,{'log_type' : 5, 'details' : LogUserEvents.notification_detail})
			