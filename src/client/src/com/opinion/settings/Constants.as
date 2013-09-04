package com.opinion.settings {
	
	/**
	 * This class contains global constants (constants only relevant to particular files
	 * are simply declared there)
	 */
	
	public class Constants {

		// General Constants
		public static const MAX_RATING:Number = 1.0;
		public static const MIN_RATING:Number = 0.0;
		public static const DEFAULT_SLIDER_VALUE:Number = (MAX_RATING - MIN_RATING) / 2;
				
		public static const AGREE_STRING:String = "Strongly Agree";
		public static const DISAGREE_STRING:String = "Strongly Disagree";
		
		public static const DEFAULT_COMMENT_INPUT_TEXT:String = "";
		
		public static const DISCUSSION_STATEMENT_INTRO:String = "Please answer the following question:";
		
		public static const DEFAULT_LANDMARK_GUESS_TEXT:String = "This person's position on the map is an extrapolation based on publicly available information.";
		
		[Embed(source="assets/slider/thumbs_down.png")] public static const THUMBS_DOWN_IMAGE:Class;
		[Embed(source="assets/slider/thumbs_up.png")] public static const THUMBS_UP_IMAGE:Class;

        public static const SAVE_RATINGS_STATUS_LOADING:String = "Saving...";
        public static const SAVE_RATINGS_STATUS_DONE:String = "Saved.";
        public static const SAVE_RATINGS_STATUS_DEFAULT:String = "";
        public static const SAVE_RATINGS_STATUS_ERROR:String = "Save failed!";
        
        public static const SAVE_COMMENT_BUTTON_LABEL:String = "Save Response";
        public static const SAVE_COMMENT_BUTTON_LOADING_LABEL:String = "Saving...";
        public static const SAVE_COMMENT_STATUS_DONE:String = "Saved.";
        public static const SAVE_COMMENT_STATUS_DEFAULT:String = "";
        public static const EDIT_COMMENT_BUTTON_LABEL:String = "Change Response";
        
        public static const SAVE_COMMENT_RATING_STATUS_LOADING:String = "Saving...";
        public static const SAVE_COMMENT_RATING_STATUS_DONE:String = "Saved.";
        public static const SAVE_COMMENT_RATING_STATUS_DEFAULT:String = "";
        public static const SAVE_COMMENT_RATING_STATUS_ERROR:String = "Save failed!";

	    public static const SAVE_BUTTON_LABEL:String = "Save";
        public static const SAVE_BUTTON_LOADING_LABEL:String = "Saving...";
        public static const SAVE_STATUS_DONE:String = "Saved.";
        public static const SAVE_STATUS_DEFAULT:String = "Saved.";
        public static const EDIT_BUTTON_LABEL:String = "Change";
        
		public static const CLEAR_SAVE_STATUS_TIMEOUT:int = 2000;
		
		public static const POPUP_WINDOW_WIDTH:int = 675;
		public static const POPUP_FORM_WIDTH:int = 425;
		public static const DEFAULT_FIELD_WIDTH:int = 170;
		public static const EMAIL_FIELD_WIDTH:int = 300;
		public static const ZIP_FIELD_WIDTH:int = 80;

		// Arc constants
		public static const ARC_LEFT_OFFSET:Number = 135;
		public static const ARC_RIGHT_OFFSET:Number = 95;
		public static const ARC_CURVE_OFFSET:Number = 190;
		public static const ARC_MASK_OFFSET:Number = 35;
		

		// Lists
		public static const LIST_OF_STATES_AND_TERRITORIES:Array = 
		["Alabama",
		"Alaska",
		"American Samoa",
		"Arizona",
		"Arkansas",
		"California",
		"Colorado",
		"Connecticut",
		"Delaware",
		"District of Columbia",
		"Florida",
		"Georgia",
		"Guam",
		"Hawaii",
		"Idaho",
		"Illinois",
		"Indiana",
		"Iowa",
		"Kansas",
		"Kentucky",
		"Louisiana",
		"Maine",
		"Maryland",
		"Massachusetts",
		"Michigan",
		"Minnesota",
		"Mississippi",
		"Missouri",
		"Montana",
		"Nebraska",
		"Nevada",
		"New Hampshire",
		"New Jersey",
		"New Mexico",
		"New York",
		"North Carolina",
		"North Dakota",
		"Northern Marianas Islands",
		"Ohio",
		"Oklahoma",
		"Oregon",
		"Pennsylvania",
		"Puerto Rico",
		"Rhode Island",
		"South Carolina",
		"South Dakota",
		"Tennessee",
		"Texas",
		"Utah",
		"Vermont",
		"Virginia",
		"Virgin Islands",
		"Washington",
		"West Virginia",
		"Wisconsin",
		"Wyoming"];
		
		public static const COUNTRIES:Array = 
		["Other",
		"Afghanistan",
		"Albania",
		"Algeria",
		"Andorra",
		"Angola",
		"Antigua and Barbuda",
		"Argentina",
		"Armenia",
		"Australia",
		"Austria",
		"Azerbaijan",
		"Bahamas",
		"Bahrain",
		"Bangladesh",
		"Barbados",
		"Belarus",
		"Belgium",
		"Belize",
		"Benin",
		"Bhutan",
		"Bolivia",
		"Bosnia and Herzegovina",
		"Botswana",
		"Brazil",
		"Brunei",
		"Bulgaria",
		"Burkina Faso",
		"Burundi",
		"Cambodia",
		"Cameroon",
		"Canada",
		"Cape Verde",
		"Central African Republic",
		"Chad",
		"Chile",
		"China",
		"Colombia",
		"Comoros",
		"Congo",
		"Congo, Democratic Republic of the",
		"Costa Rica",
		"Côte d'Ivoire",
		"Croatia",
		"Cuba",
		"Cyprus",
		"Czech Republic",
		"Denmark",
		"Djibouti",
		"Dominica",
		"Dominican Republic",
		"East Timor",
		"Ecuador",
		"Egypt",
		"El Salvador",
		"Equatorial Guinea",
		"Eritrea",
		"Estonia",
		"Ethiopia",
		"Fiji",
		"Finland",
		"France",
		"Gabon",
		"Gaza",
		"Gambia, The",
		"Georgia",
		"Germany",
		"Ghana",
		"Greece",
		"Grenada",
		"Guatemala",
		"Guinea",
		"Guinea-Bissau",
		"Guyana",
		"Haiti",
		"Honduras",
		"Hungary",
		"Iceland",
		"India",
		"Indonesia",
		"Iran",
		"Iraq",
		"Ireland",
		"Israel",
		"Italy",
		"Jamaica",
		"Japan",
		"Jerusalem", 
		"Jordan",
		"Kazakhstan",
		"Kenya",
		"Kiribati",
		"Korea, North",
		"Korea, South",
		"Kuwait",
		"Kyrgyzstan",
		"Laos",
		"Latvia",
		"Lebanon",
		"Lesotho",
		"Liberia",
		"Libya",
		"Liechtenstein",
		"Lithuania",
		"Luxembourg",
		"Madagascar",
		"Malawi",
		"Malaysia",
		"Maldives",
		"Mali",
		"Malta",
		"Marshall Islands",
		"Mauritania",
		"Mauritius",
		"Mexico",
		"Micronesia, Federated States of",
		"Moldova",
		"Monaco",
		"Mongolia",
		"Montenegro",
		"Morocco",
		"Mozambique",
		"Myanmar",
		"Namibia",
		"Nauru",
		"Nepal",
		"Netherlands",
		"New Zealand",
		"Nicaragua",
		"Niger",
		"Nigeria",
		"Norway",
		"Oman",
		"Pakistan",
		"Palau",
		"Panama",
		"Papua New Guinea",
		"Paraguay",
		"Peru",
		"Philippines",
		"Poland",
		"Portugal",
		"Qatar",
		"Republic of Macedonia",
		"Romania",
		"Russia",
		"Rwanda",
		"Saint Kitts and Nevis",
		"Saint Lucia",
		"Saint Vincent and The Grenadines",
		"Samoa",
		"San Marino",
		"Sao Tome and Principe",
		"Saudi Arabia",
		"Senegal",
		"Serbia",
		"Seychelles",
		"Sierra Leone",
		"Singapore",
		"Slovakia",
		"Slovenia",
		"Solomon Islands",
		"Somalia",
		"South Africa",
		"Spain",
		"Sri Lanka",
		"Sudan",
		"Suriname",
		"Swaziland",
		"Sweden",
		"Switzerland",
		"Syria",
		"Taiwan",
		"Tajikistan",
		"Tanzania",
		"Thailand",
		"Togo",
		"Tonga",
		"Trinidad and Tobago",
		"Tunisia",
		"Turkey",
		"Turkmenistan",
		"Tuvalu",
		"Uganda",
		"Ukraine",
		"United Arab Emirates",
		"United States of America",
		"United Kingdom",
		"Uruguay",
		"Uzbekistan",
		"Vanuatu",
		"Vatican City",
		"Venezuela",
		"Vietnam",
		"West Bank", 
		"Western Sahara",
		"Yemen",
		"Zambia",
		"Zimbabwe"];	
		
		public static const LIST_OF_AGE_GROUPS:Array = ["01-18","18-25","26-33","33-50","50+"];
	}
}