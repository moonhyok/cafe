package com.opinion.components.core
{
	import flash.display.*;
	import flash.geom.Matrix;
	
	import mx.controls.sliderClasses.SliderDataTip;	

	public class CustomSliderDataTip extends SliderDataTip
	{
		public function CustomSliderDataTip()
		{
			super();
		}
		
		override protected function createChildren():void{ 
            super.createChildren();
        }
        
        override protected function updateDisplayList(w:Number, h:Number):void {
            super.updateDisplayList(w, h);
            
            /*
            super.alpha = 0;
            
            var g:Graphics = graphics; 
            g.clear();  
            var m:Matrix = new Matrix();
            m.createGradientBox(w+100,h,0,0,0);
            g.beginGradientFill(GradientType.LINEAR,[0xFF0000,0xFFFFFF],
                [.1,1],[0,255],m,null,null,0);
            g.drawRect(-50,0,w+100,h);
            g.endFill();*/
        }
	}
}