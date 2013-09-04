package com.opinion.utils
{
	import com.opinion.utils.HTTPUtils;
	import flash.net.URLRequest;
	import flash.net.navigateToURL;
	import flash.external.ExternalInterface;
	import com.opinion.settings.Configuration;
	
	public class FacebookAuthentication
	{
		public var APP_ID:String = Configuration.FACEBOOK_APP_ID;
		
		//SOME FYI so it doesn't get lost
		/*public var API_KEY:String = "2f9c747297cf06ca9a0ab686c74f3e2f";
		public var SECRET_KEY:String = "737d22e2e0e99a2a88128dd053f027c4";*/
		
		public var URL:String ="https://www.facebook.com/dialog/oauth";
		public var REDIRECT_URI:String = ""; //"http://localhost:8000/";//
		public var PERMS:String ="user_religion_politics,user_activities,user_birthday,user_education_history,user_hometown,user_interests,user_likes,user_location";		
		
		public function FacebookAuthentication(httpUtils:HTTPUtils, registration:Boolean = false)
		{ 
			REDIRECT_URI = httpUtils.getServiceUrl("accountsjson/facebook/");
			 
			 if(REDIRECT_URI.indexOf("localhost") > -1)
				 REDIRECT_URI ="http://opinion.berkeley.edu/learning/accountsjson/facebook/";
			 
			 if(registration)
				 REDIRECT_URI = REDIRECT_URI + "register/";
			 
			 URL += "?client_id=" + APP_ID + "&redirect_uri=" + REDIRECT_URI + "&scope="+PERMS + "&display=popup";
		}
		
		public function login():void
		{
			if (ExternalInterface.available) { 
				ExternalInterface.call("window.open", URL, "win", "height=300,width=500,toolbar=no,scrollbars=no"); 
			} 
			else
			{
				navigateToURL(new URLRequest(URL), "_blank");
			}
		}
	}
}