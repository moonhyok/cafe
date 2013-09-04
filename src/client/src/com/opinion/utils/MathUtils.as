package com.opinion.utils {
	import com.opinion.settings.Constants;
	import mx.controls.Alert;
	
	import flash.utils.Dictionary;
	
	/**
	 * This class contains functions for mathematical calculation, including eigenvector manipulation.
	 */
	 
	public class MathUtils {
		/**
		 * This assumes both arrays are the same length
		 */
		public static function dotProduct(a1:Array, a2:Array):Number {
			var sum:Number = 0;
			for (var i:int = 0; i < Math.min(a1.length,a2.length); i++) {
				sum += a1[i] * a2[i];
			}		
			return sum;
		}
		
		/**
		 * Computes the dot product between a dictionary and an array
		 * The dictionary will be indexed by the id's passed by the third argument.
		 * This assumes the index array is in sorted order
		 */ 
		public static function dictArrayDotProduct(d:Dictionary, a:Array, indx:Array):Number {
			var temp:Array = [];
			for (var k:int = 0; k < indx.length; k++) {
				temp.push(d[indx[k].toString()] * a[k]);
			}
			
			var sum:Number = 0;
			for (var j:int = 0; j < temp.length; j++) {
				sum += temp[j];
			}
			
			return sum;
		}
		
		/**
		 * Turns the userRatingsDecoded array into a 1D, compressed userRatings array
		 */
		public static function compressUserRatingsDecoded(userRatingsDecoded:Array):Array {
			var userRatings:Array = [];
			for (var i:int = 0; i < userRatingsDecoded.length; i++) {
				userRatings[i] = userRatingsDecoded[i][1];
			}
			
			return userRatings;
		}
		
		/**
		 * Turns the eigenvectorsDecoded decoded array into a 2D, compressed eigenvectors array,
		 * where the row represents the eigenvector number and the column represents the coordinate number
		 * (i.e. x-coord, y-coord)
		 */
		public static function compressEigenvectorsDecoded(eigenvectorsDecoded:Array):Array {
			// This one array contains a row for each eigenvector
		    var eigenvectors:Array = new Array();
		    
		    for (var i:int = 0; i < eigenvectorsDecoded.length; i++) {
		   		var eigenvector_number:int = eigenvectorsDecoded[i][0];
		    	var coordinate_number:int = eigenvectorsDecoded[i][1];
		    	var value:Number = eigenvectorsDecoded[i][2];
		    	
		    	// If there is no eigenvector array for this eigenvector_number, create one
		    	if (eigenvectors[eigenvector_number] == undefined) {
		    		eigenvectors[eigenvector_number] = new Array();
		    	}
		    	eigenvectors[eigenvector_number][coordinate_number] = value;
		    }
		    
		    return eigenvectors;
		}
		
		/**
		 * Creates dummy eigenvectors (for an OS that hasn't had PCA run on it yet)
		 */
		public static function createDummyEigenvectors(numStatements:int):Array {
			var eigenvectors:Array = new Array();
			
	        eigenvectors[0] = new Array(numStatements);
	        eigenvectors[1] = new Array(numStatements);
	        
	        for (var i:int = 0; i < numStatements; i++) {
	            eigenvectors[0][i] = i / 10.0;
	            eigenvectors[1][i] = (i / 10.0) - 0.2;
	        }
	        
	        return eigenvectors;
		}
		
		/**
		 * Returns an array of user rating arrays, one per eigenvector, that either maximize
		 * or minimize the dot product with each eigenvector
		 */
		private static function getExtremeUserRatings(eigenvectors:Array, max:Boolean):Array {
			var extremeUserRatings:Array = [];
			
			for (var i:int = 0; i < eigenvectors.length; i++) {
			    var extremeUserRating:Array = new Array(eigenvectors[i].length);
			    	
			    for (var j:int = 0; j < eigenvectors[i].length; j++) {
			    	var value:Number = eigenvectors[i][j];
			    	
			    	// If the eigenvector value is positive, then a high value will maximize
			    	// the dot product and a low value will minimize it
			    	if (value > 0) {
			    		if (max) {
			    			extremeUserRating[j] = Constants.MAX_RATING;
			    		}
			    		else {
			    			extremeUserRating[j] = Constants.MIN_RATING;
			    		}
			    	}
			    	// If the eigenvector value is negative, then a low value will maximize
			    	// the dot product and a high value will minimize it
			    	else {
			    		if (max) {
			    			extremeUserRating[j] = Constants.MIN_RATING;
			    		}
			    		else {
			    			extremeUserRating[j] = Constants.MAX_RATING;
			    		}
			    	}
			    }
			    
			    extremeUserRatings[i] = extremeUserRating;
			}
			
			return extremeUserRatings;
		}
		
		/**
		 * Returns the minimum value of each axis, based on the dot product with user ratings
		 * vectors that minimize the dot product with each eigenvector
		 */
		public static function getAxisMin(eigenvectors:Array):Array {
			var axisMin:Array = [];
			
			var minUserRatings:Array = getExtremeUserRatings(eigenvectors, false);
			for (var i:int = 0; i < eigenvectors.length; i++) {
				axisMin[i] = MathUtils.dotProduct(minUserRatings[i], eigenvectors[i]);
			}
			
			return axisMin;
		}
		
		/**
		 * Returns the maximum value of each axis, based on the dot product with user ratings
		 * vectors that maximum the dot product with each eigenvector
		 */
		public static function getAxisMax(eigenvectors:Array):Array {
			var axisMax:Array = [];
			
			var maxUserRatings:Array = getExtremeUserRatings(eigenvectors, true);
			for (var i:int = 0; i < eigenvectors.length; i++) {
				axisMax[i] = MathUtils.dotProduct(maxUserRatings[i], eigenvectors[i]);
			}
			
			return axisMax;
		}
		
		public static function twoSliderXorY(eigenvectors:Array, index:int):String
		{
			if(eigenvectors[index].toString() == '0,1')
				return 'y';
			else
				return 'x';
		}
		
	}
}