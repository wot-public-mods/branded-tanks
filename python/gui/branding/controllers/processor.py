
import json
import os

import BigWorld
from gui import SystemMessages
from gui.app_loader.loader import g_appLoader
from gui.branding.branding_constants import BRANDING_OPERATOR_WINDOW_UI, BRANDING_PLAYER_WINDOW_UI, UI_TYPE
from gui.branding.data import g_dataHolder
from gui.branding.events import g_eventsManager
from gui.branding.lang import l10n
from gui.branding.utils import getFashionValue

from gui.branding.controllers import g_controllers

__all__ = ('ProcessorController', )

class ProcessorController(object):
	
	def __init__(self):
		pass
	
	def init(self):
		g_eventsManager.showUI += self.__showUI
	
	def fini(self):
		g_eventsManager.showUI -= self.__showUI
	
	def findPresetByID(self, presetID):
		for preset in g_dataHolder.config['presets']:
			if preset['id'] == presetID:
				return preset
		return None
	
	def processVehicleDescriptor(self, preset, vehicleDescriptor, isClean = False):
		advert = preset['advert']
		logotype = [preset['logotype'], self.__findMirroredLogo(preset['logotype'])]
		camouflage = preset['camouflage']
		vehicleDescriptor._VehicleAppearance__emblemsAlpha = 1.0
		saved = g_controllers.vehicle.savedCustomization
		
		current = vehicleDescriptor.playerInscriptions
		
		if not hasattr(vehicleDescriptor, 'backup_inscriptions'):
			vehicleDescriptor.backup_inscriptions = current
		
		if vehicleDescriptor.name in g_dataHolder.config["advertFix"]:
			vehicleDescriptor.playerInscriptions = (
				(getFashionValue(current, saved, advert[0], 0, 0, isClean), 13068864000, 0, 0), 
				(getFashionValue(current, saved, advert[0], 1, 0, isClean), 13068864000, 0, 0), 
				(getFashionValue(current, saved, advert[1], 2, 0, isClean), 13068864000, 0, 1),  
				(getFashionValue(current, saved, advert[1], 3, 0, isClean), 13068864000, 0, 1)
			)
		else:
			vehicleDescriptor.playerInscriptions = (
				(getFashionValue(current, saved, advert[0], 0, 0, isClean), 13068864000, 0, 0),
				(getFashionValue(current, saved, advert[1], 1, 0, isClean), 13068864000, 0, 0),
				(getFashionValue(current, saved, advert[0], 2, 0, isClean), 13068864000, 0, 1),
				(getFashionValue(current, saved, advert[1], 3, 0, isClean), 13068864000, 0, 1)
			)
		
		current = vehicleDescriptor.playerEmblems
		
		if not hasattr(vehicleDescriptor, 'backup_emblems'):
			vehicleDescriptor.backup_emblems = current
		
		if vehicleDescriptor.name in g_dataHolder.config["logotypeFix1"]:
			vehicleDescriptor.playerEmblems = (
				(getFashionValue(current, saved, logotype[0], 0, 1, isClean), 13068864000, 0),
				(getFashionValue(current, saved, logotype[1], 1, 1, isClean), 13068864000, 0),
				(getFashionValue(current, saved, logotype[1], 2, 1, isClean), 13068864000, 0),
				(getFashionValue(current, saved, logotype[1], 3, 1, isClean), 13068864000, 0)
			)	
		elif vehicleDescriptor.name in g_dataHolder.config["logotypeFix2"]:
			vehicleDescriptor.playerEmblems = (
				(getFashionValue(current, saved, logotype[1], 0, 1, isClean), 13068864000, 0),
				(getFashionValue(current, saved, logotype[1], 1, 1, isClean), 13068864000, 0),
				(getFashionValue(current, saved, logotype[1], 2, 1, isClean), 13068864000, 0),
				(getFashionValue(current, saved, logotype[1], 3, 1, isClean), 13068864000, 0)
			)
		else:
			vehicleDescriptor.playerEmblems = (
				(getFashionValue(current, saved, logotype[0], 0, 1, isClean), 13068864000, 0),
				(getFashionValue(current, saved, logotype[1], 1, 1, isClean), 13068864000, 0),
				(getFashionValue(current, saved, logotype[0], 2, 1, isClean), 13068864000, 0),
				(getFashionValue(current, saved, logotype[1], 3, 1, isClean), 13068864000, 0)
			)
	
		
		current = vehicleDescriptor.camouflages
		
		if not hasattr(vehicleDescriptor, 'backup_camouflages'):
			vehicleDescriptor.backup_camouflages = current
		
		vehicleDescriptor.camouflages = (
			(getFashionValue(current, saved, camouflage, 0, 2, isClean), 13068864000, 0), 
			(getFashionValue(current, saved, camouflage, 1, 2, isClean), 13068864000, 0), 
			(getFashionValue(current, saved, camouflage, 2, 2, isClean), 13068864000, 0)
		)
	
	def appendSettings(self, ctx):
		g_dataHolder.cache['currentSetup'] = [int(ctx['teamFirst']), int(ctx['teamSecond'])]
		g_dataHolder.cache['onlyOnMyTank'] = ctx['onlyOnMyTank']
		if g_dataHolder.config['UIType'] == UI_TYPE.OPERATOR:
			self.__pushSystemMessageOperator()
		elif g_dataHolder.config['UIType'] == UI_TYPE.PLAYER:
			self.__pushSystemMessagePlayer()
	
	def __showUI(self):
		if g_dataHolder.config['UIType'] == UI_TYPE.OPERATOR:
			g_dataHolder.cache['onlyOnMyTank'] = False
			g_appLoader.getDefLobbyApp().loadView(BRANDING_OPERATOR_WINDOW_UI)
		elif g_dataHolder.config['UIType'] == UI_TYPE.PLAYER:
			g_appLoader.getDefLobbyApp().loadView(BRANDING_PLAYER_WINDOW_UI)
	
	def __findMirroredLogo(self, id):
		for logotype in g_dataHolder.config['logotypes']:
			if logotype['id'] == id:
				return logotype['mirroredId']
		return -1 if id == -1 else 0
	
	def __pushSystemMessageOperator(self):
		
		preset1 = self.findPresetByID(g_dataHolder.cache['currentSetup'][0])
		name1 = preset1['name'] if preset1 else "Unknown"
		
		preset2 = self.findPresetByID(g_dataHolder.cache['currentSetup'][1])
		name2 = preset2['name'] if preset2 else "Unknown"
		
		message = l10n('ui.operator.messageTeams').format(name1=name1, name2=name2)
		
		SystemMessages.pushMessage(message, type=SystemMessages.SM_TYPE.Warning)
	
	def __pushSystemMessagePlayer(self):
		
		if g_dataHolder.cache['onlyOnMyTank']:
				
			preset = self.findPresetByID(g_dataHolder.cache['currentSetup'][0])

			name = preset['name'] if preset else "Unknown"
			
			message = l10n('ui.player.messageOwnTank').format(name=name)
			
			SystemMessages.pushMessage(message, type=SystemMessages.SM_TYPE.Warning)
		
		else:

			preset1 = self.findPresetByID(g_dataHolder.cache['currentSetup'][0])
			name1 = preset1['name'] if preset1 else "Unknown"
			
			preset2 = self.findPresetByID(g_dataHolder.cache['currentSetup'][1])
			name2 = preset2['name'] if preset2 else "Unknown"
				
			message = l10n('ui.player.messageTeams').format(name1=name1, name2=name2)
			
			SystemMessages.pushMessage(message, type=SystemMessages.SM_TYPE.Warning)