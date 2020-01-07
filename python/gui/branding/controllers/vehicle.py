import math

import BigWorld
from gui.ClientHangarSpace import hangarCFG
from gui.branding._constants import UI_TYPE
from gui.branding.controllers import g_controllers
from gui.branding.data import g_dataHolder
from gui.shared import g_eventBus
from gui.shared.events import LobbySimpleEvent
from helpers import dependency
from skeletons.gui.shared.utils import IHangarSpace

__all__ = ('VehicleController', )

class VehicleController(object):

	hangarSpace = dependency.descriptor(IHangarSpace)

	def __init__(self):
		self.__savedCameraLocation = None

	def restoreVehicle(self):

		if not self.hangarSpace.space:
			return

		# getting current vehicle outfit
		appearance = self.hangarSpace.space.getVehicleEntity().appearance
		if not appearance:
			return

		# updating vehicle customization
		self.hangarSpace.space.updateVehicleCustomization(appearance._getActiveOutfit())

		# showing current lobby subview
		g_eventBus.handleEvent(LobbySimpleEvent(LobbySimpleEvent.HIDE_HANGAR, False))

		# camera locating on previos position
		if self.__savedCameraLocation:
			manager = self.hangarSpace.space.getCameraManager()
			if manager:
				del self.__savedCameraLocation['pivotDist']
				manager.setCameraLocation(**self.__savedCameraLocation)
				self.__savedCameraLocation = None

	def showPresetInHangar(self, presetID):

		preset = g_controllers.processor.findPresetByID(presetID)
		if not preset:
			return

		# getting needed vehicle outfit
		appearance = self.hangarSpace.space.getVehicleEntity().appearance
		if not appearance:
			return

		vDesc = appearance._HangarVehicleAppearance__vDesc
		originalOutfit = appearance._getActiveOutfit()
		outfit = g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)

		# updating vehicle customization
		self.hangarSpace.space.updateVehicleCustomization(outfit)

		g_eventBus.handleEvent(LobbySimpleEvent(LobbySimpleEvent.HIDE_HANGAR, True))

		if self.__savedCameraLocation is None:
			self.__savedCameraLocation = self.hangarSpace.space.getCameraLocation()

		manager = self.hangarSpace.space.getCameraManager()
		if not manager:
			return

		cfg = hangarCFG()
		manager.setCameraLocation(
			targetPos=cfg['cam_start_target_pos'],
			pivotPos=cfg['cam_pivot_pos'],
			yaw=math.radians(cfg['cam_start_angles'][0]),
			pitch=math.radians(cfg['cam_start_angles'][1]),
			dist=cfg['cam_start_dist'] - 4,
			camConstraints=[cfg['cam_pitch_constr'], cfg['cam_yaw_constr'],	cfg['cam_dist_constr']]
		)

	@staticmethod
	def getVehicleOutfit(appereance, originalOutfit):
		vDesc = appereance.typeDescriptor
		vehicleTeam = BigWorld.player().arena.vehicles.get(appereance.id, {}).get('team', 1)
		if g_dataHolder.config['UIType'] == UI_TYPE.PLAYER:
			if g_dataHolder.cache['onlyOnMyTank']:
				preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][0])
				if preset is not None:
					if appereance.id == BigWorld.player().playerVehicleID:
						return g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)
					return originalOutfit
			else:
				isPlayerTeam = BigWorld.player().team == vehicleTeam
				if isPlayerTeam:
					preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][0])
				else:
					preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][1])
				if preset is not None:
					return g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)

		elif g_dataHolder.config['UIType'] == UI_TYPE.OPERATOR and vehicleTeam in [1, 2]:
			preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][vehicleTeam - 1])
			if preset is not None:
				return g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)

		return originalOutfit
