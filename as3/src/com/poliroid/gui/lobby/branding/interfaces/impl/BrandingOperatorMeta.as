package com.poliroid.gui.lobby.branding.interfaces.impl
{
	
	import net.wg.data.constants.Errors;
	import net.wg.infrastructure.base.AbstractWindowView;
	import net.wg.infrastructure.exceptions.AbstractException;
	
	import com.poliroid.gui.lobby.branding.data.BrandingOperatorLocalizationVO;
	import com.poliroid.gui.lobby.branding.data.BrandingOperatorSettingsVO;
	
	public class BrandingOperatorMeta extends AbstractWindowView 
	{
		
		public var onSettings:Function;
		
		public var showPreset:Function;
		
		public function BrandingOperatorMeta() 
		{
			super();
		}
		
		public function onSettingsS(team1:Number, team2:Number, onlyOnMyTank:Boolean) : void
		{
			App.utils.asserter.assertNotNull(onSettings, "onSettings" + Errors.CANT_NULL);
			onSettings(team1, team2, onlyOnMyTank);
		}
		
		public function showPresetS(teamIndex:Number) : void
		{
			App.utils.asserter.assertNotNull(showPreset, "showPreset" + Errors.CANT_NULL);
			showPreset(teamIndex);
		}
		
		public final function as_setLocalization(ctx:Object) : void
		{
			var data:BrandingOperatorLocalizationVO = new BrandingOperatorLocalizationVO(ctx);
			setLocalization(data);
			if(data)
				data.dispose();
		}
		
		public final function as_setSettings(ctx:Object) : void
		{
			var data:BrandingOperatorSettingsVO = new BrandingOperatorSettingsVO(ctx);
			setSettings(data);
			if(data)
				data.dispose();
		}
		
		protected function setLocalization(data:BrandingOperatorLocalizationVO) : void
		{
			var message:String = "as_setLocalization" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message, data);
			throw new AbstractException(message);
		}
		
		protected function setSettings(data:BrandingOperatorSettingsVO) : void
		{
			var message:String = "as_setSettings" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message, data);
			throw new AbstractException(message);
		}
	}
}
