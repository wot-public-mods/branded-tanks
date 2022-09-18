package me.poliroid.lobby.branding.data
{
	
	import net.wg.infrastructure.interfaces.entity.IDisposable;
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	import me.poliroid.lobby.branding.data.BrandingOperatorSettingItemVO;
	
	public class BrandingOperatorSettingsVO extends DAAPIDataClass
	{
		
		private static const PRESETS_FIELD_NAME:String = "presets";
		
		public var presets:Array = null;
		
		public var teamFirst:Number = 0;
		
		public var teamSecond:Number = 0;
		
		public function BrandingOperatorSettingsVO(data:Object)
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
					presets.push(new BrandingOperatorSettingItemVO(settingsItem));
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