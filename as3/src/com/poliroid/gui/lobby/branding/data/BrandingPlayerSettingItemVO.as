package com.poliroid.gui.lobby.branding.data
{
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	public class BrandingPlayerSettingItemVO extends DAAPIDataClass
	{
		public var id:Number = 0;
		
		public var name:String = "";
		
		public var icon:String = "";
		
		public function BrandingPlayerSettingItemVO(data:Object) 
		{
			super(data);
		}
	}
}