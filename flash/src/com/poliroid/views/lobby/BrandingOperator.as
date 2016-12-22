package com.poliroid.views.lobby 
{
	
	import net.wg.infrastructure.base.AbstractWindowView;
	import net.wg.gui.components.controls.SoundButton;
	import net.wg.gui.components.controls.ButtonIconNormal;
	import net.wg.gui.components.controls.DropdownMenu;
	import net.wg.gui.components.windows.Window;
	import flash.events.MouseEvent;
	import scaleform.clik.data.DataProvider;
	import flash.utils.setTimeout;
	
	public class BrandingOperator extends AbstractWindowView {
		
		public var submitButton:SoundButton;
		public var showTeam1Button:ButtonIconNormal;
		public var showTeam2Button:ButtonIconNormal;
		public var swapTeamsButton:ButtonIconNormal;
		public var team1Dropdown:DropdownMenu;
		public var team2Dropdown:DropdownMenu;
		
		public var onSettingsS:Function;
		public var onShowPresetS:Function;
		
		public function BrandingOperator() {
			super();
			canDrag = false;
			canResize = false;
			width = 300;
			height = 80;
		}
		
		override protected function configUI() : void
		{
			window.title = "Branded tanks";
			window.x = int(((App.appWidth / 2) - 20) * -1);
			window.y = int(((App.appHeight / 2) - 350) * -1);
			super.configUI();
		}
		
		override protected function onPopulate() : void
		{
			swapTeamsButton.addEventListener(MouseEvent.CLICK, onSwapBtnClick);
			submitButton.addEventListener(MouseEvent.CLICK, onSubmitBtnClick);
			showTeam1Button.addEventListener(MouseEvent.CLICK, onShowTeam1BtnClick);
			showTeam2Button.addEventListener(MouseEvent.CLICK, onShowTeam2BtnClick);
			super.onPopulate();
		}
		
		override protected function onDispose() : void
		{
			swapTeamsButton.removeEventListener(MouseEvent.CLICK, onSwapBtnClick);
			submitButton.removeEventListener(MouseEvent.CLICK, onSubmitBtnClick);
			showTeam1Button.removeEventListener(MouseEvent.CLICK, onShowTeam1BtnClick);
			showTeam2Button.removeEventListener(MouseEvent.CLICK, onShowTeam2BtnClick);
			super.onDispose();
		}
		
		public function as_syncData(settings:Array): void {
			
			var presets:Array = new Array();
			var iter:Number = 0;
			for each (var teamName:String in settings[1]) {
				presets.push( { label: String(teamName), data: Number(iter) } );
				iter = iter + 1;
			}
			
			team1Dropdown.rowCount = presets.length;
			team1Dropdown.dataProvider = new DataProvider(presets);
			team1Dropdown.selectedIndex = settings[0][0];
			
			team2Dropdown.rowCount = presets.length;
			team2Dropdown.dataProvider = new DataProvider(presets);
			team2Dropdown.selectedIndex = settings[0][1];
		}
		
		private function onSubmitBtnClick(e:MouseEvent): void {
			
			onSettingsS(team1Dropdown.selectedIndex, team2Dropdown.selectedIndex);
			guiAvailability(false);
			setTimeout(guiAvailability, 300, true);
		}
		
		private function guiAvailability(isAvaileble:Boolean) : void
		{
			swapTeamsButton.enabled = isAvaileble;
			team1Dropdown.enabled = isAvaileble;
			team2Dropdown.enabled = isAvaileble;
			submitButton.enabled = isAvaileble;
			showTeam1Button.enabled = isAvaileble;
			showTeam2Button.enabled = isAvaileble;
		}
		
		private function onSwapBtnClick(e:MouseEvent) : void 
		{
			var _team2:Number = team1Dropdown.selectedIndex;
			var _team1:Number = team2Dropdown.selectedIndex;
			team1Dropdown.selectedIndex = _team1;
			team2Dropdown.selectedIndex = _team2;
		}
		
		private function onShowTeam1BtnClick(e:MouseEvent) : void 
		{
			onShowPresetS(team1Dropdown.selectedIndex);
		}
		
		private function onShowTeam2BtnClick(e:MouseEvent) : void 
		{
			onShowPresetS(team2Dropdown.selectedIndex);
		}
	}
}
