package com.opinion.components.preloader
{
    import flash.display.Loader;
    import flash.utils.ByteArray;
    	
	public class WelcomeScreen extends Loader
	{
		
      	[Embed(source="/assets/images/preloader.jpg", mimeType="application/octet-stream")] public var WelcomeScreenGraphic:Class;
		
		public function WelcomeScreen()
		{	
			// uncomment this and replace with a custom image
			this.loadBytes( new WelcomeScreenGraphic() as ByteArray );
		}
	}
}