package me.poliroid.brandedTanks.data
{
	
	import net.wg.infrastructure.interfaces.entity.IDisposable;
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	import me.poliroid.brandedTanks.data.BrandingPlayerSettingItemVO;
	
	public class BrandingPlayerSettingsVO extends DAAPIDataClass
	{
		
		private static const PRESETS_FIELD_NAME:String = "presets";
		
		public var presets:Array = null;
		
		public var onlyOnMyTank:Boolean = false;
		
		public function BrandingPlayerSettingsVO(data:Object)
		{
			super(data);
		}
		
		override protected function onDataWrite(name:String, data:Object) : Boolean
		{
			if(name == PRESETS_FIELD_NAME)
			{
				var settingsItem:Object = null;
				var settingsItemItems:Array = data as Array;
				
				presets = [];
				
				for each(settingsItem in settingsItemItems)
				{
					presets.push(new BrandingPlayerSettingItemVO(settingsItem));
				}
				return false;
			}
			
			return super.onDataWrite(name, data);
		}
		
		override protected function onDispose() : void
		{
			var disposable:IDisposable = null;
			
			if(presets != null)
			{
				for each(disposable in presets)
				{
					disposable.dispose();
				}
				presets.splice(0, presets.length);
				presets = null;
			}
			
			super.onDispose();
		}
	}

}