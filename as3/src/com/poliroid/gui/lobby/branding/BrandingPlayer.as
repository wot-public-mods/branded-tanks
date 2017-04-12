package com.poliroid.gui.lobby.branding
{
	
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.text.TextField;
	
	import scaleform.clik.controls.ScrollingList;
	import scaleform.clik.data.DataProvider;
	import scaleform.clik.events.ListEvent;
	
	
	import net.wg.gui.components.controls.CheckBox;
	import net.wg.gui.components.advanced.FieldSet;
	import net.wg.gui.components.controls.ScrollBar;
	
	import com.poliroid.gui.lobby.branding.controls.BrandingItemRenderer;
	import com.poliroid.gui.lobby.branding.data.BrandingPlayerSettingsVO;
	import com.poliroid.gui.lobby.branding.data.BrandingPlayerSettingItemVO;
	import com.poliroid.gui.lobby.branding.data.BrandingPlayerLocalizationVO;
	import com.poliroid.gui.lobby.branding.interfaces.impl.BrandingPlayerMeta;
	
	public class BrandingPlayer extends BrandingPlayerMeta 
	{
		
		public var backgroundMC:MovieClip = null;
		
		public var headerText:TextField = null;
		
		public var scrollBar:ScrollBar = null;
		
		public var commandList:ScrollingList = null;
		
		public var onlyOnMyTank:CheckBox = null;
		
		private var allyTeamID:Number = -1;
		
		private var enemyTeamID:Number = -1;
		
		private var headerTextEnemyLabel:String = "";
		
		public function BrandingPlayer() 
		{
			super();
		}
		
		override protected function configUI(): void
		{
			super.configUI();
			commandList.addEventListener(ListEvent.ITEM_CLICK, handleTeamClick);
			onlyOnMyTank.addEventListener(Event.SELECT, handleCheackBoxClick);
		}
		
		override protected function onDispose() : void
		{
			commandList.removeEventListener(ListEvent.ITEM_CLICK, handleTeamClick);
			onlyOnMyTank.removeEventListener(Event.SELECT, handleCheackBoxClick);
			super.onDispose();
		}
		
		private function handleTeamClick(event:ListEvent) : void 
		{
			
			var target:BrandingItemRenderer = event.itemRenderer as BrandingItemRenderer;
			var data:Array = new Array();
			
			for (var i:int = 0; i < commandList.dataProvider.length; i++) 
			{
				
				var item:BrandingPlayerSettingItemVO = commandList.dataProvider[i];
				
				if (item.id == target.itemID) 
				{
					if (allyTeamID == -1)
					{
						allyTeamID = item.id;
					}	
					else
					{
						enemyTeamID = item.id;
					}
				} 
				else 
				{		
					data.push(item);
				}
				
			}
			
			if (enemyTeamID != -1 || onlyOnMyTank.selected) 
			{
				onSettingsS(allyTeamID, enemyTeamID, onlyOnMyTank.selected);
				return;
			}
			
			backgroundMC.gotoAndStop('enemy');
			headerText.text = headerTextEnemyLabel;
			commandList.dataProvider = new DataProvider(data);
			commandList.dataProvider.invalidate();
		}
		
		private function handleCheackBoxClick(event:Event) : void 
		{
			if (onlyOnMyTank.selected && allyTeamID != -1) 
			{
				onSettingsS(allyTeamID, enemyTeamID, onlyOnMyTank.selected);
			}
		}
		
		
		
		override protected function setLocalization(data:BrandingPlayerLocalizationVO) : void
		{
			window.title = data.windowTitle;
			headerText.text = data.headerTextAlly;
			headerTextEnemyLabel = data.headerTextEnemy;
			onlyOnMyTank.label = data.onlyMyTankLabel;
			onlyOnMyTank.toolTip = data.onlyMyTankToolTip;
		}
		
		override protected function setSettings(data:BrandingPlayerSettingsVO) : void 
		{
			commandList.dataProvider = new DataProvider(data.presets);
			commandList.dataProvider.invalidate();
			onlyOnMyTank.selected = data.onlyOnMyTank;
		}
	}
}
