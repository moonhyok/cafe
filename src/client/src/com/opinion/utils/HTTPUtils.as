package com.opinion.utils {
	import flash.net.URLRequest;
	import flash.net.navigateToURL;
	import mx.rpc.http.HTTPService;
	
	import mx.modules.Module;
	
	public class HTTPUtils {
		private var urlRoot:String;		
		
		public function HTTPUtils(urlRoot:String) {
			this.urlRoot = urlRoot;
		}
		
		public function getServiceUrl(urlSuffix:String):String {
			return this.urlRoot + urlSuffix;
		}
		
		public function getMediaUrl(urlSuffix:String):String {
			return this.urlRoot + "media/" + urlSuffix;
		}
		
		public function openLinkNewWindow(url:String):void {
			var u:URLRequest = new URLRequest(url);
			navigateToURL(u, "_blank");
		}
		
		public function openLinkSameWindow(url:String):void {
			var u:URLRequest = new URLRequest(url);
			navigateToURL(u, "_self");
		}
		
		public function getSWFDirectory(mod:Module):String {
			var url:String = mod.parentApplication.url;
			var path:String = "";
			
			// If the last character of the URL is a slash, remove it
			if (url.charAt(url.length - 1) == "/") {
				url = url.substring(0, url.length - 1);
			}
			
			var slashIndex:int = url.lastIndexOf("/");
			path = url.substring(0, slashIndex);

			return path;
		}
		
		public function createURLFromSWFDir(mod:Module, urlSuffix:String):String {
			var swfDir:String = getSWFDirectory(mod);
			
			return (swfDir + "/" + urlSuffix);
		}
	}
}