package com.poliroid.views.lobby 
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
	import net.wg.infrastructure.base.AbstractWindowView;
	
	import com.poliroid.components.lobby.BrandingItemRenderer;
	
	public class BrandingPlayer extends AbstractWindowView {
		
		public var finishSetupS:Function;
		public var onShowPresetS:Function;
		
		public var backgroundMC:MovieClip;
		public var headerText:TextField;
		public var scrollBar:ScrollBar;
		public var commandList:ScrollingList;
		public var onlyOnMyTank:CheckBox;
		
		private var allyTeamID:Number = -1;
		private var enemyTeamID:Number = -1;
		
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
		
		public function as_syncData(data:Array, onlyMyTank:Boolean = false) : void 
		{
		
			window.title = "Branded tanks"; 
			
			headerText.text = 'Chose your team';
			backgroundMC.gotoAndStop('ally');
			
			commandList.dataProvider = new DataProvider(data);
			commandList.dataProvider.invalidate();
			
			onlyOnMyTank.label = "Process only my vehicle";
			onlyOnMyTank.selected = onlyMyTank;
			onlyOnMyTank.toolTip = "{HEADER}Visible only on my tank{/HEADER}{BODY}If selected, branding will accepted only for your vehicle<br>All others vehicles will be cleared to default state{/BODY}";
		}
		
		private function handleTeamClick(event:ListEvent) : void 
		{
			
			var target:BrandingItemRenderer = event.itemRenderer as BrandingItemRenderer;
			var data:Array = new Array();
			
			for (var i:int = 0; i < this.commandList.dataProvider.length; i++) 
			{
				
				var item:Object = this.commandList.dataProvider[i];
				
				if (item.id != target.itemID) 
				{
					data.push(item);
				} 
				else 
				{		
					if (allyTeamID == -1)
						allyTeamID = item.id ;
					else
						enemyTeamID = item.id ;
				}
				
			}
			
			if (enemyTeamID != -1 || onlyOnMyTank.selected) 
			{
				finishSetupS(allyTeamID, enemyTeamID, onlyOnMyTank.selected);
			}
			
			backgroundMC.gotoAndStop('enemy');
			headerText.text = 'Chose enemys team';
			commandList.dataProvider = new DataProvider(data);
			commandList.dataProvider.invalidate();
		}
		
		private function handleCheackBoxClick(event:Event) : void 
		{
			if (onlyOnMyTank.selected && allyTeamID != -1) 
			{
				finishSetupS(allyTeamID, enemyTeamID, onlyOnMyTank.selected);
			}
		}
		
	}
}
