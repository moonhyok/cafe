package com.opinion.components.core
{
    import flash.geom.Matrix;
    
    import mx.skins.ProgrammaticSkin;
    import mx.utils.GraphicsUtil;

    public class GradientBackground extends ProgrammaticSkin
    {
        override public function get measuredWidth():Number
        {
            return 20;
        }
        
        override public function get measuredHeight():Number
        {
            return 20;
        }
        
        override protected function updateDisplayList(unscaledWidth:Number, unscaledHeight:Number):void
        {
            var fillColors:Array = getStyle("fillColors");
            var fillAlphas:Array = getStyle("fillAlphas");
            var cornerRadius:int = getStyle("cornerRadius");
            var gradientType:String = getStyle("gradientType");
            var angle:Number = getStyle("angle");
            var focalPointRatio:Number = getStyle("focalPointRatio");
            //var borderColor:Number = getStyle("borderColor");
            //var borderThickness:Number = getStyle("borderThickness");
            
            // Default values, if styles aren't defined
            if (fillColors == null)
                fillColors = [0xEEEEEE, 0x999999];
            
            if (fillAlphas == null)
                fillAlphas = [1, 1];
            
            if (gradientType == "" || gradientType == null)
                gradientType = "linear";
            
            if (isNaN(angle))
                angle = 90;
            
            if (isNaN(focalPointRatio))
                focalPointRatio = 0.5;
            
            var matrix:Matrix = new Matrix();
            matrix.createGradientBox(unscaledWidth, unscaledHeight, angle * Math.PI / 180);
            
            graphics.beginGradientFill(gradientType, fillColors, fillAlphas, [0, 255] , matrix, "pad", "rgb", focalPointRatio);
            //graphics.lineStyle(borderThickness, borderColor);
            //graphics.drawRect(0, 0, unscaledWidth, unscaledHeight);
            //GraphicsUtil.drawRoundRectComplex(graphics, 0, 0, unscaledWidth, unscaledHeight, cornerRadius, cornerRadius, cornerRadius, cornerRadius);

            
            graphics.drawRoundRect(0, 0, unscaledWidth, unscaledHeight, cornerRadius*.075, cornerRadius*.075);
            
             
            graphics.endFill();
        }
    }
}