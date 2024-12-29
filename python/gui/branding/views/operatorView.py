# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2024 Andrii Andrushchyshyn

from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

from ..controllers import g_controllers
from ..data import g_dataHolder
from ..lang import l10n

__all__ = ('BrandingOperatorView', )

class BrandingOperatorViewMeta(AbstractWindowView):

	def as_setLocalizationS(self, ctx):
		"""ctx represented by BrandingOperatorLocalizationVO"""
		if self._isDAAPIInited():
			return self.flashObject.as_setLocalization(ctx)

	def as_setSettingsS(self, data):
		"""ctx represented by BrandingOperatorSettingsVO"""
		if self._isDAAPIInited():
			self.flashObject.as_setSettings(data)

class BrandingOperatorView(BrandingOperatorViewMeta):

	def _populate(self):
		super(BrandingOperatorView, self)._populate()

		# localization
		self.as_setLocalizationS(self.__generateLocalizationCtx())

		# settings
		self.as_setSettingsS(self.__generateOperatorCtx())

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
		g_controllers.vehicle.restoreVehicle()

	def showPreset(self, presetID):
		g_controllers.vehicle.showPresetInHangar(int(presetID))

	def __generateLocalizationCtx(self):
		"""result represented by BrandingOperatorLocalizationVO"""
		return {
			'windowTitle': l10n('ui.operator.windowTitle')
		}

	def __generateOperatorCtx(self):
		"""result represented by BrandingOperatorSettingsVO"""
		teamFirstIdx, teamSecondIdx = 0, 0
		teamFirst, teamSecond = g_dataHolder.cache['currentSetup']
		presets = []
		for idx, preset in enumerate(g_dataHolder.config['presets']):
			presets.append(self.__generatePresetSettingsVO(preset))
			if preset['id'] == teamFirst:
				teamFirstIdx = idx
			if preset['id'] == teamSecond:
				teamSecondIdx = idx
		return {
			'presets': presets,
			'teamFirst': teamFirstIdx,
			'teamSecond': teamSecondIdx
		}

	def __generatePresetSettingsVO(self, preset):
		name = preset['name']
		return {
			'id': preset['id'],
			'label': name
		}
