# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2025 Andrii Andrushchyshyn

import BigWorld

from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider
from skeletons.gui.shared.utils import IHangarSpace
from vehicle_systems.CompoundAppearance import CompoundAppearance

from ..controllers import g_controllers
from ..data import g_dataHolder
from .._constants import UI_TYPE

__all__ = ('VehicleController', )

class VehicleController(object):

	sessionProvider = dependency.descriptor(IBattleSessionProvider)
	hangarSpace = dependency.descriptor(IHangarSpace)

	def restoreVehicle(self):

		if not self.hangarSpace.space:
			return

		# getting current vehicle outfit
		appearance = self.hangarSpace.space.getVehicleEntity().appearance
		if not appearance:
			return

		# updating vehicle customization
		vDesc = appearance._HangarVehicleAppearance__vDesc
		self.hangarSpace.space.updateVehicleCustomization(appearance._getActiveOutfit(vDesc))

	def showPresetInHangar(self, presetID):

		preset = g_controllers.processor.findPresetByID(presetID)
		if not preset:
			return

		# getting needed vehicle outfit
		appearance = self.hangarSpace.space.getVehicleEntity().appearance
		if not appearance:
			return

		vDesc = appearance._HangarVehicleAppearance__vDesc
		originalOutfit = appearance._getActiveOutfit(vDesc)
		outfit = g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)

		# updating vehicle customization
		self.hangarSpace.space.updateVehicleCustomization(outfit)

	def getVehicleOutfit(self, appereance, originalOutfit):
		arenaDP = self.sessionProvider.getArenaDP()
		vehicle_team = arenaDP.getVehicleInfo(appereance.id).team
		player_team = arenaDP.getVehicleInfo().team

		# We don't have vehicle team info
		# return an empty Outfit and replace them later
		if not vehicle_team or not player_team:
			return g_controllers.processor.getEmptyOutfit()

		vDesc = appereance.typeDescriptor

		if g_dataHolder.config['UIType'] == UI_TYPE.PLAYER:
			if g_dataHolder.cache['onlyOnMyTank']:
				preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][0])
				if preset is not None:
					if appereance.id == BigWorld.player().playerVehicleID:
						return g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)
					return originalOutfit
			else:
				isPlayerTeam = player_team == vehicle_team
				if isPlayerTeam:
					preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][0])
				else:
					preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][1])
				if preset is not None:
					return g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)

		elif g_dataHolder.config['UIType'] == UI_TYPE.OPERATOR and vehicle_team in [1, 2]:
			preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][vehicle_team - 1])
			if preset is not None:
				return g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)

		return originalOutfit
