package com.opinion.components.core {
	import flash.events.MouseEvent;
	import flash.geom.Point;
	
	import mx.charts.LinearAxis;
	import mx.charts.chartClasses.CartesianTransform;
	import mx.charts.chartClasses.ChartElement;
	import mx.managers.CursorManager;
	import mx.managers.CursorManagerPriority;

	/**
	 * The name of this class is a bit of a misnomer. All this class does is Paning, no zooming involved.
	 */
	public class PanAndZoom extends ChartElement {
		private var _startMin:Point;
		private var _startMax:Point;
		private var _startMouseData:Array;
		private var _start1PixelOffset:Array;
		private var _startOriginPixels:Point;
		private var _startMousePointInPixels:Point;
		private var _dragTool:String;
		
        [Embed(source="/assets/icons/icons/iconography.swf", symbol="IconHandOpen")] private var _iconHandOpen:Class;
		[Embed(source="/assets/icons/icons/iconography.swf", symbol="IconHandClosed")] private var _iconHandClosed:Class;
        
        private var handCursorID:Number;    
		private var handClosedCursorID:Number = 0;
		
		public var draggedOnLastMouseDown:Boolean = false;

		/**
		 * The constructor for this package. It adds the corresponding event listeners 
		 */
		public function PanAndZoom() {
			super();
			addEventListener(MouseEvent.MOUSE_DOWN,startPanAndZoom);
			addEventListener(MouseEvent.MOUSE_OUT, cursorOut);
			addEventListener(MouseEvent.MOUSE_OVER, setCursor);
		}

		/**
		 * Removes the eventlisteners and cursors when the mouse moves out the plane
		 */
		private function cursorOut(e:MouseEvent):void {
			systemManager.removeEventListener(MouseEvent.MOUSE_MOVE, panAndZoom, true);
			systemManager.removeEventListener(MouseEvent.MOUSE_UP, endPanAndZoom, true);	
			CursorManager.removeAllCursors();
			handClosedCursorID = 0;	
		}
		
		/**
		 * This sets the cursor to be the corresponding icon, the Id is returned and is used
		 * to remove the correct cursor later on
		 */
		private function setCursor(e:MouseEvent):void {	
			handCursorID = CursorManager.setCursor(_iconHandOpen,CursorManagerPriority.MEDIUM, -8);
			if (handClosedCursorID != 0){
				// This means the user went out of the plane and then came back in
				handClosedCursorID = CursorManager.setCursor(_iconHandClosed, CursorManagerPriority.HIGH, -8);
			} 
		}
		
		/**
		 * The initial pan and zoom function, it adds the corresponding event listeners and takes data from the graph
		 */
		private function startPanAndZoom(e:MouseEvent):void {
		    // Set public var alerting any listeners that a drag has occured since the last mouse down
		    draggedOnLastMouseDown = false;
		    
			handClosedCursorID = CursorManager.setCursor(_iconHandClosed, CursorManagerPriority.HIGH, -8);
			systemManager.addEventListener(MouseEvent.MOUSE_MOVE, panAndZoom, true);
			systemManager.addEventListener(MouseEvent.MOUSE_UP, endPanAndZoom, true);
			
			var hAxis:LinearAxis = LinearAxis(CartesianTransform(dataTransform).getAxis(CartesianTransform.HORIZONTAL_AXIS));
			var vAxis:LinearAxis = LinearAxis(CartesianTransform(dataTransform).getAxis(CartesianTransform.VERTICAL_AXIS));
			_startMin = new Point(hAxis.minimum, vAxis.minimum);
			_startMax = new Point(hAxis.maximum, vAxis.maximum);
			
			_startMousePointInPixels = new Point(mouseX, mouseY);
			_startMouseData = dataTransform.invertTransform(mouseX, mouseY);
			_start1PixelOffset = dataTransform.invertTransform(mouseX + 1, mouseY + 1);
			_start1PixelOffset[0] -= _startMouseData[0];
			_start1PixelOffset[1] -= _startMouseData[1];
						
			var cache:Array = [{xV:0, yV:0}];
			dataTransform.transformCache(cache, "xV", "x", "yV", "y");
			_startOriginPixels = new Point(cache[0].x, cache[0].y);
			cache[0].xV = 1;
			cache[0].yV = 1;
		}
		
		/**
		 * The function that does the work. Paning works by adjusting the maximum and minimus of the axis 
		 */
		private function panAndZoom(e:MouseEvent):void {
			var hAxis:LinearAxis = LinearAxis(CartesianTransform(dataTransform).getAxis(CartesianTransform.HORIZONTAL_AXIS));
			var vAxis:LinearAxis = LinearAxis(CartesianTransform(dataTransform).getAxis(CartesianTransform.VERTICAL_AXIS));

			var dX:Number = mouseX - _startMousePointInPixels.x;
			var dY:Number = mouseY - _startMousePointInPixels.y;
			
			hAxis.maximum = _startMax.x - dX * _start1PixelOffset[0];
			hAxis.minimum = _startMin.x - dX * _start1PixelOffset[0];
			vAxis.maximum = _startMax.y - dY * _start1PixelOffset[1];
			vAxis.minimum = _startMin.y - dY * _start1PixelOffset[1];
			
			draggedOnLastMouseDown = true;
		}
		
		/**
		 * This function removes the event listeners and makes the cursor an open hand again 
		 */
		private function endPanAndZoom(e:MouseEvent):void {
			systemManager.removeEventListener(MouseEvent.MOUSE_MOVE, panAndZoom, true);
			systemManager.removeEventListener(MouseEvent.MOUSE_UP, endPanAndZoom, true);						
			CursorManager.removeCursor(handClosedCursorID);
			handClosedCursorID = 0;
		}
		
		/**
		 * TODO: Comment this
		 */
		override protected function updateDisplayList(unscaledWidth:Number, unscaledHeight:Number):void {
			graphics.clear();
			graphics.moveTo(0, 0);
			graphics.beginFill(0, 0);
			graphics.drawRect(0, 0, unscaledWidth, unscaledHeight);
		}
	}
}