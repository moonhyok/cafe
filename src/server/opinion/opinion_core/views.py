from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.db import connection
from django.http import HttpResponseServerError
from django.http import HttpResponseRedirect

from models import *
from admin import *
from forms import *
from opinion.includes.logutils import *
from opinion.includes.jsonutils import *
from opinion.includes.mathutils import *
from opinion.includes.statsutils import *
from opinion.includes.profanityutils import *
from opinion.includes.queryutils import *
from opinion.includes.smsutils import *
from opinion.includes.accountutils import *
from opinion.settings import *
from opinion.settings_local import DATABASE_ENGINE
from opinion.settings_local import ASSETS_LOCAL
from opinion.settings_local import URL_ROOT
from opinion.settings_local import CONFIGURABLES

from opinion.settings_local import CATEGORIES
from opinion.includes.plotutils import *
from opinion.decorators import *

from django.contrib.auth import authenticate, login
from django.views.decorators.cache import cache_control

import math
import numpy
import operator
import random
import opinion.opinion_core.captcha
import opinion.opinion_core.forms
import pickle
import sys
import urllib
import datetime
import socket
import time
import datetime
import hashlib
from django.core.validators import validate_email
from django.core.exceptions import *
import smtplib

os.environ['MPLCONFIGDIR'] = "/tmp"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    import json
except ImportError:
    import simplejson as json
import os
import re
# Add more boolean logic here if we need more custom queries
if CUSTOM_LEADERBOARD_LISTS or HAVE_ADDITIONAL_QUESTIONS:
	try:
	    from opinion.includes.customutils import *
	except ImportError:
	    print u'File customutils.py is not found. Please add it in order to use custom leaderboard queries.'

#
# HTML Pages
#

def index(request):
    create_visitor(request)
    return render_to_response('app.html', context_instance = RequestContext(request, {'client_settings':get_client_settings()}))

#check if we should display report card for user with entry code( deal with refreshing and revisiting)

def return_user_first_time(request,entrycode):
    if entrycode==None: #first time user
        return False
    else:
        if request.user.is_authenticated():  #valid entry code user
           if request.session['refresh_times']==1: #1 means refresh
              return False
           else:
              return True
        else: 
           return False

def return_zipcode(request):
    if request.user.is_authenticated() and ZipCodeLog.objects.filter(user__exact=request.user).count() > 0:
       return ZipCodeLog.objects.filter(user__exact=request.user)[0].location.code
    else:
       return '0'

@cache_control(no_cache=True)
def mobile(request,entry_code=None):
    create_visitor(request)
    os = get_os(1)
    disc_stmt = get_disc_stmt(os, 1)
    active_users = list(User.objects.filter(is_active=True)) #forces eval so lazy eval doesn't act too smart!!!
    referrallink = request.GET.get('refer','')

    statements = OpinionSpaceStatement.objects.all().order_by('id')
    medians = {}
    statement_labels = {};
    for s in statements:
        medians[str(s.id)] = StatementMedians.objects.filter(statement = s)[0].rating
        if medians[str(s.id)] <= 1e-5:
            medians[str(s.id)] = 0
        statement_labels[str(s.id)] = s.statement
	
    random_username = 'user'+ ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))+'@example.com';
    random_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10));
    num_users = len(active_users)
    su = User.objects.get(id=1)
    external_count = UserData.objects.filter(user = su, key='total_count')
    if external_count.count() > 0:
       num_users = external_count[0].value

    return render_to_response('mobile.html', context_instance = RequestContext(request, {'url_root' : settings.URL_ROOT,
                                                                                         'return_user_first_time':str(return_user_first_time(request,entry_code)).lower(),
                                                                                         'zipcode': str(return_zipcode(request)),
											 'loggedIn' : str(request.user.is_authenticated()).lower(),
											 'change_prompt' : str(request.user.is_authenticated()).lower(),
											 'client_data': mobile_client_data(request),
											 'entry_code': str(entry_code!=None).lower(),
											 'refer': referrallink,
                                             'statement_hist': get_statement_histograms(),
											 'client_settings': get_client_settings(True),
                                             'horizontal_slide': settings.HORIZONTAL_SLIDE,
											 'topic': DiscussionStatement.objects.filter(is_current=True)[0].statement,
											 'short_topic': DiscussionStatement.objects.filter(is_current=True)[0].short_version,
											 'statements': statements,
											 'init_score': len(get_fully_rated_responses(request, disc_stmt)),
											 'random_username': random_username,
											 'random_password': random_password,
											 'num_users': num_users,
                                             'statement_labels': json.dumps(statement_labels),
											 'medians': json.dumps(medians)}))

def confirmation_mail(request):
    email = request.REQUEST.get('mail','')
    try:
      validate_email(email)
    except ValidationError:
      return json_error("Please enter a valid email address or leave it blank to skip.")

    if not request.user.is_authenticated():
        return json_error("Must be authenticated to run this command.")

    if request.user.email == None or len(request.user.email)==0:
        in_use = (User.objects.filter(is_active = True, email = email).count() >= 1)

        if in_use:
            return json_error("This email address is already in use.")

        request.user.email = email
        request.user.save()

        entrycode = hashlib.sha224(email).hexdigest()[0:7]
        ECobject=EntryCode(username=request.user.username,code=entrycode, first_login=False)
        ECobject.save()

        subject = "Your unique link to the California Report Card v1.0"
        email_list = [email]
        message = render_to_string('registration/confirmation_email.txt',
                                        { 'url_root': settings.URL_ROOT, 
										 'entrycode': entrycode,
										 'user_id': request.user.id,
                                          })
        try:
           #send_mail(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'), email_list)
           print 'email'
        except:
           return json_error("We were unable to send an email. Try again later.")

        return json_success()
    else:
        return json_error("You have already submitted an email address.")

def crcstats(request,entry_code=None):

    os = get_os(1)
    disc_stmt = get_disc_stmt(os, 1)
    
    user = None
    
    #Case 1: User is logged in
    if request.user.is_authenticated():
        user = request.user
       
    #Case 2: Entry using a code
    elif entry_code!=None:
        user = authenticate(entrycode=entry_code)
        if user!=None:
           ec = list(EntryCode.objects.filter(code=entry_code))[-1]
           ec.first_login = True
           ec.save()
           login(request,user)
    #Case 3: Testing argument based user id
    else:
        uid = request.GET.get('username',-1)
        user_list = User.objects.filter(id = uid)
        if len(user_list) > 0:
            user = user_list[0]
            

    level8 = (user != None) # Do we have a valid user?

    #initialize scores
    score = 0
    given = 0
    received = 0
    ordinal=''
    comment=''
    uid = -1
    show_hist1=False
    show_hist2=False
    lastVisit=''
    newUser=0
    if level8:
        score = CommentAgreement.objects.filter(rater = user,is_current=True).count()*100 + user_author_score(user)
        given = 2*CommentAgreement.objects.filter(rater = user,is_current=True).count()
        received = 2*CommentAgreement.objects.filter(comment__in = DiscussionComment.objects.filter(user = user),is_current=True).count()
        comment_list=DiscussionComment.objects.filter(user=user,is_current=True)
        if len(comment_list) > 0:
            comment=comment_list[0].comment
            slider1=CommentAgreement.objects.filter(comment=comment_list[0])
            slider2=CommentRating.objects.filter(comment=comment_list[0])
            if len(slider1)>0:
                show_hist1=True
            if len(slider2)>0:
                show_hist2=True

        ordinal = number_to_ordinal(user.id)
        uid = user.id
        lastVisit=user.date_joined.date
        newUser=User.objects.filter(date_joined__gte=lastVisit).count()

    active_users = list(User.objects.filter(is_active = True))

    statements = OpinionSpaceStatement.objects.all().order_by('id')
    medians = []
    for s in statements:
        medians.append({'statement': s.statement,'id':s.id})

    return render_to_response('crc_stats.html', context_instance = RequestContext(request, {'num_participants': len(active_users),
                                                                                            'level8':level8,
                                                                                            'ordinal':ordinal,
                                                                                            'show_hist1':str(show_hist1).lower(),
                                                                                            'show_hist2':str(show_hist2).lower(),
                                                                                            'date':datetime.date.today(),
                                                                                            'comment':comment,
                                                                                            'left_comment': (comment != ''),
                                                                                            'participant': uid,
                                                                                            'entrycode': entry_code,
                                                                                            'uid':uid,
                                                                                            'given': given,
                                                                                            'received': received,
                                                                                            'score': min(score,30000),
                                                                                            'LastVisit': lastVisit,
                                                                                            'newUser':newUser,
                                                                                            'numberRater':received/2,
                                                                                            'num_ratings': CommentAgreement.objects.filter(rater__in = active_users, is_current=True).count()*2,
                                                                                            'url_root' : settings.URL_ROOT,
                                                                                            'medians': medians,
                                                                                            }))

def crc_generic_stats(request):

    os = get_os(1)
    disc_stmt = get_disc_stmt(os, 1)   

    active_users = list(User.objects.filter(is_active = True))

    statements = OpinionSpaceStatement.objects.all().order_by('id')
    medians = []
    for s in statements:
        medians.append({'statement': s.statement, 'id':s.id})

    return render_to_response('crc_generic_stats.html', context_instance = RequestContext(request, {'num_participants': len(active_users),
                                                                                            'date':datetime.date.today(),
                                                                                            'num_ratings': CommentAgreement.objects.filter(rater__in = active_users, is_current=True).count()*2,
                                                                                            'url_root' : settings.URL_ROOT,
                                                                                            'medians': medians,
                                                                                            }))

def app(request, username=None):
	#if request.mobile:
		#return HttpResponseRedirect(URL_ROOT + "/mobile/")
    return mobile(request)
# 	create_visitor(request)
# 	if username != None:
# 		if not Settings.objects.boolean('SOFT_ENTRY_CODES'):
# 			users = User.objects.filter(username = username)
# 			if users.count()==0:
# 				username = NULL_USER_INDICATOR
# 			elif len(DiscussionComment.objects.filter(user = users[0])) == 0:
# 				username = NULL_USER_INDICATOR
# 		return render_to_response('app.html', context_instance = RequestContext(request, {'username': username, 'client_settings':get_client_settings()}))
	#else:
	#	return render_to_response('app.html', context_instance = RequestContext(request, {'client_settings':get_client_settings(),'refer': request.GET.get('refer','')}))

def get_client_settings(dic=False):
	client_settings = {}
	if SEND_CLIENT_SETTINGS:
		for setting in Settings.objects.all():
			if setting.key not in CONFIGURABLES or 'send' not in CONFIGURABLES[setting.key] or CONFIGURABLES[setting.key]['send']:
				client_settings[setting.key] = setting.value
	if not dic: 
	    return json.dumps(client_settings)
	else:
	    return client_settings
	
def about(request):
    return render_to_response('about.html', context_instance = RequestContext(request))

def unavailable(request):
    return render_to_response('unavailable.html', context_instance = RequestContext(request))	

def sample_iframe(request):
	return render_to_response('sample_iframe.html', context_instance = RequestContext(request))

def newcontent(request):
	return render_to_response('newcontent.html', context_instance = RequestContext(request))

def home(request):
	return render_to_response('home.html', {})

def new_content_banner(request):
	return render_to_response('new_content_iframe.html', {})

def solid_nofilter(request):
	return render_to_response('solid_nofilter.html', context_instance = RequestContext(request))
	
def soft_launch(request, username=None):
	if username != None:
		return render_to_response('soft_launch.html', context_instance = RequestContext(request,{'username':username}))
	else:
		return render_to_response('soft_launch.html', context_instance = RequestContext(request))	

#
# Admin panel html pages
# Added by Dhawal M
#

