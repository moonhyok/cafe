package com.opinion.utils
{
	import mx.rpc.http.HTTPService;
	import mx.rpc.AsyncToken;
	import mx.rpc.events.FaultEvent;
	import com.opinion.settings.Configuration;
	import mx.controls.Alert;
	import mx.rpc.events.ResultEvent;
	import mx.core.Application
	import flash.utils.*;
	public class ExtendedHTTPService extends HTTPService
	{
		public var lastCallParameters:Object = null;
		public var _failure_function = null;
		public var _retry_function = null;
		public var backOffTimer:int = 4;
		public var maxBackOff:Boolean = false;
		public var stateless:Boolean = false;
		
		public override function send(parameters:Object = null):AsyncToken
		{
			//logs
			addEventListener("fault",handleFault);
			addEventListener("result",handleResult);
			lastCallParameters = parameters;
			
			//setting default settings
			this.requestTimeout = Configuration.HTTP_REQUEST_TIMEOUT;
			
			return super.send(parameters);
		}
		
		private function updateBackOff(fail:Boolean = true):void{
			
			var nominal:int = backOffTimer;
			if(fail)
				nominal = nominal * 2;
			else
				nominal = nominal / 2;
			
			backOffTimer = Math.min(64,Math.max(nominal,1));
		}
		
		
		//Generic fault handling function (same function is executed for every objects fault)
		private function handleFault(fault:FaultEvent):void
		{
			//Alert.show(Configuration.HTTP_ERROR_USER_STRING);
			if(_failure_function != null)
				_failure_function();
			
			if(backOffTimer > 32 && maxBackOff)
				return;
			
			if(_retry_function != null)
				setTimeout(_retry_function,backOffTimer*1000);
			else if (stateless)
				setTimeout(send,backOffTimer*1000,lastCallParameters);
			
			updateBackOff();
			logFaultEvent(fault);
		}
		
		public function backOffReset():void
		{
			backOffTimer = 4;
		}
		
		//Same as above this function is called on every requests result (regardless of MXML configuration)
		private function handleResult(event:ResultEvent):void
		{
			logResultEvent(event)
		}
		
		//TODO change to new logging system when ready
		private function logFaultEvent(event:FaultEvent):void{
			var os_id:int = Application.application.opinionSpaceId;
			Application.application.log.logError(os_id, event.target.url.toString(), event.fault.faultString);
		}
		
		//TODO change to new logging system when ready
		private function logResultEvent(event:ResultEvent):void{
		}
		
		//TODO change to new logging system when ready
		private function logString(string:String):void
		{
			//TODO
		}
		
		public static function faultEventRequestMethod(event:FaultEvent):String
		{
			if(event == null)
				return "";
			else if (event.target == null)
				return "";
			else if(event.target.method == null)
				return "";
			
			return event.target.method.toString();
		}
		
		public static function faultEventRequestURL(event:FaultEvent):String
		{
			if(event == null)
				return "";
			else if (event.target == null)
				return "";
			else if(event.target.url == null)
				return "";
			
			return event.target.url.toString();
		}
		
		public static function faultEventErrorString(event:FaultEvent):String
		{
			return event.fault.faultString;
		}
		
		public static function faultEventErrorAtttr(event:FaultEvent, attr:String):String
		{
			return event.fault[attr];
		}
		
		public static function faultEventTargetAttrr(event:FaultEvent,attr:String):String
		{
			return event.target[attr];
		}
	}
}