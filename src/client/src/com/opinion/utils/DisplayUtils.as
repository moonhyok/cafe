package com.opinion.utils {
	import mx.containers.TitleWindow;
	import mx.core.Application;
	import mx.managers.PopUpManager;
	import mx.core.IFlexDisplayObject;
	import flash.display.DisplayObject;
	import com.opinion.components.core.Popup;

	public class DisplayUtils {
		public static function displayPopup(parentApp:Object, state:String):void {
			if (parentApp.popup == null) {
				parentApp.popup = Popup(PopUpManager.createPopUp(DisplayObject(parentApp.parentDocument), Popup, true));
				parentApp.popup.currentState = state;
			}
			else {
				parentApp.popup.currentState = state;
			}
		}
	}
}