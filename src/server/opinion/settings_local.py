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
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_DIR_NAME = "media"

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'REPLACE_THIS_WITH_SECRET_KEY'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.dirname(DOC_ROOT) + '/../client/' + MEDIA_DIR_NAME + '/'


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
FEEDBACK_EMAIL_TO = 'California Report Card Feedback <messages@californiareportcard.org>'
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
EMAIL_RECIPIENTS = ["angelaslin@berkeley.edu"] # before it was set to None
TROUBLESHOOT_EMAIL_RECIPIENTS = ['patel.jay@berkeley.edu']

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
                 'WELCOME_PAGE_HEADER',
                 'WELCOME_PAGE_TEXT1',
                 'WELCOME_PAGE_TEXT2',
                 'WELCOME_PAGE_ABOUT_LINK'
                 ],['1.png']),
               
               ('About Page',
                ['ABOUT_PAGE_HEADER', 
                 'ABOUT_PAGE_TEXT',
                 ],[]),
               
               ('Report Card',
                ['REPORT_CARD_HEADER',                 
                 'REPORT_CARD_NEXT_BUTTON',
                 'REPORT_CARD_INST',
                 'AVG_EXPLAIN_HEADER',
                 'AVG_EXPLAIN_TEXT',
                 ],['2.png']),

               ('Demographics',
                ['DEMOGRAPHICS_DISCLAIMER'
                ], []),

               ('Zip Code',
                ['ZIP_CODE_INSTRUCTIONS',
                 'ZIP_CODE_BUTTON',

                 ],['3.png']),

               ('CAFE Interface',
                ['DISCUSSION_DIALOG_HEADER',
                 'DISCUSSION_DIALOG_TEXT1',
                 'DISCUSSION_DIALOG_TEXT2',
                 'INSTRUCTIONS_1',
                 'INSTRUCTIONS_2',
                 'INSTRUCTIONS_3',
                 'YOUR_SCORE_LANGUAGE',
                 'SCORE_DIALOG_TEXT',
                 'RATE_IMPORTANCE_QUESTION',
                 'RESPONSE_SAVED_HEADER',
                 'RESPONSE_SAVED_TEXT1',
                 'RESPONSE_SAVED_TEXT2',
                 'EMAIL_ASK_TEXT',
                 'STATS_BUTTON_TEXT',
                 'LOGOUT_BUTTON_TEXT',
                 'LOGOUT_DIALOG_TEXT',
                 'START_OVER_BUTTON_TEXT'
                 ],[]),


               ('Help Pages',
                ['HELP_ABOUT',
                 'HELP_ASSIGN_GRADES',
                 'HELP_MEDIAN_GRADES',
                 'HELP_PRIVACY',
                 'HELP_CAFE_WELCOME',
                 'HELP_CAFE_ABOUT',
                 'HELP_CAFE_ABOUT_MUGS',
                 'HELP_CAFE_LOGOUT_OR_CONTINUE',
                 'HELP_CAFE_SUGGESTION',
                 'HELP_CAFE_GRADE',
                 'HELP_RETURNING_EMAIL'
                ], []),


               ('Sliders',
                [ 'SLIDER1_LEFT',
                 'SLIDER1_RIGHT',
                 'SLIDER2_LEFT',
                 'SLIDER2_RIGHT',
                 ],[]),

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

