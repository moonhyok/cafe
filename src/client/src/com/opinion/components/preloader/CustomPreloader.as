package com.opinion.components.preloader
{
    import flash.events.ProgressEvent;
    import flash.text.Font;
    import flash.text.TextField;
    import flash.text.TextFormat;
    import flash.geom.Rectangle;
    import mx.graphics.RoundedRectangle;
    import com.opinion.settings.Configuration;
	import mx.core.Application;
    
    import mx.preloaders.*;
    
    public class CustomPreloader extends DownloadProgressBar
    {
    	//[Embed(source='/assets/fonts/helvetica/HelveticaNeueCondensedBold.ttf', fontFamily='Helvetica', fontWeight='bold')] public var Helvetica:Class;
    	public var text:TextField;
    	public var welcome:TextField;
    	
        public function CustomPreloader()
        {   
            super();
			
            // Set the download label.
            downloadingLabel="Launching...";
            // Set the initialization label.
            initializingLabel="Launching...";
            // Set the minimum display time to 3 seconds.
            MINIMUM_DISPLAY_TIME=7000;
						            
            this.showLabel = true; 
        }
        
		override protected function get barFrameRect():RoundedRectangle
		{
			return new RoundedRectangle(14, 40, 200, 4);
		}
		
		override protected function get barRect():RoundedRectangle
		{
			return new RoundedRectangle(14, 39, 200, 6, 0);
		}
		
		override protected function get borderRect():RoundedRectangle
		{
			return new RoundedRectangle(0, 0, 228, 60, 4);
		}      
        
        // Make the label text field larger
        override protected function get labelRect():Rectangle
		{
			return new Rectangle(14, 17, 200, 25);
		}

		// Set our own label format        
        override protected function get labelFormat():TextFormat
		{
//            var helvetica:Font = new Helvetica();
            var txtFormat:TextFormat = new TextFormat();
            txtFormat.color = 0x646462;
  //          txtFormat.font = helvetica.fontName;
            txtFormat.size = 14;
            txtFormat.bold = true; 
            return txtFormat;	
		}
        
        // Override to return true so progress bar appears
        // during initialization.       
        override protected function showDisplayForInit(elapsedTime:int, 
            count:int):Boolean {
			// Draw the instructional text - unused but keep here in case you need to add text
			var helvetica:Font = new Configuration.Helvetica();
			var txtFormat:TextFormat = new TextFormat();
			txtFormat.color = 0x000000;
			txtFormat.font = helvetica.fontName;
			txtFormat.size = 18;
			txtFormat.align = "center";
			text = new TextField();
			text.wordWrap = true;
			text.width = 400;
			text.height = 150;
			text.text = Configuration.WELCOME_PAGE_DEFAULT_TEXT;
			text.embedFonts = true;               
			text.setTextFormat(txtFormat);
			text.x = this.stage.stageWidth/2  - 200;
			text.y =150;
			this.addChild(text);
            return true;
        }

        // Override to return true so progress bar appears during download.     
        override protected function showDisplayForDownloading(
            elapsedTime:int, event:ProgressEvent):Boolean {
			
			var wcs:WelcomeScreen = new WelcomeScreen();
			// Hard code in the dimensions of the i-frame and picture
			wcs.x = this.stage.stageWidth/2-321;
			wcs.y = 70;
			this.addChild(wcs);
			
			// Draw the instructional text - unused but keep here in case you need to add text
			var helvetica:Font = new Configuration.Helvetica();
			var txtFormat:TextFormat = new TextFormat();
			txtFormat.color = 0x000000;
			txtFormat.font = helvetica.fontName;
			txtFormat.size = 24;
			txtFormat.align = "center";
			text = new TextField();
			text.wordWrap = true;
			text.width = 500;
			text.height = 150;
			text.text = Configuration.WELCOME_PAGE_DEFAULT_TEXT;
			text.embedFonts = true;               
			text.setTextFormat(txtFormat);
			text.x = this.stage.stageWidth/2  - 250;
			text.y =30;
			
			var bl:Logo = new Logo();
			// Hard code in the dimensions of the i-frame and picture
			bl.x = this.stage.stageWidth/2-119;
			bl.y = this.stage.stageHeight-200;
			this.addChild(bl);
			
			this.addChild(text);
                return true;
        }

    }
}