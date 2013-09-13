import os
from django.conf.urls.defaults import *
import datetime

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DOC_ROOT = os.path.dirname(os.path.abspath(__file__))
URL_ROOT = 'http://localhost:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'os.sqlite'
    }
}
DATABASE_ENGINE = 'sqlite3'                     # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.

EMAIL_HOST = 'localhost'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 25

MEDIA_DIR_NAME = "media"

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'REPLACE_THIS_WITH_SECRET_KEY'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.dirname(DOC_ROOT) + '/' + MEDIA_DIR_NAME + '/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/' + MEDIA_DIR_NAME + '/'

STATIC_MEDIA_PATTERN = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':  MEDIA_ROOT}),
	(r'^html5/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/path/to/html5/code/'}),
)

# Methods that allow unauthenticated access
ALLOW_UNAUTH_ACCESS_METHODS = ['os_unrated_comments', 'os_get_user_info']

# IP_Tracking = False
# Session Cookie is above - Warning: It is a Django settings, so do not change the variable name

# UserData keys
# Types: 'nominal', 'ordinal', 'quantitative'
# 'subgroup_analysis' means that the field should be included in the analysis of subgroups
# 'possible_values' should be encoded in order if the data is ordinal
USER_DATA_KEYS = { # Example:
				  'age': {'filterable': True, 'subgroup_analysis' : False, 'type' : 'ordinal', 'possible_values': ('01-19','20-29','30-39','40-49','50-59','60+')},
				  'firstname' : { 'filterable' : False, 'subgroup_analysis' : False, 'type' : 'nominal', 'possible_values': ()},
				  'lastname'  : { 'filterable' : False, 'subgroup_analysis' : False, 'type' : 'nominal', 'possible_values': ()},
				  'picture'  : { 'filterable' : False,'subgroup_analysis' : False, 'type' : 'nominal', 'possible_values': ()},
				
				  # Append configuration specific UserData keys here:
				  }


# Subgroup Analysis
# Aggregrate, top 50 authors, reviewers, and bottom 50 authors are automatically processed
# Ex: SUBGROUPS = {'young-male' : {'Gender' : ['Male'], 'Age' : ['18-29']}, 'old-rich-female' : {'Gender' : ['Female'], 'Age' : ['50-59', '60-70'], 'Income' : ['$100,000 to $124,999', '$125,000 to $149,999', '$150,000 to $199,999','$200,000 to $249,999','$250,000 or more']}}
# Lists of fields per key use "OR" logic
SUBGROUPS = {}

# Start and end dates for the adminpanel analysis
# These should be set to the dates of the launch
ADMINPANEL_START_DATE = datetime.datetime(year=2010, month=11, day=15)
ADMINPANEL_END_DATE = datetime.datetime(year=2011, month=1, day=15)

"""
Registration Fields for the registration form

	Note: Some registration fields are not listed here, i.e. Location,

	UserDemographics holds gender, year_born, location, political_party, heard_about
	UserData holds the rest

	Use this dictionary to set which fields are required for registration
	To change required fields for UserDemographics, change the model, as the form is based off the model
	No fields are "required" for UserData. 
"""
REGISTRATION_FIELD_TABLE = {'username': {'required':True},
							'email': {'required':False},
							'first_name': {'required':False},
							'url': {'required':False},
							'question': {'required':False}, 
							'answer': {'required':False}
							}
							
# Point settings
NUM_TOP_RESPONSES = 10
NUM_TOP_REVIEWERS = 10

# Session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 5184000 # Keep sessions open for 2 months

# Settings for the feedback form
FEEDBACK_MIN_LENGTH = 10
FEEDBACK_MAX_LENGTH = 5000
FEEDBACK_EMAIL_TO = 'Hybrid Wisdom Feedback <support@hybridwisdom.com>'
FEEDBACK_EMAIL_SUBJECT = 'User has left feedback'

# Some meta options for the user settings
USER_SETTINGS_META = {
    'emailme': {'default': '1', 'possible_values': ('0', '1'), 'allow_any': False, 'allow_none': False},
    'username_format': {'default': '', 'allow_any':True, 'allow_none':False},
    'url':{'default': '', 'allow_any':True, 'allow_none':True}
}

# Minimum username length during registration
MIN_USERNAME_LENGTH = 3

# Add more boolean logic here if we need more custom queries
CUSTOM_LEADERBOARD_LISTS = False
HAVE_ADDITIONAL_QUESTIONS = False