config_defaults = {
    'WELCOME_PAGE_TEXT1' : "Take a moment to assign grades and share ideas about California's government.",
    'WELCOME_PAGE_TEXT2' : "Works best when holding your mobile screen vertically.",
    'DEMOGRAPHICS_DISCLAIMER': 'Your email address will not be displayed and we promise not to share your email address with any third parties.',
    'ABOUT_PAGE_TEXT' : '''
          <strong>Overview</strong><br/>
          The California Report Card is based on a new interactive platform that engages public interest in government.
          In this experiment, developed by the CITRIS Data and Democracy Initiative at UC Berkeley with advice from Lt. Governor Gavin Newsom and other public officials,
          visitors are invited to grade how effectively state representatives are working to address 6 key subjects.
          Visitors are then asked for suggestions on how California should spend the 2014 budget surplus.
          The platform is designed to engage visitors by providing instant feedback, a unique visualization of opinions, and a new approach to eliciting and rating suggestions.
          The Report Card uses CAFE, a "Collective Assessment and Feedback Engine," modeled after grassroots over coffee, to assess changes over time and to engage public interest in state government.
          <br/><br/>

          <strong>Privacy</strong><br/>
          Comments and suggestions will be scanned to omit identifiable information.
          We respect your privacy and will not share your email address with third parties.<br/><br/>

          <strong>Statistical Significance</strong><br/>

          The California Report Card (CRC) aims to increase communication between elected officials and the public.
          The CRC differs from randomized telephone polls and surveys.
          Participation is self-selective and accessible so far only to English speakers with access to a smart phone or web browser.
          We are working on extending the interface to Spanish speakers and persons with disabilities.

          After you enter each grade, you see the Average Grade based on input from all previous participants.
          This is intended to provide rapid feedback to each participant.
          We realize this may have a biasing effect: some may adjust their grade to be closer to the average resulting in a form of regression toward the mean.
          We will report the number of such adjustments and the before and after values in the public dataset.<br/><br/>

          <strong>More</strong><br/>
          Please see the CRC website for more about the project history, stats to date, related links, and to download anonymized data when it is available:<br/><br/>

          The California Report Card<br/>
          <a href="http://californiareportcard.org/">http://californiareportcard.org/</a>''',
    'INSTRUCTIONS_1' : 'Click on any mug to begin',
    'INSTRUCTIONS_2' : 'To enter your own idea, click on your mug (highlighted in green).',
    'INSTRUCTIONS_3' : "Now what's your idea?  Click on your mug (in green) to join the discussion.",
    'SCORE_DIALOG_TEXT' : "You earn points by rating others and when others rate your idea. Rate one more person's idea before entering your own...",
    'RATE_IMPORTANCE_QUESTION': "How important is this issue for the next Report Card?",
    
    'RESPONSE_SAVED_TEXT1': "Thank you for providing feedback on a way this course could be enhanced to " \
    "make it more valuable for you. You can log out now and return using the unique link that will be emailed " \
    "to you. Or you are welcome to continue grading other students\' ideas.", 
    
    'RESPONSE_SAVED_TEXT2': "Thank you for participating!  Logout now or grade more mugs.",

    'RETURNING_TEXT': "If you have already registered your email with M-Cafe, please enter it here." \
    "You will be able to update your evaluations, add a new suggestion, and read/rate other participants.",
    'HELP_ABOUT': '''To learn more about this project, its history, related projects, and the team that built '''\
    '''it, visit <a href="http://opinion.berkeley.edu/" target="_blank" style="color: #ffffff;">opinion.berkeley.edu</a>.''',
    
     'HELP_ABOUT': '''To learn more about this project, its history, related projects, and the team that built '''\
    '''it, visit <a href="http://opinion.berkeley.edu/" target="_blank" style="color: #ffffff;">opinion.berkeley.edu</a>.''',
    
    'HELP_ASSIGN_GRADES': '''The CRC allows visitors to grade issues facing California. \
Press the buttons to assign grades to these 6 issues facing California (click the skip button for issues where you don\'t want to assign a grade.) \
          <br/><br/> \
          <em>Q:</em> How can I learn more about the six issues we are grading?<br/> \
          <em>A:</em> Here is an overview of each issue:<br/><br/> \
           \
          <div> <em>Implementation of the Affordable Care Act (\'Obamacare\')</em><br/>  \

              California was the first state to pass legislation creating a health insurance marketplace--Covered California. As of Dec 2013, Covered California had over 630,000 enrollees.<br/><br/> \

              <em>Quality of K-12 public education</em><br/> \

              California recently adopted the \"common core\" challenges, which emphasize critical thinking and analysis in K-12 education to better prepare students for college and the workforce.<br/><br/> \ 

              <em>Affordability of state colleges and universities</em><br/> \
              \
              The 2014-15 draft California budget calls for a 10.8% increase in higher education funding, which could keep current tuition costs stable.<br/><br/> \

              <em>Access to state services for undocumented immigrants</em><br/> \
              \
              Passed in 2006, California Senate Bill 1569 extends eligibility for undocumented immigrants in California for food assistance, supplemental security income, and health insurance. \
              Passed in 2011, The California Dream Act grants undocumented immigrant access to state aid at public universities and colleges.<br/><br/> \

              <em>Laws and regulations regarding recreational marijuana</em><br/> \

              California was the first state to legalize the distribution of medical marijuana in 1996. \
              Recreational use of marijuana is illegal in the State of California. However, California lawmakers are currently considering legalizing, taxing, and regulating marijuana for recreational use.<br/><br/> \

              <em>Marriage rights for same-sex partners</em><br/> \

              California legalized same sex marriage in 2008. However, Proposition 8, which revoked marriage rights for same sex couples, was also passed in 2008. \
              Proposition 8 was overturned in 2013.<br/><br/> \
          </div> \

          More information on the issues is available on our project website.<br/><br/> \

          <em>Q:</em> Do I have to grade all issues?<br/> \
          <em>A:</em> No, just click the skip button for issues where you don't want to assign a grade.<br/><br/> \

          <em>Q:</em> Why do the sliders require dragging?  If I tap on A, it should go there.<br/> \
          <em>A:</em> We decided to remove the tap feature since as you slide down to see more issues you may accidentally tap the sliders.<br/><br/> \

          <em>Q:</em> How can I grade K-12 Education when there are so many aspects, the effectiveness of the teachers, or the quality of school facilities, etc.?<br/> \
          <em>A:</em> That\'s a great point; we\'re asking people to give an overall grade, which is indeed a coarse measure! \
          But it\'s also like grading a student for a class, they may have done well on some things, poorly on others, etc...<br/><br/>''',
    
    'HELP_MEDIAN_GRADES': '''<em>Q:</em>  After I enter each grade, the Median Grade based on input from all previous participants is revealed. \
          Then I can change my grade: Won\'t this bias me and other participants?<br/> \

          <em>A:</em> Revealing the Median values is intended to provide instant feedback \
in contrast to traditional polls and surveys. We realize this may have a biasing effect: some may adjust their \
grade to be closer to the average resulting in a form of regression toward the mean. We believe this will be rare, especially for Californians.''',
    
    'HELP_PRIVACY': '''<em>Q:</em> Why do I need to enter my zip code?<br/> \
          <em>A:</em> This will allow participants to compare results by region on a geographic map.''',
    
    'HELP_CAFE_WELCOME': "You are invited to enter an online \"cafe\" where you can propose issues that you\'d like to \
see included in the next report card (version 2.0 will come out later this Spring). \
You\'ll be asked to grade other participants\' suggestions. Each participant\'s suggestion is represented by a mug on the table.",
    
    'HELP_CAFE_ABOUT': '''<em>Q:</em> What should I do on this page?<br/> \
          <em>A:</em> Click any mug (each participant has a mug, we display only 8 at a time)<br/><br/> \
\
          <em>Q:</em> How are the mugs arranged on the table?<br/> \
          <em>A:</em> The placement of each participant's mug is based on how he or she graded the first 6 issues. \
          Think of each issue as one dimension of a 6-dimensional space. \
          The grades you assign define a point in this space.  \
          We use dimensionality reduction (currently Principal Component Analysis) to project that space onto the table. \
          If you and another participant assigned very similar grades, your mugs will be close together.\
          Mugs that are distant from yours belong to participants who graded very differently than you.<br/><br/> \
\
          <em>Q:</em> Why do I only see 8-10 mugs arranged on the table?<br/> \
          <em>A:</em> To avoid overcrowding, we display only a few mugs at a time for grading. \
          The selection of which participants\' mugs to display is random but biased toward newer mugs, those that have received fewer ratings. \
          Specifically, the likelihood of displaying a mug is based on its standard error = stdev / sqrt(k) where k is the number \
of times it has been graded so far, and stdev is the variance of those grades. Over time, this ensures that the confidence, or \
error-bar on the estimated grade for each mug, tends to be the same length for all mugs. Each time you finish grading a set of mugs, \
the table will be refreshed with more mugs.<br/><br/>''',
    
    'HELP_CAFE_ABOUT_MUGS': '''You can continue grading more mugs and whenever you\'re ready, just click on your mug \
(with the blue coaster) to enter an issue that you\'d like to see on the next report card (version 2.0 will come \
out later this Spring).<br/><br/> \
          <em>Q:</em> Why is my mug located at this position on the table?<br/> \
          <em>A:</em> The placement of each participant's mug is based on how he or she graded the first 6 issues. \
          Think of each issue as one dimension of a 6-dimensional space. \
          The grades you assign define a point in this space. We use dimensionality reduction (currently Principal \
Component Analysis) to project that space onto the table. \
If you and another participant assigned very similar grades, your mugs will be close together. \
Mugs that are distant from yours belong to participants who graded very differently than you.''',
    
    'HELP_CAFE_LOGOUT_OR_CONTINUE': 'You can either log out now and return anytime using the unique link we emailed you. \
Or you are welcome to continue grading participants\' suggestions for the next report card (version 2.0 will come out later this Spring).' ,
    
    'HELP_CAFE_SUGGESTION': 'Please propose an issue you\'d like to see on the next report card \
(version 2.0 will come out later this Spring).  Click Save when you\'re done.',
    
    'HELP_CAFE_GRADE': '''<em>Q:</em> How do I grade a suggestion?<br/> \
          <em>A:</em> After clicking a mug, that participant\'s suggestion is displayed. \
          You can skip to another one or mark this suggestion as irrelevant or inaccurate \
          (click again to undo).  Otherwise, drag the two slider handles to assign grades.<br/><br/>''',
    
    'HELP_RETURNING_EMAIL': '''<em>Q:</em> Why should I enter my email address?<br/>''' \
    '''<em>A:</em> So we can send you a unique link to see the grades your suggested issue receives.''',
    

    'EMAIL_ASK_TEXT' : "Please provide your email to receive a customized link where you can see how others rate your idea.",
    'LOGOUT_DIALOG_TEXT' : """Thank you for participating!""",
    'REPORT_CARD_INST' : "Drag the handle to grade from A to F how well you feel California's elected officials are working to address the following 6 subjects:",
    'ZIP_CODE_INSTRUCTIONS' : "Enter your zip code to save your grades and join the discussion",
    'DISCUSSION_DIALOG_TEXT1' : "Thank you for grading these issues.  We now invite you to consider and propose additional issues you feel should have priority for attention at the state level.", 
    'DISCUSSION_DIALOG_TEXT2' : '',
    'AVG_EXPLAIN_TEXT' : "The Median Grade is based on the grades from all participants thusfar."
}

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


