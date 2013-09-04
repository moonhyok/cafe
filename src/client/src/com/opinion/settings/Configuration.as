package com.opinion.settings{
	import flash.utils.Dictionary;
	
	public class Configuration
	{
		public static var OPINION_SPACE_ID:int = 1; // For now, we hardcode the OS ID - you can change this to allow multiple OS instances if needed
		
		//Title Branding
		public static var PRODUCT_NAME:String = "Collective Discovery Engine"; //This name is propagated down to all relevant options
		[Bindable] public static var HEADER_TITLE:String = "OPINION SPACE"; //Project Name
		[Bindable] public static var HEADER_TITLE_VERSION:String = "LEARNING"; //Project subtitle
		[Bindable] public static var HEADER_IMAGE:Boolean = false; //Project logo
		[Bindable] public static var HEADER_IMAGE_SOURCE:String = "";
		[Bindable] public static var HEADER_IMAGE_LINK:String = "";
		[Bindable] public static var WELCOME_PAGE_TITLE:String = "THE COLLECTIVE DISCOVERY ENGINE";
		[Bindable] public static var FUN_COLORS:Boolean =true;
		[Bindable] public static var NO_SKIP:Boolean = false;
		[Bindable] public static var COMMENT_TITLES:Boolean = false;
		
		[Bindable] public static var SLIDER_SUBSET:int = 5;
		[Bindable] public static var SCORE_SIZE:int = 35;
		
		[Bindable] public static var HELP_LOCATION:String = "";
		
		//Welcome page
		[Binbable] public static var WELCOME_PAGE_SUBLOGO_TEXT:String = "The Role of Social Media in Primary and Secondary Education";
		[Binbable] public static var OPINIONS_EXPRESSED_NUM_USERS:Boolean = true;
		[Binbable] public static var USER_POST_TEXT:String = "PARTICIPANTS";
		[Binbable] public static var ANNOUNCEMENT:Boolean = false;
		[Binbable] public static var ANNOUNCEMENT_TEXT:String = String("Social Media and Education").toUpperCase();
		
		//User help features
		[Bindable] public static var SHOW_FEEDBACK:Boolean = false; //feedback (error emails)
		[Bindable] public static var FEEDBACK_TEXT:String = "FOUND A BUG?";
		[Bindable] public static var SHOW_HELP:Boolean = true; //help page (also called aboutpage)
		[Bindable] public static var HELP_TEXT:String = "ABOUT";
		
		//Login Details
		[Bindable]public static var ALLOW_EXTERNAL_LOGIN:Boolean = true;//allow facebook and twitter
		[Bindable] public static var INCLUDE_FACEBOOK:Boolean = true;
		[Bindable] public static var FACEBOOK_APP_ID:String = "376089995779662";
		[Bindable] public static var INCLUDE_TWITTER:Boolean = false;
		[Bindable] public static var ALLOW_TWITTER_FB_POST:Boolean = true;
		
		//Sliders
		[Bindable] public static var SHOW_AGREEMENT_SLIDER:Boolean = true;
		[Bindable] public static var AGREEMENT_TEXT:String = "How innovative is this idea?";
		[Bindable] public static var AGREEMENT_LEFT_TEXT:String = "Not innovative";
		[Bindable] public static var AGREEMENT_RIGHT_TEXT:String = "Very innovative";
		[Bindable] public static var AGREEMENT_HISTOGRAM_TEXT:String = "Innovative";
		[Bindable] public static var LEGEND_AGREEMENT_LEFT:String = "Less Innovative";
		[Bindable] public static var LEGEND_AGREEMENT_RIGHT:String = "More Innovative";
		[Bindable] public static var SHOW_INSIGHT_SLIDER:Boolean = true;
		[Bindable] public static var INSIGHT_TEXT:String = "How effective will this idea be?";
		[Bindable] public static var INSIGHT_LEFT_TEXT:String = "Not Effective";
		[Bindable] public static var INSIGHT_RIGHT_TEXT:String = "Very Effective";
		[Bindable] public static var INSIGHT_HISTOGRAM_TEXT:String = "Effective";
		[Bindable] public static var LEGEND_INSIGHT_LEFT:String = "Less Effective";
		[Bindable] public static var LEGEND_INSIGHT_RIGHT:String = "More Effective";

		// Walkthrough
		[Bindable] public static var SHOW_WALKTHROUGH:Boolean = false;
		[Bindable] public static var WALKTHROUGH_INTRO_TEXT:String = "Welcome to the\n"+ "Collective Discovery Engine";
		[Bindable] public static var WALKTHROUGH_SEARCH_DESCRIPTION:String = "The "+"Collective Discovery Engine"+" is focused around a primary question of interest, such as \“How can social media be used to benefit primary and secondary learning?\”";
		[Bindable] public static var WALKTHROUGH_TOP_TEXT:String = "Note the colorful circular \"blooms\" (like plants). Each bloom represents an idea or answer suggested by a participant. The bloom's position depends on the opinions of its author. Its size and color depend on how others have rated it.\n\nNexus 7's will be awarded for the three best ideas!";
		[Bindable] public static var WALKTHROUGH_TEXT:String = "Continue";
		
		public static var EXPLORE_THRESHOLD_RATINGS:Number = 2.0*SCORE_SCALE_FACTOR;
		
		[Bindable] public static var INSTRUCTIONS_1:String = "Thanks for visiting!  Please start by evaluating the suggestions from\ntwo prior visitors. Click any bloom to start...";
		[Bindable] public static var INSTRUCTIONS_2:String = "Rating the ideas of other participants earns points.";
		[Bindable] public static var INSTRUCTIONS_3:String = "You've earned a point!  Now click another bloom...";
		[Bindable] public static var INSTRUCTIONS_4:String = "Great!  To join the discussion and create your own bloom,\njust tell us your opinions...";
		[Bindable] public static var INSTRUCTIONS_4alt:String = "Thank you for visiting!  To join the discussion, respond to these two questions:";
		[Bindable] public static var INSTRUCTIONS_5:String = "Quickly create your own account...";
		[Bindable] public static var INSTRUCTIONS_6:String = "Now enter your own idea (to fill your bloom)!";
		[Bindable] public static var INSTRUCTIONS_7:String = "Super! You'll earn points by evaluating more blooms, and \nwhen other participants evaluate your bloom.";
		
		//deprecated
		[Bindable] public static var WALKTHROUGH_INTRO2_TEXT:String = "Evaluate 2 other participants' ideas by clicking on the blooms.";
		[Bindable] public static var STATEMENTS_INTRO_TEXT:String = "Now plant your own idea!\nOn the right side there will be 8 propositions. Use the sliders to indicate your opinions on these propositions. Remember to scroll down if neccessary, and click \"Done\" when finished.";
		[Bindable] public static var FIRST_TIME_RATE_STEP:String = "";
		[Bindable] public static var FIRST_TIME_RATE_PROMPT:String = "Click any bloom to begin.";//"Rate " + int(EXPLORE_THRESHOLD_RATINGS).toString() + " responses to the following question. Click any bloom to begin.";
		[Bindable] public static var FIRST_TIME_STATEMENT_STEP:String = "";
		[Bindable] public static var FIRST_TIME_STATEMENTS_INSTRUCTIONS:String = "Please express your opinions on the statements to the right.  Note how your bloom moves in response.";
		[Bindable] public static var FIRST_TIME_SIGNUP_STEP:String = "";
		[Bindable] public static var FIRST_TIME_SIGNUP_INSTRUCTIONS:String = "After registration you can submit your own idea to the discussion.";
		[Bindable] public static var COMMENT_NOT_FINISHED_TEXT:String = "";
		[Bindable] public static var POST_REGISTRATION_TITLE:String = "Thank you!  Please contribute your own idea...";
		[Bindable] public static var POST_REGISTRATION_TEXT:String = "We welcome your ideas for how social media can be used to improve pirmary and secondary education.   If you do not wish to enter an idea now, click \"Skip\". You can always enter one later.";
		[Bindable] public static var POST_LEAVERESPONSE_TITLE:String = "Thank you for joining the discussion!";
		[Bindable] public static var POST_LEAVERESPONSE_TEXT:String = "You are now done placing your bloom. You should now read and evaluate the responses of other participants. You can track your progress in the Stats tab.";
		[Bindable] public static var YOUR_SCORE_LANGUAGE:String = "Score: ";
		
		//Contact email
		[Bindable] public static var CONTACT_SUPPORT_EMAIL:String = "sanjaykrishn@gmail.com";
		
		
		//System configurables below
		
		
		/***********************************************************************************************************
		************ System config below, user should not be allowed to modify these through the database **********
		************************************************************************************************************/
		
		
		public static var DEBUG_LOGGING:Boolean = false;
		[Embed(source='/assets/fonts/helvetica/HelveticaNeueLTStd-Roman.otf', fontFamily='Helvetica')] public static var Helvetica:Class;
		/*Eye-candy
		 ****
		 * Section relates to effects and animations that can be removed without breaking anything
		 */
		public static var BANG_ON:Boolean = true; //Big Bang Effect
		public static var ARCS_ON:Boolean = false; //Draw Arcs
		public static var ALLOW_USER_TO_SEE_RATERS:Boolean = true; //Users that have rated me
		public static var SHOW_RATERS_BUTTON:String = "Show users that have rated me"; 
		public static var HIDE_RATERS_BUTTON:String = "Hide users that have rated me"; 
		public static var USE_PROFILE_PIC:Boolean = false;
		public static var PROFILE_PIC_WIDTH:int = 49;
		public static var PROFILE_PIC_HEIGHT:int = 65;
		public static var PROFILE_PIC_TOOLTIP:String = "Click here to upload your own profile picture.";
		[Embed(source="/assets/img/default-user-image.png")] public static var UNKNOWN_USER:Class;
		
		// Upload.mxml
		public static var PICTURE_UPLOAD_ON:Boolean = false;
		public static var PICTURE_UPLOAD_TEXT:String = "\n\nTo change your profile picture, please upload a picture. Be aware that this picture will be saved on the Opinion Space server and will visible to all other users. We currently support JPEG, PNG, and GIF images.";
		
		/*Header
		 ****
		 * Title text and formatting
		 * Misc text
		 * Determines whether to use the default "welcome xyz from xyz author score:..." header or a custom header
		 */
		public static var USE_DEFAULT_HEADER:Boolean = false;
		public static var CUSTOM_HEADER:String = "Custom Header Goes Here";

		

		/*Footer
		****
		*Footer, as layed out in opinionflex.mxml, it contains links and is something that will have to be modified for each client
		*each client will presumably have a different set of logos and links to use.
		*/
		
		//BCNM LOGO--should probably be in every instance of OS, but just in case
		//[Embed(source="assets/img/bcnm_logo_resized.png")] public static var BCNM_LOGO:Class;
			//											   public static var BCNM_DESCRIPTION:String = "Berkeley Center for New Media";
				//										   public static var BCNM_HYPERLINK:String = 'http://bcnm.berkeley.edu';
					//									   public static var SHOW_BCNM:Boolean = false;
		//Client LOGO												   
		//[Embed(source="assets/img/bcnm_logo_resized.png")] public static var CLIENT_LOGO:Class; lets be efficient...
		//public static var CLIENT_LOGO:Class = BCNM_LOGO;
			//													public static var CLIENT_DESCRIPTION:String = "My Company Inc.";
				//												public static var CLIENT_HYPERLINK:String = "http://localhost/";
					//											public static var SHOW_CLIENT_LOGO:Boolean = false;
		//Additional Links														
		public static var USE_ADDITIONAL_LINKS:Boolean = false; //toggle on or off
		public static var ADDITIONAL_LINKS_DESCRIPTION:String = "Other Social Medial Link"; //label for the additional links menu
		public static var ADDITIONAL_LINKS:Array = new Array("http://blogs.state.gov/", "http://www.state.gov/misc/echannels/66791.htm", 
			"https://service.govdelivery.com/service/multi_subscribe.html?code=USSTATEBPA", "http://www.facebook.com/usdos", 
			"http://www.youtube.com/user/statevideo", "http://www.flickr.com/photos/statephotos", "http://twitter.com/dipnote"); 
		//^List of URLS, Must match 1 - 1 for the corresponding labels below 
		public static var ADDITIONAL_LINKS_LABELS:Array = new Array("Dipnote Blog", "RSS Feeds", "Email Subscriptions", "Facebook", "YouTube", "Flickr", "Twitter");
		
		
		//Twitter
		//[Embed(source="assets/img/twitter_favicon.jpg")] public static var TWITTER_ICON:Class;
			//											 public static var TWITTER_DESCRIPTION:String = "Follow us on Twitter!";
				//										 public static var TWITTER_HYPERLINK:String= "http://twitter.com/OpinionSpace";
					//									 public static var SHOW_TWITTER:Boolean = false;
		
		[Embed(source="/assets/images/twitter-signin.png")] public static var TWITTER_IMAGE:Class; // Login image
														 
	   /* Text and Presentation 
		****
		* This section relates to configuring Text and Buttons, for the most part its just a substitution of variables for
		* ones referenced in the this file.
		*/
		//The Minimum Dimensions of the space
		public static var MIN_WIDTH:int = 890;
		public static var MIN_HEIGHT:int = 540;
		
		//Facebook config
		//Flag for facebook popup notification
		public static var FACEBOOK_POPUP_TEXT:String = "Click OK after you log in to Facebook\n\nIf you are unable to see a new window please allow popups for this site, press OK and try again.";
		
		//facebook connect image
		[Embed(source="/assets/images/facebook-signin.png")] public static var FACEBOOK_CONNECT_IMAGE:Class		
		
		/* Module Specific Configuration Variables
		 ****
		 * This section contains any variables needed in configuring a core module.
		 * If you need to configure values in a module that are not present here, add
		 * a variable here and replace the value in the module with the variable
		 */
		 
		// OpinionMap.mxml variables
		public static var MAP_LEFT_PANEL_PADDING_BOTTOM:Number = 55;
		public static var SHOW_DEMO:Boolean = false; // Show the walkthrough for first time users
		public static var EDIT_PROFILE_ENABLED:Boolean = false;
		
		[Bindable] public static var MAX_COMMENT_LENGTH:int = 1000;
		
		// map notifications
		public static var MAP_NOTIFICATION_TIMEOUT:int = 4000;
		public static var RATED_ALL_COMMENTS_MSG:String = "You have rated all the ideas in the space...";
		public static var NOT_RATED_ANY_RESP_MSG:String = "You have not rated any ideas yet...";
		public static var NOT_RATED_BY_OTHER_MSG:String = "Your idea has not yet been rated by other participants...";
		public static var FINISHED_SERIALIZED_MSG:String = "To get started, click on any of the white points in the space.";
		public static var NO_RATED_UPDATED_MSG:String = "There are no newly updated ideas...";
		public static var NO_NEW_RESPONSES_MSG:String = "There are no new participant ideas...";
		
		// Toolbar variables
		public static var LENSES_ENBALED:Boolean = false;
		public static var LENSES_DISPLAY_NAME:String = "Lenses";
		public static var LENSES_COLOR_PALETTE:Array = [0x67001F, 0xB2182B, 0xD6604D, 0xF4A582, 0xFDDBC7, 0xF7F7F7, 0xD1E5F0, 0x92C5DE, 0x4393C3, 0x2166AC, 0x053061]; // From Cynthia Brewer
		public static var LENSES_COLOR_BY_RESPONSE_COLORS:Array = [0xCC0033, 0xFFCC33, 0x00CC99];
		
		public static var QUERIES_ENABLED:Boolean = true;
		public static var QUERIES_DISPLAY_NAME:String = "";
		public static var FILTER_FIELD_MAX_WIDTH:int = 180;
        
        public static var ALL_COMMENTS_LABEL:String = "All participants";
        public static var ALL_COMMENTS_ENABLED:Boolean = false;
        public static var ALL_COMMENTS_TOOLTIP:String = "Click here to show all ideas in the space";
        public static var SHUFFLE_LABEL:String = "More Ideas";
        public static var SHUFFLE_ENABLED:Boolean = false;
        public static var SHUFFLE_TOOLTIP:String = "Click here to see ideas that you have not yet rated";
        
        public static var UPDATED_TOOLTIP:String = "Click here to see ideas you've rated that have been updated";
        
        // Leaderboard Variables - lists are now configurable
        public static var LEADERBOARD_LABEL:String = "Top Ideas";
        [Bindable] public static var LEADERBOARD_ENABLED:Boolean = false;
        public static var LEADERBOARD_TOOLTIP:String = "Click here to see the top ideas in the space";
       [Bindable] public static var SHOW_SCORE:Boolean = true;
	   [Bindable] public static var SHOW_LEADERBOARD_SCORE:Boolean = false;
        public static var LIST_1:String = "Leaderboard";
        public static var LIST_1_ENABLED:Boolean = true;
        public static var LIST_2:String = "TOP IDEAS 11-20";
        public static var LIST_2_ENABLED:Boolean = false;
        public static var LIST_3:String = "Rising Authors";
        public static var LIST_3_ENABLED:Boolean = false;
        
        public static var RATED_LABEL:String = "Rated Ideas";
        public static var RATED_ENABLED:Boolean = false;
        public static var RATED_TOOLTIP:String = "Click here to see the ideas you have rated";
        public static var RATED_BY_LABEL:String = "Who's rated me";
        public static var RATED_BY_ENABLED:Boolean = false;
        public static var RATED_BY_TOOLTIP:String = "Click here to see the ideas of the participants who have rated you";
        
        // Dot and drawing/visualization variables
        public static var USER_DOT_COLOR:Number = 0x00F5FE;//0x525252;
        public static var USER_DOT_ALPHA:Number = 1;
        public static var OTHER_DOT_ALPHA:Number = .85;
        public static var LOW_CONFIDENCE_DOT_COLOR:Number = 0xffffff;//0x9f99cb; // Color for new responses with low confidence
        public static var LOW_CONF_ALPHA:Number = 0.7;//0.7;
        public static var OTHER_DOT_UNCOMMENTED_ALPHA:Number = .2; // Make this smaller if you want the dots w/o comments to be darker
        public static var OTHER_DOT_COLOR:Number = 0xffffff;
        public static var MOUSEOVER_ALPHA:Number = 1.0;
        public static var MOUSEOVER_COLOR:Number = 0x3555a5;//0xf0f56e;
        public static var LANDMARK_ALPHA:Number = 0.5;
        public static var LANDMARK_COLOR:Number = 0x0090ff;
        [Bindable] public static var BACKGROUND_POINT_MAX_ALPHA:Number = 0.0;
        
		// Rating color (rating buckets go from lowest rating to highest rating)
        public static var BUCKET_1_COLOR:Number = 0xe04f63;
		public static var BUCKET_2_COLOR:Number = 0xd4823f;
        public static var BUCKET_3_COLOR:Number = 0xfcc281;
        public static var BUCKET_4_COLOR:Number = 0x8cc63f;
        public static var BUCKET_5_COLOR:Number = 0x5f9b3c;
        public static var BUCKET_6_COLOR:Number = 0x8bb13f; 
		
		// Welcome text properties
		public static var WELCOME_TEXT_INTRODUCTION:String = "Welcome to Opinion Space";
		public static var WELCOME_TEXT_BODY:String = "Opinion Space is designed to help communities exchange ideas and suggestions about the issues, policies, and products they are passionate about.  Opinion Space introduces a graphical \"starfield\" that displays patterns, trends, and insights from all members and a game structure that rewards the most active and insightful members.\n\nClick a point to see how it works...then join the discussion!";
		public static var WELCOME_TEXT_COLOR:Number = 0xffffff;
		public static var WELCOME_TEXT_OFFSET_Y:Number = 10;
		public static var WELCOME_TEXT_WIDTH:Number = 220;
		
		// First time instructional text on OpinionMap.mxml mapLeftPanel
		public static var FIRST_TIME_INSTRUCTION_TEXT:String = "[Sample]: PRESS PLAY FOR AN OPINION SPACE DEMO";
		
		// Flags for optional parameters
		public static var REFRESH_BUTTON_VISIBLE:Boolean = false;
		 
		// OpinionMap.mxml Add Ons
		public static var OPINION_MAP_ADD_ON:Boolean = false;
		public static var OPINION_MAP_ADD_ONS:Array = [];		
		
		// RatingModule.mxml variables
		public static var TEXT_NORMAL:Number = 0x646462;
		public static var TEXT_OVER:Number = 0x777777;
		public static var ALLOW_EDIT_COMMENT:Boolean = true;
		public static var ALLOW_EDIT_SLIDERS:Boolean = true;
		public static var REVERT_TO_BG_SLIDER_TEXT:String = "Go back to my position";
		public static var RATING_MODULE_SLIDER_TOOLTIP_ENABLED:Boolean = false;
		public static var RATING_MODULE_SLIDER_TOOLTIP:String = "Drag the slider to rate this statement from strongly disagree (left) to strongly agree (right)";
		
		public static var YOUR_PROFILE_TITLE:String = "Your Idea";
		
		//size of the comment input text area
		public static var RATING_MODULE_COMMENT_INPUT_TEXT_HEIGHT:int = 125;
		
		// CommentModule.mxml variables
		public static var COMMENT_MODULE_COMMENT_INPUT_TEXT_HEIGHT:int = 125;
		public static var ALLOW_VIEW_OPINIONS:Boolean = false;
		
		// SignupPage.mxml variables
		public static var SHOW_PRIVACY_POLICY:Boolean = false;
		public static var REGISTER_FORM_WIDTH:int = 425;
		public static var SHOW_DECLINE_TO_STATE:Boolean = true;
		public static var REGISTRATION_FIELDS_TABLE:Object = {'username': {'show' : true, 'required' : true}, // required field unused as we take the asterisk out of the UI
																'location': {'show' : true, 'required' : false}, 
																'email': {'show' : true, 'required' : true}, 
																'sex': {'show' : false, 'required' : true}, 
																'age-group': {'show' : true, 'required' : false},
																'firstname': {'show' : false, 'required' : true},
																'lastname': {'show' : false, 'required' : true},
																'picture': {'show' : false, 'required' : true},
																'question': {'show' : false, 'required' : false},
																'answer': {'show' : false, 'required' : false},
																'url': {'show' : false, 'required' : false},
																'heard_about': {'show' : false, 'required' : false}
																}; 		
		public static var SIGNUP_PAGE_REGISTER_PROMPT:String = "Create an account";
		public static var REGISTER_BUTTON_TEXT:String = "Create Account";
		public static var USERNAME_INSTRUCTION_TEXT:String = "Choose a username that is between 3 and 30 characters and contains only letters and numbers";
		public static var EMAIL_INSTRUCTION_TEXT:String = "";//"Recommended as an easy-to-remember way to login";
		
		// CheckAvailability.mxml
		public static var SHOW_CHECKCROSS_IMAGES:Boolean = false;
		public static var USERNAME_AVAILABLE_TEXT:String = "Username is available!";
		public static var USERNAME_UNAVAILABLE_TEXT:String = "Sorry, this username has been taken.";
		public static var YOUR_USERNAME_TEXT:String = "This is your current username.";
		public static var USERNAME_CHECKING_TEXT:String = "Checking availability...";
		public static var USERNAME_INVALID_TEXT:String = "This username is invalid.";
		
		// SignupPage.mxml Add Ons
		public static var SIGNUP_PAGE_ADD_ON:Boolean = false;
		public static var SIGNUP_PAGE_ADD_ONS:Array = [];
		
		
		
		// Extra registration 
		// **Additional fields NEED TO MATCH THE NAMES OF THE USERDATA KEYS IN SETTINGS_LOCAL.PY
		// **type is the type of input. Valid values are 'text' or 'list'. Lists include all mxml objects
		//   with a selectedItem attribute.
		// **input is the id of the input object
		// **path is the path from within the module to the input
		
		// Demographics.mxml extra registration add ons
		public static var DEMOGRAPHICS_ADD_ON:Boolean = false;
		public static var DEMOGRAPHICS_EXTRA_REGISTRATION:Boolean = false;
		public static var EXTRA_REGISTRATION_FIELDS_LIST:Array = []; 
				
		// The value of 'handle' must be the index of REG_FIELDS in order to get a handle on the object
		public static var EXTRA_REGISTRATION_HANDLE:int = -1;
		public static var DEMOGRAPHICS_ADD_ONS:Array = [];
		
		/* Example from Unilever
		public static var EXTRA_REGISTRATION_FIELDS_LIST:Array = [{'field': 'pillar', 'input': '_pillar', 'type':'list', 'path':['extraRegMainVBox', 'extraRegPillarFormItem', 'extraRegPillarFormItemBox']},
																	{'field': 'function', 'input': '_function', 'type':'list', 'path':['extraRegMainVBox', 'extraRegFunctionFormItem', 'extraRegFunctionFormItemBox']}]; 
		
		public static var REG_FIELDS:ExtraRegistrationFields = new ExtraRegistrationFields();
		
		// The value of 'handle' must be the index of REG_FIELDS in order to get a handle on the object
		public static var EXTRA_REGISTRATION_HANDLE:int = 0;
		public static var DEMOGRAPHICS_ADD_ONS:Array = [{'child':REG_FIELDS, 'parent':['signupPageBody', 'registrationBox', 'form', 'formBox']}];
		*/		
		
		// LoginForm.mxml
		public static var LOGIN_FORM_USER_PROMPT:String = "Username";
		public static var SHOW_CASE_SENSITIVE_WARNING:Boolean = true;
		public static var SHOW_USERNAME_ASTERISK:Boolean = true;
		public static var SHOW_PASSWORD_ASTERISK:Boolean = true;
		public static var SHOW_SCREEN_SIZE_NOTICE:Boolean = false;
		public static var SCREEN_SIZE_NOTICE:String = 'Please ensure that your browser screen resolution is at least ' + Configuration.MIN_WIDTH + ' pixels by ' + Configuration.MIN_HEIGHT + ' pixels.';
		
		public static var LOGIN_INTRO:String = "<b>ALREADY HAVE AN ACCOUNT?</b><br/>Please enter your username and password below, or sign in through Facebook.";
		public static var LOGIN_INTRO_BOTTOM:String = "<b>DON'T HAVE AN ACCOUNT?</b><br/>Click on the First Time button on the splash page.";
		
		// LoggedOutPage.mxml
		public static var LOGGED_OUT_PAGE_TEXT_1:String = "Thank you for participating!"
		public static var LOGGED_OUT_PAGE_TEXT_1_SUB:String = ""
		public static var LOGGED_OUT_PAGE_TEXT_2:String = "Return at any time to check your progress!\nYou can see how other participants are rating your idea.";
		
		//Include system for replaceable text
		//Includes for files in the about page
		/* Adding dynamic data to the about page
		*  ABOUT_URLS is a list of urls whose data is "included" in the About page, at the top of each url must be the text <_fieldname> that tells the mxml file which text object to populate
		*  ABOUT_LIST_ENTRIES collection of objects, with the fields label = Human Readable label of the page, map = asset to use. For local mxml objects use syntax local:objectname, for urls use the key <_fieldname> that you put at the top of the corresponding file
		*/
		/*[Embed(source="/assets/text/intro.html", mimeType="application/octet-stream")] public static var INTRO_FILE:Class;
		[Embed(source="/assets/text/misc.html", mimeType="application/octet-stream")] public static var MISC_FILE:Class;
		[Embed(source="/assets/text/welcome.html", mimeType="application/octet-stream")] public static var WELCOME_FILE:Class; // effectively welcome -> textual how it works
		[Embed(source="/assets/text/privacy.html", mimeType="application/octet-stream")] public static var PRIVACY_FILE:Class;
		[Embed(source="/assets/text/quickstart.html", mimeType="application/octet-stream")] public static var QUICKSTART_FILE:Class;
		[Embed(source="/assets/text/faq.html", mimeType="application/octet-stream")] public static var FAQ_FILE:Class;
		[Embed(source="/assets/text/contact.html", mimeType="application/octet-stream")] public static var CONTACT_FILE:Class;*/
		//public static var ABOUT_URLS:Array = new Array(INTRO_FILE, WELCOME_FILE, PRIVACY_FILE, QUICKSTART_FILE,MISC_FILE, FAQ_FILE,CONTACT_FILE);
		/*public static var ABOUT_LIST_ENTRIES:ArrayCollection = new ArrayCollection([{label: "An Introduction from Unilever", map: "intro"},
																					{label: "How It Works", map: "welcome"},
																					{label: "Understanding the Visualization", map: "special:howitworks" },
																					  {label: "FAQ", map: "faq" },
																					 // {label: "Quick Start Guide", map: "quickstart" },
																					  
																					  {label: "Reporting on Jon Ingham's Blog", map: "misc" },
																					  //{label: "References", map: "local:referencesDiv"},
																					  //{label: "Project Team", map: "local:teamDiv"},
																					  {label: "Contact & Support", map: "contact" },
																					  {label: "Terms and Conditions", map: "privacy" },
																					  
																					  {label: "Go Back", map: "special:back"}
																					]);*/
		
		public static var ABOUT_INTRO_TITLE:String = "The Collective Discovery Engine";
		public static var ABOUT_INTRO_ENABLED:Boolean = true;
		public static var ABOUT_INTRO_CONTENT:String = "";
		[Bindable] public static var ABOUT_INTRO_URL:String = "";
		
		public static var ABOUT_HOW_TITLE:String = "How It Works";
		public static var ABOUT_HOW_ENABLED:Boolean = false;
		public static var ABOUT_HOW_CONTENT:String = "";
		[Bindable] public static var ABOUT_HOW_URL:String = "";
		
		public static var ABOUT_VIS_TITLE:String = "Understanding the Visualization";
		public static var ABOUT_VIS_ENABLED:Boolean = false;	
		
		public static var ABOUT_FAQ_TITLE:String = "FAQ";
		public static var ABOUT_FAQ_ENABLED:Boolean = false;
		public static var ABOUT_FAQ_CONTENT:String = "";
		[Bindable] public static var ABOUT_FAQ_URL:String = "";
		
		public static var ABOUT_SUPPORT_TITLE:String = "Contact & Support";
		public static var ABOUT_SUPPORT_ENABLED:Boolean = true;
		public static var ABOUT_SUPPORT_CONTENT:String = "";
		[Bindable] public static var ABOUT_SUPPORT_URL:String = "";
		
		public static var ABOUT_PRIVACY_TITLE:String = "Terms and Conditions";
		public static var ABOUT_PRIVACY_ENABLED:Boolean = false;
		public static var ABOUT_PRIVACY_CONTENT:String = "";
		[Bindable] public static var ABOUT_PRIVACY_URL:String = "";
		
		public static var ABOUT_MISC_TITLE:String = "Reporting on Jon Ingham's Blog";
		public static var ABOUT_MISC_ENABLED:Boolean = false;
		public static var ABOUT_MISC_CONTENT:String = "";
		[Bindable] public static var ABOUT_MISC_URL:String = "";
		
		public static var SCREEN_RESOLUTION_WINDOWS:String = "1. Open <b>Display</b> in <b>Control Panel</b>\n\n2. On the <b>Settings</b> tab, under <b>Screen Resolution</b>, drag the slider, and then click <b>Apply</b>";
		public static var SCREEN_RESOLUTION_MAC:String = "1. Open <b>Displays</b> in <b>System Preferences</b>\n\n2. On the <b>Display</b> tab, under <b>Resolutions</b>, choose a higher resolution value";																			
																					
		
		//NETWORK SETTINGS
		public static var HTTP_REQUEST_TIMEOUT:int = 100; //Upper Bound in secs for how long a HTTP Service call should take
		public static var HTTP_ERROR_USER_STRING:String = "Error communicating with server, some data has been omitted";
	
		//Statements vBox Stuff
		public static var STATEMENTS_PAGE_INSTRUCTIONS_VISIBLE:Boolean = false;
		public static var STATEMENTS_NOT_FINISHED_TEXT:String = "STEP 1";
		public static var STATEMENTS_NOT_FINISHED_BUTTON_TEXT:String = "Express Your Opinions";
		public static var COMMENT_NOT_FINISHED_BUTTON_TEXT:String = "Click Here to Enter Your Response";
		public static var DISCUSSION_STATEMENT_DISCLAIMER_TEXT:String = "Read the discussion question to the left and enter your response below.";
		
		//public static var thumbsDownImageBMP:BitmapAsset = new Constants.THUMBS_DOWN_IMAGE() as BitmapAsset;
	//	public static var thumbsUpImageBMP:BitmapAsset = new Constants.THUMBS_UP_IMAGE() as BitmapAsset;
		
		/*Example Usage
		public static var STATEMENT_PAGE_LABELS:Object = {1: {leftText: 'Very Strongly Disagree', rightText: Constants.AGREE_STRING, leftPic: Constants.THUMBS_DOWN_IMAGE, rightPic: Constants.THUMBS_UP_IMAGE},
															4: {leftText: Constants.DISAGREE_STRING, rightText: 'Very Strongly Agree', leftPic: Constants.THUMBS_DOWN_IMAGE, rightPic: Constants.THUMBS_UP_IMAGE}};*/
		public static var STATEMENT_PAGE_LABELS:Object = {};
		public static var STATEMENT_PAGE_DEFAULT:Object = {leftText: Constants.DISAGREE_STRING, rightText: Constants.AGREE_STRING, leftPic: Constants.THUMBS_DOWN_IMAGE, rightPic: Constants.THUMBS_UP_IMAGE};
																						
		
		public static var DEMOGRAPHICS_NOT_FINISHED_TEXT:String = "Fill out your profile";
		public static var ALLOW_PROFILE_MULTIPLE_EDIT:Boolean = true;
		
		public static var COMMENT_TEASER:String = "Sign in to rate this response!";
		
		public static var COMMENT_ENTRY_PROMPT:String = "";
		public static var SHOW_COMMENT_ENTRY_PROMT:Boolean = false;
		
		// First time trial
		// NOTE: This only prevents a user from viewing the OpinionMap if they are logged out
		// the "first time trial" is merely interacting with the opinion map in the logged out state
		public static var FIRST_TIME_TRIAL_AVAILABLE:Boolean = true; 
		
		//Entry Codes
		public static var USE_ENTRY_CODES:Boolean = false;
		public static var SOFT_ENTRY_CODES:Boolean = false;
		public static var ALLOW_USERNAME_CHANGE:Boolean = false;
		
		// Commented out, needs to be commented back in for Unilever, until we have a more flexible
		// way of doing this...
		//public static var ENTRY_CODE_LOGIN_TEXT:String = "<h2>welcome to the Hive!</h2>\n\n<b>Make sure to bookmark this page, as the only way to access your account is through your unique URL.</b> To log in, please enter the first part of your Unilever email address (eg. john.smith) below as your password.\n";
		public static var ENTRY_CODE_LOGIN_TEXT:String = "<h2>welcome to the Garden!</h2>\n\n<b>Make sure to bookmark this page, as the only way to access your account is through your unique URL.</b>\n\nTo log in, please enter your password below.\n";
		
		public static var ENTRY_CODE_HELLO_TEXT:String = "Hello $u,";
		public static var ENTRY_CODE_LOGIN_TEXT_FIRST:String = "";//"(The one in the email invite)";
		
		//public static var ENTRY_CODE_ABOVE_ENTER_TEXT:String = "I, %u, commit to complete the four challenges and to feedback my experiences to the group.";
		public static var ENTRY_CODE_ABOVE_ENTER_TEXT:String = "";
		
		public static var FIRST_TIME_ENTRY_TEXT:String = "Modify Account Details";
		public static var ALLOW_PASSWORD_CHANGE:Boolean = false;
		public static var USERNAME_UPDATE_INTRO_TEXT:String = "Would you like to modify your username?";
		public static var PASSWORD_UPDATE_INTRO_TEXT:String = "We highly recommend that you choose a password that is both secure and easy for you to remember.";
		public static var UPDATE_BUTTON_PROMPT:String = "Submit";
		public static var SKIP_UPDATE_BUTTON_PROMPT:String = "Skip";
		
		// Assets for username availability
		[Embed(source="/assets/img/check.png")] public static var CHECK:Class;
		[Embed(source="/assets/img/cross.png")] public static var CROSS:Class;
		
		// WelcomePage.mxml
		[Binbable] public static var NUM_WELCOME_POINTS:int = 10;
		public static var OPINIONS_EXPRESSED_POST_TEXT:String = "IDEAS EXPRESSED";
		public static var WELCOME_PAGE_ADD_ON:Boolean = false;
		public static var WELCOME_PAGE_ADD_ONS:Array = [];
		public static var USE_DEFAULT_WELCOME_PAGE_CONTENT:Boolean = true;
		public static var WELCOME_PAGE_DEFAULT_TEXT:String = "Welcome to the Collective Discovery Engine";
		public static function opinionsExpressedCalculation(numActiveUsers:int):int
		{
			return numActiveUsers;
		}
		public static var WELCOME_PAGE_TOGGLE_TEXT:Boolean = false;
		
		public static var WELCOME_PAGE_FACES_ENABLED:Boolean = true;
		public static var AUTO_FADE_POINTS_TO_TEXT:Boolean = false;
		public static var AUTO_FADE_DURATION:int = 10000;
		public static var WELCOME_PAGE_SHOW_HEADER:Boolean = false;
		public static var WELCOME_PAGE_VID_URL:String = ""; // Allow an intro video on the front screen
		public static var WELCOME_PAGE_VID_PROMPT:String = ""; // Prompt for intro video on the front screen
		
		
		// MapOverlay.mxml		  
		// Process of filling out statements, discussion question, and possible extra questions
		public static var SERIALIZED_OPINION_PROFILE:Boolean = false;
		public static var HAVE_ADDITIONAL_PROFILE_QUESTIONS:Boolean = false;
		public static var MAP_OVERLAY_ADDITIONAL_QUESTIONS:Array = [];
		public static var ADDITIONAL_QUESTIONS_STEP:String = "Step 3";
		public static var ADDITIONAL_QUESTIONS_PROMPT:String = "Please answer the following questions";
		
		public static function finishedWithProfile(hasFinishedStatements:Boolean, hasFinishedComment:Boolean, hasFinishedDemographics:Boolean, hasFinishedAdditional:Boolean):Boolean
		{
			return (hasFinishedStatements && hasFinishedComment);
		}
		
		public static var SERIALIZED_WELCOME_TITLE:String = "WELCOME TO THE GARDEN";
		public static var SERIALIZED_WELCOME_TOP_TEXT:String = "People's comments are arranged as \"blooms\" in the system. Neighbouring blooms represent participants with similar attitudes.";
		public static var SERIALIZED_WELCOME_TEXT:String = "To continue, please complete your opinion profile.";
		public static var SERIALIZED_WELCOME_CONTINUE_BUTTON:String = "Complete Opinion Profile";
		public static var SERIALIZED_FINISHED_TEXT:String = "You may now read, rate, and respond to your colleagues ideas. Click on any bloom to get started.";
		public static var SERIALIZED_STATEMENTS_TITLE:String = "<b>Step 1/3</b>: Please enter your opinion on the following statements";
		public static var SERIALIZED_COMMENT_TITLE:String = "<b>Step 2/3</b>: Please answer the following discussion question";
		public static var SERIALIZED_ADDITIONAL_TITLE:String = "<b>Step 3/3</b>: Please answer the following questions";
		
		// ContactSupport.mxml
		public static var CONTACT_SUPPORT_TEXT:String = "For questions regarding logins and passwords, contact:";
		
		public static var HIGHLIGHTED_POINT_CLICK_NOTICE:String = "Welcome to Opinion Space, a new approach to generating and exchanging insightful ideas about issues and policies. Click the glowing point to begin...";
		public static var SIGNUP_NOTIFICATION:String = "Let's get started!";
		public static var SIGNUP_SUB_NOTIFICATION:String = "It only takes a minute.";
		
		// CustomPreloader.as
		public static var USE_PRELOADER_IMAGE:Boolean	= false;
		
		public static var SHOW_BOOKMARK:Boolean = false;
		public static var BOOKMARK_TITLE:String = "Opinion Space";
		//public static var BOOKMARK_URL:String = "http://opinion.berkeley.edu/x/";
		public static var CREATE_BOOKMARK_LINK:String = "Click here to bookmark this page";
		public static var CREATE_BOOKMARK_LINK_ALT:String = "Press Crtl-D to bookmark this page";
		
		
		//[Embed(source="/assets/slider/thumbs_up_large.png")] public static var THUMBS_UP:Class
		//[Embed(source="/assets/slider/thumbs_down_large.png")] public static var THUMBS_DOWN:Class
		public static var SPACE_DIMENSIONS:int = 500;
		public static var NO_SLIDER_SCALE:int = 0;
		public static var DIRECTIVES_WIDTH:int = 600;
		public static var SLIDER_OFFSET_DOWN:int= 10;
		public static var SLIDER_PADDING:int = 30;
		public static var SLIDER_THICKNESS:int = 0;
		
		public static var SHOW_LOCATION:Boolean = false;
		public static var LOGGED_IN_SLIDERS_ENABLED:Boolean = true;
		
		public static var POLLING_ENABLED:Boolean = true;
		public static var POLLING_FREQUENCY:int = 300000;
		
		// Scoring system language
		public static var CLAIM_YOUR_SCORE_LANGUAGE:String = "Join the Discussion";
		public static var INCREASE_SCORE_PROMPT_LANGUAGE:String = String("Rate the " + int(EXPLORE_THRESHOLD_RATINGS).toString() + " blooms below using both of the sliders in the right panel.").toUpperCase(); 
		public static var INCREASE_SCORE_TOOLTIP_LANGUAGE:String = "Increase your score by clicking on this point and rating the response to the discussion question";
		public static var SCORE_PRECISION:int = 0;
		public static var YOUR_SCORE_TOOLTIP:String = "";//"Your score is calculated based on your activity in the space. You earn points by rating the responses of others and when others rate your response";
		public static var SCORE_SCALE_FACTOR:Number = 9;
		public static var UNIFIED_SCORE:Boolean = false;
		
		// Scoring system function
		public static function calculateClientSideScore(authorScore:Number, reviewerScore:Number, hasFinishedStatements:Boolean, hasFinishedComment:Boolean, numFullyRatedResponses:int):Number
		{
			if(UNIFIED_SCORE)
				return (numFullyRatedResponses + authorScore)*SCORE_SCALE_FACTOR;
			else
				return (numFullyRatedResponses)*SCORE_SCALE_FACTOR;
		}
		
		// First time scoring system function
		public static function calculateFirstTimeScore(insightRatings:Dictionary, agreementRatings:Dictionary, usernameSearchFirstTime:Boolean = false):Number
		{
			var score:Number = 0;
			for(var key:Object in insightRatings)
			{
				if(agreementRatings[key] != null)
					score = score + 1;
			}
			if(usernameSearchFirstTime)
				return score - 1;
			else
				return score*SCORE_SCALE_FACTOR;
		}
		
		// First time prompts
		public static var FIRST_TIME_RATING_NOTICE:String = String("Click on any bloom to get started...").toUpperCase();//"To join the garden, review " + int(EXPLORE_THRESHOLD_RATINGS).toString() + " ideas from others by clicking the flowers and using the sliders on the lower right of the screen.";//"This point represents a participant's response to the discussion question. To join the discussion, first read and rate this response...";
		public static var FIRST_TIME_ENTER_SPACE:String = String("Thanks for joining! Next, enter your response to the discussion question.").toUpperCase();
		public static var FIRST_TIME_ENTER_SPACE_NO_STATEMENTS:String = String("Thanks for joining! You can now seed your idea by clicking on the button in the right panel.").toUpperCase();
		public static var FINISH_SAVING_RESPONSE:String = String("Your idea has been saved. You'll be notified of its progress in the Stats and Notifications tabs to the right. Now, evaluate and contribute to the ideas of others to earn points and collaborate in the search for the most insightful ideas!").toUpperCase();
		
		public static var FIRST_TIME_COMMENT_INSTRUCTIONS:String = "Enter your response to the discussion question by typing your response in the box below the question.";
		
		public static var ALLOW_UNAUTH_EXPLORE:Boolean = true;
		
		// Stage 2: Place your bud/seed
		public static var PLACE_SEED_INTRO:String = String("Now, plant your own seed!").toUpperCase();
		public static var PLACE_SEED_INTRO_NO_STATEMENTS:String = String("Step 2: seed your own idea by answering the discussion question above!").toUpperCase();
		public static var PLACE_SEED_PROMPT:String = String("Find your location in the system by answering the statements to the right.").toUpperCase(); // used for > 2 statements
		public static var DRAG_SEED_PROMPT:String = "Drag and drop this seed according to your own opinions!"; // used for 2 statements
		public static var REGISTER_SEED_PROMPT_NO_STATEMENTS:String = String("Next, Register to create an account and seed your idea!").toUpperCase();
		public static var REGISTER_SEED_PROMPT:String = String("Step 3: Register to seed your own idea!").toUpperCase();
		
		public static var Q_VALUE_TEXT:String = "How helpful is this suggestion to your idea?";
		public static var Q_VALUE_TEXT_OTHERS:String = "Author's rating of this suggestion: ";
		public static var SUGGESTION_RATING_SLIDERS:Boolean = false;
		public static var SUGGESTIONS_ENABLED:Boolean = false;
		
		public static var SAVE_SUGGESTION_MESSAGE:String = "Your suggestion has been saved. Click on the history button to view your suggestion.";
		[Embed(source="assets/commentmodule/X-out.png")] public static var CLOSE_BUTTON:Class;
		[Embed(source="assets/commentmodule/X-out.png")] public static var CLOSE_BUTTON_DOWN:Class;
		public static var SAVE_COMMENT_MESSAGE:String = "Your comment has been saved. Click on the opinions button to view your comment.";
		
		
		//[Embed(source="/assets/img/profileNavigationLeft.png")] public static var NAVIGATE_LEFT:Class
		//[Embed(source="/assets/img/profileNavigationRight.png")] public static var NAVIGATE_RIGHT:Class
		
		
		// Stats Panel
		public static var AUTHOR_SCORE_THRESHOLDS:Array = [10,20,50,70];
		public static var AUTHOR_RATINGS_THRESHOLDS:Array = [2,6,8,10];
		public static var AUTHOR_SCORE_ON:Boolean = true;
		public static var SUGGESTER_SCORE_THRESHOLDS:Array = [10,20];
		public static var SUGGESTER_SCORE_ON:Boolean = false;
		public static var EXPLORE_SCORE_THRESHOLDS:Array = [10,20];
		public static var EXPLORE_SCORE_ON:Boolean = false;
		public static var VIEW_HISTOGRAMS_THRESHOLD:int = 5;
		public static var AUTHOR_LEVELS:Array = ["Seed", "Budding", "Blooming", "Mature", "Fully Mature"];
		public static var SUGGESTER_LEVELS:Array = ["Suggester 1", "Suggester 2", "Suggester 3"];
		public static var EXPLORER_LEVELS:Array = ["Explorer 1", "Explorer 2", "Explorer 3"];
		public static var IDEA_RATED_ALPHA:Number = 0;
		public static var STATS_RESPONSE_TERM:String = "Idea";
		public static var STATS_ENABLED:Boolean = true;
		
		/* First time prompts */
		public static var FLOATING_PROMPT_WIDTH:int = 270;
		public static var RATE_RESPONSE_PROMPT:String = "Rate this idea using both of the sliders to right";
		public static var SCORE_EXPLANATION_BOX:String = "You'll earn 100 'Reputation' points each time you rate an idea.  After posting your own idea, you also earn points whenever it's rated by others.";
		public static var LEAVE_SUGGESTION_PROMPT:String = "Leave a suggestion to improve this idea";
		public static var RATED_TRANSLUCENT_PROMPT:String = "After rating a bloom, it is removed from the display. To view blooms you've rated, click on the 'Rated Ideas' button on the upper right";
		
		// Flags for if there is a general splash page that allows access to multiple discussion questions
		// e.g. Unilever PEP
		public static var SPLASH_PAGE_RETURN:Boolean = false;
		public static var FORCE_LOGIN:Boolean = false;
		
		// Display Hybrid Wisdom Website
		//public static var WEBSITE:Boolean = true;
		
		// Rate three comments rather than rate statements
		public static var NO_STATEMENTS:Boolean = false;
		public static var NO_REVISIONS:Boolean = true;
		
		// Footer logo
		/*[Embed(source="/assets/img/hwl-logo-footer.png")] public static var LOGO_FOOTER_LEFT:Class;
		public static var FOOTER_LEFT_TEXT:String = "HYBRID WISDOM LABS";
		[Bindable] public static var FOOTER_LEFT_LINK:String = "http://hybridwisdom.com/main-site/?about=true";
		
		public static var FOOTER_RIGHT_TEXT:String = "WHAT IS COLLABORATIVE DISCOVERY?";
		public static var FOOTER_RIGHT_LOGO_SOURCE:String = "";
		[Bindable] public static var FOOTER_RIGHT_LINK:String = "http://hybridwisdom.com/main-site/?whatis=true";*/
		
		public static var CAN_FLAG_COMMENT:Boolean = true;
		[Bindable] public static var UNILEVER_WELCOME_PAGE:Boolean = false;
		
		//[Bindable]public static var SHOW_SPONSORS:Boolean = false;
		[Bindable]public static var SPONSOR_TEXT:String = "";
		[Bindable]public static var SPONSOR_LOGO1:String = null;
		[Bindable]public static var SPONSOR_LOGO1_LINK:String = "";
		[Bindable]public static var SPONSOR_LOGO2:String = null;
		[Bindable]public static var SPONSOR_LOGO3:String = null;
		[Bindable]public static var SPONSOR_LOGO4:String = null;
		[Bindable]public static var SPONSOR_LOGO5:String = null;
		
		[Bindable] [Embed(source="/assets/images/gil-background.jpg")] public static var MAP_BACKGROUND:Class;
		[Bindable]public static var RANK_ON:Boolean = false;
		public static var VIEW_RANK_THRESHOLD:int = 5;
		
		public static var MIN_COMMENT_WORD_COUNT:int = 10;
		public static var STATEMENTS_ERROR_MESSAGE:String = "You must indicate your opinion on the statements to the right in order to continue.";
		public static var COMMENT_ERROR_MESSAGE:String = "Your response must be at least 10 words long.";
		public static var COMMENT_NOT_FINISHED_TEXT_INTRO:String = "ANSWER THE FOLLOWING DISCUSSION QUESTION:";
		public static var WELCOME_PAGE_TITLE_BOX_WIDTH:int = 650;
		public static var WELCOME_PAGE_TITLE_FONT_SIZE:int = 38;
		
		public static var ANNOUNCEMENT_BOX_TOP_PADDING:int = 150;
		public static var ANNOUNCEMENT_BOX_WIDTH:int = 240;
		public static var ANNOUNCEMENT_BOX_FONTSIZE:int = 19;
		public static var ANNOUNCEMENT_BOX_FONTWEIGHT:String = "bold";
		
		public static var VERTICAL_ORIENTATION:Boolean = false;
		
		public static var RATING_MODULE_VISIBLE:Boolean = true;
		public static var SHOW_LEGEND:Boolean = false;
		
		public static var RATING_TOOLTIP_POSTTEXT:String = "%";
		
		public static var ONA_ON:Boolean = false;
		
		public static var AFFINE_TRANSFORM_SCALEX:Number = 1;//2;
		public static var AFFINE_TRANSFORM_SCALEY:Number = 1;//2;
		public static var AFFINE_TRANSFORM_SHIFTX:Number = 0;//.5;
		public static var AFFINE_TRANSFORM_SHIFTY:Number = 0;//-1;
		// Legend logo
		//[Embed(source="/assets/images/legend.jpg")] public static var LEGEND:Class;
		public static var PROJECTOR_MODE:Boolean = false;
		public static var ROLLING_LEADERBOARD:Boolean = true;
	}
}
