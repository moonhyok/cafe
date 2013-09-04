package com.themorphicgroup.controls.sliderClasses {

    import flash.events.MouseEvent;
    import flash.geom.Point;
    
    import mx.controls.sliderClasses.Slider;
    import mx.controls.sliderClasses.SliderThumb;
    import mx.core.mx_internal;
    
    use namespace mx_internal;
    
    /**
     * Extending the Flex Slider class to allow the ability to begin dragging the slider thumb by clicking on the track. 
     * Normally the thumb just tweens to the location clicked but does not begin dragging.
     */
    public class Slider extends mx.controls.sliderClasses.Slider {
        
        [Inspectable(defaultValue="true")]

        /**
         * Specifies whether clicking on the track will begin dragging the slider thumb. 
         * You must also set allowTrackClick = false. 
         *
         *  @default true
         */
        public var allowTrackClickDragSliderThumb:Boolean = true;
        
        public function Slider() {
            super();
        }
        
        override protected function createChildren():void
        {
            super.createChildren();
    
            getTrackHitArea().addEventListener(MouseEvent.MOUSE_DOWN,
                                               track_mouseDownHandler);
        }
        
        private function track_mouseDownHandler(event:MouseEvent):void {
            if (event.target != getTrackHitArea())
                return;
            if (enabled && allowTrackClickDragSliderThumb && !allowTrackClick)
            {
                var pt:Point = new Point(event.localX, event.localY);
                var xM:Number = pt.x;
                var minIndex:Number = 0;
                var minDistance:Number = 10000000;
    
                // find the nearest thumb
                var n:int = thumbCount;
                for (var i:int = 0; i < n; i++)
                {
                    var d:Number = Math.abs(SliderThumb(getThumbAt(i)).xPosition - xM);
                    if (d < minDistance)
                    {
                        minIndex = i;
                        minDistance = d;
                    }
                }
                var thumb:SliderThumb = SliderThumb(getThumbAt(minIndex));
                if (!isNaN(snapInterval) && snapInterval != 0)
                    xM = getXFromValue(getValueFromX(xM));
                
                // Move the thumb.
                thumb.xPosition = xM;
                
                // Start the dragging process by dispatching the mouseDown event.
                thumb.dispatchEvent(new MouseEvent(MouseEvent.MOUSE_DOWN, true, false, thumb.xPosition - thumb.x));
            }
        }
    }
}