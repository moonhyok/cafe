package com.opinion.utils {
	import flash.utils.Dictionary;
	import com.opinion.settings.Constants;
	
	/**
	 * This class contains functions for converting between different data structures
	 */
	public class ConversionUtils {
		/**
		 * Builds a userRating array from an array of sliders
		 */
		public static function sliderToUserRating(sliders:Array):Array {
			var userRating:Array = [];
			
			for (var i:int = 0; i < sliders.length; i++) {
				if (userRating.length != 0) {
					userRating[i] = sliders[i].value;
				}
				else {
			        userRating.push(sliders[i].value);
				}
			}
			
			return userRating;
		}
		
		public static function sliderToNameToRatingMap(sliders:Array):Object {
			var nameToRateMap:Object = {};
			
			for (var i:int = 0; i < sliders.length; i++) {
				nameToRateMap[sliders[i].name] = sliders[i].value;
			}
			
			return nameToRateMap;
		}
		
		/**
		 * Assumes dict is indexed like an array, indexed by Strings
		 */
		public static function dictToArray(dict:Dictionary):Array {
			var arr:Array = [];
			for (var key:String in dict) {
				arr[int(key)] = dict[key];
			}
			return arr;
		}
		
		public static function slidersAreDefault(sliders:Array):Boolean {
			for (var i:int = 0; i < sliders.length; i++) {
				if (sliders[i].value != Constants.DEFAULT_SLIDER_VALUE) {
					return false;
				}
			}
						
			return true;
		}
	}
}