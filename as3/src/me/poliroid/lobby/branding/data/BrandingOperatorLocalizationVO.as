package me.poliroid.lobby.branding.data
{
	
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	public class BrandingOperatorLocalizationVO extends DAAPIDataClass
	{
		
		public var windowTitle:String = "";
		
		public function BrandingOperatorLocalizationVO(data:Object) 
		{
			super(data);
		}
	}
}
