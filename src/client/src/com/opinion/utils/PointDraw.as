package com.opinion.utils
{
	import flash.display.GradientType;
	import flash.display.Shape;
	import flash.display.Sprite;
	
	public class PointDraw
	{
		
		public function PointDraw()
		{
			
		}
		
		public function ideaProgression():Array
		{
			var arr:Array = new Array();
			//arr.push(drawIdeaStage1([[0x989ecf], [0xf47d5e], [0xfaac63], [0xffd335], [0xa1bc3b]], [[.75],[.75],[.75],[.75],[.75]], [[0],[0],[0],[0],[0]], [[20],[20],[20],[20],[20]], 20/3, Math.PI));
			//arr.push(drawIdeaStage2([[0xed9cbe], [0xf47d5e], [0xfaac63], [0xffd335], [0xc7df8c], [0xa1bc3b], [0x92d2c1], [0xafc8cc], [0x9ab5df], [0xc7b0d5], [0x989ecf]], [[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9]], [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]], [[24],[24],[24],[24],[24], [24],[24],[24],[24],[24],[24]], 8, Math.PI));
			//arr.push(drawIdeaStage3([[0xed9cbe], [0xf47d5e], [0xfaac63], [0xffd335], [0xc7df8c], [0xa1bc3b], [0x92d2c1], [0xafc8cc], [0x9ab5df], [0xc7b0d5], [0x989ecf]], [[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9]], [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]], [[35],[35],[35],[35],[35], [35],[35],[35],[35],[35],[35]], 12, Math.PI));
			//arr.push(drawIdeaStage4([[0xafc8cc], [0x6c8fbf], [0x9377b6], [0xc7b0d5], [0x989ecf],[0xe5562f], [0xf47d5e], [0xf57e20], [0xc78230], [0xfaac63],[0xffd335], [0xd0ae4e], [0xa1bc3b], [0xb0c66f], [0xc7df8c]], [[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8]], [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]], [[30],[30],[30],[30],[30],[30],[30],[30],[30],[30],[30],[30],[30],[30],[30]], 15, Math.PI));
			
			var sizes:Array = [7, 12.5, 16, 20, 23, 27.5, 31, 35];
			var colors:Array = [0xffda10, 0xffaa10, 0xff5b11, 0xef3a47, 0xc22f3a, 0xc22faf, 0x9e2fc2];
			
			for (var i:int=0; i<colors.length; i++)
			{
				arr.push(drawDisc(colors[i],0,0, sizes[i]/7,sizes[i]));	
			}
			
			/*
			arr.push(drawDisc(0xcccccc,4,0, 2,sizes[0]));
			
			
			colors.splice(cindx, 1);
			cindx = Math.random() * colors.length;
			
			arr.push(drawDisc(colors[cindx],2,0, sizes[2]/7,sizes[2]));
			colors.splice(cindx, 1);
			cindx = Math.random() * colors.length;
			
			arr.push(drawDisc(colors[cindx],3,0, sizes[3]/7,sizes[3]));
			colors.splice(cindx, 1);
			cindx = Math.random() * colors.length;
			
			arr.push(drawDisc(colors[cindx],4,0, sizes[4]/7,sizes[4]));*/
			return arr;
		}
		
		public function colorLegend(outerR:int = 7):Array
		{
			var colors:Array = [0xffda10, 0xffaa10, 0xff5b11, 0xef3a47, 0xc22f3a, 0xc22faf, 0x9e2fc2];
			var arr:Array = [];
			for (var i:int=0; i<colors.length; i++)
			{
				arr.push(drawDisc(colors[i],0,0,outerR/7,outerR));	
			}
			return arr;
		}
		
		public function sizeLegend(baseR:int = 7):Array
		{
			var sizes:Array = [baseR,baseR * 10/7, baseR * 12.5/7];
			var arr:Array = [];
			for (var i:int=0; i<sizes.length; i++)
			{
				arr.push(drawDisc(0xcccccc,0,0, sizes[i]/7,sizes[i]));	
			}
			return arr;
		}
		
		/**
		 * Returns 25 of flowers to be drawn in a 5 x 5 grid displaying different sizes, color palettes, and stages of development
		 */ 
		public function calibrateDrawing():Array
		{
			var radius:Number = 20;
			var decay:Number = .75;
			var alphaArr:Array = [0.75, 0.8, 0.8];
			var numPetalArr:Array = [8, 10, 10];
			var colorArr:Array = [0x488214, 0x4B0082, 0xFFD700];
			var layerOffsetArr:Array = [Math.PI/4, 0, 0];
			
			// container for grid sprites
			var arr:Array = new Array();
			
			// BUDS
			var numBudSegments:int = 5;
			
			// Walkthrough sequence:
			var colors:Array = new Array();
			var alphas:Array = new Array();
			var ratios:Array = new Array();
			
			// populate gradient arrays
			for (var j:int= 0; j < 5; j++)
			{
				colors.push([0x8ac545, 0x376b19]);
				alphas.push([1, 1]);
				ratios.push([0, 25]);
			}
			
			/*
			arr.push(drawBud(10, alphas, colors, ratios));
			arr.push(drawDaisy(20, [1,1,1], 7, [0xf9b2a8 , 0xfef05f, 0xffcfb6], [0,40, 120]));
			arr.push(drawDaisy(35, [1,1,1], 12, [0xf9b2a8 , 0xfef05f, 0xffcfb6], [0,40, 120]));
			*/
			//
			// Flower sequence 1:
			//
			
			// 2 color gradient arrays			
			var colors:Array = new Array();
			var alphas:Array = new Array();
			var ratios:Array = new Array();
			
			// populate gradient arrays
			for (var j:int= 0; j < numBudSegments; j++)
			{
				colors.push([0xfc8ccd, 0x980f30]);
				alphas.push([1, 0.7]);
				ratios.push([0, 30]);
			}
			
			// draw flower stages
			/*
			arr.push(drawBud(10, alphas, colors, ratios)); // bud
			arr.push(drawFlower(15, 0.75, [[.8,.8]], [15], [[0xfc8ccd, 0x980f30]], [[0,60]], [0])); // single layer flower
			arr.push(drawFlower(30, 0.7, [[.7,.7], [.8,.8]], [15, 18], [[0xfc8ccd, 0x980f30],[0x980f30, 0xfc8ccd]], [[0,127],[0,60]], [0, Math.PI/4])); // larger double layer flower

			// Cross breeds
			arr.push(drawFlower(40, 0.7, [[.7,.7], [.8,.8], [.8,.8]], [15, 18, 15], [[0xfc8ccd, 0x980f30],[0x9155c7, 0x980f30], [0x980f30, 0xf9df07]], [[0, 127],[0, 90],[0, 60]], [0, Math.PI/4, Math.PI/8])); // larger double layer flower
			arr.push(drawFlower(50, 0.7, [[.7,.7], [.8,.8], [.8,.8]], [15, 18, 15], [[0xfc8ccd, 0x980f30],[0x9155c7, 0x980f30], [0x980f30, 0xf9df07]], [[0, 127],[0, 90],[0, 60]], [0, Math.PI/4, Math.PI/8])); // larger double layer flower
			*/
			//
			// Flower sequence 2:
			//
			
			// 2 color gradient arrays			
			var colors1:Array = new Array();
			var alphas1:Array = new Array();
			var ratios1:Array = new Array();
			
			// populate gradient arrays
			for (var k:int= 0; k < numBudSegments; k++)
			{
				colors1.push([0x9155c7, 0xf9df07]);
				alphas1.push([1, 0.7]);
				ratios1.push([0, 30]);
			}
			
			// draw flower stages
			/*
			arr.push(drawBud(10, alphas1, colors1, ratios1)); // bud
			arr.push(drawDaisy(10, [1,1], 10, [0xFF0000,0xFFFFFF], [0,30])); // single layer flower
			arr.push(drawFlower(30, 0.7, [[.7,.7], [.8,.8]], [15, 18], [[0x9155c7, 0xf9df07],[0x9155c7, 0xf9df07]], [[0,127],[0,60]], [0, Math.PI/4])); // larger double layer flower
			
			// Cross breeds
			arr.push(drawFlower(40, 0.7, [[.9,.9], [.8,.8], [.8,.8]], [15, 18, 15], [[0x9155c7, 0xf9df07], [0x980f30, 0x9155c7], [0xf9df07, 0xfc8ccd]], [[0, 127],[0, 90],[0, 60]], [0, Math.PI/4, Math.PI/8])); // larger double layer flower
			arr.push(drawFlower(50, 0.7, [[.9,.9], [.8,.8], [.8,.8]], [15, 18, 15], [[0x9155c7, 0xf9df07], [0x980f30, 0x9155c7], [0xf9df07, 0xfc8ccd]], [[0, 127],[0, 90],[0, 60]], [0, Math.PI/4, Math.PI/8])); // larger double layer flower
			*/
			
			// Sample larger petal
			//arr.push(drawPetal([0xafe0ea], [1], [0], 50, Math.PI/12, 100, 100));
			//arr.push(drawIdeaStage1([[0xafc8cc], [0xfbc0a9], [0xfcda96], [0xfef4a0], [0xc7df8c]], [[.8],[.8],[.8],[.8],[.8]], [[0],[0],[0],[0],[0]], [[60],[60],[60],[60],[60]], 20, Math.PI));
            arr.push(drawIdeaStage1([[0xafc8cc], [0xfbc0a9], [0xfcda96], [0xfef4a0], [0xc7df8c]], [[.8],[.8],[.8],[.8],[.8]], [[0],[0],[0],[0],[0]], [[20],[20],[20],[20],[20]], 20/3, Math.PI));
			arr.push(drawIdeaStage2([[0xed9cbe], [0xf47d5e], [0xfaac63], [0xffd335], [0xc7df8c], [0xa1bc3b], [0x92d2c1], [0xafc8cc], [0x9ab5df], [0xc7b0d5], [0x989ecf]], [[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9]], [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]], [[24],[24],[24],[24],[24], [24],[24],[24],[24],[24],[24]], 8, Math.PI));
			arr.push(drawIdeaStage3([[0xed9cbe], [0xf47d5e], [0xfaac63], [0xffd335], [0xc7df8c], [0xa1bc3b], [0x92d2c1], [0xafc8cc], [0x9ab5df], [0xc7b0d5], [0x989ecf]], [[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9],[.9]], [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]], [[35],[35],[35],[35],[35], [35],[35],[35],[35],[35],[35]], 12, Math.PI));
			arr.push(drawIdeaStage4([[0xafc8cc], [0x6c8fbf], [0x9377b6], [0xc7b0d5], [0x989ecf],[0xe5562f], [0xf47d5e], [0xf57e20], [0xc78230], [0xfaac63],[0xffd335], [0xd0ae4e], [0xa1bc3b], [0xb0c66f], [0xc7df8c]], [[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8],[.8]], [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]], [[30],[30],[30],[30],[30],[30],[30],[30],[30],[30],[30],[30],[30],[30],[30]], 15, Math.PI));
			
			return arr;
		}
		
		/**
		 * Draws a multi-layer flower, drawing the lowest layer first with radius = outerRadius, where the color, number of petals,
		 * and alpha per layer are defined in the arrays (these must all be the same length). The radius of each layer decays by
		 * radiusDecay.
		 * 
		 * alphaArr, colorArr, and ratiosArr are all arrays of arrays used to draw gradients
		 * 
		 */ 
		public function drawFlower(outerRadius:Number, radiusDecay:Number, alphaArr:Array, numPetalArr:Array, colorArr:Array, ratioArr:Array, layerOffsetArr:Array):Sprite
		{
			var flower:Sprite = new Sprite();
			
			// Iterate through layers
			for (var i:int = 0; i < alphaArr.length; i++)
			{
				
				// Draw each petal per layer
				for (var j:int = 0; j < numPetalArr[i]; j++)
				{
					var radius:Number = outerRadius * Math.pow(radiusDecay, i)
					flower.addChild(drawPetal(colorArr[i], alphaArr[i], ratioArr[i], radius, 2*Math.PI * j / numPetalArr[i] + layerOffsetArr[i], radius*2/3, radius*1/3));
				}
			}
			
			return flower;
		}
		
		
		public function drawDaisy(radius:Number,alphasArr:Array, numPetals:int, colorArr:Array, ratioArr:Array):Sprite
		{
			var flower:Sprite = new Sprite();
			
			for (var j:int = 0; j < numPetals; j++)
			{
				/*
				if(numPetals <= 8)
					flower.addChild(drawPetal(colorArr, alphasArr, ratioArr, radius, 2*Math.PI * j / numPetals, radius, radius*1/2));
				else*/
				flower.addChild(drawPetal(colorArr, alphasArr, ratioArr, radius, 2*Math.PI * j / numPetals, radius*.95, radius*1/3));
			}
			
			var center:Shape = new Shape();
			center.graphics.beginGradientFill(GradientType.RADIAL,[0x999900, 0xFFFF00], [1,.5], [0,60]);
			center.graphics.drawCircle(0, 0, radius*.2);
			var wrapper:Shape = new Shape();
			wrapper.graphics.beginFill(0xFFFFFF,0);
			wrapper.graphics.drawCircle(0, 0, radius);
			flower.addChild(center);
			flower.addChild(wrapper);
			return flower;
		}
		
		/**
		 * Draws a petal using polar coordinates as input. This assumes the petal starts at (0,0)
		 * 
		 * 	- radius = length of petal
		 *  - theta = angle in radians relative to right horizontal line in euclidean space
		 *  - controlXOffset = x offset from 0,0 horizontally along the angle theta used to define the control point 
		 *  - controlYOffset = y offset from 0,0 perpendicular to the line defined by angle theta used to define the control point
		 */ 		
		private function drawPetal(colors:Array, alphas:Array, ratios:Array, radius:Number, theta:Number, controlXOffset:int, controlYOffset:int):Shape
		{
			var petal:Shape = new Shape();
			
			// The length from (0,0) to the control point
			var controlR:Number = Math.sqrt(Math.pow(controlXOffset, 2) + Math.pow(controlYOffset, 2)); 
			
			// The angle between the line to the control point and the center of the petal
			var beta:Number = Math.atan(controlYOffset/controlXOffset);
			
			// Draw the petal from (0,0) around upper control point and then around lower control point			
			petal.graphics.moveTo(0,0);
			petal.graphics.beginGradientFill(GradientType.RADIAL, colors, alphas, ratios);
			//petal.graphics.lineStyle(1, 0x000000, .25);
			petal.graphics.curveTo(controlR * Math.cos(theta + beta), controlR * Math.sin(theta + beta), radius * Math.cos(theta), radius * Math.sin(theta));
			petal.graphics.curveTo(controlR * Math.cos(theta - beta), controlR * Math.sin(theta - beta), 0,0); 
			
			return petal;
		}
		
		/**
		 * Draws a bud
		 * 
		 * alphaArr, colorArr, and ratiosArr are all arrays of arrays used to draw gradients
		 * 
		 */ 
		public function drawBud(radius:Number, alphaArr:Array, colorArr:Array, ratiosArr:Array):Sprite
		{
			var bud:Sprite = new Sprite();
			
			// Iterate per segment
			for (var i:int = 0; i < colorArr.length; i++)
				bud.addChild(drawBudSegment(colorArr[i], alphaArr[i], ratiosArr[i], radius, 2*Math.PI / colorArr.length * i, 2*Math.PI / colorArr.length)); 		
			
			return bud;
		}
		
		/**
		 * Draw a bud segment as an arc with curved edges
		 * 
		 * Edges are draw with curves that  
		 */ 
		private function drawBudSegment(colors:Array, alphas:Array, ratios:Array, radius:Number, theta_offset:Number, theta_width:Number):Shape
		{
			var budseg:Shape = new Shape();
			
			// The length from (0,0) to the control point
			var contXRatio:Number = 1/2;
			var contYRatio:Number = 1/3;
			var controlR:Number = Math.sqrt(Math.pow(radius * contXRatio, 2) + Math.pow(radius * contYRatio, 2)); 
			
			// The angle between the line to the control point and the center of the petal
			var beta:Number = Math.atan((radius * contYRatio) / (radius * contXRatio));
			
			// Draw bottom curved edge
			budseg.graphics.moveTo(0,0);
			budseg.graphics.beginGradientFill(GradientType.RADIAL, colors, alphas, ratios);
			budseg.graphics.lineStyle(1, 0x000000, .25);
			budseg.graphics.curveTo(controlR * Math.cos(theta_offset - beta), controlR * Math.sin(theta_offset - beta), radius * Math.cos(theta_offset), radius * Math.sin(theta_offset));
			
			// Draw arc with control point a fraction of the length of the radius and halfway in the arc
			var contRadiusRatio:Number = 13/10;
			budseg.graphics.curveTo(contRadiusRatio * radius * Math.cos(theta_offset + theta_width/2), contRadiusRatio * radius * Math.sin(theta_offset + theta_width/2), radius * Math.cos(theta_offset + theta_width), radius * Math.sin(theta_offset + theta_width));
			
			// Draw upper curved edge back to 0,0
			budseg.graphics.curveTo(controlR * Math.cos(theta_offset + theta_width - beta), controlR * Math.sin(theta_offset + theta_width - beta), 0,0);
			
			return budseg;
		}
		
		public function drawIdeaStage1(petalColors:Array, petalAlphas:Array, petalRatios:Array, petalRadii:Array, ringRadius:Number, initialOffset:Number):Sprite {
			var idea:Sprite = new Sprite();
			
			for (var i:int = 0; i < petalColors.length; i++)
			{
				var petal:Shape = drawPetal(petalColors[i], petalAlphas[i], petalRatios[i], petalRadii[i], Math.PI/2 + Math.PI*2/petalColors.length * i, .4545 * petalRadii[i], .4 * petalRadii[i]);
				
				var z:Number = Math.sqrt(Math.pow(ringRadius, 2) + Math.pow(petalRadii[i]/2, 2));
				var beta:Number = Math.atan(petalRadii[i]/2 / ringRadius);
				petal.x = z * Math.cos(beta + initialOffset + Math.PI*2/petalColors.length * i);
				petal.y = z * Math.sin(beta + initialOffset + Math.PI*2/petalColors.length * i);
				 
				idea.addChild(petal);
			}
			
			return idea;
		}
		
		public function drawIdeaStage2(petalColors:Array, petalAlphas:Array, petalRatios:Array, petalRadii:Array, ringRadius:Number, initialOffset:Number):Sprite {
			var idea:Sprite = new Sprite();
			
			for (var i:int = 0; i < petalColors.length; i++)
			{
				var petal:Shape = drawPetal(petalColors[i], petalAlphas[i], petalRatios[i], petalRadii[i], Math.PI/2 + Math.PI*2/petalColors.length * i, .4545 * petalRadii[i], .2 * petalRadii[i]);
				
				var z:Number = Math.sqrt(Math.pow(ringRadius, 2) + Math.pow(petalRadii[i]*4/5, 2));
				var beta:Number = Math.atan(petalRadii[i]*4/5 / ringRadius);
				petal.x = z * Math.cos(beta + initialOffset + Math.PI*2/petalColors.length * i);
				petal.y = z * Math.sin(beta + initialOffset + Math.PI*2/petalColors.length * i);
				 
				idea.addChild(petal);
			}
			
			return idea;
		}
		
		public function drawIdeaStage3(petalColors:Array, petalAlphas:Array, petalRatios:Array, petalRadii:Array, ringRadius:Number, initialOffset:Number):Sprite {
			var idea:Sprite = new Sprite();
			
			for (var i:int = 0; i < petalColors.length; i++)
			{
				var petal:Shape = drawPetal(petalColors[i], petalAlphas[i], petalRatios[i], petalRadii[i], Math.PI/2 + Math.PI*2/petalColors.length * i, .4545 * petalRadii[i], .2 * petalRadii[i]);
				
				var z:Number = Math.sqrt(Math.pow(ringRadius, 2) + Math.pow(petalRadii[i]*3/5, 2));
				var beta:Number = Math.atan(petalRadii[i]*3/5 / ringRadius);
				petal.x = z * Math.cos(beta + initialOffset + Math.PI*2/petalColors.length * i);
				petal.y = z * Math.sin(beta + initialOffset + Math.PI*2/petalColors.length * i);
				 
				idea.addChild(petal);
			}
			
			return idea;
		}
		
		public function drawIdeaStage4(petalColors:Array, petalAlphas:Array, petalRatios:Array, petalRadii:Array, ringRadius:Number, initialOffset:Number):Sprite {
			var idea:Sprite = new Sprite();
			
			for (var i:int = 0; i < petalColors.length; i++)
			{
				var petal:Shape = drawPetal(petalColors[i], petalAlphas[i], petalRatios[i], petalRadii[i], Math.PI/2 + Math.PI*2/petalColors.length * i, .4545 * petalRadii[i], .4 * petalRadii[i]);
				
				var z:Number = Math.sqrt(Math.pow(ringRadius, 2) + Math.pow(petalRadii[i]/2, 2));
				var beta:Number = Math.atan(petalRadii[i]/2 / ringRadius);
				petal.x = z * Math.cos(beta + initialOffset + Math.PI*2/petalColors.length * i);
				petal.y = z * Math.sin(beta + initialOffset + Math.PI*2/petalColors.length * i);
				 
				idea.addChild(petal);
			}
			
			return idea;
		}
		
		public function drawDisc(color:Number, quarters:int, offset:Number, innerRadius:Number, outerRadius:Number, thickWhiteRing:Boolean=false):Sprite
		{
			// Disc
			var disc:Sprite = new Sprite();
			
			// Changed to full discs
			if (thickWhiteRing) 
			{
				disc.graphics.beginFill(0xFFFFE0, 1);
				disc.graphics.drawCircle(0,0,outerRadius*9/7);
				disc.graphics.beginFill(color, 1);
				disc.graphics.drawCircle(0,0,outerRadius);
				disc.graphics.drawCircle(0,0,innerRadius);
				disc.graphics.endFill();	
			} else
			{
				/*
				disc.graphics.beginFill(color, 1);
				disc.graphics.drawCircle(0,0,outerRadius);
				disc.graphics.beginFill(0xffffff, 1);
				disc.graphics.drawCircle(0,0,innerRadius);
				disc.graphics.endFill();
				*/
				disc.graphics.beginFill(0xffffff, 1);
				disc.graphics.drawCircle(0,0,outerRadius+1);
				disc.graphics.beginFill(color, 1);
				disc.graphics.drawCircle(0,0,outerRadius);
				disc.graphics.drawCircle(0,0,innerRadius);
				disc.graphics.endFill();		
			}
			
			
			
				
			
			/*
			if (quarters == 0)
				disc.graphics.beginFill(color, .2);
			else
			{
				disc.graphics.beginFill(color, 1);
				quarters-=1;
			}

		    var c1:Number=outerRadius * (Math.SQRT2 - 1);
		    var c2:Number=outerRadius * Math.SQRT2 / 2;
		    
		    var c1in:Number=innerRadius * (Math.SQRT2 - 1);
		    var c2in:Number=innerRadius * Math.SQRT2 / 2;
		    
		    disc.graphics.moveTo(0,0);

			// First quarter + subtract
			disc.graphics.lineTo(outerRadius, 0);
			disc.graphics.curveTo(outerRadius,c1,c2,c2);
			disc.graphics.curveTo(c1,outerRadius,0,outerRadius);
			disc.graphics.lineTo(0,0);
			disc.graphics.lineTo(innerRadius, 0);
			disc.graphics.curveTo(innerRadius,c1in,c2in,c2in);
			disc.graphics.curveTo(c1in,innerRadius,0,innerRadius);
			disc.graphics.lineTo(0,0);
			disc.graphics.endFill();
			
		    if (quarters == 0)
				disc.graphics.beginFill(color, .2);
		    else
		    {
		    	quarters -= 1;
		    	disc.graphics.beginFill(color, 1);
		    }

			disc.graphics.moveTo(0,outerRadius);				
		    disc.graphics.curveTo(-c1,outerRadius,-c2,c2);
		    disc.graphics.curveTo(-outerRadius,c1,-outerRadius,0);
		    disc.graphics.lineTo(0,0);
		    disc.graphics.lineTo(0,innerRadius);
		    disc.graphics.curveTo(-c1in,innerRadius,-c2in,c2in);
		    disc.graphics.curveTo(-innerRadius,c1in,-innerRadius,0);
		    disc.graphics.lineTo(0,0);
			disc.graphics.endFill();

			if (quarters == 0)
				disc.graphics.beginFill(color, .2);
		    else
		    {
		    	quarters -= 1;
		    	disc.graphics.beginFill(color, 1);
		    }

			disc.graphics.moveTo(-outerRadius,0);			
			disc.graphics.curveTo(0-outerRadius,0-c1,0-c2,0-c2);
		    disc.graphics.curveTo(0-c1,0-outerRadius,0,0-outerRadius);
		    disc.graphics.lineTo(0,0);
		    disc.graphics.lineTo(-innerRadius,0);
		    disc.graphics.curveTo(0-innerRadius,0-c1in,0-c2in,0-c2in);
		    disc.graphics.curveTo(0-c1in,0-innerRadius,0,0-innerRadius);
		    disc.graphics.lineTo(0,0);
		    disc.graphics.endFill();
		    
			if (quarters == 0)
				disc.graphics.beginFill(color, .2);
		    else
		    {
		    	quarters -= 1;
		    	disc.graphics.beginFill(color, 1);
		    }
		    
		    disc.graphics.moveTo(0,-outerRadius);
		    disc.graphics.curveTo(0+c1,0-outerRadius,0+c2,0-c2);
		    disc.graphics.curveTo(0+outerRadius,0-c1,0+outerRadius,0);
		    disc.graphics.lineTo(0,0);
		    disc.graphics.lineTo(0,-innerRadius);
		    disc.graphics.curveTo(0+c1in,0-innerRadius,0+c2in,0-c2in);
		    disc.graphics.curveTo(0+innerRadius,0-c1in,0+innerRadius,0);
		    disc.graphics.lineTo(0,0);
		    disc.graphics.endFill();*/
			
			
			return disc;
		}
	}
}