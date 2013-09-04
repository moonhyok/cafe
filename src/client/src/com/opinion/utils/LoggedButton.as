package com.opinion.utils
{
	import flash.events.MouseEvent;
	import flash.filters.DropShadowFilter;
	import flash.text.TextFieldAutoSize;
	
	import mx.controls.Button;
	import mx.core.Application;
	
	[Style(name="innerShadowColor", type="Number")]
	
	public class LoggedButton extends Button
	{
		private var innerShadowColor:Number;
		private var __textWrap:Boolean = true;
		
		public function LoggedButton()
		{
			super();
			this.buttonMode = true;
		}
		
		public function set textWrap(textWrap: Boolean): void
		{
			__textWrap = textWrap;
		}
		
		public function get textWrap(): Boolean
		{
			return __textWrap;
		}
		
		protected override function clickHandler(event:MouseEvent):void
		{
			var os_id:int = Application.application.opinionSpaceId;
			Application.application.log.logUserEvent(os_id, Log.USER_BUTTONCLICK, this.name);
			super.clickHandler(event);
		}
		
		override protected function createChildren():void
        {
                super.createChildren();
					
				var textShadow:DropShadowFilter = new DropShadowFilter();
                textShadow.color = 0x000000;
                textShadow.angle = -90;
                textShadow.distance = .5;
                textShadow.blurX = 0;
                textShadow.blurY = 0;
                textShadow.alpha = .75;
				textField.filters = [textShadow];
				
				var buttonShadow:DropShadowFilter = new DropShadowFilter();
                buttonShadow.color = 0x000000;
                buttonShadow.angle = 135;
                buttonShadow.distance = 1.75;
                buttonShadow.blurX = 0;
                buttonShadow.blurY = 0;
                buttonShadow.alpha = .4;
                
                innerShadowColor = getStyle("innerShadowColor");
                
                var innerShadow1:DropShadowFilter = createInnerShadow(0, innerShadowColor);
                var innerShadow2:DropShadowFilter = createInnerShadow(90, innerShadowColor);
                var innerShadow3:DropShadowFilter = createInnerShadow(180, innerShadowColor);
                var innerShadow4:DropShadowFilter = createInnerShadow(270, innerShadowColor);
                
				this.filters = [innerShadow1, innerShadow2, innerShadow3, innerShadow4, buttonShadow]; 
				
				if(__textWrap == false)
					return;
				
                textField.multiline = true;
                textField.wordWrap = true;
                textField.autoSize = TextFieldAutoSize.CENTER;
        }
        
        override protected function updateDisplayList(unscaledWidth:Number, unscaledHeight:Number):void
        {
                super.updateDisplayList(unscaledWidth, unscaledHeight);
                
                textField.y = (this.height - textField.height) >> 1;
                //this.height = textField.height + getStyle("paddingTop") + getStyle("paddingBottom");
                
        }
        
        private function createInnerShadow(angle:Number, color:Number):DropShadowFilter
        {
        	var innerShadow:DropShadowFilter = new DropShadowFilter();
            innerShadow.inner = true;
            innerShadow.color = color;
            innerShadow.angle = angle;
            innerShadow.distance = 1.25;
            innerShadow.blurX = 0;
            innerShadow.blurY = 0;
            innerShadow.alpha = 1;
                
        	return innerShadow;
        }
        
	}
}