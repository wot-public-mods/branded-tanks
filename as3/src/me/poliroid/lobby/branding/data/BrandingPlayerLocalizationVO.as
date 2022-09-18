package me.poliroid.lobby.branding.data
{
	
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	public class BrandingPlayerLocalizationVO extends DAAPIDataClass
	{
		
		public var windowTitle:String = "";
		
		public var headerTextAlly:String = "";
		
		public var headerTextEnemy:String = "";
		
		public var onlyMyTankLabel:String = "";
		
		public var onlyMyTankToolTip:String = "";
		
		public function BrandingPlayerLocalizationVO(data:Object) 
		{
			super(data);
		}
	}
}
