﻿package me.poliroid.brandedTanks.interfaces.impl
{
	
	import net.wg.data.constants.Errors;
	import net.wg.infrastructure.base.AbstractWindowView;
	import net.wg.infrastructure.exceptions.AbstractException;
	
	import me.poliroid.brandedTanks.data.BrandingPlayerLocalizationVO;
	import me.poliroid.brandedTanks.data.BrandingPlayerSettingsVO;
	
	public class BrandingPlayerMeta extends AbstractWindowView 
	{
		
		public var onSettings:Function;
		
		public var showPreset:Function;
		
		public function BrandingPlayerMeta() 
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
			var data:BrandingPlayerLocalizationVO = new BrandingPlayerLocalizationVO(ctx);
			setLocalization(data);
			if(data)
				data.dispose();
		}
		
		public final function as_setSettings(ctx:Object) : void
		{
			var data:BrandingPlayerSettingsVO = new BrandingPlayerSettingsVO(ctx);
			setSettings(data);
			if(data)
				data.dispose();
		}
		
		protected function setLocalization(data:BrandingPlayerLocalizationVO) : void
		{
			var message:String = "as_setLocalization" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message, data);
			throw new AbstractException(message);
		}
		
		protected function setSettings(data:BrandingPlayerSettingsVO) : void
		{
			var message:String = "as_setSettings" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message, data);
			throw new AbstractException(message);
		}
	}
}
