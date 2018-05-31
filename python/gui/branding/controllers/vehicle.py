
import BigWorld
from gui.branding.branding_constants import UI_TYPE
from gui.branding.controllers import g_controllers
from gui.branding.data import g_dataHolder
from gui.branding.utils import getHangarVehicle
from gui.shared import g_eventBus
from gui.shared.events import LobbySimpleEvent
from gui.shared.gui_items.customization.outfit import Outfit
from gui.shared.utils.HangarSpace import g_hangarSpace

__all__ = ('VehicleController', )

class VehicleController(object):
	
	def __init__(self):
		self.__savedCameraLocation = None
	
	def init(self):
		pass
		
	def fini(self):
		self.__savedCameraLocation = None
	
	def restoreVehicle(self):
		
		# getting current vehicle outfit
		outfit = g_hangarSpace.space.getVehicleEntity().appearance._getActiveOutfit()
		
		# updating vehicle customization
		g_hangarSpace.space.updateVehicleCustomization(outfit)
		
		# showing current lobby subview 
		g_eventBus.handleEvent(LobbySimpleEvent(LobbySimpleEvent.HIDE_HANGAR, False))
		
		# camera locating on previos position
		if self.__savedCameraLocation:
			manager = g_hangarSpace.space._ClientHangarSpace__cameraManager
			if manager:
				del self.__savedCameraLocation['pivotDist']
				manager.setCameraLocation(**self.__savedCameraLocation)
				self.__savedCameraLocation = None
	
	def showPresetInHangar(self, presetID):
		
		preset = g_controllers.processor.findPresetByID(presetID)
		if not preset:
			return

		# getting needed vehicle outfit
		appearance = g_hangarSpace.space.getVehicleEntity().appearance
		vDesc = appearance._HangarVehicleAppearance__vDesc
		originalOutfit = appearance._getActiveOutfit()
		outfit = g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)
		
		# updating vehicle customization
		g_hangarSpace.space.updateVehicleCustomization(outfit)
		
		g_eventBus.handleEvent(LobbySimpleEvent(LobbySimpleEvent.HIDE_HANGAR, True))
		
		if self.__savedCameraLocation is None:
			self.__savedCameraLocation = g_hangarSpace.space.getCameraLocation()

		g_hangarSpace.space.locateCameraToPreview()
	
	def getVehicleOutfit(self, appereance, originalOutfit):
		
		vDesc = appereance._CompoundAppearance__typeDesc
		vehicleInfo = BigWorld.player().arena.vehicles.get(appereance.id)
		
		if g_dataHolder.config['UIType'] == UI_TYPE.PLAYER:
			if g_dataHolder.cache['onlyOnMyTank']:
				preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][0])
				if preset is not None:
					if appereance.id == BigWorld.player().playerVehicleID:
						return g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)
					else:
						return originalOutfit
			else:
				isPlayerTeam = BigWorld.player().team == int(vehicleInfo['team'])
				if isPlayerTeam:
					preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][0])
				else:
					preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][1])
				if preset is not None:
					return g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)
		
		if g_dataHolder.config['UIType'] == UI_TYPE.OPERATOR:
			if vehicleInfo['team'] in [1, 2]:
				preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][vehicleInfo['team'] - 1])
				if preset is not None:
					return g_controllers.processor.getOutfit(originalOutfit, preset, vDesc)
		
		return originalOutfit