@admin_required
def get_csv_report(request):
    from django.core.servers.basehttp import FileWrapper
    f = open(MEDIA_ROOT + "../report.csv")
    response = HttpResponse(FileWrapper(f), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=report.csv'
    return response

def connect_visitor_to_user(request, user_id):
	visitor_id = request.session.get('visitor_id', False)
	if visitor_id:
		Visitor.objects.filter(id = visitor_id).update(user = user_id)

@admin_required
def get_overview(request):
	total_users = User.objects.all().count()#total number of users
	new_users = User.objects.filter(date_joined__gte=datetime.date.today()).count() #new users
	new_logins_users = User.objects.filter(last_login__gte=datetime.date.today()).count() #activity
	total_visitors = LogUserEvents.objects.filter(details='welcome_first-time',log_type=5).count() #all site visitors
	
	total_comments = DiscussionComment.objects.all().count()
	total_insight = CommentRating.objects.all().count()
	total_agreement = CommentAgreement.objects.all().count()
	
	statements = OpinionSpaceStatement.objects.all()
	result = []
	titles = []
	for sid in statements:
		# get user ratings
		ratings = UserRating.objects.filter(opinion_space_statement = sid, is_current = True)
		raw_vals = [r.rating for r in ratings]
		if len(raw_vals) == 0:
			result.append(0)
		else:
			result.append(numpy.mean(raw_vals))
		titles.append(sid.short_version)
		#result[sid.id]['std'] = numpy.std(raw_vals)

	ud_objects = UserDemographics.objects.all()
	locations = {}
	for u in ud_objects:
		if u.location != '':
			if locations.has_key(u.location):
				locations[u.location] = locations[u.location] + 1
			else:
				locations[u.location] = 1
	locations_pie = []
	location_titles = []
	for k in locations.keys():
		locations_pie.append(locations[k])
		if k == 'United States of America':
			k = 'USA'
		location_titles.append(k)
	
	age_objects = UserData.objects.filter(key='age')
	ages = {}
	for a in age_objects:
		if ages.has_key(a.value):
			ages[a.value] = ages[a.value] + 1
		else:
			ages[a.value] = 1
	
	age_pie = []
	age_titles = []
	for k in ages.keys():
		age_pie.append(ages[k])
		age_titles.append(k)
	
	context_dict = {'total_users':total_users,
					'new_users': new_users,
					'new_logins_users': new_logins_users,
					'total_visitors': total_visitors,
					'total_comments': total_comments,
					'total_insight': total_insight,
					'total_agreement': total_agreement,
					'statements': result,
					'statement_titles': json.dumps(titles),
					'locations':locations_pie,
					'location_titles':json.dumps(location_titles),
					'ages': age_pie,
					'age_titles': json.dumps(age_titles),
					'statements_count': len(result)
					}
	
	return render_to_response('overview.html', context_instance = RequestContext(request,context_dict))

@admin_required
def get_flaggedcomments(request):
	return render_to_response('flaggedcomments.html', context_instance = RequestContext(request))

@admin_required	
def get_blacklisteduser(request):
	return render_to_response('blacklisteduser.html', context_instance = RequestContext(request))

@admin_required	
def get_highvariancecomments(request):
	return render_to_response('highvariance.html', context_instance = RequestContext(request))

@admin_required	
def get_newadditions(request):
	return render_to_response('newadditions.html', context_instance = RequestContext(request))

@admin_required
def get_search(request):
	return render_to_response('search.html', context_instance = RequestContext(request))

@admin_required
def custom_statistics(request):
	if request.method=="POST":
		try:
			d = int(request.POST.get("days", '').strip())
			p = Plotter(path=ASSETS_LOCAL+'statistics/')
			p.start_plot(startDate=datetime.datetime.now()-datetime.timedelta(days=d),  path_segment=str(d)+"days", name=str(d) + "  days", custom=True)
			p.create_plots()
			result = {'name': str(d) + "  days",
				  'path_segment': p.current_plot,
				  'stats':p.stats[p.current_plot]}
			del p.stats[p.current_plot]
			return json_result(result)
		except Exception, e:
			return json_error("Python threw an exception with the following message: " + str(e))

	return json_error("ERROR: You did not enter a valid number, there were no valid data associated with the number you returned, or you did not make a GET request")

@admin_required
def get_statistics(request):	
	comments = DiscussionComment.objects.filter(is_current=True)
	comment_lengths = []
	for c in comments:
		length = len(c.comment.split())
		if length > 5:
			comment_lengths.append(length)
	max_comment = numpy.max(comment_lengths)
	
	comment_read = {}
	view_comment_objects = LogCommentView.objects.filter(is_visitor=False)
	for v in view_comment_objects:
		if comment_read.has_key(v.logger_id):
			comment_read[v.logger_id] = comment_read[v.logger_id] + 1
		else:
			comment_read[v.logger_id] = 1
	comment_read_hist = []
	for k in comment_read.keys():
		comment_read_hist.append(comment_read[k])
	max_comment_read = numpy.max(comment_read_hist)
	visits = {}
	visit_objects = LogUserEvents.objects.filter(log_type=5,details='welcome_sign-in')
	for v in visit_objects:
		if visits.has_key(v.logger_id):
			 visits[v.logger_id] =  visits[v.logger_id] + 1
		else:
			 visits[v.logger_id] = 1
	visits_hist = []
	for k in  visits.keys():
		 visits_hist.append(visits[k])
		
	arc_graph = {}
	users = [ d.user for d in DiscussionComment.objects.filter(is_current=True).exclude(normalized_score_sum=None).order_by('normalized_score_sum').reverse()[:50]]#[r.user for r in ReviewerScore.objects.all().order_by('reviewer_score').reverse()[:50]]
	nodes = [{'nodeName':u.username,'group':1} for u in users]
	links = []
	for r in CommentRating.objects.filter(is_current=True):
		if r.rater in users and r.comment.user in users:
			links.append({'source':(users.index(r.rater)),'target':(users.index(r.comment.user)),'value':r.rating*2})
	arc_graph = {'nodes': nodes, 'links':links}
	
	context_dict = {'word_count': comment_lengths,
					'comment_read': comment_read_hist,
					'visits': visits_hist,
					'arc_graph': json.dumps(arc_graph),
					'max_comment':max_comment,
					'max_comment_read':max_comment_read}
	return render_to_response('statistics.html', context_instance = RequestContext(request,context_dict))

def get_suggestions(request):
	return render_to_response('suggestion.html', context_instance = RequestContext(request))

def get_loginerror(request):
	return render_to_response('loginerror.html', context_instance = RequestContext(request))

@admin_required	
def get_blacklistedcomments(request):
	return render_to_response('blacklistedcomments.html', context_instance = RequestContext(request))

@admin_required	
def get_bannedusers(request):
	import urllib
	import string
	f = urllib.urlopen('http://www.textfixer.com/resources/common-english-words-with-contractions.txt')
	line = f.readline()
	stop_words = line.split(',')
	word_counts = {}
	comments = DiscussionComment.objects.filter(is_current=True)
	for c in comments:
		for w in c.comment.split():
			exclude = set(string.punctuation)
			w = ''.join(ch for ch in w.lower() if ch not in exclude)
			if w not in stop_words and len(w) > 4:
				if word_counts.has_key(w):
					word_counts[w] = word_counts[w] + 1
				else:
					word_counts[w] = 1
	word_list = []
	for k in word_counts.keys():
		word_list.append((word_counts[k],k))
	word_list.sort(reverse=True)
	word_list = word_list[:10]
	return render_to_response('bannedusers.html', context_instance = RequestContext(request,{'word_list':json.dumps([w[1] for w in word_list])}))

@admin_required	
def get_userdetails(request):
	comment_ratings = CommentRating.objects.filter(is_current=True).order_by("?")[:2500]
	ratings_scatter = []
	for cr in comment_ratings:
		comment_agreement = CommentAgreement.objects.filter(is_current=True,comment=cr.comment,rater=cr.rater)
		if len(comment_agreement) > 0:
			ratings_scatter.append({'x': cr.rating, 'y':comment_agreement[0].agreement,'z':10})
	context_dict = {'ratings_scatter': ratings_scatter}
	return render_to_response('userdetails.html', context_instance = RequestContext(request,context_dict))
#End of Dhawal's additions

@admin_required
def get_subgroupplot(request):
	users = User.objects.all()
	points = []
	sampling = []
	agreement = []
	eigenvector1 = OpinionSpaceEigenvector.objects.filter(is_current=True,eigenvector_number=0)
	eigenvector2 = OpinionSpaceEigenvector.objects.filter(is_current=True,eigenvector_number=1)
	max_x = 0
	max_y = 0
	min_x = 0
	min_y = 0
	
	for u in users:
		ratings = UserRating.objects.filter(user=u,is_current=True).order_by('opinion_space_statement')
		if len(ratings) == len(eigenvector1):
			x = 0
			for i in range(0,len(ratings)):
				x = x + ratings[i].rating*eigenvector1[i].value
			y = 0
			for i in range(0,len(ratings)):
				y = y + ratings[i].rating*eigenvector2[i].value	
			comment = DiscussionComment.objects.filter(is_current=True,user=u)
			score = -1
			sample = 10
			a_score = -1
			if len(comment) > 0 and comment[0].normalized_score_sum != None:
				score = 50*comment[0].normalized_score_sum
				if score < 30:
					score = score/2
			if len(comment) > 0 and comment[0].query_weight != None:
				sample = 10*comment[0].query_weight
			if len(comment) > 0:
				agreements = CommentAgreement.objects.filter(comment = comment[0])
				raw_values = [a.agreement for a in agreements]
				a_score = numpy.mean(raw_values)*52
				if a_score < 40:
					a_score = a_score/4
			if x < min_x:
				min_x = x
			if x > max_x:
				max_x = x
			if y < min_y:
				min_y = y
			if y > max_y:
				max_y = y
			score = max(score,1)
			if score > 0 and len(agreements) >= 2:
				points.append({'x':x,'y':y,'z':score})
			sampling.append({'x':x,'y':y,'z':sample})
			if a_score > 0 and len(agreements) >= 5:
				agreement.append({'x':x,'y':y,'z':a_score})
	context_dict = {'all_points':json.dumps(points),
					'sampling':json.dumps(sampling),
					'agreement':json.dumps(agreement),
					'max_x':max_x,
					'max_y':max_y,
					'min_x':min_x,
					'min_y':min_y}
	return render_to_response('subgroup.html', context_instance = RequestContext(request,context_dict))


#
# Admin panel methods
#
def find_seconds(td):
	return float(td.days*24*3600 + td.seconds)

@admin_required
def configure_client(request):
	if not SHOW_ADVANCED_OPTIONS:
		return HttpResponse("Access Denied By Server Configuration", status = 403)
	updated = None
	if request.method == 'POST':
		for key in request.POST:
			if key in CONFIGURABLES:
				setting = Settings.objects.get_or_create(key=key)[0]
				setting.value= escape_settings(request.POST[key])
				setting.save()
				updated = True
	for setting in Settings.objects.all():
		if setting.key in CONFIGURABLES:
			CONFIGURABLES[setting.key]['default'] = setting.value
	form = ConfigurationForm().create_form(CONFIGURABLES)	
	return render_to_response('configuration.html', context_instance = RequestContext(request, {'form':form, 'saved':updated, 'categories':CATEGORIES}))

def seed_client(request):
	updated = None
	if request.method == 'POST':
		for key in request.POST:
			id = int(key.split()[1])+1
			d = DiscussionComment.objects.filter(user=User.objects.filter(id=id)[0],is_current=True)[0]
			d.comment = request.POST.get(key,'')
			d.save()
			updated = True

	d1 = DiscussionComment.objects.filter(user=User.objects.filter(id=2)[0],is_current=True)[0]
	d2 = DiscussionComment.objects.filter(user=User.objects.filter(id=3)[0],is_current=True)[0]
	d3 = DiscussionComment.objects.filter(user=User.objects.filter(id=4)[0],is_current=True)[0]
	d4 = DiscussionComment.objects.filter(user=User.objects.filter(id=5)[0],is_current=True)[0]
	
	form = SeedForm().create_form([d1.comment,d2.comment,d3.comment,d4.comment])	
	return render_to_response('seed.html', context_instance = RequestContext(request, {'form':form, 'saved':updated}))
	
@admin_required
def install_client(request):
	if not SHOW_ADVANCED_OPTIONS:
		return HttpResponse("Access Denied By Server Configuration", status = 403)
	updated = None
	if request.method == 'POST':
		for key in request.POST:
			if key == 'Discussion Question':
				question = DiscussionStatement.objects.filter(is_current=True)[0]
				question.statement = request.POST[key]
				question.save()
			elif key == 'Discussion Question Short':
				question = DiscussionStatement.objects.filter(is_current=True)[0]
				question.short_version = request.POST[key]
				question.save()
			else:
				statement = OpinionSpaceStatement.objects.filter(id=key)
				if len(statement) > 0:
					statement[0].statement = request.POST[key]
					statement[0].save()
		updated = True
	data = []
	data.append({'type': 'question','text':DiscussionStatement.objects.filter(is_current=True)[0].statement})
	data.append({'type': 'squestion','text':DiscussionStatement.objects.filter(is_current=True)[0].short_version})
	statements = OpinionSpaceStatement.objects.all()
	for s in statements:
		data.append({'type': 'statement','text':s.statement,'id': s.id})
	form = InstallForm().create_form(data)	
	return render_to_response('install.html', context_instance = RequestContext(request, {'form':form, 'saved':updated, 'categories':CATEGORIES}))

@admin_required
def proof_read_comments(request):
    cid = request.REQUEST.get('cid',-1)
    language = request.REQUEST.get('language', 'english')
    updated = None
    if request.method == 'POST':
        for key in request.POST:
            if key != 'language':
                query = DiscussionComment.objects.filter(id=key)
                if len(query) == 0:
                    return HttpResponse("This comment does not exist", status = 404)
                else:
                    if language == 'english':
                        query[0].comment = request.POST[key]
                    else: # we will return here to implement MANDARIN
                        query[0].spanish_comment = request.POST[key]
                    if query[0].original_language == language: # Sets the translation_is_reviewed flag to True if the comment we are editing and 
                        query[0].translation_is_reviewed = True
                    query[0].save()
                    updated = True
                    cid = key

    if cid == -1:
        return HttpResponse("This comment does not exist", status = 404)
    else:
        query = DiscussionComment.objects.filter(id=cid)
        if len(query) == 0:
            return HttpResponse("This comment does not exist", status = 404)
        data = []
        if language == 'english':
            data.append({'type': cid,'text':query[0].comment, 'language': language})
        else: # we will return here
            data.append({'type': cid,'text':query[0].spanish_comment, 'language' : language})

        form = ProofreadForm().create_form(data)    
        return render_to_response('proofread.html', context_instance = RequestContext(request, {'form':form, 'saved':updated}))
        
def manual_login(request, user):
    connect_visitor_to_user(request, user.id)
    request.session['user_id'] = user.id
    request.session['_auth_user_id'] = user.id
    request.session['_auth_user_backend'] = 'opinion.email-auth.EmailOrUsernameModelBackend'

def connect_visitor_to_user(request, user_id):
    visitor_id = request.session.get('visitor_id', False)
    if visitor_id:
        Visitor.objects.filter(id = visitor_id).update(user = user_id)

def admin_panel_login(request):
	if request.user.is_authenticated():
		adminuser = AdminPanelUser.objects.filter(user = request.user.id)
		if len(adminuser) > 0 or request.user.id == 1:
			return HttpResponseRedirect(URL_ROOT+'/adminpanel/overview/')
	fail = None
	if request.method == 'POST':
		username = request.POST.get('Username','')
		password = request.POST.get('Password','')
		user = User.objects.filter(username = username)
		if len(user) > 0:
			if user[0].check_password(password):
				manual_login(request,user[0])
				return HttpResponseRedirect(URL_ROOT+'/adminpanel/overview/')
			else:
				fail = True
		else:
			fail = True
	form = AdminPanelLoginForm().create_form(None)	
	return render_to_response('aplogin.html', context_instance = RequestContext(request, {'form':form,'fail':fail}))
	
# only escaping double quotes for now
def escape_settings(value):
	segments = value.split('"')
	result = segments[0]
	for i in range(1, len(segments)):
		if result[-1] != '\\':
			result = result +'\\\"'+ segments[i]
		else:
			result = result + '"'+segments[i]
	return result

#@admin_required
def get_subgroup_data(request):
  s = ASSETS_LOCAL+'statistics/subgroup.pkl'
  if os.path.isfile(s):
      data = pickle.load(open(s, 'r'))
      return json_result({'success': True, 'data': data})
  else:
  	  return json_result({'success': False})

#@admin_required
def get_adminpanel_stats(request, timeperiod):

  s=ASSETS_LOCAL+'statistics/data.pkl'
  plotdata= pickle.load(open(s,"r"))
  #plotdata[timeperiod]['last_updated'] = '2000-02-06'
  #plotdata[timeperiod]['start_date'] = '2000-02-06'
#  plotdata[timeperiod]['end_date'] = '2000-02-06'
  return json_result({'success':True, 'data':plotdata[timeperiod]})


#@admin_required
def get_admin_content(request, os_id, disc_id=None):
	try:
		os = OpinionSpace.objects.get(pk = os_id)
	except OpinionSpace.DoesNotExist:
		return json_result({'success':False, 'error_message':'This opinion space does not exist.'})

	#Retrieve the discussion statement matching disc_id, if we cant find it, default to the current one.
	discussion_statement = None
	if disc_id != None:
		discussion_statement = os.discussion_statements.filter(pk=disc_id)
		if len(discussion_statement)>0:
			discussion_statement = discussion_statement[0]
		else:
			discussion_statement = None
	if discussion_statement == None:
		discussion_statement = os.discussion_statements.get(is_current = True) 
	
	params = request.REQUEST
	requested_keys = params.get('request', {})
	if requested_keys != {}:
		requested_keys = requested_keys.split(",")
	
	requested_data = {}
	
	if requested_key_apc("unapproved", requested_keys):
		# Retrieve unapproved comments
		unapproved, unapproved_oneday, unapproved_twodays, unapproved_alltime = get_unapproved_comments_apc(os, discussion_statement)
		requested_data["unapproved"] = unapproved
		requested_data["unapproved_oneday"] = unapproved_oneday
		requested_data["unapproved_twodays"] = unapproved_twodays
		requested_data["unapproved_alltime"] = unapproved_alltime
			
	if requested_key_apc("flagged_comments", requested_keys):
		# Retrieve the flagged comments
		requested_data["flagged_comments"] = get_flagged_comments_apc(discussion_statement)
	
	if requested_key_apc("high_variance_comments", requested_keys):
		# Retrieve high variance comments (comments with low confidence i.e. SE >= .15)
		requested_data["high_variance_comments"] = get_high_variance_comments_apc(os, discussion_statement)
	
	if requested_key_apc("new_comments_prev_bl", requested_keys):
		# Retrieve new comments from previously blacklisted responses
		requested_data["new_comments_prev_bl"] = get_new_comments_from_previously_blacklisted_apc(os, discussion_statement)
	
	if requested_key_apc("feedback", requested_keys):
		# Retrieve feedback
		requested_data["feedback"] = get_feedback_apc()
	
	if requested_key_apc("statistics", requested_keys):
		# Retrieve statistics
		requested_data["statistics"] = get_statistics_apc(os, discussion_statement)
	
	if requested_key_apc("blacklisted_comments", requested_keys):
		# Retrieve blacklisted comments	
		requested_data["blacklisted_comments"] = get_blacklisted_comments_apc(os, discussion_statement)
	
	if requested_key_apc("banned_users", requested_keys):
		# Retrieve banned users
		requested_data["banned_users"] = get_banned_users_apc()
	
	if requested_key_apc("button_stats", requested_keys):
		# Retrieve button stats
		requested_data["button_stats"] = get_button_stats_apc()

	if requested_key_apc("suggestions", requested_keys):
		# Retrieve suggestion stats
		requested_data["suggestions"] = get_suggestion_stats_apc(os, discussion_statement)

	if requested_key_apc("statements", requested_keys):
		# Retrieve statements stats
		requested_data["statements"] = get_statements_stats_apc(os)

	# Always retrieving discussion statements
	requested_data["discussion_statements"] = get_discussion_statements_apc(os)
	
   	return json_result({'success':True, 'data':requested_data})

def requested_key_apc(key, request):
	return key in request or 'all' in request
		
def get_button_stats_apc():
	button_total = 0
	button_count = {}
	button_press = LogUserEvents.objects.filter(log_type=5)

	for log in button_press:
		name = log.details
		if name in button_count:
			button_count[name] += 1
		else:
			button_count[name] = 1
		button_total += 1

	for k,v in button_count.items():
		button_count[k] = (1.0*v)/button_total * 100

	button_stats = sorted(button_count.items(), key=(lambda x: x[1]))
	button_stats.reverse()
	return button_stats

def get_suggestion_stats_apc(os, discussion_statement):
	suggestions = Suggestion.objects.filter(comment__discussion_statement = discussion_statement)
	num_suggestions = suggestions.count()
	suggestion_q = [s.q for s in suggestions.filter(q__isnull=False)]
	suggestions_rated = len(suggestion_q)
	if num_suggestions != 0:
		percent_rated = 100.0*len(suggestion_q)/num_suggestions
	else:
		percent_rated = 0
	average_num_suggestions = 1.0*num_suggestions/User.objects.count()
	
	average = numpy.mean(suggestion_q)
	stdev = numpy.std(suggestion_q)
	
	return {'num_suggestions':num_suggestions, 
			'percent_rated':percent_rated, 
			'num_suggestions_rated':suggestions_rated,
			'num_suggestions_per_user':average_num_suggestions,
			'std':stdev,
			'avg':average,
			'values':suggestion_q,
			}

def get_discussion_statements_apc(os):
	disc_stmt_objs = []
	discussion_statements = os.discussion_statements.all()
	for disc in discussion_statements:
		disc_stmt_objs.append({'id': disc.id, 'is_current': disc.is_current, 'statement':disc.statement, 'short':disc.short_version})
	return disc_stmt_objs

def get_banned_users_apc():
	banned_users = []
	banned_objs = BanishedUser.objects.all()
	for bu in banned_objs:
		banned_users.append(format_user_object(bu.user, os_id))
	return banned_users

def get_blacklisted_comments_apc(os, discussion_statement):
	blacklist_filter = os.comments.filter(is_current = True, discussion_statement = discussion_statement, blacklisted = True).order_by('-created')
	blacklisted_comments = []
	for comment in blacklist_filter:
		if not_admin_approved(comment):
			blacklisted_comments.append(format_general_discussion_comment(comment))
	return blacklisted_comments

def get_statistics_apc(os, discussion_statement):
	if Settings.objects.boolean('USE_ENTRY_CODES'):
		new_users = len(UserData.objects.filter(key = 'first_login', updated__gte = datetime.date.today()))
		total_active_users = len(EntryCode.objects.filter(first_login = False))
		total_users = User.objects.count()
		num_responses = os.comments.filter(is_current = True, discussion_statement = discussion_statement).count()
		response_rate = (1.0*num_responses)/total_users * 100
		statistics = {'new_users':new_users,
			      'total_active_users':total_active_users,
			      'total_users': total_users,
			      'num_responses': num_responses,
			      'response_rate': response_rate}
	else:
		new_users = len(User.objects.filter(date_joined__gte = datetime.date.today()))
		total_active_users = User.objects.count()
		
		facebook_users = [fc.user for fc in ForeignCredential.objects.filter(foreignid__endswith='facebook')]
		num_facebook_users = len(facebook_users)
		facebook_emails = UserData.objects.filter(user__in = facebook_users, key='email').count()
		num_twitter_users = ForeignCredential.objects.filter(foreignid__endswith='twitter').count()
		
		statistics = {'new_users':new_users,
			      	  'total_active_users':total_active_users,
			      	  'num_facebook_users':num_facebook_users,
			      	  'num_facebook_emails':facebook_emails,
			      	  'num_twitter_users':num_twitter_users,
			      	  }
	return statistics

def get_feedback_apc():
	feedback_filter = Feedback.objects.filter(created__gte = datetime.date.today())
	feedback = []
	for f in feedback_filter:
		username = ''
		email = ''
		if f.user != None:
			username = f.user.username
			email = f.user.email
		feedback.append({'username':username, 'email':email, 'date': f.created, 'response':f.feedback})
	return feedback

def get_new_comments_from_previously_blacklisted_apc(os, discussion_statement):
	blacklist_filter = os.comments.filter(is_current = False, discussion_statement = discussion_statement, blacklisted = True)
	new_comments_prev_bl = []
	for comment in blacklist_filter:
		new_comment_filter = os.comments.filter(is_current = True, blacklisted = False, discussion_statement = discussion_statement, user = comment.user)
		if len(new_comment_filter) != 0:
			if new_comment_filter[0] not in new_comments_prev_bl:
				# There may be dulplicates if a user has had more than one blacklisted comment
				if not_admin_approved(new_comment_filter[0]):
					new_comments_prev_bl.append(format_general_discussion_comment(new_comment_filter[0]))
	return new_comments_prev_bl

def get_high_variance_comments_apc(os, discussion_statement):
	high_variance_filter = os.comments.filter(is_current = True, blacklisted = False, discussion_statement = discussion_statement).order_by('-confidence')[:20]
	high_variance_comments = []
	for comment in high_variance_filter:
		if not_admin_approved(comment):
			high_variance_comments.append(format_general_discussion_comment(comment))
	return high_variance_comments

def get_flagged_comments_apc(discussion_statement):
	flagged = FlaggedComment.objects.all()
	flagged_comments = []
	hashCount = {}
	added = {}
	for f in flagged:
		if f.comment.discussion_statement == discussion_statement:
			if hashCount.has_key(f.comment.id):
				hashCount[f.comment.id] += 1
			else:
				hashCount[f.comment.id] = 1
			added[f.comment.id] = False
	for f in flagged:
		if f.comment.discussion_statement == discussion_statement:
			if not_admin_approved(f.comment):
				if not f.comment.blacklisted:
					if not added[f.comment.id]:
						temp_dict = format_general_discussion_comment(f.comment)
						temp_dict['num_flags'] = hashCount[f.comment.id]
						flagged_comments.append(temp_dict)
						added[f.comment.id] = True
	return flagged_comments

def get_unapproved_comments_apc(os, discussion_statement):
	# Retrieve the unapproved comments that are less than a week old within the top 20 comments
	top_comments = os.comments.filter(is_current = True, discussion_statement = discussion_statement, blacklisted = False, confidence__lte = Settings.objects.float('CONFIDENCE_THRESHOLD'), confidence__isnull = False).order_by('-normalized_score_sum')[0:20]
	unapproved = []
	unapproved_oneday = []
	unapproved_twodays = []
	unapproved_alltime = []
	
	for comment in top_comments:
		if comment.created.date() >= datetime.date.today() - datetime.timedelta(days=7):
			if not_admin_approved(comment):
				unapproved.append(format_general_discussion_comment(comment))
		if comment.created.date() >= datetime.date.today() - datetime.timedelta(days=1):
			if not_admin_approved(comment):
				unapproved_oneday.append(format_general_discussion_comment(comment))
		if comment.created.date() >= datetime.date.today() - datetime.timedelta(days=2):
			if not_admin_approved(comment):
				unapproved_twodays.append(format_general_discussion_comment(comment))
		if not_admin_approved(comment):
				unapproved_alltime.append(format_general_discussion_comment(comment))
	return unapproved, unapproved_oneday, unapproved_twodays, unapproved_alltime

def get_statements_stats_apc(os):
	result = {}
	statements = os.statements.all()
	for sid in statements:
		# get user ratings
		ratings = UserRating.objects.filter(opinion_space_statement = sid, is_current = True)
		raw_vals = [r.rating for r in ratings]
		result[sid.id] = {}
		result[sid.id]['mean'] = numpy.mean(raw_vals)
		result[sid.id]['std'] = numpy.std(raw_vals)
	return result

@admin_required
def approve_comment(request, comment_id):
	
	"""
	
	A comment that is unapproved or flagged may still show up in the top authors; only blacklisted
	comments or comments from banished users are prevented from showing up
	
	"""
	
	comment = AdminApprovedComment.objects.filter(comment = comment_id)
	if len(comment) != 0:
		return json_result({'success':False, 'error_message':'Comment already approved.'})
	else:
		try:
			comment = DiscussionComment.objects.get(id = comment_id)
		except DiscussionComment.DoesNotExist:
			return json_result({'success':False, 'error_message':'Comment does not exist.'})
			
		approved_comment = AdminApprovedComment(comment = comment, admin = request.user) 
		approved_comment.save()
		return json_result({'success':True})


@admin_required
def admin_tag_comment(request, comment_id):
    comment = DiscussionComment.objects.filter(id = comment_id)
    if not len(comment) == 1:
        return json_result({'success':False, 'error_message':'Comment does not exist'})

    new_tag = request.REQUEST.get('tag', '')
    comment=comment[0]
    existing_tags = AdminCommentTag.objects.filter(comment=comment)


    if existing_tags:
        existing_tags.update(tag=new_tag)
        return json_result({'success':True})
    else:
        a = AdminCommentTag(comment=comment, tag=new_tag)
        a.save()
        return json_result({'success':True})     

@admin_required
def blacklist_comment(request, comment_id):
	comment = DiscussionComment.objects.filter(id = comment_id)
	if not len(comment) == 1:
		return json_result({'success':False, 'error_message':'Comment does not exist'})
	else:
		comment.update(blacklisted = True)
		return json_result({'success':True})

@admin_required		
def unblacklist_comment(request, comment_id):
	comment = DiscussionComment.objects.filter(id = comment_id)
	if not len(comment) == 1:
		return json_result({'success':False, 'error_message':'Comment does not exist'})
	else:
		comment.update(blacklisted = False)
		return json_result({'success':True})

@admin_required
def banish_user(request, user_id):
	banished = BanishedUser.objects.filter(user = user_id)
	if len(banished) != 0:
		return json_result({'success':False, 'error_message':'User already banished.'})
	else:
		try:
			user = User.objects.get(id = user_id)
		except User.DoesNotExist:
			return json_result({'success':False, 'error_message':'User does not exist.'})
			
		banished_user = BanishedUser(user = user, banisher = request.user) 
		banished_user.save()
		
		# Blacklist all the user's comments **WARNING** this is irreversible
		comment_filter = DiscussionComment.objects.filter(user = user).update(blacklisted = True)
		
		return json_result({'success':True})
		
#@admin_required
def search(request, os_id, username=''):

    user = User.objects.filter(username__icontains= username)
    if not len(user):
      return json_result({'success':False, 
                          'error_message':'No users matching that username.'})

    comments = []
    for u in user:
        comments.extend(list(DiscussionComment.objects.filter(user=u, is_current=True, blacklisted=False)))
	
    #return json_result({'success':True, 
    #                    'data':[format_user_object(u, os_id) for u in user]})

    return json_result({'success':True, 'data':[format_general_discussion_comment(c) for c in comments]})

	
@admin_required
def get_new_users(request, os_id, time):
	return json_result({'success':True, 'data':get_new_users_since(int(time), os_id)})

# End admin panel methods
	
"""
def contact(request):
    if request.method == 'POST':
        # Check the captcha
        check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
        if check_captcha.is_valid is False:

            return json_error()
        form = ContactForm(request.POST)
        if form.is_valid():
            return json_success()
    else:
        form = ContactForm()
        html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)
    return render_to_response('contact.html', {'form': form, 'html_captcha': html_captcha})
"""

def feedback(request):
    text = request.REQUEST.get('feedback', '').strip()
    
    length = len(text)
    if length < FEEDBACK_MIN_LENGTH or length > FEEDBACK_MAX_LENGTH:
        return json_error('Please enter feedback that is between %d and %d characters.' % (FEEDBACK_MIN_LENGTH, FEEDBACK_MAX_LENGTH))
    
    # Store in database
    fb = Feedback(feedback = text)
    if request.user.is_authenticated():
        fb.user = request.user
    fb.save()
    
    # Send out an email
    send_mail(FEEDBACK_EMAIL_SUBJECT,
              text,
              Settings.objects.string('FEEDBACK_EMAIL_FROM'),
              [FEEDBACK_EMAIL_TO],
              fail_silently = True)
    
    return json_success()

def suggestion(request):
	os_name = request.REQUEST.get('opinionspace_name')
	p1 = request.REQUEST.get('proposition1', '')
	p2 = request.REQUEST.get('proposition2', '')
	# These are optional, they might be empty strings
	p3 = request.REQUEST.get('proposition3', '')
	p4 = request.REQUEST.get('proposition4', '')
	p5 = request.REQUEST.get('proposition5', '')
	discussion_statement = request.REQUEST.get('discussionstatement1', '')
	landmarks = request.REQUEST.get('landmarknames', '')
	print os_name
	print p1
	print p2
	print p3
	if p4 != "":
		print p4
	if p5 != "":
		print p5
		
	print request.user
	print request.user.is_authenticated()
	
	# Save to the model
	new_suggestion = Suggestion(opinionspace_name = os_name, 
								proposition1 = p1, 
								proposition2 = p2, 
								proposition3 = p3, 
								proposition4 = p4, 
								proposition5 = p5, 
								discussionstatement1 = discussion_statement, 
								landmarknames = landmarks)
	
	if request.user.is_authenticated():
		new_suggestion.user = request.user
	new_suggestion.save()
	
	return json_success()

#
# Logging methods
#

def log_http_error(request):
	return create_http_error_log(request)

def log_user_event(request):
	return create_user_event_log(request)

def log_comment_view(request):
	return create_comment_view_log(request)

def log_landmark_view(request):
    logger_id, is_visitor = get_logger_info(request)
    
    args = request.REQUEST
    
    try:
        os_id = int(args.get('os_id', ''))
        landmark_id = int(args.get('landmark_id', ''))
    except ValueError:
        return json_error('Invalid parameters')
    
    landmark_name = args.get('landmark_name', None)
    if landmark_name == None:
        return json_error('Invalid landmark name')
    
    return json_success()

#
# JSON pages
#
def os_list(request):
    return json_result(tuple(OpinionSpace.objects.all().values_list('id', 'name')))

def os_test_auth(request):
    return json_result({'is_user_authenticated': request.user.is_authenticated()})

def os_show(request, os_id, disc_stmt_id = None):
    """
	
	Returns the state variables required for the creation of an Opinion Space or
	a system refresh of the space.
	
    """

	# Obtain a reference to the os
    try:
    	os = get_os(os_id)
    except QueryUtilsError, q:
    	return json_error(q.error_message)

    name = os.name
    statements_objects = os.statements.all()
    statements = []
	#.values_list('id', 'statement', 'short_version'))
	
    for s in statements_objects:
        statements.append((s.id,s.statement,s.short_version,
                           numpy.median(UserRating.objects.filter(opinion_space_statement=s,is_current=True).values_list('rating'))))

	# Get all discussion statements for the selected Opinion Space
    current_disc_stmt = None
    disc_stmt_objs = []
    discussion_statements = DiscussionStatement.objects.filter(opinion_space = os)
    for disc in discussion_statements:
		# Get a reference to the selected discussion statement
		if disc_stmt_id == None:
			if disc.is_current == True:
				current_disc_stmt = disc
		else:
			if disc.id == int(disc_stmt_id):
				current_disc_stmt = disc
		
		disc_stmt_objs.append({'id': disc.id, 'is_current': disc.is_current, 'statement':disc.statement, 'short':disc.short_version})
	
    if current_disc_stmt == None:
    	if TEMP_DEBUG_LOGGING:
    		TEMP_DEBUG_FILE.write(json_error('That discussion statement does not exist.').content)
    		TEMP_DEBUG_FILE.close()
    	return json_error('That discussion statement does not exist.')

    eigenvectors = tuple(os.eigenvectors.filter(is_current = True).values_list('eigenvector_number', 'coordinate_number', 'value')[:2*len(statements)])
    
    if request.user.is_authenticated():
        ratings = tuple(os.ratings.filter(user = request.user, is_current = True).values_list('opinion_space_statement', 'rating')[:len(statements)])

	comment_filter = os.comments.filter(user = request.user, is_current = True, discussion_statement = current_disc_stmt)
        comment_filter_nc = os.comments.filter(user = request.user,discussion_statement = current_disc_stmt)
        comment = tuple(comment_filter.values_list('comment')[:1])
        comment_score = tuple([[0]])
		
        if len(comment_filter) > 0:
            comment_score = tuple([[numpy.sum(CommentRating.objects.filter(comment__in=comment_filter_nc,is_current=True).values_list('rating'))]])
			
        normalized_score = tuple(comment_filter.values_list('normalized_score_sum')[:1])
        
        # Get suggestion score
        suggestion_score_object = SuggesterScore.objects.filter(user = request.user)
        if suggestion_score_object.count() > 0:
        	suggestion_score_sum = suggestion_score_object[0].score_sum
        else:
        	suggestion_score_sum = 0
        
        # Get previous revisions
        prev_comments = get_revisions_and_suggestions(request.user, os, current_disc_stmt)
        
        # Get user settings
        db_settings = UserSettings.objects.filter(user = request.user)
        
        settings_dict = {}
        for setting in db_settings:
            settings_dict[setting.key] = setting.value
        
        for key in USER_SETTINGS_META:
            if not settings_dict.has_key(key):
                settings_dict[key] = USER_SETTINGS_META[key]['default']
        
        # Get the reviewer score for the user
        reviewer_score = ReviewerScore.objects.filter(user = request.user)
        if len(reviewer_score) != 0:
			reviewer_score = reviewer_score[0].reviewer_score
        else:
			reviewer_score = 0
		
		# Return the username, location, and id
        user_name = request.user.username

        try: #empty OS
            user_location = UserDemographics.objects.filter(user = request.user).values_list('location')[:1][0][0]
        except IndexError:
            user_location = None
            
        user_id = request.user.id
        user_data = get_user_data(request.user)

		# Return if additional questions are finished
        finished_additional_questions = False
        if HAVE_ADDITIONAL_QUESTIONS:
        	finished_additional_questions = additional_questions_finished(request.user)

		# Get num fully rated comments for current disc question
        num_fully_rated = 0
        num_fully_rated += len(get_fully_rated_responses(request, current_disc_stmt))
    else:
        ratings, comment, comment_score, normalized_score, settings_dict, reviewer_score, rated_by_ids, user_name, user_location, user_id, finished_additional_questions, num_fully_rated, prev_comments, suggestion_score_sum = [], [], [], [], {}, 0, [], "", "", 0, False, 0, [], 0

        user_data = {}			
    
	# Get the filterable keys
    filterable_keys = {}
    for key in USER_DATA_KEYS:
		if USER_DATA_KEYS[key]['filterable']:
			filterable_keys[key] = USER_DATA_KEYS[key]['possible_values']
    bg_points = []	
    bg = request.REQUEST.get('background_points', False)
    if bg:
    	bg_points = get_background_points(request, os, Settings.objects.int('NUM_BACKGROUND_POINTS'))

    # Get adminpanel users
    adminpanel_uids = []
    for apu in AdminPanelUser.objects.all():
    	adminpanel_uids.append(apu.user.id)

    # Total number of users
    if Settings.objects.boolean('USE_ENTRY_CODES'):
    	num_users_total = EntryCode.objects.filter(first_login = False)
    	num_users_total = len(num_users_total)
    else:
    	num_users_total = User.objects.count()

    # Total number of responses (across all discussion statements)
    total_ideas = User.objects.all().count()#DiscussionComment.objects.filter(is_current = True, opinion_space = os, blacklisted = False).count()
    
	# Log the user's loading of the space if logged in
	# - For notifications, to track the last time the user was present
	# - TODO: Save state of the user to enable replaying the space
    if request.user.is_authenticated():
    	create_user_event_log(request, {"log_type": LogUserEvents.sys_load})

    now = datetime.datetime.utcnow()
    date_dict = {'month': now.month, 'day': now.day, 'year': now.year, 'hour': now.hour, 'minute': now.minute}
	
    if request.user.is_authenticated():
        cur_comment_id = DiscussionComment.objects.filter(user = request.user, is_current = True).order_by('-created')
        if len(cur_comment_id) > 0:
            cur_comment_id = cur_comment_id[0].id
        else:
            cur_comment_id = -1	
    else:
            cur_comment_id = -1    
    
    result = {'name': name,
              'statements': statements,
              'discussion_statements': disc_stmt_objs,
              'eigenvectors': eigenvectors,
              'cur_user_ratings': ratings,
              'cur_user_comment': comment,
              'prev_comments': prev_comments,
              'cur_user_settings': settings_dict,
              'cur_user_comment_score': comment_score,
              'cur_user_normalized_score': normalized_score,
              'cur_user_rater_score': reviewer_score,
              'cur_user_suggester_score':suggestion_score_sum,
              'cur_username':user_name,
              'cur_user_id':user_id,
              'cur_user_location': user_location,
              'is_user_authenticated': request.user.is_authenticated(),
              'num_users_total': num_users_total,
              'total_ideas': total_ideas,
              'user_data': user_data,
	      	  'filterable_keys': filterable_keys,
              'background_points': bg_points,
			  'finished_additional_questions': finished_additional_questions,
			  'num_fully_rated': num_fully_rated,
			  'adminpanel_uids': adminpanel_uids,
	      'never_seen_comments': os_never_seen_comments_json(request,os_id,disc_stmt_id),
              'cur_comment_id': cur_comment_id,
			  'date' : date_dict}

    return json_result(result)

@auth_required
def os_all_current_comments(request, os_id, disc_stmt_id = None):
	"""
	Returns all the current comments in the system for the lens interface
	"""
							
	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
		disc_stmt = get_disc_stmt(os, disc_stmt_id)
	except QueryUtilsError, q:
		return json_error(q.error_message)
		
	all_comments = get_all_current_comments(request, os, disc_stmt)
	
	# Get the user ratings
	uids = []
	for comment in all_comments:
		uids.append(comment['uid'])
	user_ratings = get_user_ratings(request, os, uids)
		
	# Get user data
	user_data = {}
	for tup in user_ratings:
		data = get_user_data(tup[0])
		if len(data) > 0:
			user_data[tup[0]] = data	

	# create log
	#create_comments_returned_log(request, os, all_comments, LogCommentsReturned.all)

	#return JSON
	return json_result({'comments':all_comments,
						'ratings': user_ratings,
						'user_data': user_data,
						'sorted_comments_ids': sort_by_response_score(all_comments),
						'sorted_avg_agreement':sort_by_avg_agreement(all_comments)})	

@auth_required
def os_unrated_comments(request, os_id, disc_stmt_id = None):

	"""
	Returns the dots the user has not rated split into two categories: high and low confidence.
	
	On the loading of the page, these points are ordered by number of ratings and time created
	If the the points are returned as a result of a shuffle, they are random
	
	16 April 2011:
	Changing code to no longer return responses from participants who have not rated a single proposition
	(ie they have no rows in the user_ratings table)
	
	"""
	
	if TEMP_DEBUG_LOGGING:
		TEMP_DEBUG_FILE = open(TEMP_DEBUG_FILENAME, 'a')
		TEMP_DEBUG_FILE.write("\nOS/UNRATED:" + str(datetime.datetime.now())+"\n")
	
	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
		disc_stmt = get_disc_stmt(os, disc_stmt_id)
	except QueryUtilsError, q:
		if TEMP_DEBUG_LOGGING:
			TEMP_DEBUG_FILE.write(json_error(q.error_message).content)
			TEMP_DEBUG_FILE.close()
		return json_error(q.error_message)
     
	shuffle = request.REQUEST.get('shuffle', False)

	# Get points that the user has not rated ordered by number of ratings and time
	rated_cids = get_user_rated_cids(request, disc_stmt)
	unrated_comments = get_unrated_comments(request,os,disc_stmt,rated_cids,Settings.objects.int('MAX_NUM_TOTAL_DOTS'),shuffle)

	# Check for an argument username -- this param is only sent on createOS
	username = request.REQUEST.get('username', False)
	if username:
		unrated_comments += get_comment_by_username(request, username, os, disc_stmt)
	
	# Get the user ratings
	uids = []
	for comment in unrated_comments:
		uids.append(comment['uid'])
	user_ratings = get_user_ratings(request, os, uids)
		
	# Get user data
	user_data = {}
	for tup in user_ratings:
		data = get_user_data(tup[0])
		if len(data) > 0:
			user_data[tup[0]] = data	

	# create log
	create_comments_returned_log(request, os, unrated_comments, LogCommentsReturned.unrated)

	#return JSON
	tmp = json_result({'comments':unrated_comments,
						'ratings': user_ratings,
						'user_data': user_data,
						'shuffle': shuffle,
						'sorted_comments_ids': sort_by_response_score(unrated_comments),
						'sorted_avg_agreement':sort_by_avg_agreement(unrated_comments)})
						
	if TEMP_DEBUG_LOGGING:
		TEMP_DEBUG_FILE.write(tmp.content)
		TEMP_DEBUG_FILE.close()

	return json_result({'comments':unrated_comments,
						'ratings': user_ratings,
						'user_data': user_data,
						'shuffle': shuffle,
						'sorted_comments_ids': sort_by_response_score(unrated_comments),
						'sorted_avg_agreement':sort_by_avg_agreement(unrated_comments)})

@auth_required	
def os_leaderboard_comments(request, os_id, disc_stmt_id = None):
	"""
	Returns the following:
		- The top 10 responses for the discussion statement
		- The top 10 reviewers with responses to the discussion statement
		- The top 10 rising authors for the discussion statement
		
		- Or if CUSTOM_LEADERBOARD_LISTS is True, returns a custom query
	"""
	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
		disc_stmt = get_disc_stmt(os, disc_stmt_id)
	except QueryUtilsError, q:
		return json_error(q.error_message)

	# Custom leaderboard query now supported, only need to format according to lists
	if CUSTOM_LEADERBOARD_LISTS:
		list_1 = get_custom_list_1(os, disc_stmt, request)
		list_2 = get_custom_list_2(os, disc_stmt, request)
		list_3 = get_custom_list_3(os, disc_stmt, request)
	else:	
		# Retrieve the top 20 responses and reviewers
		list_1 = get_top_scores(os, disc_stmt, request, 10)
		list_2 = [] #get_top_responses(os, disc_stmt, request, 20)[10:] #get_top_reviewers(os, disc_stmt, request, NUM_TOP_REVIEWERS)

		# Get the rising authors only if the discussion statement is the active discussion statement
		list_3 = []
		#if (disc_stmt == os.discussion_statements.filter(is_current = True)[0]):
		#	list_3 = get_rising_comments(request)
	
	# Get the user ratings	
	uids = []
	for group in [list_1, list_2, list_3]:
		for comment in group:
			uids.append(comment['uid'])
	user_ratings = get_user_ratings(request, os, uids)
	
	# Get user data
	user_data = {}
	for tup in user_ratings:
		data = get_user_data(tup[0])
		if len(data) > 0:
			user_data[tup[0]] = data			
	
	# create log
	create_comments_returned_log(request, os, list_1 + list_2 + list_3, LogCommentsReturned.leaderboard)
	
	return json_result({'list_1': list_1,
						'list_2': list_2,
						'list_3': list_3,
						'ratings': user_ratings,
						'user_data': user_data,
						'sorted_comments_ids': sort_by_response_score(list_1 + list_2 + list_3),
						'sorted_avg_agreement':sort_by_avg_agreement(list_1 + list_2 + list_3)})

@auth_required			
def os_rated_comments(request, os_id, disc_stmt_id = None):
	"""
	Returns the comments the user has rated for the argument Opinion Space and discussion statement
	"""
	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
		disc_stmt = get_disc_stmt(os, disc_stmt_id)
	except QueryUtilsError, q:
		return json_error(q.error_message)	
	
	# Get the comments
	rated_comments = get_user_rated_comments(request, os, disc_stmt, Settings.objects.int('MAX_NUM_USER_RATED_DOTS'))
	
	# Get the user ratings
	uids = []
	for comment in rated_comments:
		uids.append(comment['uid'])
	user_ratings = get_user_ratings(request, os, uids)	
	
	# Get user data
	user_data = {}
	for tup in user_ratings:
		data = get_user_data(tup[0])
		if len(data) > 0:
			user_data[tup[0]] = data	
	
	# create log
	create_comments_returned_log(request, os, rated_comments, LogCommentsReturned.i_rated)
	
	# return HttpResponseServerError(); to test logging

	return json_result({'comments':rated_comments,
						'ratings': user_ratings,
						'user_data': user_data,
						'sorted_comments_ids': sort_by_response_score(rated_comments),
						'sorted_avg_agreement':sort_by_avg_agreement(rated_comments)})

@auth_required	
def os_rated_by_comments(request, os_id, disc_stmt_id = None):
	"""
	Returns the comments of the users that have rated the current user's comment
	for the argument Opinion Space and discussion statement
	"""
	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
		disc_stmt = get_disc_stmt(os, disc_stmt_id)
	except QueryUtilsError, q:
		return json_error(q.error_message)	
	
	# Get the comments. For now, don't send over the uids
	rated_by_comments = get_rated_by_comments(request, os, disc_stmt, Settings.objects.int('MAX_NUM_USER_RATED_DOTS'))[0]
	
	# Get the user ratings
	uids = []
	for comment in rated_by_comments:
		uids.append(comment['uid'])
	user_ratings = get_user_ratings(request, os, uids)
	
	# Get user data
	user_data = {}
	for tup in user_ratings:
		data = get_user_data(tup[0])
		if len(data) > 0:
			user_data[tup[0]] = data	
	
	# create log
	create_comments_returned_log(request, os, rated_by_comments, LogCommentsReturned.rated_by)
		
	return json_result({'comments': rated_by_comments,
						'ratings': user_ratings,
						'user_data': user_data,
						'sorted_comments_ids': sort_by_response_score(rated_by_comments),
						'sorted_avg_agreement':sort_by_avg_agreement(rated_by_comments)})

@auth_required	
def os_user_list(request, os_id, disc_stmt_id = None):
	"""
	Returns the comments of the users from a json encoded list
	"""
	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
		disc_stmt = get_disc_stmt(os, disc_stmt_id)
	except QueryUtilsError, q:
		return json_error(q.error_message)	
	
	user_list_string = request.REQUEST.get('userlist',[])
	user_list = json.loads(user_list_string)
	
	# Get the comments. For now, don't send over the uids
	rated_by_comments = get_formated_comments_from_user_list(request.user,user_list,os, disc_stmt, Settings.objects.int('MAX_NUM_USER_RATED_DOTS'))[0]
	
	# Get the user ratings
	uids = []
	for comment in rated_by_comments:
		uids.append(comment['uid'])
	user_ratings = get_user_ratings(request, os, uids)
	
	# Get user data
	user_data = {}
	for tup in user_ratings:
		data = get_user_data(tup[0])
		if len(data) > 0:
			user_data[tup[0]] = data	
	
	# create log
	create_comments_returned_log(request, os, rated_by_comments, LogCommentsReturned.rated_by)
		
	return json_result({'comments': rated_by_comments,
						'ratings': user_ratings,
						'user_data': user_data,
						'sorted_comments_ids': sort_by_response_score(rated_by_comments),
						'sorted_avg_agreement':sort_by_avg_agreement(rated_by_comments)})

def os_other_users(request, os_id, disc_stmt_id = None):

    """
	This query returns the following
		- The top 10 responses for the current question
		- The top 10 reviewers with responses to the current question
		- The users who have rated the current user
		- The comments the user has rated
		- The dots the user has not rated split into two categories: high and low confidence
			These are ordered by number of ratings and time created
		- the user if the username argument is provided
		
	UPDATE: 2010.08.05 - The sample size has been decreased. We will now allow the client
	to handle switching between these sets of points returned. All the points will be sent
	to the front-end, but only some will be drawn. This is for simplicity now, but can be
	changed/optimized in the future.

	There is a risk that an ID returned of the top 20 reviewers/responses or of the users that have rated
	the current user may not have any user ratings associated with it (i.e. they never answered the first
	5 propositions). These will be handled on the front-end with a null check (simplest solution).

	The json object returned consists of the ratings of the dots returned and the comments of those dots.
	There are also other objects returned regarding the top authors and reviewers of the space.

	Dots are ultimately drawn on the front end if there is a userrating object associated with it

	Other Notes:
		- null confidence scores are converted to 1 on the client side
    """
	
	# Obtain a reference to the current OS
    try:
        os = OpinionSpace.objects.get(pk = os_id)
    except OpinionSpace.DoesNotExist:
        return json_error('That Opinion Space does not exist.')
    
    # Get a reference to the selected discussion statement
    if disc_stmt_id == None:
		current_discussion_statement = os.discussion_statements.filter(is_current = True)[0]
    else:
		try:
			current_discussion_statement = os.discussion_statements.get(id = disc_stmt_id)
		except DiscussionStatement.DoesNotExist:
			return json_error('That discussion statement does not exist.')
					
    # Get latest points that the user has rated				
    rated_responses = get_user_rated_comments(request, os, current_discussion_statement)
      	
    # Get points that the user has not rated ordered by number of ratings and time
    rated_cids = get_user_rated_cids(request, current_discussion_statement)
    unrated_comments = get_unrated_high_confidence_comments(request, os, current_discussion_statement, rated_cids, 10)
    unrated_comments += get_unrated_low_confidence_comments(request, os, current_discussion_statement, rated_cids, 5)

    # The commented dots include the comments the user has rated and a mix of unrated high and low confidence dots
    commented_dots = rated_responses + unrated_comments
    commented_dot_user_ids = [dot['uid'] for dot in commented_dots]

	# Retrieve the top 20 responses and reviewers
    top_responses = get_top_responses(os, current_discussion_statement, request, Settings.objects.int('NUM_TOP_RESPONSES'))
    top_reviewers = get_top_reviewers(os, current_discussion_statement, request, Settings.objects.int('NUM_TOP_REVIEWERS'))

    # Get the rising authors only if the discussion statement is the active discussion statement
    rising_comments = []
    if (current_discussion_statement == os.discussion_statements.filter(is_current = True)[0]):
    	rising_comments = get_rising_comments(request)

	# Get the comments of the users who have rated the current user's response
    rated_by_comments = get_rated_by_comments(request, os, current_discussion_statement, Settings.objects.int('MAX_NUM_USER_RATED_DOTS'))[0]

	# Retrieve the username argument and if it is set, add it to the commented dots
	# This param is only sent on createOS
    username_argument_comment = []
    params = request.REQUEST
    username = params.get('username', False)
    if username:
		username_user_filter = User.objects.filter(username = username)
		if len(username_user_filter) != 0:
			username_comment_filter = os.comments.filter(is_current = True, blacklisted = False, discussion_statement = current_discussion_statement, user = username_user_filter[0])
			if len(username_comment_filter) != 0:
				username_argument_comment = [format_discussion_comment(request.user, username_comment_filter[0])]

    # Add the comments of the top reviewer/responses, rising comments, and comments of the users who
 	# have rated the current user that are not currently in the returned set of dots
    for group in [top_responses, top_reviewers, rising_comments, rated_by_comments, username_argument_comment]:
		to_add = get_to_add(request, group, commented_dot_user_ids)
		commented_dots += to_add
		commented_dot_user_ids = [dot['uid'] for dot in commented_dots]	# **This needs to be updated every iteration after appending any comments to commented_dots
					
	# Check if we don't have enough unrated points to return
    need_more = (len(unrated_comments) < Settings.objects.int('MAX_NUM_TOTAL_DOTS'))

	# Get the ratings corresponding to the points being returned (commented_dots)
    other_ratings = UserRating.objects.filter(is_current = True, opinion_space = os_id, user__in = commented_dot_user_ids)
    if need_more:
        uncommented_ratings = UserRating.objects.filter(is_current = True, opinion_space = os_id).exclude(user__in = commented_dot_user_ids)
    
    if request.user.is_authenticated():
        other_ratings = other_ratings.exclude(user = request.user)
        if need_more:
            uncommented_ratings = uncommented_ratings.exclude(user = request.user)
    
    # Get the slider ratings corresponding to the commented (or possibly uncommented) dots we retreived
    other_ratings = tuple(other_ratings.values_list('user', 'opinion_space_statement', 'rating'))
    if need_more:
        # Get number of ratings per dot to figure out how many ratings we need
        num_ratings = OpinionSpaceStatement.objects.filter(opinion_space = os_id).count()
        limit = (Settings.objects.int('MAX_NUM_TOTAL_DOTS') - len(unrated_comments)) * num_ratings
        other_ratings += tuple(uncommented_ratings.values_list('user', 'opinion_space_statement', 'rating')[:limit])
    
    
    # Retrieve all UserData key value pairs
    filterable_keys = {}
    for key in USER_DATA_KEYS:
		if USER_DATA_KEYS[key]['filterable']:
			filterable_keys[key] = USER_DATA_KEYS[key]['possible_values']
			
    user_data = {}
    for tup in other_ratings:
		data = get_user_data(tup[0])
		if len(data) > 0:
			user_data[tup[0]] = data
			
    user_data_info = {'filterable_keys': filterable_keys, 'user_data': user_data}

    # Log all the ID's of the commented dots we're showing, for data analysis
    logger_id, is_visitor = get_logger_info(request)
    if os_id == -1:
        os = None
    else:
        os = OpinionSpace.objects.get(id = os_id)


    return json_result({'other_ratings':other_ratings, 
						'comments':commented_dots,
						'unrated_comments':[d['uid'] for d in unrated_comments],
						'rated_comments': [d['uid'] for d in rated_responses], 
						'top_responses': top_responses,
						'top_reviewers': top_reviewers,
						'rising_comments': rising_comments,
						'user_data_info': user_data_info})

def os_landmarks(request, os_id):
    landmarks = Landmark.objects.filter(opinion_space = os_id, is_current = True)
    landmarks = landmarks.values_list('name', 'description', 'guess_text', 'image_path', 'ratings_json', 'id')
    
    return json_result(tuple(landmarks))

def os_get_previous_comment(request, os_id, user_id):
    disc = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = False).order_by('-created')[:1]
    
    if len(disc) == 0:
        return json_error('No previous discussion question found.')
    
    disc_comment = DiscussionComment.objects.filter(discussion_statement = disc[0], user = user_id).order_by('-created')[:1]
    
    if len(disc_comment) > 0:
        comment_text = disc_comment[0].comment
    else:
        comment_text = None
    
    return json_result((disc[0].statement, comment_text))