# Debug settings
TEMP_DEBUG_LOGGING = False
TEMP_DEBUG_FILENAME = "/tmp/os-debug.log"

#Example Server Config
#ASSETS_LOCAL = '/var/www/opinion.berkeley.edu/assets/'
#Assets for local dev make sure you make this folder

ASSETS_LOCAL = MEDIA_ROOT+'assets/'
ASSETS_URL = URL_ROOT + MEDIA_URL + 'assets/'
IMAGE_WIDTH = 49
IMAGE_HEIGHT = 65

# Email report recipients
EMAIL_RECIPIENTS = ['sanjaykrishn@gmail.com', 'sirdavidwong@gmail.com', 'thomaslam.hm@gmail.com', 'goldberg@berkeley.edu']

# Social media keys
FB_APP_ID = "122406921176585"
FB_SECRET_KEY = "88b0123c6ca39c4e55cfaf50d7337b36"
FB_REDIRECT_URI = URL_ROOT + "/accountsjson/facebook/"
TWITTER_KEY = '7ZgGeudviRlKQFpIKozYeA'
TWITTER_SECRET = 'NXyt7wzm35shKjeAet26emRv8ZkeLwDOutdYyors'

# Minimum floating point precision before sending to client
MIN_FLOAT = 0.0001
NOTIFICATION_SESSIONS = 3
NOTIFICATION_NUMBER = 10
#SMS field
SMS_KEYWORD = "Txthwl"

# if NO_STATEMENTS = True, then we use ratings of comments to place the user
# We use the comments of user_id = 1,...,n, where n is the number and id of each statements
#
# if NO_STATEMENTS = False, we use the n statements as usual
#NO_STATEMENTS = False
SEND_REVISIONS = False
NULL_USER_INDICATOR = "~NULL"
SESSION_COOKIE_NAME = "cookie"

CHOICE_TF = (('true', 'Yes'), ('false', 'No'))
CATEGORIES = [ ('Welcome Page Customizations',
                    ['WELCOME_PAGE_TITLE', 
					 'WELCOME_PAGE_SUBLOGO_TEXT',
                     'OPINIONS_EXPRESSED_NUM_USERS',
                     'USER_POST_TEXT',
                     'ANNOUNCEMENT',
                     'ANNOUNCEMENT_TEXT',
                    ],['2.jpg']),
					
				('Header Image',
                    ['HEADER_IMAGE', 
					 'HEADER_IMAGE_SOURCE',
                     'HEADER_IMAGE_LINK',
                    ],['1.jpg']),
					
			  ('Redesign Variables',
                    ['SHOW_SCORE',
                     'LEADERBOARD_ENABLED',
                     'FUN_COLORS',  
					 'SCORE_SCALE_FACTOR',
					 'YOUR_SCORE_LANGUAGE',
					 'SLIDER_SUBSET',
					 'NO_SKIP',
					 'UNIFIED_SCORE',
					 'EXPLORE_THRESHOLD_RATINGS',
					 'MAX_COMMENT_LENGTH',
					 'BACKGROUND_POINT_MAX_ALPHA',
					 'SHOW_LEADERBOARD_SCORE',
					 'LEADERBOARD_ENABLED',
					 'SOFT_ENTRY_CODES',
					 'ALLOW_EDIT_COMMENT',
					 'SCORE_SIZE',
                    ],[]),
              ('Help and Feedback',
                    ['CONTACT_SUPPORT_EMAIL',
					 'SHOW_FEEDBACK',
					 'FEEDBACK_TEXT',
					 'SHOW_HELP',
					 'HELP_TEXT',
					 'HELP_LOCATION',
                    ],['3.jpg']),
              ('Authentication',
                    ['ALLOW_EXTERNAL_LOGIN',
                     'INCLUDE_FACEBOOK',
                     'FACEBOOK_APP_ID',
                     'INCLUDE_TWITTER',
					 'ALLOW_TWITTER_FB_POST',
                    ],['4.jpg']),
			  ('Sliders',
					['SHOW_AGREEMENT_SLIDER',
					 'AGREEMENT_TEXT',
					 'AGREEMENT_LEFT_TEXT',
					 'AGREEMENT_RIGHT_TEXT',
					 'AGREEMENT_HISTOGRAM_TEXT',
					 'LEGEND_AGREEMENT_LEFT',
					 'LEGEND_AGREEMENT_RIGHT',
					 'SHOW_INSIGHT_SLIDER',
					 'INSIGHT_TEXT',
					 'INSIGHT_LEFT_TEXT',
					 'INSIGHT_RIGHT_TEXT',
					 'INSIGHT_HISTOGRAM_TEXT',
					 'LEGEND_INSIGHT_LEFT',
					 'LEGEND_INSIGHT_RIGHT',
					 ],[]),
              ('Popup Description',
                    ['SHOW_WALKTHROUGH',
                     'WALKTHROUGH_INTRO_TEXT',
                     'WALKTHROUGH_SEARCH_DESCRIPTION',
                     'WALKTHROUGH_TOP_TEXT',
                     'WALKTHROUGH_TEXT',
                    ],['5.jpg']),
			  ('Instruction Text',
                    ['INSTRUCTIONS_1',
                     'INSTRUCTIONS_2',
                     'INSTRUCTIONS_3',
                     'INSTRUCTIONS_4',
                     'INSTRUCTIONS_5',
					 'INSTRUCTIONS_6',
					 'INSTRUCTIONS_7',
                    ],['5.jpg']),
			  ('Map Scaling',
                    ['AFFINE_TRANSFORM_SCALEX',
                     'AFFINE_TRANSFORM_SCALEY',
                     'AFFINE_TRANSFORM_SHIFTX',
                     'AFFINE_TRANSFORM_SHIFTY',
                    ],[]),
			  ('Server Variables',
                    ['MAX_NUM_USER_RATED_DOTS',
                     'MAX_NUM_TOTAL_DOTS',
                     'CONFIDENCE_THRESHOLD',
                     'MINIMUM_WORD_COUNT',        
                     'NUM_BACKGROUND_POINTS',
                     'DEFAULT_FROM_EMAIL',
                     'FEEDBACK_EMAIL_FROM',
                    ],[]),
              ]

