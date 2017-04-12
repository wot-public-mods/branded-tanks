package com.poliroid.gui.lobby.branding
{
	
	import flash.events.MouseEvent;
	import flash.utils.setTimeout;
	
	import scaleform.clik.data.DataProvider;
	
	import net.wg.gui.components.controls.SoundButton;
	import net.wg.gui.components.controls.ButtonIconNormal;
	import net.wg.gui.components.controls.DropdownMenu;
	import net.wg.gui.components.windows.Window;
	
	import com.poliroid.gui.lobby.branding.data.BrandingOperatorLocalizationVO;
	import com.poliroid.gui.lobby.branding.data.BrandingOperatorSettingsVO;
	import com.poliroid.gui.lobby.branding.interfaces.impl.BrandingOperatorMeta;
	
	public class BrandingOperator extends BrandingOperatorMeta {
		
		public var submitButton:SoundButton;
		public var showTeam1Button:ButtonIconNormal;
		public var showTeam2Button:ButtonIconNormal;
		public var swapTeamsButton:ButtonIconNormal;
		public var team1Dropdown:DropdownMenu;
		public var team2Dropdown:DropdownMenu;
		
		public function BrandingOperator() {
			super();
			canDrag = false;
			canResize = false;
			width = 300;
			height = 80;
		}
		
		override protected function configUI() : void
		{
			window.x = int(((App.appWidth / 2) - 20) * -1);
			window.y = int(((App.appHeight / 2) - 350) * -1);
			super.configUI();
		}
		
		override protected function onPopulate() : void
		{
			super.onPopulate();
			swapTeamsButton.addEventListener(MouseEvent.CLICK, onSwapBtnClick);
			submitButton.addEventListener(MouseEvent.CLICK, onSubmitBtnClick);
			showTeam1Button.addEventListener(MouseEvent.CLICK, onShowTeamClick);
			showTeam2Button.addEventListener(MouseEvent.CLICK, onShowTeamClick);
		}
		
		override protected function onDispose() : void
		{
			swapTeamsButton.removeEventListener(MouseEvent.CLICK, onSwapBtnClick);
			submitButton.removeEventListener(MouseEvent.CLICK, onSubmitBtnClick);
			showTeam1Button.removeEventListener(MouseEvent.CLICK, onShowTeamClick);
			showTeam2Button.removeEventListener(MouseEvent.CLICK, onShowTeamClick);
			super.onDispose();
		}
		
		private function onSubmitBtnClick(e:MouseEvent): void {
			
			onSettingsS(team1Dropdown.selectedIndex, team2Dropdown.selectedIndex, false);
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
		
		private function onShowTeamClick(e:MouseEvent) : void 
		{
			var presetID:Number;
			
			if (e.target == showTeam1Button) 
				presetID = team1Dropdown.selectedIndex;
			else
				presetID = team2Dropdown.selectedIndex
			
			showPresetS(presetID);
		}
		
		override protected function setLocalization(data:BrandingOperatorLocalizationVO) : void
		{
			window.title = data.windowTitle;
		}
		
		override protected function setSettings(data:BrandingOperatorSettingsVO) : void 
		{
			team1Dropdown.dataProvider = new DataProvider(data.presets);
			team2Dropdown.dataProvider = new DataProvider(data.presets);
			team1Dropdown.rowCount = team1Dropdown.dataProvider.length;
			team2Dropdown.rowCount = team1Dropdown.dataProvider.length;
			team1Dropdown.selectedIndex = data.teamFirst;
			team2Dropdown.selectedIndex = data.teamSecond;
			team1Dropdown.dataProvider.invalidate();
			team2Dropdown.dataProvider.invalidate();
		}
	}
}
