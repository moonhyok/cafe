package com.opinion.components.core
{
	import flash.events.Event;
	import flash.events.MouseEvent;
	
	import mx.containers.TitleWindow;

	public class DraggableTitleWindow extends TitleWindow {
		private var xVal:Number;
		private var yVal:Number;
		
		public function DraggableTitleWindow() {
			super();
		}

		private function handleDown(e:Event):void {
			this.startDrag()
		}
		
		private function handleUp(e:Event):void {
			this.stopDrag()
			xVal = this.x;
			yVal = this.y;
		}

		override protected function updateDisplayList(unscaledWidth:Number, unscaledHeight:Number):void {
			super.updateDisplayList(unscaledWidth, unscaledHeight);
			if (!isNaN(xVal) && !isNaN(yVal)) {
				this.move(xVal, yVal);
			}
		}
		
		override protected function createChildren():void {
			super.createChildren();
			super.titleBar.addEventListener(MouseEvent.MOUSE_DOWN,handleDown);
			super.titleBar.addEventListener(MouseEvent.MOUSE_UP,handleUp);
		}
	}
}