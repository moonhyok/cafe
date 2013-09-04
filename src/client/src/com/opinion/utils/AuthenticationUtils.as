package com.opinion.utils {
	import flash.utils.Dictionary;
	
	import mx.controls.Text;
	
	/**
	 * Functions for sending login/registration information
	 */
	public class AuthenticationUtils {
		/**
		 * Returns whether or not the result of an HTTPService call is a success (not an error)
		 */
		public static function resultIsSuccess(decodedResult:Object):Boolean {
			return decodedResult["success"];
		}
		
		/**
		 * Returns whether or not the result of an HTTPService call is an error because login was required
		 */
		public static function resultIsAuthRequired(decodedResult:Object):Boolean {
			var result:Boolean = false;
			if (decodedResult["auth_required"] != null)
				result = decodedResult["auth_required"];
			return result;
		}
		
		/**
		 * Error handling function that does not change any fields.
		 */
		public static function handleErrorsNoFields(decodedResult:Object, mod:Object):Boolean {
			return handleErrors(decodedResult, mod, null, null);
		}
		
		/**
		 * Error handling function that changes one error field, but does not deal with forms.
		 */
		public static function handleErrorsGlobalField(decodedResult:Object, mod:Object, globalErrorField:Text):Boolean {
			return handleErrors(decodedResult, mod, globalErrorField, null);
		}
		
		/**
		 * Basic error handling function that only changes form fields.
		 */
		public static function handleErrorsFormFields(decodedResult:Object, mod:Object, errorFormFields:Array):Boolean {
			return handleErrors(decodedResult, mod, null, errorFormFields);
		}
		
		/**
		 * General error handling function for form errors and other errors.
		 */
		public static function handleErrors(decodedResult:Object, mod:Object, globalErrorField:Text, errorFormFields:Array):Boolean {
			var errorFormFieldsMap:Dictionary = null;

			// Clear all error fields
			if (globalErrorField != null) {
				globalErrorField.text = "";
			}
			if (errorFormFields != null) {
				for each (var errorFormField:Text in errorFormFields) {
					errorFormField.text = "";
				}
			}
			
			// Create a map from errorFormField.id to errorFormField
			if (errorFormFields != null) {
				errorFormFieldsMap = new Dictionary();
				for each (errorFormField in errorFormFields) {
					errorFormFieldsMap[errorFormField.id] = errorFormField;
				}				
			}
			
			// If there is a login_required error, ensure that the application is logged out
			if (decodedResult["login_required"]) {
				if (mod.parentApplication.isUserAuthenticated) { // If the application is logged in, logout
					mod.parentApplication.logout();
				}
			}
			
			// If there is a global error, display it
			if (decodedResult["error"]) {
				if (globalErrorField != null) {
					globalErrorField.text = decodedResult["error"];
					globalErrorField.visible = true;
				}
			}
			
			// if there is an error specific to forms, display it
			if (decodedResult["form_errors"]) {
				if (errorFormFieldsMap != null) {
					var formErrors:Object = decodedResult["form_errors"];
					
					for (var key:String in formErrors) {
						var errorMessage:String = formErrors[key];
						var errorFormFieldId:String = "_error_" + key;
						if (!(errorFormFieldsMap[errorFormFieldId] === undefined)) {
							if(errorMessage == "Enter a valid value." && key == 'username')
								errorMessage = "Usernames must only contain letters and numbers";
							errorFormFieldsMap[errorFormFieldId].text = errorMessage;
							errorFormFieldsMap[errorFormFieldId].visible = true;
							
							if(!errorFormFieldsMap[errorFormFieldId].includeInLayout)
							{
								errorFormFieldsMap[errorFormFieldId].includeInLayout = true;
							}
						}
					}
				}
			}
			
			return resultIsSuccess(decodedResult);
		}
		
		public static function generateRandomString(newLength:uint = 8, userAlphabet:String = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):String {
      		var alphabet:Array = userAlphabet.split("");
      		var alphabetLength:int = alphabet.length;
      		var randomLetters:String = "";
      		for (var i:uint = 0; i < newLength; i++) {
        		randomLetters += alphabet[int(Math.floor(Math.random() * alphabetLength))];
      		}
      		
      		return randomLetters;
    	}		
	}
}