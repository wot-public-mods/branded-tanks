
import json
import os

import BigWorld
from gui import SystemMessages
from gui.app_loader.loader import g_appLoader
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.shared.gui_items import GUI_ITEM_TYPE
from gui.shared.gui_items.customization.outfit import Outfit
from gui.shared.gui_items.customization.c11n_items import Camouflage, Emblem, Decal
from items.components.c11n_constants import ApplyArea
from items.customizations import CustomizationOutfit, CamouflageComponent, DecalComponent

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
	
	def getOutfit(self, originalOutfit, preset, vDesc):
		
		camouflages, decals = [], []
		hullSlotsNum, turretSlotsNum = 0, 0
		
		for emblemSlot in vDesc.hull.emblemSlots:
			if emblemSlot.type == 'inscription':
				hullSlotsNum += 1
		for emblemSlot in vDesc.turret.emblemSlots:
			if emblemSlot.type == 'inscription':
				turretSlotsNum += 1
		
		cammoCompID = preset['camouflage']
		logoCompID = preset['logotype']
		advertCompID1, advertCompID2 = preset['advert']

		if cammoCompID == 0 and logoCompID == 0 and advertCompID1 == 0 and advertCompID2 == 0:
			return originalOutfit

		if cammoCompID == -1:
			pass
		elif cammoCompID != 0:
			camouflages.append(CamouflageComponent(id = cammoCompID, appliedTo = ApplyArea.HULL))
			camouflages.append(CamouflageComponent(id = cammoCompID, appliedTo = ApplyArea.TURRET))
			camouflages.append(CamouflageComponent(id = cammoCompID, appliedTo = ApplyArea.GUN))
		
		if logoCompID == -1:
			pass
		elif logoCompID != 0:
			decals.append(DecalComponent(id = logoCompID, appliedTo = ApplyArea.HULL))
			decals.append(DecalComponent(id = logoCompID, appliedTo = ApplyArea.HULL_1))
			decals.append(DecalComponent(id = logoCompID, appliedTo = ApplyArea.TURRET))
			decals.append(DecalComponent(id = logoCompID, appliedTo = ApplyArea.TURRET_1))
			decals.append(DecalComponent(id = logoCompID, appliedTo = ApplyArea.GUN))
			decals.append(DecalComponent(id = logoCompID, appliedTo = ApplyArea.GUN_1))
		
		storedSoloSlot = False

		if advertCompID1 == -1:
			pass
		elif advertCompID1 != 0:
			if hullSlotsNum == 1 and turretSlotsNum == 1:
				decals.append(DecalComponent(id = advertCompID1, appliedTo = ApplyArea.HULL_2))
				decals.append(DecalComponent(id = advertCompID1, appliedTo = ApplyArea.HULL_3))
			elif hullSlotsNum == 2:
				decals.append(DecalComponent(id = advertCompID1, appliedTo = ApplyArea.HULL_2))
			elif turretSlotsNum == 2:
				decals.append(DecalComponent(id = advertCompID1, appliedTo = ApplyArea.TURRET_2))
				decals.append(DecalComponent(id = advertCompID1, appliedTo = ApplyArea.GUN_2))
			elif hullSlotsNum + turretSlotsNum == 1:
				decals.append(DecalComponent(id = advertCompID1, appliedTo = ApplyArea.HULL_2))
				decals.append(DecalComponent(id = advertCompID1, appliedTo = ApplyArea.HULL_3))
				storedSoloSlot = True
		
		if advertCompID2 == -1:
			pass
		elif advertCompID2 != 0:
			if hullSlotsNum == 1 and turretSlotsNum == 1:
				decals.append(DecalComponent(id = advertCompID2, appliedTo = ApplyArea.TURRET_2))
				decals.append(DecalComponent(id = advertCompID2, appliedTo = ApplyArea.GUN_2))
				decals.append(DecalComponent(id = advertCompID2, appliedTo = ApplyArea.TURRET_3))
				decals.append(DecalComponent(id = advertCompID2, appliedTo = ApplyArea.GUN_3))
			elif hullSlotsNum == 2:
				decals.append(DecalComponent(id = advertCompID2, appliedTo = ApplyArea.HULL_3))
			elif turretSlotsNum == 2:
				decals.append(DecalComponent(id = advertCompID2, appliedTo = ApplyArea.TURRET_3))
				decals.append(DecalComponent(id = advertCompID2, appliedTo = ApplyArea.GUN_3))
			elif hullSlotsNum + turretSlotsNum == 1 and not storedSoloSlot:
				decals.append(DecalComponent(id = advertCompID2, appliedTo = ApplyArea.HULL_2))
				decals.append(DecalComponent(id = advertCompID2, appliedTo = ApplyArea.HULL_3))
		
		customizationOutfit = CustomizationOutfit(camouflages=camouflages, decals=decals)
		return Outfit(customizationOutfit.makeCompDescr())
	
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
			g_appLoader.getDefLobbyApp().loadView(SFViewLoadParams(BRANDING_OPERATOR_WINDOW_UI, BRANDING_OPERATOR_WINDOW_UI), {})
		elif g_dataHolder.config['UIType'] == UI_TYPE.PLAYER:
			g_appLoader.getDefLobbyApp().loadView(SFViewLoadParams(BRANDING_PLAYER_WINDOW_UI, BRANDING_PLAYER_WINDOW_UI), {})
	
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