package me.poliroid.lobby.branding.events
{
	
	import flash.events.Event;
	
	public class BrandingEvent extends Event
	{

		public static const PREVIEW_PRESET:String = "branding_preview_preset";

		public function BrandingEvent(type:String, bubbles:Boolean = true, cancelable:Boolean = false)
		{
			super(type, bubbles, cancelable);
		}
		
		override public function clone() : Event
		{
			return new BrandingEvent(type, bubbles, cancelable);
		}
	}
}
