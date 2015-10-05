package  {
	
	import net.wg.infrastructure.base.AbstractWindowView;
	import net.wg.gui.components.controls.SoundButton;
	import net.wg.gui.components.controls.ButtonIconNormal;
	import net.wg.gui.components.controls.DropdownMenu;
	import net.wg.gui.components.controls.CheckBox;
	import flash.events.MouseEvent;
	import flash.events.Event;
	import net.wg.gui.components.advanced.FieldSet;
	import scaleform.clik.data.DataProvider;
	import scaleform.clik.events.ListEvent;
	
	public class brandingUI extends AbstractWindowView {
		
		private var submitBtn:SoundButton;
		private var showTeam1:ButtonIconNormal;
		private var showTeam2:ButtonIconNormal;
		private var swapBtn:ButtonIconNormal;
		
		private var team1:DropdownMenu;
		private var team2:DropdownMenu;
		
		public var py_onSettings:Function;
		public var py_onShowPreset:Function;
		
		public function brandingUI() {
			super();
			this.canDrag = true;
			this.canResize = false;
			this.isCentered = true;
			this.canClose = true;
			this.width = 275;
			this.height = 75;
		}
		
		public function as_syncData(settings:Array): void {
			
			if (window) {
				window.title = "Брендированные танки"; 
			}
			
			this.swapBtn = App.utils.classFactory.getComponent("ButtonIconNormalUI", ButtonIconNormal);
			this.swapBtn.width = 25;
			this.swapBtn.iconSource = "../maps/icons/buttons/swap.png";
			this.swapBtn.x = 125;
			this.swapBtn.y = 12;
			this.swapBtn.addEventListener(MouseEvent.CLICK, this.onSwapBtnClick, false, 0, true);
			this.addChild(this.swapBtn);
			
			
			this.team1 = App.utils.classFactory.getComponent("DropdownMenu", DropdownMenu);
			this.team1.itemRenderer = "DropDownListItemRendererSound";
			this.team1.dropdown = "DropdownMenu_ScrollingList";
			this.team1.menuDirection = "down";
			this.team1.menuMargin = 1;
			this.team1.menuRowsFixed = false;
			this.team1.menuWrapping = "normal";
			this.team1.scrollBar = "";
			this.team1.showEmptyItems = false;
			this.team1.x = 10;
			this.team1.y = 10;
			this.team1.width = 105;
			this.team1.menuWidth = -1;
			this.team1.menuRowsFixed = true;
			this.team1.soundId = "";
			this.team1.soundType = "dropDownMenu";
			this.team1.autoSize = "none";
			this.team1.enabled = true;
			this.team1.enableInitCallback = false;
			this.team1.focusable = true;
			this.addChild(this.team1);
			this.team1.validateNow();
			this.team1.addEventListener(ListEvent.INDEX_CHANGE, this.onSettinsChange);
			
			
			this.team2 = App.utils.classFactory.getComponent("DropdownMenu", DropdownMenu);
			this.team2.itemRenderer = "DropDownListItemRendererSound";
			this.team2.dropdown = "DropdownMenu_ScrollingList";
			this.team2.menuDirection = "down";
			this.team2.menuMargin = 1;
			this.team2.menuRowsFixed = false;
			this.team2.menuWrapping = "normal";
			this.team2.scrollBar = "";
			this.team2.showEmptyItems = false;
			this.team2.x = 160;
			this.team2.y = 10;
			this.team2.width = 105;
			this.team2.menuWidth = -1;
			this.team2.menuRowsFixed = true;
			this.team2.soundId = "";
			this.team2.soundType = "dropDownMenu";
			this.team2.autoSize = "none";
			this.team2.enabled = true;
			this.team2.enableInitCallback = false;
			this.team2.focusable = true;
			this.addChild(this.team2);
			this.team2.validateNow();
			this.team2.addEventListener(ListEvent.INDEX_CHANGE, this.onSettinsChange);
			
			var presets:Array = new Array();
			var iter:Number = 0;
			for each (var teamName:String in settings[1]) {
				presets.push( { label: String(teamName), data: Number(iter) } );
				iter = iter + 1;
			}
			
			this.team1.rowCount = presets.length;
			this.team2.rowCount = presets.length;
			
			this.team1.dataProvider = new DataProvider(presets);
			this.team2.dataProvider = new DataProvider(presets);
			
			this.team1.selectedIndex = settings[0][0];
			this.team2.selectedIndex = settings[0][1];
			
			
			
			
			this.submitBtn = App.utils.classFactory.getComponent("ButtonNormal", SoundButton);
			this.submitBtn.width = 155;
			this.submitBtn.x = 60;
			this.submitBtn.y = 45;
			this.submitBtn.label = "Применить";
			this.submitBtn.addEventListener(MouseEvent.CLICK, this.onSubmitBtnClick, false, 0, true);
			this.addChild(this.submitBtn);
			
			
			this.showTeam1 = App.utils.classFactory.getComponent("ButtonIconNormalUI", ButtonIconNormal);
			this.showTeam1.width = 35;
			this.showTeam1.iconSource = "../maps/icons/buttons/Tank-ico.png";
			this.showTeam1.x = 15;
			this.showTeam1.y = 45;
			this.showTeam1.addEventListener(MouseEvent.CLICK, this.onShowTeam1BtnClick, false, 0, true);
			this.addChild(this.showTeam1);
			
			this.showTeam2 = App.utils.classFactory.getComponent("ButtonIconNormalUI", ButtonIconNormal);
			this.showTeam2.width = 35;
			this.showTeam2.iconSource = "../maps/icons/buttons/Tank-ico.png";
			this.showTeam2.x = 225;
			this.showTeam2.y = 45;
			this.showTeam2.addEventListener(MouseEvent.CLICK, this.onShowTeam2BtnClick, false, 0, true);
			this.addChild(this.showTeam2);
		}
		
		
		private function onSubmitBtnClick(param1:MouseEvent): void {
			this.py_onSettings([this.team1.selectedIndex, this.team2.selectedIndex]);
			this.handleWindowClose();
		}
		
		private function onSwapBtnClick(param1:MouseEvent): void {
			var _team2:Number = this.team1.selectedIndex;
			var _team1:Number = this.team2.selectedIndex;
			this.team1.selectedIndex = _team1;
			this.team2.selectedIndex = _team2;
			this.py_onSettings([this.team1.selectedIndex, this.team2.selectedIndex]);
		}
		
		private function onSettinsChange(e:Event): void {
			//this.py_onSettings([this.team1.selectedIndex, this.team2.selectedIndex]);
		}
		
		private function onShowTeam1BtnClick(e:Event): void {
			this.py_onShowPreset(this.team1.selectedIndex);
		}
		
		private function onShowTeam2BtnClick(e:Event): void {
			this.py_onShowPreset(this.team2.selectedIndex);
		}
	}
}
