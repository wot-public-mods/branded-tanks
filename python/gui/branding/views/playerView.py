
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

from ..controllers import g_controllers
from ..data import g_dataHolder
from ..lang import l10n
from ..utils import getIconPatch

__all__ = ('BrandingPlayerView', )

class BrandingPlayerViewMeta(AbstractWindowView):

	def as_setLocalizationS(self, ctx):
		"""ctx represented by BrandingPlayerLocalizationVO"""
		if self._isDAAPIInited():
			return self.flashObject.as_setLocalization(ctx)

	def as_setSettingsS(self, ctx):
		"""ctx represented by BrandingPlayerSettingsVO"""
		if self._isDAAPIInited():
			self.flashObject.as_setSettings(ctx)

class BrandingPlayerView(BrandingPlayerViewMeta):

	def _populate(self):
		super(BrandingPlayerView, self)._populate()

		# localization
		self.as_setLocalizationS(self.__generateLocalizationCtx())

		# settings
		self.as_setSettingsS(self.__generatePlayerCtx())

	def onWindowClose(self):
		g_controllers.vehicle.restoreVehicle()
		self.destroy()

	def onTryClosing(self):
		return True

	def as_isModalS(self):
		if self._isDAAPIInited():
			return False

	def onSettings(self, teamFirst, teamSecond, onlyOnMyTank):
		g_controllers.processor.appendSettings({
			'teamFirst': teamFirst,
			'teamSecond': teamSecond,
			'onlyOnMyTank': onlyOnMyTank
		})
		self.onWindowClose()

	def showPreset(self, presetID):
		g_controllers.vehicle.showPresetInHangar(int(presetID))

	def __generateLocalizationCtx(self):
		"""result represented by BrandingPlayerLocalizationVO"""
		return {
			'windowTitle': l10n('ui.operator.windowTitle'),
			'headerTextAlly': l10n('ui.player.headerTextAlly'),
			'headerTextEnemy': l10n('ui.player.headerTextEnemy'),
			'onlyMyTankLabel': l10n('ui.player.onlyMyTank.label'),
			'onlyMyTankToolTip': l10n('ui.player.onlyMyTank.toolTip')
		}

	def __generatePlayerCtx(self):
		"""result represented by BrandingPlayerSettingsVO"""
		presets = []
		preview = g_dataHolder.config.get('preview', False)
		for idx, preset in enumerate(g_dataHolder.config['presets']):
			presets.append(self.__generatePresetSettingsVO(idx, preset, preview))
		onlyOnMyTank = g_dataHolder.cache['onlyOnMyTank']
		return {
			'presets': presets,
			'onlyOnMyTank': onlyOnMyTank
		}

	def __generatePresetSettingsVO(self, idx, preset, preview):
		name = preset['name']
		icon = getIconPatch(preset)
		return {
			'id': idx,
			'presetID': preset['id'],
			'name': name,
			'icon': icon,
			'preview': preview
		}
