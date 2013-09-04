package com.opinion.utils
{
	import flash.display.GradientType;
	import flash.display.Sprite;
	import flash.filters.DropShadowFilter;
	import flash.text.StyleSheet;
	import flash.text.TextField;
	public class HiveDraw
	{
		[Embed(source="/assets/fonts/helvetica/HelveticaNeueCondensedBold.ttf", fontFamily="Helvetica", fontWeight="bold",mimeType="application/x-font-truetype")] private static const Helvetica:Class;
		
		public function HiveDraw()
		{
		}
		
			
		public static function drawPolygon(sides:Number, radius:Number,alphas:Array, colors:Array, ratios:Array, h1:String="", h2:String="", style:String="default",border:int =5,now_open:Boolean=false, show_closed:Boolean=false):Sprite
		{   
			// Create a new style sheet object
			var style_sheet:StyleSheet = new StyleSheet();
			
			var defaultStyle:Object = new Object();
			defaultStyle.fontFamily = "Helvetica";
			defaultStyle.fontWeight = "bold";
			defaultStyle.color = "#4c4c4a";
			
			var secondary:Object = new Object();
			secondary.fontFamily = "Helvetica";
			secondary.fontWeight = "bold";
			secondary.color = "#656565";
			
			var resourcesStyle:Object = new Object();
			resourcesStyle.fontFamily = "Helvetica";
			resourcesStyle.fontWeight = "bold";
			resourcesStyle.color = "#ec8d24";
			
			style_sheet.setStyle('.default', defaultStyle);
			style_sheet.setStyle('.resources', resourcesStyle);
			style_sheet.setStyle('.secondary', secondary);
			 
			var shape:Sprite = new Sprite();    
			
			var innerShadow:DropShadowFilter = new DropShadowFilter();
            innerShadow.color = 0x000000;
            innerShadow.inner = true;
            innerShadow.angle = 45;
            innerShadow.distance = 7;
            innerShadow.strength = 3;
            innerShadow.blurX = 10;
            innerShadow.blurY = 10;
            innerShadow.alpha = .2;

			shape.graphics.lineStyle(border, 0x7f7f7f, .7);
			shape.filters = [innerShadow];
			
			shape.graphics.beginGradientFill(GradientType.RADIAL, colors,alphas, ratios);
				
			var angle:Number = 360/sides;     
			var current_side:Number = 0;     
			while (current_side<=sides) 
			{         
				var a:Number = angle*current_side/180*Math.PI;         
				var x:Number = radius*Math.sin(a);         
				var y:Number = radius*Math.cos(a);         
				if (!current_side) 
					shape.graphics.moveTo(x, y);         
				else    
					shape.graphics.lineTo(x, y);         
				current_side++;     
			} 		
			
			var lines:Array = h1.split('\n');
			for(var i:int = 0; i<lines.length;i++){
				var startText:TextField = new TextField();
				startText.embedFonts = true;
				startText.styleSheet = style_sheet;
				startText.htmlText = "<span class=\""+style+"\">"+ lines[i] + "</span>";
				startText.width = radius *2 - 10;
				startText.x = -startText.textWidth/2;//-Math.sqrt(3)*(radius)/2;
				startText.y = -startText.textHeight -10 + i*13;
				shape.addChild(startText);
			}

			
			var nextText:TextField = new TextField();
			nextText.embedFonts = true;
			nextText.styleSheet = style_sheet; 
			nextText.htmlText = "<span class='secondary'>"+ h2 + "</span>";
			
			if (now_open)
			{
				var openText:TextField = new TextField();
				openText.embedFonts = true;
				openText.styleSheet = style_sheet; 
				openText.htmlText = "<span class='secondary'>"+ "NOW OPEN" + "</span>";
				openText.x = -25;
				openText.y = -40;
				shape.addChild(openText);
			}
			
			if (show_closed)
			{
				var openText:TextField = new TextField();
				openText.embedFonts = true;
				openText.styleSheet = style_sheet; 
				openText.htmlText = "<span class='secondary'>"+ "CLOSED" + "</span>";
				openText.x = -20;
				openText.y = -40;
				shape.addChild(openText);
			}

			nextText.x = -nextText.textWidth/2;
			nextText.y = -nextText.textHeight + 30;
			shape.addChild(nextText);
			return shape;
		}
		
	}
}