@auth_required
def os_get_user_info(request, os_id, user_id):
    ratings = UserRating.objects.filter(user = user_id, opinion_space = os_id, is_current = True)
    ratings = tuple(ratings.values_list('opinion_space_statement_id', 'rating'))

	# Get the username and location
    user = User.objects.get(id = user_id)	
    name_settings = UserSettings.objects.filter(user = user, key = 'username_format')[:1]
    if (len(name_settings) > 0):
		username = name_settings[0].value
    else: 
		username = user.username
    try:
        demo = UserDemographics.objects.get(user = user)
        location = demo.location
    except UserDemographics.DoesNotExist:
        demo = None
        location = None
	
    # Log all the ratings retrieved every time a user clicks 'Show Ratings'
    logger_id, is_visitor = get_logger_info(request)
    if os_id == -1:
        os = None
    else:
        os = OpinionSpace.objects.get(id = os_id)
    
    return json_result([ratings, {'username':username, 'location':location}])
            
def os_get_landmark_ratings(request, os_id, landmark_id):
    try:
        landmark = Landmark.objects.get(id = landmark_id, opinion_space = os_id)
    except Landmark.DoesNotExist:
        return json_error('That landmark does not exist.')
    ratings = decode_string(landmark.ratings_json)
    
    # This assumes that the statement ID's are 1, 2, 3, 4, 5
    ratings = [(i + 1, rating) for i, rating in enumerate(ratings)]
    
    # Log all the ratings retrieved every time a user clicks 'Show Ratings'
    logger_id, is_visitor = get_logger_info(request)
    if os_id == -1:
        os = None
    else:
        os = OpinionSpace.objects.get(id = os_id)
    
    return json_result(ratings)

