/*
* The contents of this file are subject to the Mozilla Public License Version
* 1.1 (the "License"); you may not use this file except in compliance with
* the License. You may obtain a copy of the License at
* http://www.mozilla.org/MPL/
*
* Software distributed under the License is distributed on an "AS IS" basis,
* WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
* for the specific language governing rights and limitations under the
* License.
*
* The Original Code is the Flex OpenID Login Component.
*
* The Initial Developer of the Original Code is
* Anirudh Sasikumar (http://anirudhs.chaosnet.org/).
* Portions created by the Initial Developer are Copyright (C) 2008
* the Initial Developer. All Rights Reserved.
*
* Contributor(s):
*
*/
package com.opinion.components.registration
{
	import flash.events.Event;
	
	public class OpenIDLoginEvent extends Event
	{
		public var url:String;
		public static const EVENT_OPENID_WINDOW_LOGIN:String = "openidLogin";
		public static const EVENT_OPENID_WINDOW_CLOSE:String = "openidClose";
		
		public function OpenIDLoginEvent(type:String, bubbles:Boolean=false, cancelable:Boolean=false, openidurl:String="")
		{
			super(type, bubbles, cancelable);
			url = openidurl;
		}
		
		override public function clone():Event
		{
			return new OpenIDLoginEvent(type, bubbles, cancelable, url);
		}
		
	}
}