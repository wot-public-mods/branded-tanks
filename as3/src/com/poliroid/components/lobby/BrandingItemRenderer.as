package com.poliroid.components.lobby {
	
	import flash.display.MovieClip;
	import flash.display.Loader;
	import flash.text.TextField;
	import flash.events.Event;
	import flash.net.URLRequest;
	
	import scaleform.clik.constants.InvalidationType;
	import net.wg.gui.components.controls.SoundListItemRenderer;
	import net.wg.gui.components.controls.Image;
	
	public class BrandingItemRenderer extends SoundListItemRenderer {
		
		public var teamIconMC:Image = null;
		public var teamNameTF: TextField = null;
		public var itemID:Number = -1;
		
		public function BrandingItemRenderer() {
			super();
		}
		
		override protected function configUI() : void 
		{
			super.configUI();
			if (data) 
				setup();
		}
		
		override protected function onDispose(): void
		{
			teamIconMC = null;
			teamNameTF = null;
			super.onDispose();
		}
		
		override public function setData(newData:Object) : void 
		{
			if (newData == null) 
				return;
			data = newData;
			invalidateData();
		}
		
		override protected function draw() : void 
		{
		
			if (isInvalid(InvalidationType.DATA)) 
				setup(); 	
			
			if (!data)
				visible = false;
				
			super.draw();
		}
		
		private function setup() : void 
		{
			if (!data)
				return;
			
			itemID = data.id;
			teamNameTF.text = data.name;
			
			teamIconMC.visible = false;
			if (data.icon) {
				teamIconMC.source = "../../" + data.icon;
				teamIconMC.visible = true;
			}
		}
	}
}