@auth_required
def os_get_comment(request, os_id, user_id, disc_stmt_id = None):
	"""
	This method is called only after a user has rated the comment in order 
	to refresh the comment information as well as the top scores
	"""
	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
	except QueryUtilsError, q:
		return json_error(q.error_message)

    # Get a reference to the discussion statement
	if disc_stmt_id == None:
		current_discussion_statement = os.discussion_statements.filter(is_current = True)[0]
	else:
		try:
			current_discussion_statement = os.discussion_statements.get(id = disc_stmt_id)
		except DiscussionStatement.DoesNotExist:
			return json_error('That discussion statement does not exist.')

	# Custom leaderboard query now supported, only need to format according to lists
	if CUSTOM_LEADERBOARD_LISTS:
		list_1 = get_custom_list_1(os, current_discussion_statement, request)
		list_2 = get_custom_list_2(os, current_discussion_statement, request)
		list_3 = get_custom_list_3(os, current_discussion_statement, request)
	else:	
		# Retrieve the top 20 responses and reviewers
		list_1 = get_top_responses(os, current_discussion_statement, request, Settings.objects.int('NUM_TOP_RESPONSES'))
		list_2 = get_top_reviewers(os, current_discussion_statement, request, Settings.objects.int('NUM_TOP_REVIEWERS'))

		# Get the rising authors only if the discussion statement is the active discussion statement
		list_3 = []
		if (current_discussion_statement == os.discussion_statements.filter(is_current = True)[0]):
			list_3 = get_rising_comments(request)

	comment = os.comments.filter(is_current = True, discussion_statement = current_discussion_statement, user = user_id)
	if len(comment) != 0:		
		return json_result({'comment':format_discussion_comment(request.user, comment[0]), 
							'list_1': list_1,
							'list_2': list_2,
							'list_3': list_3})
	else:
		return json_error('Comment does not exist')

