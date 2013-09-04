package com.opinion.components.preloader
{
    import flash.display.Loader;
    import flash.utils.ByteArray;
    	
	public class Logo extends Loader
	{
		
      	[Embed(source="/assets/images/berkeley-logo.png", mimeType="application/octet-stream")] public var WelcomeScreenGraphic:Class;
		
		public function Logo()
		{	
			// uncomment this and replace with a custom image
			this.loadBytes( new WelcomeScreenGraphic() as ByteArray );
		}
	}
}