CONFIGURABLES = {   
    'PRODUCT_NAME':{'default':'Collective Discovery Engine','name':'Name of the Product'},
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


    ##########################
    # NEW CAFE CONFIGURABLES
    # (note: some of these are duplicated from above)
    ##########################

    'WELCOME_PAGE_TITLE':{'default':'California Report Card','name':'Welcome Page Title'},
    'WELCOME_PAGE_HEADER':{'default':'''California<br />Report Card''','name':'Welcome Page Header'},
    'WELCOME_PAGE_TEXT1':{'display':'TEXTAREA', 'default':config_defaults['WELCOME_PAGE_TEXT1'],'name':'Welcome Page Top'},
    'WELCOME_PAGE_TEXT2':{'display':'TEXTAREA', 'default':config_defaults['WELCOME_PAGE_TEXT2'],'name':'Welcome Page Bottom'},
    'WELCOME_PAGE_ABOUT_LINK' : {'default':'ABOUT','name':'Welcome Page - About Link'},

    'ABOUT_PAGE_HEADER':{'default':'About','name':'About Page Header'},
    'ABOUT_PAGE_TEXT':{'display':'TEXTAREA', 'default':config_defaults['ABOUT_PAGE_TEXT'],'name':'About Page Text (HTML)'},

    'REPORT_CARD_HEADER':{'default':"Grade California",'name':'Report Card Header'},
    'REPORT_CARD_NEXT_BUTTON':{'default':'Next','name':'Report Card Next Button'},
    'REPORT_CARD_INST' : {'display':'TEXTAREA', 'default':config_defaults['REPORT_CARD_INST'],'name':'Report Card Instructions'},
    'AVG_EXPLAIN_HEADER' : {'default':"Median Grades",'name':'Averages Explanation Header'},
    'AVG_EXPLAIN_TEXT' : {'display':'TEXTAREA', 'default':config_defaults['AVG_EXPLAIN_TEXT'],'name':'Avg Explanation Text'},
    
 
    'DEMOGRAPHICS_DISCLAIMER':{'display': 'TEXTAREA', 'default': config_defaults['DEMOGRAPHICS_DISCLAIMER'], 'name': 'Demographics Disclaimer'},

    'RESPONSE_SAVED_TEXT1':{'display': 'TEXTAREA', 'default': config_defaults['RESPONSE_SAVED_TEXT1'], 'name': 'Response Saved - Use Email Link or Continue'},
    'RESPONSE_SAVED_TEXT2':{'display': 'TEXTAREA', 'default': config_defaults['RESPONSE_SAVED_TEXT2'], 'name': 'Response Saved - Continue or Logout'},

    'RETURNING_TEXT':{'display': 'TEXTAREA', 'default': config_defaults['RETURNING_TEXT'], 'name': 'Returning Users Prompt'},


    'HELP_ABOUT': {'display': 'TEXTAREA', 'default': config_defaults['HELP_ABOUT'], 'name': 'Help - Learn about the team'},
    'HELP_ASSIGN_GRADES': {'display': 'TEXTAREA', 'default': config_defaults['HELP_ASSIGN_GRADES'], 'name': 'Help - How to Assign Grades'},
    'HELP_MEDIAN_GRADES': {'display': 'TEXTAREA', 'default': config_defaults['HELP_MEDIAN_GRADES'], 'name': 'Help - How are Median Grades Calculated'},
    'HELP_PRIVACY': {'display': 'TEXTAREA', 'default': config_defaults['HELP_PRIVACY'], 'name': 'Help - Privacy and Email'},
    'HELP_CAFE_WELCOME': {'display': 'TEXTAREA', 'default': config_defaults['HELP_CAFE_WELCOME'], 'name': 'Help - Welcome to the CAFE portion'},
    'HELP_CAFE_ABOUT': {'display': 'TEXTAREA', 'default': config_defaults['HELP_CAFE_ABOUT'], 'name': 'Help - About the CAFE portion'},
    'HELP_CAFE_ABOUT_MUGS': {'display': 'TEXTAREA', 'default': config_defaults['HELP_CAFE_ABOUT_MUGS'], 'name': 'Help - Mug Positioning Algorithm'},
    'HELP_CAFE_LOGOUT_OR_CONTINUE': {'display': 'TEXTAREA', 'default': config_defaults['HELP_CAFE_LOGOUT_OR_CONTINUE'], 'name': 'Help - Logout or Continue Grading'},
    'HELP_CAFE_SUGGESTION': {'display': 'TEXTAREA', 'default': config_defaults['HELP_CAFE_SUGGESTION'], 'name': 'Help - Suggestion'},
    'HELP_CAFE_GRADE': {'display': 'TEXTAREA', 'default': config_defaults['HELP_CAFE_GRADE'], 'name': 'Help - Grade a Suggestion'},
    'HELP_RETURNING_EMAIL': {'display': 'TEXTAREA', 'default': config_defaults['HELP_RETURNING_EMAIL'], 'name': 'Help - Returning Email Link'}, 

    'ZIP_CODE_INSTRUCTIONS':{'display':'TEXTAREA', 'default':config_defaults['ZIP_CODE_INSTRUCTIONS'],'name':'Zip Code Instructions'},
    'ZIP_CODE_BUTTON':{'default':'Save and Join','name':'Zip Code Button'},

    'DISCUSSION_DIALOG_HEADER':{'default':'The Discussion','name':'Discussion Dialog Header'},
    'DISCUSSION_DIALOG_TEXT1':{'display':'TEXTAREA', 'default':config_defaults['DISCUSSION_DIALOG_TEXT1'],'name':'Discussion Text1'},
    'DISCUSSION_DIALOG_TEXT2':{'display':'TEXTAREA', 'default':config_defaults['DISCUSSION_DIALOG_TEXT2'],'name':'Discussion Text2'},

    'INSTRUCTIONS_1':{'display':'TEXTAREA', 'default':config_defaults['INSTRUCTIONS_1'],'name':'Instructions 1'},
    'INSTRUCTIONS_2':{'display':'TEXTAREA', 'default':config_defaults['INSTRUCTIONS_2'],'name':'Instructions 2'},
    'INSTRUCTIONS_3':{'display':'TEXTAREA', 'default':config_defaults['INSTRUCTIONS_3'],'name':'Instructions 3'},
    
    'SLIDER1_LEFT' : {'default':'Not Important','name':'Slider 1 Left'},
    'SLIDER1_RIGHT' : {'default':'Very Important','name':'Slider 1 Right'},
    'SLIDER2_LEFT' : {'default':'Not Interested','name':'Slider 2 Left'},
    'SLIDER2_RIGHT' : {'default':'Very Interested','name':'Slider 2 Right'},

    'YOUR_SCORE_LANGUAGE': {'default':'Your Score', 'name':'Language for scoring system, (Note: This is not just number of ratings.'},
    'SCORE_DIALOG_TEXT' : {'display':'TEXTAREA', 'default':config_defaults['SCORE_DIALOG_TEXT'],'name':'Score Dialog Text'},

    'RATE_IMPORTANCE_QUESTION' : {'display':'TEXTAREA', 'default':config_defaults['RATE_IMPORTANCE_QUESTION'],'name':'Rate Importance Question - Other People\'s Suggestsions'},

    'RESPONSE_SAVED_HEADER' : {'default':'Response Saved!', 'name':'Response Saved Header'},

    'EMAIL_ASK_TEXT' : {'display':'TEXTAREA', 'default':config_defaults['EMAIL_ASK_TEXT'],'name':'Ask for Email Text'},

    'STATS_BUTTON_TEXT' : {'default':'Stats','name':'Stats Button Text'},
    'LOGOUT_BUTTON_TEXT' : {'default':'Logout','name':'Logout Button Text'},    
    'LOGOUT_DIALOG_TEXT' : {'display':'TEXTAREA', 'default':config_defaults['LOGOUT_DIALOG_TEXT'],'name':'Logout Dialog Text'},
    'START_OVER_BUTTON_TEXT' : {'default':'Start Over','name':'Logout Page - Start Over Button Text'},    

    #server variables
    'MAX_NUM_USER_RATED_DOTS':{'default':'300','name':'Max points pulled by the rated query'},
    'MAX_NUM_TOTAL_DOTS':{'default':'21','name':'Points on the map'}, #for unrated points
    'MINIMUM_WORD_COUNT':{'default':'5','name':'Word count before shown on map'}, # Required minimum word count for responses returned in shuffle
    'NUM_BACKGROUND_POINTS':{'default':'500','name':'Background distribution'},
    'DEFAULT_FROM_EMAIL':{'default':'California Report Card Admin <CRC-admin@californiareportcard.org>','name':'Automated email from'}, # The from address of outgoing emails
    'FEEDBACK_EMAIL_FROM':{'default':'Hybrid Wisdom Support <support@hybridwisdom.com>','name':'User email from'},
    'CONFIDENCE_THRESHOLD':{'default':'.15','name':'Standard error thresh before on leaderboard'},
    'SOFT_ENTRY_CODES':{'default':'false', 'choices':CHOICE_TF,'name':'Use Entry Codes'},
    }        
SEND_CLIENT_SETTINGS = True
NEVER_SEEN_TIGHT_BOUND = True
SHOW_ADVANCED_OPTIONS = True
HORIZONTAL_SLIDE= False