#
# Methods that require logging in
#

@auth_required
def os_flag_comment(request, os_id, comment_id):
    discussion_statement = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = True)[0]
    comment = DiscussionComment.objects.filter(id=comment_id)[:1]
    
    if not len(comment) == 1:
        return json_error('That comment does not exist.')
    
    flag_count = comment[0].flags.filter(reporter = request.user).count()
    
    if flag_count == 0:
        # Hasn't been flagged by this user yet
        flag = FlaggedComment(comment = comment[0], reporter = request.user)
        flag.save()
    
    return json_success()

@auth_required
def os_save_ratings(request, os_id):
    params = request.REQUEST
    
    # Save ratings
    i = 1
    st_id = params.get('statement_id_%s' % (i), False)
    
    if st_id:
        # Set old ratings as not current
        UserRating.objects.filter(user = request.user,
                                  opinion_space = os_id,
                                  is_current = True).update(is_current = False)
    
    while (st_id):
        # Make the rating a float between allowed max and min values
        try:
            value = float(params.get('rating_%s' % (i)))
            value = max(value, MIN_RATING)
            value = min(value, MAX_RATING)
        except ValueError:
            value = (MAX_RATING - MIN_RATING) / 2
        
        rating = UserRating(user = request.user, 
                            opinion_space_id = os_id, 
                            opinion_space_statement = OpinionSpaceStatement.objects.get(pk = st_id),
                            rating = value,
                            is_current = True)
        rating.save()
        
        i += 1
        st_id = params.get('statement_id_%s' % (i), False)
    
    return json_success()

