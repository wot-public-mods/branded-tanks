package me.poliroid.brandedTanks.controls
{
	import flash.text.TextField;
	import flash.events.MouseEvent;
	import flash.display.MovieClip;

	import scaleform.clik.constants.InvalidationType;

	import net.wg.gui.components.controls.Image;
	import net.wg.gui.components.controls.SoundListItemRenderer;

	import me.poliroid.brandedTanks.events.BrandingEvent;
	import me.poliroid.brandedTanks.data.BrandingPlayerSettingItemVO;

	public class BrandingItemRenderer extends SoundListItemRenderer
	{
		public var teamIconMC:Image = null;
		public var teamNameTF:TextField = null;
		public var previewIcon:MovieClip = null;

		public var itemID:Number = -1;
		public var model:BrandingPlayerSettingItemVO = null;

		override protected function configUI() : void 
		{
			super.configUI();
			setup();
		}

		override protected function handleMouseRelease(param1:MouseEvent) : void
		{
			if (model.preview && isOverIcon(param1.localX, param1.localY))
				return
			super.handleMouseRelease(param1);
		}

		override protected function handleMousePress(param1:MouseEvent) : void
		{
			if (model.preview && isOverIcon(param1.localX, param1.localY))
				dispatchEvent(new BrandingEvent(BrandingEvent.PREVIEW_PRESET));
			else
				super.handleMousePress(param1);
		}

		private function isOverIcon(locX:Number, locY:Number) : Boolean
		{
			if (locX < previewIcon.x || locX > previewIcon.x + previewIcon.width)
				return false;
			if (locY < previewIcon.y || locY > previewIcon.y + previewIcon.height)
				return false;
			return true;
		}

		override public function setData(param1:Object) : void
		{
			if (param1 == null) 
			{
				visible = false;
				return;
			}
			super.setData(param1);
			model = BrandingPlayerSettingItemVO(data);
			invalidateData();
		}

		override protected function onDispose(): void
		{
			teamIconMC = null;
			teamNameTF = null;
			super.onDispose();
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
			visible = true;
			itemID = model.id;
			teamNameTF.text = model.name;
			teamIconMC.visible = false;
			previewIcon.visible = model.preview;
			if (data.icon)
			{
				teamIconMC.source = "../../" + model.icon;
				teamIconMC.visible = true;
			}
		}
	}
}
