package com.poliroid.views.lobby 
{
	
	import flash.display.MovieClip;
	import flash.display.Bitmap;
	import flash.display.Loader;
	import flash.text.TextField;
	import net.wg.gui.components.controls.ScrollBar;
	import net.wg.infrastructure.base.AbstractWindowView;
	import net.wg.gui.components.controls.SoundButton;
	import net.wg.gui.components.controls.ButtonIconNormal;
	import net.wg.gui.components.controls.CheckBox;
	
	import scaleform.clik.controls.ScrollingList;
	import poliroid.utils.Base64;
	
	import flash.events.MouseEvent;
	import flash.events.Event;
	import net.wg.gui.components.advanced.FieldSet;
	import scaleform.clik.data.DataProvider;
	import scaleform.clik.events.ListEvent;
	import flash.utils.setTimeout;
	
	import poliroid.components.BrandingItemRenderer;
	
	public class BrandingPlayer extends AbstractWindowView {
		
		
		public var py_onSettings:Function;
		public var py_onShowPreset:Function;
		public var py_onFinish:Function;
		public var debugLogS:Function;
		
		public var backgroundMC:MovieClip;
		
		private var scrollBar:ScrollBar;
		private var commandList:ScrollingList;
		private var headerText:TextField;
		private var bottomText:TextField;
		private var onlyOnMyTank:CheckBox;
		private var nextSteep:SoundButton;
		
		private var teamp_1:Number = -1;
		private var teamp_2:Number = -1;
		
		public function BrandingPlayer() {
			super();
			this.canDrag = true;
			this.canResize = false;
			this.isCentered = true;
			this.canClose = true;
			this.width = 282;
			this.height = 470;
		}
		
		public function as_syncData(data:Array, onlyMyTank:Boolean = false): void {
			
			if (window) {
				window.title = "Branded tanks"; 
			}
		
			headerText.text = 'Chose your team';
			backgroundMC.gotoAndStop('ally');
		
			for (var i:int = 0; i < data.length; i++) {
				var item:Object = data[i];
				var iconLoader:Loader = new Loader();
				iconLoader.loadBytes(Base64.decodeToByteArray(item.icon));
				data[i].iconLoader = iconLoader;
				data[i].selected = false;
				data[i].disabled = false;
			}
			
			
			try {
				
				
				
				
				
				this.scrollBar = App.utils.classFactory.getComponent("ScrollBar", ScrollBar);
				this.scrollBar.y = 73;
				this.scrollBar.x = 265;
				this.scrollBar.height = 344;
				
				this.commandList = App.utils.classFactory.getComponent("ScrollingList", ScrollingList);
				this.commandList.width = 280;
				this.commandList.margin = 0;
				this.commandList.rowHeight = 70;
				this.commandList.rowCount = 5;
				this.commandList.wrapping = "normal";
				this.commandList.x = 1;
				this.commandList.y = 70;
				this.commandList.itemRenderer = BrandingItemRenderer;
				this.commandList.itemRendererInstanceName = "";
				this.commandList.dataProvider = new DataProvider(data);
				this.commandList.scrollBar = this.scrollBar;
				this.commandList.validateNow();
				this.commandList.addEventListener(ListEvent.ITEM_CLICK, this.handleTeamClick);
				
				
				this.onlyOnMyTank = CheckBox(App.utils.classFactory.getComponent("CheckBox", CheckBox));
				this.onlyOnMyTank.label = "Process only my vehicle";
				this.onlyOnMyTank.selected = false;
				this.onlyOnMyTank.x = 15;
				this.onlyOnMyTank.y = 435;
				this.onlyOnMyTank.selected = onlyMyTank;
				this.onlyOnMyTank.width = 200;
				this.onlyOnMyTank.toolTip = "{HEADER}Visible only on my tank{/HEADER}{BODY}If selected, branding will accepted only for your vehicle<br>All others vehicles will be cleared to default state{/BODY}";
				this.onlyOnMyTank.infoIcoType = "info";
				this.onlyOnMyTank.addEventListener(Event.SELECT, this.handleCheackBoxClick);
				
				
				
				this.addChild(this.commandList);
				this.addChild(this.scrollBar);
				this.addChild(this.onlyOnMyTank);
				
			} catch(err: Error) {
				this.debugLogS("as_syncData:ERROR \n" + err.getStackTrace());
			}
			
			
		}
		
		private function handleTeamClick(event:ListEvent):void {
			
			var target:BrandingItemRenderer = event.itemRenderer as BrandingItemRenderer;
			var target_id:Number = target.itemID 
			var data:Array = new Array();
			
			for (var i:int = 0; i < this.commandList.dataProvider.length; i++) {
				var item:Object = this.commandList.dataProvider[i];
				if (item.id != target_id) {
					item.selected = false;
					item.disabled = true;
					data.push(item);
				} else {
					
					if (this.allyBG.visible) { 
						this.teamp_1 = item.id ;
					} else {
						this.teamp_2 = item.id ;
					}
					
				}
				
			}
			
			this.commandList.dataProvider = new DataProvider(data);
			this.commandList.dataProvider.invalidate();
			/*
			if (this.enemyBG.visible || this.onlyOnMyTank.selected) {
				this.py_onFinish([this.teamp_1, this.teamp_2, this.onlyOnMyTank.selected]);
			}
			*/
			
			
			backgroundMC.gotoAndStop('enemy');
			headerText.text = 'Chose enemys team';
		}
		
		private function handleCheackBoxClick(event:Event):void {
			/*if (this.onlyOnMyTank.selected && this.teamp_1 != -1) {
				this.py_onFinish([this.teamp_1, this.teamp_2, this.onlyOnMyTank.selected]);
			}*/
		}
		
	}
}