all = []
for category in CATEGORIES:
    for i in xrange(len(category[1])):
        category[1][i] = category[1][i].replace('_',' ')
    all.extend(category[1])
#CATEGORIES.append(('OTHER',all))



""" 
CONFIGURABLES README:
 All configurable variables must be defined in the CONFIGURABLES dictionary with its default value.
 For consistency, the default values for each variable must match the values found in the flash client.
 By default, the variables are displayed as text inputs; however this can be changed by specifying additional
 setting k,v pairs in configurables.
 
 Additional Display types:
   SELECT:     this renders the field as a select input;
               to enable, add the key "choices" with its value being a tuple of pairs where each pair contains 
               (actual value, display value). See CHOICE_TF for an example.
   TEXTAREA:   this renders the field as a textarea;
               to enable, add the key "display" with its value being "TEXTAREA"
 
 CAUTION:
  make sure all double quotes are properly escaped if they appear in the default value. 
"""


CONFIGURABLES = {   'PRODUCT_NAME':{'default':'Collective Discovery Engine','name':'Name of the Product'},
					'HEADER_TITLE':{'default':'Opinion Space','name': 'Upper Left Header Main'},
					'HEADER_TITLE_VERSION':{'default':'', 'name': 'Upper Left Header Subtitle'},
					'HEADER_IMAGE':{'default':'false', 'choices':CHOICE_TF,'name':'Upper Left Image?'},
                    'HEADER_IMAGE_SOURCE':{'default':"",'name':'Upper Left Image URL'},                        
                    'HEADER_IMAGE_LINK':{'default':"",'name':'Upper Left Link'}, 
					'WELCOME_PAGE_TITLE':{'default':'The Collective Discovery Engine','name':'Splash Page Title'},

					'WELCOME_PAGE_SUBLOGO_TEXT':{'default':'Question and Description Go Here','name':'Text under main title'}, 
					'OPINIONS_EXPRESSED_NUM_USERS':{'default':'true', 'choices':CHOICE_TF,'name':'Show the number of users in space?'},
					'USER_POST_TEXT':{'default':'PARTICIPANTS','name':'What to call users?'}, 
					'ANNOUNCEMENT':{'default':'true', 'choices':CHOICE_TF,'name':'Text above user count?'},
					'ANNOUNCEMENT_TEXT':{'display':'TEXTAREA','default':'Talk about project and possible incentives','name':'Text above user count'}, 

                    'SHOW_FEEDBACK':{'default':'true', 'choices':CHOICE_TF,'name':'Feedback Link?'},    
                    'CONTACT_SUPPORT_EMAIL':{'default':'sanjaykrishn@gmail.com','name':'Support Email'},
                    'SHOW_HELP':{'default':'true', 'choices':CHOICE_TF,'name':'About Page?'},                        
                    'HELP_TEXT':{'default':"ABOUT",'name':'What to call the about page'},
					'FEEDBACK_TEXT':{'default':"FOUND A BUG?",'name':'Label for feeback link'},
					
					'ALLOW_EXTERNAL_LOGIN':{'default':'true', 'choices':CHOICE_TF,'name':'Enable Social Media Module'},
					'INCLUDE_TWITTER':{'default':'false', 'choices':CHOICE_TF,'name':'Twitter logins'},
					'INCLUDE_FACEBOOK':{'default':'true', 'choices':CHOICE_TF,'name':'Facebook logins'},
					'FACEBOOK_APP_ID':{'default':'376089995779662','name':'Facebook Application ID'},
					'ALLOW_TWITTER_FB_POST':{'default':'true', 'choices':CHOICE_TF,'name':'Allow Posting Ideas to Social Media'},
					
					'SHOW_WALKTHROUGH':{'default':'true', 'choices':CHOICE_TF,'name':'Walkthrough on first time click?'},
					'WALKTHROUGH_INTRO_TEXT':{'display':'TEXTAREA','default':'Welcome to the\nCollaborative Discovery Engine','name':'Title for walkthrough slide 1'},
					'WALKTHROUGH_SEARCH_DESCRIPTION':{'display':'TEXTAREA','default':'The Collective Discovery Engine is focused around a primary question of interest','name':'Walkthrough slide 1 main text'},
                    'WALKTHROUGH_TOP_TEXT':{'display':'TEXTAREA','default':"Note the colorful circular \"blooms\" (like plants). Each bloom represents an idea or answer suggested by a participant. The bloom's position depends on the opinions of its author. Its size and color depend on how others have rated it.\n\nKindle Fires will be awarded for the three best ideas!",'name':'Walkthrough slide 1 paragraph 2'},
					'WALKTHROUGH_TEXT':{'default':'Continue','name':'Walkthrough slide 1 next slide'},
					'WALKTHROUGH_INTRO2_TEXT':{'display':'TEXTAREA','default':'Evaluate other participant\'s ideas by clicking on the blooms.','name':'Walkthrough slide 2 text'},
					'STATEMENTS_INTRO_TEXT':{'display':'TEXTAREA','default':'Now plant your own idea!\nOn the right side there will be 5 propositions. Use the sliders to indicate your opinions on these propositions. Remember to scroll down if neccessary, and click "Done" when finished.','name':'Walkthrough slide after rating done'},
					
					'SHOW_AGREEMENT_SLIDER':{'default':'true', 'choices':CHOICE_TF,'name':'Show top slider(unscored)?'},
					'SHOW_INSIGHT_SLIDER':{'default':'true', 'choices':CHOICE_TF,'name':'Show bottom slider (scored)?'},
					'AGREEMENT_TEXT':{'default':'How innovative is this idea?','name':'Top slider text'},
					'AGREEMENT_LEFT_TEXT':{'default':'Not Innovative','name':'Top slider left'},
					'AGREEMENT_RIGHT_TEXT':{'default':'Very Innovative','name':'Top slider right'},
					'AGREEMENT_HISTOGRAM_TEXT':{'default':'Innovative','name':'Top slider stats page description'},
					'LEGEND_AGREEMENT_LEFT':{'default':'Less Innovative','name':'Top slider lengend left'},
					'LEGEND_AGREEMENT_RIGHT':{'default':'More Innovative','name':'Top slider legend right'},
					'INSIGHT_TEXT':{'default':'How effective is this idea?','name':'Bottom slider text'},
					'INSIGHT_LEFT_TEXT':{'default':'Not Effective','name':'Bottom slider left'},
					'INSIGHT_RIGHT_TEXT':{'default':'Very Effective','name':'Bottom slider right'},
					'INSIGHT_HISTOGRAM_TEXT':{'default':'Effective','name':'Bottom slider stats page description'},
					'LEGEND_INSIGHT_LEFT':{'default':'Less Effective','name':'Bottom slider legend left'},
					'LEGEND_INSIGHT_RIGHT':{'default':'More Effective','name':'Bottom slider legend right'},
					
					'INSTRUCTIONS_1':{'display':'TEXTAREA','default':"Thanks for visiting!  Please start by evaluating the suggestions from\ntwo prior visitors. Click any bloom to start...",'name':'Instruction 1'}, 
					'INSTRUCTIONS_2':{'display':'TEXTAREA','default':"Rating the ideas of other participants earns points.",'name':'Instruction 2'},
					'INSTRUCTIONS_3':{'display':'TEXTAREA','default':"You've earned a point!  Now click another bloom...",'name':'Instruction 3'},
					'INSTRUCTIONS_4':{'display':'TEXTAREA','default':"Great!  To join the discussion and create your own bloom,\njust tell us your opinions...",'name':'Instruction 4'},
					'INSTRUCTIONS_5':{'display':'TEXTAREA','default':"Quickly create your own account...",'name':'Instruction 5'},
					'INSTRUCTIONS_6':{'display':'TEXTAREA','default':"Now enter your own idea (to fill your bloom)!",'name':'Instruction 6'},
					'INSTRUCTIONS_7':{'display':'TEXTAREA','default':"Super! You'll earn points by evaluating more blooms, and \nwhen other participants evaluate your bloom.",'name':'Instruction 7'}, 
					
					'SHOW_SCORE':{'default':'true', 'choices':CHOICE_TF,'name':'Show user score in the bottom left?'},
					'FUN_COLORS':{'default':'true', 'choices':CHOICE_TF,'name':'Use new CDE color scheme?'},
					'LEADERBOARD_ENABLED':{'default':'true', 'choices':CHOICE_TF,'name':'Show the leaderboard?'},  					
					'SCORE_SCALE_FACTOR':{'default':'1.0', 'name':'Scale score by this number'},
					'YOUR_SCORE_LANGUAGE': {'default':'SCORE', 'name':'Language for scoring system, note that this is not just number of ratings.'},
					'NO_SKIP': {'default':'false', 'choices':CHOICE_TF,'name':'No Skipping Comment'},
					'SLIDER_SUBSET': {'default':'5', 'name':'Show at most n of the sliders'},
					'UNIFIED_SCORE':{'default':'true', 'choices':CHOICE_TF,'name':'Combine author and reviewer scores?'},
					'EXPLORE_THRESHOLD_RATINGS':{'default':'2.0', 'name':'Threshold for tutorial score'},
					'MAX_COMMENT_LENGTH':{'default':'1000', 'name':'Max comment length (in chars)'},
					'ALLOW_EDIT_COMMENT':{'default':'true', 'choices':CHOICE_TF,'name':'Allow comment editing?'},
					'SCORE_SIZE':{'default':'42', 'name':'Font size of score text'},
					'BACKGROUND_POINT_MAX_ALPHA':{'default':'0.5', 'name':'Visibility of background points'},
					'SHOW_LEADERBOARD_SCORE':{'default':'true', 'choices':CHOICE_TF,'name':'Leaderboard score?'},
					'LEADERBOARD_ENABLED':{'default':'true', 'choices':CHOICE_TF,'name':'Show leaderboard'},
					'HELP_LOCATION':{'default':'', 'name':'IFRAME to Help Content'},
					
					'AFFINE_TRANSFORM_SCALEX': {'default':'1.0', 'name':'Rescale X coordinate'},
					'AFFINE_TRANSFORM_SCALEY': {'default':'1.0', 'name':'Rescale Y coordinate'},
					'AFFINE_TRANSFORM_SHIFTX': {'default':'0', 'name':'Shift X coordinate right'},
					'AFFINE_TRANSFORM_SHIFTY': {'default':'0', 'name':'Chift Y coordiante down'},

                    #server variables
                    'MAX_NUM_USER_RATED_DOTS':{'default':'300','name':'Max points pulled by the rated query'},
                    'MAX_NUM_TOTAL_DOTS':{'default':'21','name':'Points on the map'}, #for unrated points
                    'MINIMUM_WORD_COUNT':{'default':'5','name':'Word count before shown on map'}, # Required minimum word count for responses returned in shuffle
                    'NUM_BACKGROUND_POINTS':{'default':'500','name':'Background distribution'},
                    'DEFAULT_FROM_EMAIL':{'default':'Hybrid Wisdom Support <support@hybridwisdom.com>','name':'Automated email from'}, # The from address of outgoing emails
                    'FEEDBACK_EMAIL_FROM':{'default':'Hybrid Wisdom Support <support@hybridwisdom.com>','name':'User email from'},
                    'CONFIDENCE_THRESHOLD':{'default':'.15','name':'Standard error thresh before on leaderboard'},
                    'SOFT_ENTRY_CODES':{'default':'false', 'choices':CHOICE_TF,'name':'Use Entry Codes'},
                    }        
SEND_CLIENT_SETTINGS = True
NEVER_SEEN_TIGHT_BOUND = True
SHOW_ADVANCED_OPTIONS = True
