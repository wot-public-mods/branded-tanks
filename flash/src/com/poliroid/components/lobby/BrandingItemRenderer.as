package poliroid.components {
	
	import flash.display.MovieClip;
	import flash.utils.ByteArray;
	import flash.events.MouseEvent;
	import flash.display.Loader;
	import flash.text.TextField;
	import flash.display.BitmapData;
	import flash.display.Bitmap;
	import flash.events.Event;
	import flash.filters.DropShadowFilter;
	import flash.filters.ColorMatrixFilter;
	import poliroid.utils.Base64;
	import scaleform.clik.constants.InvalidationType;
	import net.wg.gui.components.controls.SoundListItemRenderer;
	
	public class BrandingItemRenderer extends SoundListItemRenderer {
		
		[Embed(source="../../../res/branding/button_default.png")]
		private static var imageButtonDefault:Class;
		
		[Embed(source="../../../res/branding/button_hovered.png")]
		private static var imageButtonHovered:Class;
		
		[Embed(source="../../../res/branding/button_selected.png")]
		private static var imageButtonSelected:Class;
		
		[Embed(source="../../../res/branding/button_disabled.png")]
		private static var imageButtonDisabled:Class;
		
		[Embed(source="../../../res/branding/button_pressed.png")]
		private static var imageButtonPressed:Class;
		
		private var teamName:TextField;
		private var teamIcon:MovieClip;
		
		
		private var state_hovered:Boolean = false;
		private var state_pressed:Boolean = false;
		private var state_disabled:Boolean = false;
		private var state_selected:Boolean = false;
		public var itemID:Number = -1;
		
		private var images:Object = new Object();
		
		public function BrandingItemRenderer() {
			super();
		}
		
		override public function setData(newData:Object): void {
			if(newData == null) {
				return;
			}
			this.data = newData;
			invalidateData();
		}

		override protected function configUI(): void {
			super.configUI();
			
			this.width = 280;
			this.height = 70;
			
			this.images.button_default = new imageButtonDefault() as Bitmap;
			this.images.button_default.visible = true;
			this.addChild(this.images.button_default);
			
			this.images.button_hovered = new imageButtonHovered() as Bitmap;
			this.images.button_hovered.visible = false;
			this.addChild(this.images.button_hovered);
			
			this.images.button_selected = new imageButtonSelected() as Bitmap;
			this.images.button_selected.visible = false;
			this.addChild(this.images.button_selected);
			
			this.images.button_disabled = new imageButtonDisabled() as Bitmap;
			this.images.button_disabled.visible = false;
			this.addChild(this.images.button_disabled);
			
			this.images.button_pressed = new imageButtonPressed() as Bitmap;
			this.images.button_pressed.visible = false;
			this.addChild(this.images.button_pressed);
			
			this.teamName = new TextField();
			this.teamName.x = 85;
			this.teamName.y = 20;
			this.teamName.width = 190;
			this.teamName.height = 25;
			this.teamName.alpha = 1;
			this.addChild(this.teamName);
			
			this.teamIcon = new MovieClip();
			this.teamIcon.x = 10;
			this.teamIcon.y = 15;
			this.teamIcon.width = 50;
			this.teamIcon.height = 50;
			this.addChild(this.teamIcon);
			
			if(this.data) {
				this.setup();
			}
		}
		
		override protected function handleMousePress(event:MouseEvent): void {
			super.handleMousePress(event);
			this.state_pressed = true;
			this.updateBackGround();
		}
		
		override protected function handleMouseRelease(event:MouseEvent): void {
			super.handleMouseRelease(event);
			this.state_pressed = false;
			this.updateBackGround();
		}
		
		override protected function handleMouseRollOver(event:MouseEvent): void {
			super.handleMouseRollOver(event);
			this.state_hovered = true;
			this.updateBackGround();
		}
		
		override protected function handleMouseRollOut(event:MouseEvent): void {
			super.handleMouseRollOut(event);
			this.state_hovered = false;
			this.state_pressed = false;
			this.updateBackGround();
		}
		
		override protected function draw(): void {
			if(isInvalid(InvalidationType.DATA)) {
				this.setup();
			}			
			super.draw();
			if(!this.data) {
				this.visible = false;
			}
		}
		
		private function setup(): void {
			if (this.data) {
				
				this.itemID = this.data.id;
				this.state_disabled = this.data.disabled;
				this.state_selected = this.data.selected;
				if (!this.data.iconLoader.contentLoaderInfo.hasEventListener(Event.COMPLETE)) {
					this.data.iconLoader.contentLoaderInfo.addEventListener(Event.COMPLETE, this.onTeamIconLoaded);
				}
				
				this.teamName.htmlText = '<font size="16" color="#DDDDD0" face="$FieldFont"><b>' + this.data.name + '</b></font>';
				
				this.updateTeamIcon();
				this.updateBackGround();
			}
		}
		
		
		private function updateBackGround():void {
			this.images.button_hovered.visible = this.state_hovered && !this.state_pressed ;//&& !state_disabled;
			this.images.button_pressed.visible = this.state_pressed ;//&& !state_disabled;
			this.images.button_selected.visible = this.state_selected;// && !state_disabled;
			//this.images.button_disabled.visible = state_disabled;
		}
		
		private function updateTeamIcon(): void {
			
			var iconData:BitmapData = new BitmapData(50, 50, true, 0x0);
			iconData.draw(this.data.iconLoader);
			
			var iconHolder:MovieClip = new MovieClip();
			iconHolder.x = 15;
			iconHolder.y = 10;
			iconHolder.addChild(new Bitmap(iconData));
			iconHolder.width = 50;
			iconHolder.height = 50;
			iconHolder.filters = new Array(new DropShadowFilter(0, 0, Number('0x000000'), 0.7, 4, 4, 3, 8));
			iconHolder.alpha = 1;
			
			this.removeChild(this.teamIcon);
			this.teamIcon = iconHolder;
			this.addChild(this.teamIcon);
		}
		
		private function onTeamIconLoaded(e: Event): void { 
			this.updateTeamIcon();
		}
		
	}
}
