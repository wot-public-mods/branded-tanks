
import BigWorld
from gui.branding.branding_constants import UI_TYPE
from gui.branding.controllers import g_controllers
from gui.branding.data import g_dataHolder
from gui.branding.utils import getHangarVehicle
from gui.shared import g_eventBus
from gui.shared.events import LobbySimpleEvent
from gui.shared.utils.HangarSpace import g_hangarSpace

__all__ = ('VehicleController', )

class VehicleController(object):
	
	savedCustomization = property(lambda self: self.__savedCustomization)

	def __init__(self):
		self.__savedCustomization = None
		self.__savedCameraLocation = None
	
	def init(self):
		pass
		
	def fini(self):
		self.__savedCustomization = None
		self.__savedCameraLocation = None
	
	def restoreVehicle(self):
		
		if not self.__savedCustomization:
			return
		
		descr, state = getHangarVehicle()
		if not descr:
			return
		
		descr.playerInscriptions = self.__savedCustomization[0]
		descr.playerEmblems = self.__savedCustomization[1]
		descr.camouflages = self.__savedCustomization[2]
		self.__savedCustomization = None

		# recreating hangar vehicle with old vehicle vehicleDescriptor
		g_hangarSpace.space.recreateVehicle(descr, state)
		
		# showing current lobby subview 
		g_eventBus.handleEvent(LobbySimpleEvent(LobbySimpleEvent.HIDE_HANGAR, False))
		
		# camera locating on previos position
		if self.__savedCameraLocation is not None:
			g_hangarSpace.space.setCameraLocation(**self.__savedCameraLocation)
			self.__savedCameraLocation = None
	
	def showPresetInHangar(self, presetID):
		
		preset = g_controllers.processor.findPresetByID(presetID)
		if not preset:
			return
		
		descr, state = getHangarVehicle()
		if not descr:
			return
		
		if self.__savedCustomization is None:
			self.__savedCustomization = [descr.playerInscriptions, descr.playerEmblems, descr.camouflages]
		
		if self.__savedCameraLocation is None:
			self.__savedCameraLocation = g_hangarSpace.space.getCameraLocation()
		
		g_controllers.processor.processVehicleDescriptor(preset, descr)
		
		# recreating hangar vehicle with new vehicle vehicleDescriptor
		g_hangarSpace.space.recreateVehicle(descr, state)
		
		# hiding current lobby subview 
		g_eventBus.handleEvent(LobbySimpleEvent(LobbySimpleEvent.HIDE_HANGAR, True))
		
		# camera locating on vehicle preview
		g_hangarSpace.space.locateCameraToPreview()
		
	def processCompoundAppearance(self, appereance):
		
		vehicleInfo = BigWorld.player().arena.vehicles.get(appereance.id)

		if g_dataHolder.config['UIType'] == UI_TYPE.PLAYER:
			if g_dataHolder.cache['onlyOnMyTank']:
				preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][0])
				if preset is not None:
					if appereance.id == BigWorld.player().playerVehicleID:
						g_controllers.processor.processVehicleDescriptor(preset, appereance._CompoundAppearance__typeDesc)
					else:
						g_controllers.processor.processVehicleDescriptor(preset, appereance._CompoundAppearance__typeDesc, True)
			else:
				
				isPlayerTeam = BigWorld.player().team == int(vehicleInfo['team'])
				if isPlayerTeam:
					preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][0])
				else:
					preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][1])
				if preset is not None:
					g_controllers.processor.processVehicleDescriptor(preset, appereance._CompoundAppearance__typeDesc)
		
		if g_dataHolder.config['UIType'] == UI_TYPE.OPERATOR:
			
			if vehicleInfo['team'] not in [1, 2]:
				return
			
			preset = g_controllers.processor.findPresetByID(g_dataHolder.cache['currentSetup'][vehicleInfo['team'] - 1])
			
			if preset is not None:
				g_controllers.processor.processVehicleDescriptor(preset, appereance._CompoundAppearance__typeDesc)
