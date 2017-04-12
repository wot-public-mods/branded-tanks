package com.poliroid.gui.lobby.branding.data
{
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	public class BrandingOperatorSettingItemVO extends DAAPIDataClass
	{
		public var id:Number = 0;
		
		public var label:String = "";
		
		public function BrandingOperatorSettingItemVO(data:Object) 
		{
			super(data);
		}
	}
}