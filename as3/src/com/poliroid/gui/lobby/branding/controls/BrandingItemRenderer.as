package com.poliroid.gui.lobby.branding.controls
{

	import flash.display.MovieClip;
	import flash.display.Loader;
	import flash.text.TextField;
	import flash.events.Event;
	import flash.net.URLRequest;
	
	import scaleform.clik.constants.InvalidationType;
	
	import net.wg.gui.components.controls.Image;
	import net.wg.gui.components.controls.SoundListItemRenderer;
	
	import com.poliroid.gui.lobby.branding.data.BrandingPlayerSettingItemVO;
	
	public class BrandingItemRenderer extends SoundListItemRenderer {
		
		public var teamIconMC:Image = null;
		public var teamNameTF: TextField = null;
		public var itemID:Number = -1;
		public var model:BrandingPlayerSettingItemVO = null;
		
		public function BrandingItemRenderer() 
		{
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
		
		override public function setData(data:Object) : void 
		{
			
			if (data == null) 
				return;
			
			super.setData(data);
			model = BrandingPlayerSettingItemVO(data);
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
			
			itemID = model.id;
			teamNameTF.text = model.name;
			
			teamIconMC.visible = false;
			if (data.icon) {
				teamIconMC.source = "../../" + model.icon;
				teamIconMC.visible = true;
			}
		}
	}
}
