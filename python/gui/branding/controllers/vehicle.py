
import Math
import BigWorld
import CGF

from cgf_components.hangar_camera_manager import HangarCameraManager
from gui.ClientHangarSpace import hangarCFG
from gui.shared import g_eventBus
from gui.shared.events import LobbySimpleEvent
from helpers import dependency
from skeletons.gui.shared.utils import IHangarSpace

from ..controllers import g_controllers
from ..data import g_dataHolder
from .._constants import UI_TYPE

__all__ = ('VehicleController', )

class VehicleController(object):

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

		# showing current lobby subview
		g_eventBus.handleEvent(LobbySimpleEvent(LobbySimpleEvent.HIDE_HANGAR, False))

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

		g_eventBus.handleEvent(LobbySimpleEvent(LobbySimpleEvent.HIDE_HANGAR, True))

		cameraManager = CGF.getManager(self.hangarSpace.spaceID, HangarCameraManager)
		if not cameraManager:
			return

		cfg = hangarCFG()

		cameraManager.moveCamera(
			targetPos=cfg.get('cam_start_target_pos', Math.Vector3(0, 0, 0)),
			yaw=-1.0, pitch=-0.5, distance=1.5
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