@auth_required
def os_save_rating(request, os_id):
    params = request.REQUEST

    st_id = params.get('id', False)
    
    if st_id:
        # Set old rating as not current
        UserRating.objects.filter(user = request.user,
                                  opinion_space = os_id,
                                  opinion_space_statement = OpinionSpaceStatement.objects.get(pk = st_id),
                                  is_current = True).update(is_current = False)
                                      
        # Make the rating a float between allowed max and min values
        try:
            value = float(params.get('rating'))
            value = max(value, MIN_RATING)
            value = min(value, MAX_RATING)
        except ValueError:
            value = (MAX_RATING - MIN_RATING) / 2

        rating = UserRating(user = request.user, 
                            opinion_space_id = os_id, 
                            opinion_space_statement = OpinionSpaceStatement.objects.get(pk = st_id),
                            rating = value,
                            is_current = True)
        user_data_cache = UserData.objects.filter(user = request.user, key = 'first_rating')
        if user_data_cache.count() == 0:
            user_data_cache = UserData(user = request.user, key = 'first_rating', value='')
            user_data_cache.save()
        rating.save()

    return json_success()

@auth_required
def os_save_comment(request, os_id, disc_stmt_id = None):
    params = request.REQUEST
    

    new_comment = params.get('comment', False)
    new_comment = decode_to_unicode(new_comment)
    comment_language = params.get("commentLanguage", "english")
    comment_language = decode_to_unicode(comment_language) # What does decode to unicode do?
    
    if new_comment != False:
        
        # Get a reference to the discussion question
        if disc_stmt_id == None:
            disc_stmt = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = True)[0]
        else:
            try:
                disc_stmt = DiscussionStatement.objects.get(id = disc_stmt_id)
            except DiscussionStatement.DoesNotExist:
                return json_error('That discussion statement does not exist.')
        
        new_comment = new_comment.strip()[:MAX_COMMENT_LENGTH]
        old_comment = DiscussionComment.objects.filter(user = request.user,
                                                        opinion_space = os_id,
                                                        discussion_statement = disc_stmt,
                                                        is_current = True)
        
        # Check for a previous comments and mark them as old
        old_comment_recent = None
        if len(old_comment) > 0:
            old_comment_recent = old_comment[0]
            old_comment_text = decode_to_unicode(old_comment_recent.comment)
            if old_comment_text == new_comment:
    
                # Get previous revisions
                prev_comments = get_revisions_and_suggestions(request.user, os_id, disc_stmt)
                return json_result({'success': True, 'prev_comments': prev_comments})
            
            old_comment.update(is_current = False)
        
        # Save new comment if it's not an empty string
        if new_comment != '':
            if comment_language == 'english':
                comment = DiscussionComment(user = request.user,
                                            opinion_space_id = os_id,
                                            discussion_statement = disc_stmt,
                                            comment = new_comment,
                                            spanish_comment = translate_to_spanish(new_comment),
                                            original_language = comment_language,
                                            query_weight = -1,
                                            is_current = True)
            else: # comment is in Spanish
                comment = DiscussionComment(user = request.user,
                                            opinion_space_id = os_id,
                                            discussion_statement = disc_stmt,
                                            comment = translate_to_english(new_comment),
                                            spanish_comment =  new_comment,
                                            original_language = comment_language,
                                            query_weight = -1,
                                            is_current = True)      
          

            # Set score variables as the previous comment's score 
            if old_comment_recent:
                comment.average_rating = old_comment_recent.average_rating
                comment.average_score = old_comment_recent.average_score
                comment.score_sum = old_comment_recent.score_sum
                comment.normalized_score = old_comment_recent.normalized_score
                comment.normalized_score_sum = old_comment_recent.normalized_score_sum
                comment.confidence = old_comment_recent.confidence
                comment.query_weight = old_comment_recent.query_weight

            comment.save()
            update_query_weight(comment)
            
            # Check the comment for profanity
            profanity_result = check_bad_words(new_comment)
            if profanity_result[0]:
                pfc = ProfanityFlaggedComment(comment = comment, profanity = profanity_result[1], original_words = profanity_result[2])
                pfc.save()
    
    # Get previous revisions
    prev_comments = get_revisions_and_suggestions(request.user, os_id, disc_stmt)
    return json_result({'success': True, 'prev_comments': prev_comments})

