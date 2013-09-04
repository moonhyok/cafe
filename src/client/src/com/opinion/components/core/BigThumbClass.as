package com.opinion.components.core {
	// See: http://blog.flexexamples.com/2007/09/12/changing-a-slider-controls-thumb-skin/
	
    import mx.controls.sliderClasses.SliderThumb;
    
    public class BigThumbClass extends SliderThumb {
        public function BigThumbClass() {
            super();
            this.width = 30;
            this.height = 15;
        }
    }
}