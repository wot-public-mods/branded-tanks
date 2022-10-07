package me.poliroid.brandedTanks.data
{
	import net.wg.data.daapi.base.DAAPIDataClass;

	public class BrandingPlayerSettingItemVO extends DAAPIDataClass
	{
		public var id:Number = 0;

		public var presetID:Number = 0;

		public var name:String = "";

		public var icon:String = "";

		public var preview:Boolean = false;

		public function BrandingPlayerSettingItemVO(data:Object) 
		{
			super(data);
		}
	}
}