@auth_required
def os_save_first_time_ratings(request, os_id):
	if request.method == "POST":
		
	    # Obtain a reference to the os and discussion statement
		try:
			os = get_os(os_id)
			disc_stmt = get_disc_stmt(os)
		except QueryUtilsError, q:
			return json_error(q.error_message)
		
		post = request.POST.copy()
		dict_type = post.get('type')
		post.pop('type')
		ratings_list = post.items()
		
		process_ratings_list(request, ratings_list, dict_type, os_id, disc_stmt)
		
	return json_result({'success':True, 'type':dict_type})


@auth_required
def os_save_comment_agreement(request, os_id, user_id, disc_stmt_id = None):
    if int(user_id) == request.user.id:
        return json_error("You can't rate your own comment.")
    
    # Get discussion statement
    if disc_stmt_id == None:
    	disc_stmt = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = True)[0]
    else:
		try:
			disc_stmt = DiscussionStatement.objects.get(id = disc_stmt_id)
		except DiscussionStatement.DoesNotExist:
			return json_error('That discussion statement does not exist.')
	
    agreement = request.REQUEST.get('agreement', None)
    if agreement is None:
		return json_error('Invalid value')
	
    return save_agreement_rating(request, agreement, int(user_id), os_id, disc_stmt)
	
@auth_required
def os_save_comment_rating(request, os_id, user_id, disc_stmt_id = None):
    if int(user_id) == request.user.id:
        return json_error("You can't rate your own comment.")
    
    # Get discussion statement
    if disc_stmt_id == None:
    	disc_stmt = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = True)[0]
    else:
		try:
			disc_stmt = DiscussionStatement.objects.get(id = disc_stmt_id)
		except DiscussionStatement.DoesNotExist:
			return json_error('That discussion statement does not exist.')			

    rating = request.REQUEST.get('rating', None)
    if rating is None:
		return json_error('Invalid value')
		
    return save_insightful_rating(request, rating, int(user_id), os_id, disc_stmt)

@auth_required
def os_update_comment(request, os_id, user_id, disc_stmt_id = None):
	# Get discussion statement
    if disc_stmt_id == None:
    	disc_stmt = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = True)[0]
    else:
		try:
			disc_stmt = DiscussionStatement.objects.get(id = disc_stmt_id)
		except DiscussionStatement.DoesNotExist:
			return json_error('That discussion statement does not exist.')		
		
    return update_comment(user_id, os_id, disc_stmt)

@auth_required
def os_save_comment_suggestion(request):
	if request.method == "POST":
		params = request.POST
		suggestion = params.get('suggestion','')
		cid = params.get('cid', -1)
		
		# Check for cid param
		if cid == -1:
			return json_error('Comment does not exist')

		# Check if comment exists
		comment = DiscussionComment.objects.filter(id = cid)
		if len(comment) == 0:
			return json_error('Comment does not exist')
		
		# Sanitize suggestion
		suggestion = suggestion.strip()
		if len(suggestion) == 0:
			return json_error('Suggestion must not be null')
			
		# profanity check?
		
		suggestion = Suggestion(suggester = request.user, comment = comment[0], q = None, score = 0, suggestion = suggestion)
		suggestion.save()
		
		return json_success()

	else:
		return json_error('Request Invalid')

@auth_required
def os_update_user_settings(request):
    for key, value in request.REQUEST.items():
        # Make sure this is a valid option
        if not USER_SETTINGS_META.has_key(key):
            continue
        
        # Reasons to revert to default value for this setting:
        # 1) allow_none is False and the value is empty
        # 2) allow_any is False and the value is not in possible_values
        if (len(value) == 0 and not USER_SETTINGS_META[key]['allow_none']) \
                or (not USER_SETTINGS_META[key]['allow_any'] and not value in USER_SETTINGS_META[key]['possible_values']):
            value = USER_SETTINGS_META[key]['default']
        
        # Get or create the setting
        db_settings = UserSettings.objects.filter(user = request.user, key = key)[:1]
        if len(db_settings) > 0:
            db_setting = db_settings[0]
        else:
            db_setting = UserSettings(user = request.user, key = key)
        
        # Save the new settings
        db_setting.value = value
        db_setting.save()
    
    return json_success()

@auth_required
def get_stats(request, os_id, disc_stmt_id=None):

	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
		disc_stmt = get_disc_stmt(os, disc_stmt_id)
	except QueryUtilsError, q:
		return json_error(q.error_message)
	
	allow_suggestion_rating = Settings.objects.filter(key = 'SUGGESTION_RATING_SLIDERS')
	if allow_suggestion_rating.count() > 0:
		allow_suggestion_rating = allow_suggestion_rating[0].value == 'true'
	else:
		allow_suggestion_rating = True

	# Get the collaborator score
	if allow_suggestion_rating:
		suggestion_score_object = SuggesterScore.objects.filter(user = request.user)
		suggestion_score_sum = 0
		suggestion_normalized_score_sum = 0
		if suggestion_score_object.count() > 0:
			suggestion_score_sum = suggestion_score_object[0].score_sum
			suggestion_normalized_score_sum = suggestion_score_object[0].normalized_score_sum
	else:
		# just return the count
		comment_filter = os.comments.filter(user = request.user, is_current = True, discussion_statement = disc_stmt)		
		if comment_filter.count() > 0:
			suggestion_score_sum = Suggestion.objects.filter(suggester = request.user).exclude(comment = comment_filter[0]).count()
		else:
			suggestion_score_sum = Suggestion.objects.filter(suggester = request.user).count()
		
		suggestion_normalized_score_sum = suggestion_score_sum

	# Send the total number of users the user has been rated by and the
	# the total number of users the user has rated	
	user_num_rated = 0#len(get_user_rated_comments(request, os, disc_stmt))
	user_num_rated_by_with_comments = 0#len(get_rated_by_comments(request, os, disc_stmt)[0])		
	user_num_rated_by = len(get_new_ratings(request.user, os, disc_stmt, -1))
	num_new_comments = 0#get_never_seen_comments(request.user,os,disc_stmt,None,True)
	num_rated_updated_comments = 0#len(get_rated_updated_comments(request.user,os,disc_stmt))
	num_suggestions = Suggestion.objects.filter(suggester = request.user).count()
	
	# Show the score as calculated with the constant offest (THIS HAS A SIGNIFICANT BIAS TO # OF RATINGS 
	# WHEN COMPARED WITH THE NON CONSTANT OFFSET)
	comment_filter_nc = DiscussionComment.objects.filter(user = request.user,discussion_statement = disc_stmt)
	comment_score = tuple([[0]])
	if len(comment_filter_nc) > 0:
		comment_score = tuple([[numpy.sum(CommentRating.objects.filter(comment__in=comment_filter_nc,is_current=True).values_list('rating'))]])
	
	# This query is essentially the top_responses query
	rank_list = os.comments.filter(is_current = True, discussion_statement = disc_stmt, confidence__lte = Settings.objects.float('CONFIDENCE_THRESHOLD')).exclude(confidence = None).exclude(normalized_score_sum = None).order_by('-normalized_score_sum')
	
	# If we're using comments to position users
	if Settings.objects.boolean('NO_STATEMENTS'):

		# remove the comments of users whose ids match the statement ids
		statement_ids = os.statements.values_list('id')
		rank_list = rank_list.exclude(user__in = statement_ids)	
	
	rank_total = os.comments.filter(is_current = True, blacklisted = False).count()
	rank = 0
	found = False
	for c in rank_list:
		rank = rank + 1
		if c.user == request.user:
			found = True
			break
	
	if not found:
		rank = -1
		rank_total = -1
	
	result = {'other_agreement_buckets' : get_rated_agreement_buckets(request.user,os,disc_stmt),
			  'other_insight_buckets' : get_rated_insight_buckets(request.user,os,disc_stmt),
			  'user_agreement_buckets' : get_ratedby_agreement_buckets(request.user,os,disc_stmt),
			  'user_insight_buckets': get_ratedby_insight_buckets(request.user,os,disc_stmt),
			  'user_num_rated': user_num_rated,
			  'user_num_rated_by': user_num_rated_by,
			  'user_num_rated_by_with_comments': user_num_rated_by_with_comments,
			  'num_new_comments': num_new_comments,
			  'num_suggestions': num_suggestions,
			  'num_rated_updated_comments': num_rated_updated_comments,
			  'suggestion_score_sum': suggestion_score_sum,
			  'suggestion_normalized_score_sum': suggestion_normalized_score_sum,
			  'cur_user_comment_score': comment_score,
			  'comment_rank': rank,
			  'comment_rank_total': rank_total,			
			  }
	return json_result(result)

@auth_required
def get_notifications(request,os_id,disc_stmt_id = None):
	
	"""
	Sends to the user,
		- The number of raters who have just rated you and the number of those raters with a comment and statement ratings
		- The total number of comments you've rated
		- The total number of users who have just rated you
	"""
	
	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
		disc_stmt = get_disc_stmt(os, disc_stmt_id)
	except QueryUtilsError, q:
		return json_error(q.error_message)
	
	#get a certain number of notifications
	notifications = get_n_recent_notification_events(NOTIFICATION_NUMBER,request.user,os,disc_stmt)
	
	if len(notifications) == 0:
		return json_result({'notifications' : notifications, 'timestamp': str(time.time())})
	
	#smart session query based on the earliest notifications
	sessions = UserData.objects.filter(user = request.user, key = 'last_notification_query')
	#group all notifications by sessions
	if len(sessions) == 0:
		for j in range(0,len(notifications)):
			notifications[j]['session_group'] = j
			notifications[j]['label'] = 'New'
			notifications[j]['time'] = str(notifications[j]['time'].time())
	else:
		last_session = sessions[0]
		group_number = 0
		for j in range(0,len(notifications)):
			notifications[j]['session_group'] = group_number
			if notifications[j]['time'] > datetime.datetime.fromtimestamp(float(last_session.value)):
				notifications[j]['label'] = 'New'
			else:
				notifications[j]['label'] = time_to_label(notifications[j]['time']) #convert the time into a label
			notifications[j]['time'] = str(notifications[j]['time'].time())
			group_number = group_number + 1
				
	return json_result({'notifications' : notifications, 'timestamp': str(time.time())})

