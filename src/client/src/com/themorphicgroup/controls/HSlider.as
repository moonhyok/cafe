package com.themorphicgroup.controls {

    import com.themorphicgroup.controls.sliderClasses.Slider;
    
    import flash.events.MouseEvent;
    import flash.geom.Point;
    
    import mx.controls.sliderClasses.SliderDirection;
    
    public class HSlider extends Slider {
        
        public function HSlider() {
            super();
            direction = SliderDirection.HORIZONTAL;
        }
    }

}
