package com.opinion.utils {
	
	import mx.controls.Alert;
	import mx.rpc.events.FaultEvent;
	
	public class Log {
		
		// user events
		// commented out events are logged on server-side, included for reference
		//public static const USER_LOGIN:int = 0;
		//public static const USER_LOGOUT:int = 1;
		public static const USER_LEAVE:int = 4;
		public static const USER_BUTTONCLICK:int = 5;
		public static const USER_PLOTCLICK:int = 6;
		public static const USER_CLICKUSERDOT:int = 7;
		
		// url strings
		private static const URL_HTTPERROR:String = "log/httperror/";
		private static const URL_USEREVENT:String = "log/userevent/";
		private static const URL_COMMENTVIEW:String = "log/commentview/";
		private static const URL_FIRSTTIME:String = "log/firsttime/";
		
		private var httpUtils:HTTPUtils;
		//private var httpObj:ExtendedHTTPService;
		private var httpObj:ExtendedHTTPService;
		
		public function Log(urlRoot:String) {
			
			this.httpUtils = new HTTPUtils(urlRoot);
			this.httpObj = new ExtendedHTTPService();	
			httpObj.addEventListener("fault", handleFault);			
			httpObj.useProxy = false;
			httpObj.method = "POST";
			
		}
		
		public function logError(os_id:int, url:String, message:String, error_type:int = 0):void{
			var info:Object = new Object();
			info['os_id'] = os_id.toString();
			info['url'] = url;
			info['error_type'] = error_type.toString();
			info['message'] = message;
			
			this.httpObj.url = this.httpUtils.getServiceUrl(URL_HTTPERROR);
			httpObj.send(info);
		}
		
		public function logUserEvent(os_id:int, log_type:int, details:String = ""):void{
			var info:Object = new Object();
			info['os_id'] = os_id.toString();
			info['log_type'] = log_type.toString();
			info['details'] = details;
			
			this.httpObj.url = this.httpUtils.getServiceUrl(URL_USEREVENT);
			httpObj.send(info);
		}
		
		public function logCommentView(comment_id:int):void{
			var info:Object = new Object();
			info['comment_id'] = comment_id.toString();
			
			this.httpObj.url = this.httpUtils.getServiceUrl(URL_COMMENTVIEW);
			httpObj.send(info);
		}
		
		public function logFirstTime(comment_id:int,rating:Number,type:String):void{
			var info:Object = new Object();
			info['id'] = comment_id.toString();
			info['value'] = rating;
			info['type'] = type;
			
			this.httpObj.url = this.httpUtils.getServiceUrl(URL_FIRSTTIME);
			httpObj.send(info);
		}
		
		public function handleFault(event:FaultEvent):void{
		}
	}
}