@auth_required
def os_get_received_suggestions(request,os_id,disc_stmt_id=None):
	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
		disc_stmt = get_disc_stmt(os, disc_stmt_id)
	except QueryUtilsError, q:
		return json_error(q.error_message)
	
	comments = DiscussionComment.objects.filter(user = request.user, opinion_space = os, discussion_statement = disc_stmt)
	
	if comments.count() == 0:
		return json_error('User does not have a comment')
	
	suggestions = Suggestion.objects.filter(comment__in = comments).order_by('created')
	return json_result([{'id': suggestion.id, 'q': suggestion.q, 'text': suggestion.suggestion, 'suggester_id': suggestion.suggester.id, 'suggester_name': suggestion.suggester.username, 'owner': suggestion.comment.user.username, 'comment': format_general_discussion_comment(suggestion.comment), 'time': suggestion.created.strftime("%B %d, %Y")} for suggestion in suggestions])

@auth_required
def os_get_given_suggestions(request,os_id,disc_stmt_id=None):
	# Obtain a reference to the os and discussion statement
	try:
		os = get_os(os_id)
		disc_stmt = get_disc_stmt(os, disc_stmt_id)
	except QueryUtilsError, q:
		return json_error(q.error_message)
		
	suggestions = Suggestion.objects.filter(suggester = request.user).order_by('created').reverse()
	return json_result([{'id': suggestion.id, 'q': suggestion.q, 'text': suggestion.suggestion, 'suggester_id': suggestion.suggester.id, 'suggester_name': suggestion.suggester.username, 'owner': suggestion.comment.user.username, 'comment': format_general_discussion_comment(suggestion.comment)} for suggestion in suggestions if suggestion.comment.discussion_statement == disc_stmt])
	
@auth_required
def os_save_suggestion_rating(request):
	sid = request.REQUEST.get('id','')
	if sid == '':
		return json_error('Did not provide a suggestion id')
	else:
		suggestion = Suggestion.objects.filter(id = sid)
		if len(suggestion) == 0 or suggestion[0].comment.user.id != request.user.id:
			return json_error('Invalid suggestion rating')
		else:
			q = request.REQUEST.get('q','')
			if q == '':
				return json_error('Invalid q value provided')
			else:
				suggestion[0].q = float(q)
				suggestion[0].save()
				update_suggestion_score(suggestion[0])
				return json_success()
				
#
# SMS Receive
#
def os_receive_sms_comment(request):
    #Make sure only txtimpact is sending requests to this view, otherwise don't do anything
    host = socket.gethostbyaddr(request.META['REMOTE_ADDR'])
    if host[0] == 'wire2air.com':
        qdict = receive_sms(request)
        
        #check that the appropriate parameters have been provided
        if qdict==False:
                return HttpResponse("Error receiving SMS message: missing http GET information.")
        msg = qdict.__getitem__("message")
        msg = msg.strip()
        keyword = msg[:6]
        msg = msg[7:]
        phono = qdict.__getitem__("mobilenumber")
        phonostr = str(phono)
        
        #make sure phonenumber is exactly 11 digits
        if len(phonostr) != 11:
               return HttpResponse("Error: Invalid phone number.")
        regexCheck = re.match('\d\d\d\d\d\d\d\d\d\d\d',phonostr)
        if not(regexCheck):
                return HttpResponse("Error: Invalid phone number.")

        #make sure the message has the proper keyword
        if keyword != SMS_KEYWORD:
                return HttpResponse("Error: Message received without the appropriate keyword.")    

        #make sure a non-empty message has been sent to the server, otherwise inform the user of the problem
        if len(msg) == 0:
                send_sms(phono,"Error: The system received an empty message.")
                return HttpResponse()
        else:
                #if we have an actual comment to use in the system, make a username and password
                #for a new User (but first check if the user already exists for both ForeignCredential and User objects)
                pw = User.objects.make_random_password(8)

                #possible exception by the get_os() call -- if we get one, exit out of the protocol              
                try:
                        theOS = get_os(1)
                except QueryUtilsError:
                        return HttpResponse("Error: Invalid query.")

                #make sure an existing user doesn't exist with the user's phone number as that user's username
                filter_results = ForeignCredential.objects.filter(foreignid=str(phono)+'_sms')
                filter_users = User.objects.filter(username=str(phono))
                if filter_results.count() != 0 or filter_users.count() != 0:
                        send_sms(phono,"Error: A user already exists in the system with this phone number. Please login at "+URL_ROOT)
                        return HttpResponse()
                
                #get the discussion statements
                disc_stmts = DiscussionStatement.objects.filter(opinion_space = get_os(1), is_current = True)
                #if no discussion statement exists, send a message to the phone number indicating the problem
                if disc_stmts.count() == 0:
                        send_sms(phono,"Error: Invalid query.")
                        return HttpResponse()
                                            
                disc_stmt = disc_stmts[0]

                #create the User object, Discussion_Comment, and Foreign_Credential for the current user
                user = User.objects.create_user(phono,"",pw)
                newuser = ForeignCredential(user=user,foreignid=str(phono)+'_sms')
                newuser.save()
                cmment = DiscussionComment(user = user,opinion_space=theOS,discussion_statement = disc_stmt,comment = msg,query_weight = -1,is_current = True)
                cmment.save()
                update_query_weight(cmment)
                
                # Check the comment for profanity, if there is profanity, flag it by creating a ProfanityFlaggedComment that links to the Discussion_Comment
                profanity_result = check_bad_words(msg)
                if profanity_result[0]:
                        pfc = ProfanityFlaggedComment(comment = cmment, profanity = profanity_result[1], original_words = profanity_result[2])
                    	pfc.save()
                send_sms(phono,"Thank you! Your response has been saved. To access your account, login at "+URL_ROOT+" with username: "+str(phono)+" and password: "+pw)
                return HttpResponse()
    return HttpResponse("Error: Invalid host.")

def application_close(request):
	if request.session.get('first_time_data','') != '':
		first_time_data_structure = json.loads(request.session['first_time_data'])
		agreement_ratings = len(first_time_data_structure['agreement_ratings'].keys())
		insight_ratings = len(first_time_data_structure['insight_ratings'].keys())
		time_per_rating = (float(first_time_data_structure['updated']) - float(first_time_data_structure['created']))/(agreement_ratings)
		details = json.dumps({'num_agreement':agreement_ratings, 'num_insight':insight_ratings, 'secs_per_rating': time_per_rating, 'return': request.session.get('returning',False)})
		create_user_event_log(request,{'log_type' : LogUserEvents.first_time_incomplete, 'details' : details})
	# log closing of window
	create_user_event_log(request,{'log_type' : 4, 'details' : 'Window closed'})	
	request.session['returning'] = True
	# if the user is not authenticated then either they never logged in
	# or it was called on logout
	if request.user.is_authenticated():
		application_close_helper(request)
	
	return HttpResponse("")#if not empty string causes issues in some browsers

def os_never_seen_comments(request,os_id,disc_stmt_id=None):
	os = get_os(os_id)
	
	if disc_stmt_id == None:
		disc_stmt = os.discussion_statements.filter(is_current = True)
	else:
		disc_stmt = DiscussionStatement.objects.filter(id = disc_stmt_id)
	
	if os == None or len(disc_stmt) == 0:
		return json_error('Invalid Request')
	    
	cache = NeverSeenCache.objects.filter(created__gte=datetime.date.today()).order_by('-created')
	if len(cache) > 0 and not request.user.is_authenticated():
	    cache = cache[0]
	    return json_result(json.loads(cache.value))

	#query = request.REQUEST.get('query', False)
	#no_statements = request.REQUEST.get('no_statements', False)
	#if no_statements == "false": # Flash booleans aren't transferred correctly
	#	no_statements = False

	never_seen_comments = get_never_seen_comments(request.user,os,disc_stmt[0],7, False)
	# Check for an argument username -- this param is only sent on createOS
	#username = request.REQUEST.get('username', False)
	#if username:
	#	never_seen_comments += get_comment_by_username(request, username, os, disc_stmt)
	
	# create log 
	create_comments_returned_log(request, os, never_seen_comments, LogCommentsReturned.unrated)
	
	# Get the user ratings
	uids = []
	for comment in never_seen_comments:
		uids.append(comment['uid'])
	user_ratings = get_user_ratings(request, os, uids)
	
	# Get user data
	user_data = {}
	for tup in user_ratings:
		data = get_user_data(tup[0])
		if len(data) > 0:
			user_data[tup[0]] = data	
	result = {'comments': never_seen_comments,
						'ratings': user_ratings,
						'user_data': user_data,
						'sorted_comments_ids': sort_by_response_score(never_seen_comments),
						'sorted_avg_agreement':sort_by_avg_agreement(never_seen_comments)}
	nc = NeverSeenCache(value=json.dumps(result))
        
        nc.save()            
            

	return json_result(result)
    
def os_never_seen_comments_json(request,os_id,disc_stmt_id=None):
	os = get_os(os_id)
	
	if disc_stmt_id == None:
		disc_stmt = os.discussion_statements.filter(is_current = True)
	else:
		disc_stmt = DiscussionStatement.objects.filter(id = disc_stmt_id)
	
	if os == None or len(disc_stmt) == 0:
		return json_error('Invalid Request')
	
	never_seen_comments = get_never_seen_comments(request.user,os,disc_stmt[0],7, False)
	
	# create log 
	create_comments_returned_log(request, os, never_seen_comments, LogCommentsReturned.unrated)
	
	# Get the user ratings
	uids = []
	for comment in never_seen_comments:
		uids.append(comment['uid'])
	user_ratings = get_user_ratings(request, os, uids)
	
	# Get user data
	user_data = {}
	for tup in user_ratings:
		data = get_user_data(tup[0])
		if len(data) > 0:
			user_data[tup[0]] = data	
	result = {'comments': never_seen_comments,
						'ratings': user_ratings,
						'user_data': user_data,
						'sorted_comments_ids': sort_by_response_score(never_seen_comments),
						'sorted_avg_agreement':sort_by_avg_agreement(never_seen_comments)}
	nc = NeverSeenCache(value=json.dumps(result))
	nc.save()
	return result
	
@auth_required	
def os_rated_updated_comments(request,os_id,disc_stmt_id=None):
	os = get_os(os_id)
	
	if disc_stmt_id == None:
		disc_stmt = os.discussion_statements.filter(is_current = True)
	else:
		disc_stmt = DiscussionStatement.objects.filter(id = disc_stmt_id)
	
	if os == None or len(disc_stmt) == 0:
		return json_error('Invalid Request')

	rated_updated_comments = get_rated_updated_comments(request.user,os,disc_stmt[0])
	
	# Get the user ratings
	uids = []
	for comment in rated_updated_comments:
		uids.append(comment['uid'])
	user_ratings = get_user_ratings(request, os, uids)
	
	# Get user data
	user_data = {}
	for tup in user_ratings:
		data = get_user_data(tup[0])
		if len(data) > 0:
			user_data[tup[0]] = data	
		
	return json_result({'comments': rated_updated_comments,
						'ratings': user_ratings,
						'user_data': user_data,
						'sorted_comments_ids': sort_by_response_score(rated_updated_comments),
						'sorted_avg_agreement':sort_by_avg_agreement(rated_updated_comments)})

def os_first_time_log(request):
	"""
	Format: {agreement_ratings: {cid1: rating1,cid2: rating2,...},insight_ratings: {cid1: rating1,cid2: rating2,...}, updated: timestamp, created: timestamp}
	"""
	cid = request.REQUEST.get('id',-1)
	type = request.REQUEST.get('type','')
	value = request.REQUEST.get('value',.5)
	created = False
	if cid == -1 or not (type == 'agreement' or type == 'insight') or value == .5:
		return json_error('Invalid Request')
	if request.session.get('first_time_data','') == '':
		request.session['first_time_data'] = json.dumps({'agreement_ratings': {}, 'insight_ratings': {}, 'updated':''})
		created = True
	first_time_data_structure = json.loads(request.session['first_time_data'])
	if type == 'agreement':
		first_time_data_structure['agreement_ratings'][str(cid)] = str(value)
	elif type == 'insight':
		first_time_data_structure['insight_ratings'][str(cid)] = str(value)
		
	first_time_data_structure['updated'] = str(time.time())
	
	if created:
		first_time_data_structure['created'] = str(time.time())
	request.session['first_time_data'] = json.dumps(first_time_data_structure)
	return json_result(first_time_data_structure)
