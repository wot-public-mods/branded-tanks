


# WOT_INFO ==> GUI_MODS MODS PATH VERSION
exec 'eJyNjk1vAiEQhu/7K+YGJAT7cdP00KZfHnSNa/VgjGGB3U7Lwgaw7c8vGzX22NszzPPOSxN8Bz6KXqZ3wK73IQFGjQFkBFk0w3\
pp4qwN563vjauMSujd4NRH5wHbjQ9Wn63vdt+atAheH1RamxBPelNouIOGMhF7i4kSTljR+AAK0EFNiRCj4S9R/HSWsC1ZDAPZiS9pDy\
ZSNi4AG5BUCRmrFNC1bAwm37w8TKAORn4WysoYYVOu9tP5c5mDs/KxyiYZEfHh0dGt4UCiCtinSDIqi8algTqvcymbwOJ+9ZojZgLrp2\
U1Led5oOgS1durHeNwxOsL3lzwdsfyhZe36f7/xe0B//YX2liQHGoOioPmkIPNL83ZhzY='.decode('base64').decode('zlib')



import codecs
import datetime
import time
import json
from VehicleAppearance import VehicleAppearance
from vehicle_systems.CompoundAppearance import CompoundAppearance
from VehicleStickers import VehicleStickers
from gui.mods.modsListApi import g_modsListApi
from gui.app_loader.loader import g_appLoader
from gui.Scaleform.framework import g_entitiesFactories, ViewSettings, ViewTypes, ScopeTemplates
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.shared import g_eventBus
from gui.shared.events import LobbySimpleEvent
from gui.shared.utils.HangarSpace import g_hangarSpace
from gui import SystemMessages 
from gui.customization.elements import Element



class branding():
	
	def __init__(self):
		
		self.onlyOnMyTank = False
		self.isPlayerLogic = False
		
		self.__oldCustomization = None
		self.__prevCameraLocation = None
		
		with codecs.open('/'.join([WOT_INFO.GUI_MODS, 'mod_branding', 'brandingConfig.json']), 'r', 'utf-8-sig') as f:
			data = f.read()
			self.config = json.loads(data)
		
		with open('/'.join([WOT_INFO.GUI_MODS, 'mod_branding', 'brandingIcon.png']), 'rb') as fh:
			modIcon = fh.read().encode("base64").replace('\n', '')

		g_modsListApi.addMod(
			id = "mod_branding",
			#name = 'Брендированные танки', 
			name = 'Branded tanks', 
			#description = 'Подмена камуфляжей и надписей для команд', 
			description = 'Spoofing camouflage and inscriptions for teams', 
			icon = modIcon, 
			enabled = True, 
			login = True, 
			lobby = True, 
			callback = self.loadUI
		)
		
		# Change camo and another staff on all tanks in battle
		baseFunc_start = CompoundAppearance.start
		CompoundAppearance.start = lambda baseClass, vehicle, prereqs = None: self.__hooked_start(baseClass, baseFunc_start, vehicle, prereqs)
		
		# delete clan emblems
		VehicleStickers.setClanID = lambda *args: None
		
		# premature alpha = 1 on stickers
		def fakeInit(baseClass, baseFunc, vehicleDesc, insigniaRank = 0):
			baseFunc(baseClass, vehicleDesc, insigniaRank)
			baseClass._VehicleStickers__defaultAlpha = 1.0
		baseFuncVehicleStickersInit = VehicleStickers.__init__
		VehicleStickers.__init__ = lambda baseClass, vehicleDesc, insigniaRank = 0: fakeInit(baseClass, baseFuncVehicleStickersInit, vehicleDesc, insigniaRank)
		
		# fix ingame customization prices
		def newElementInit(obj, params):
			if params['itemID'] >= 5000:
				params["allowedVehicles"] = ["ussr:MS-1_bot"]
			return oldElementInit(obj, params)
		oldElementInit = Element.__init__
		Element.__init__ = newElementInit
		def newGetPrice(obj, duration):
			try: return int(round(obj._getPrice(duration) * obj._getVehiclePriceFactor() * obj._getPriceFactor()))
			except: return 0
		Element.getPrice = newGetPrice




		# init gui
		g_entitiesFactories.addSettings(ViewSettings('brandingOperator', brandingOperator, '../../scripts/client/gui/mods/mod_branding/brandingOperator.swf', ViewTypes.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE))
		g_entitiesFactories.addSettings(ViewSettings('brandingPlayer', brandingPlayer, '../../scripts/client/gui/mods/mod_branding/brandingPlayer.swf', ViewTypes.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE))
	
	def loadUI(self): 
		if self.config['UIType'] == 1:
			g_appLoader.getDefLobbyApp().loadView('brandingOperator')
		elif self.config['UIType'] == 2:
			g_appLoader.getDefLobbyApp().loadView('brandingPlayer')
		
	def restoreHangarVehicle(self):
		if self.__oldCustomization is None:
			return
		else:
			try:
				vDesc = g_hangarSpace.space._ClientHangarSpace__vAppearance._VehicleAppearance__vDesc
				vState = g_hangarSpace.space._ClientHangarSpace__vAppearance._VehicleAppearance__vState	
			except:
				return
			vDesc.playerInscriptions = self.__oldCustomization[0]
			vDesc.playerEmblems = self.__oldCustomization[1]
			vDesc.camouflages = self.__oldCustomization[2]
			self.__oldCustomization = None
			g_hangarSpace.space.recreateVehicle(vDesc, vState)
			g_eventBus.handleEvent(LobbySimpleEvent(LobbySimpleEvent.HIDE_HANGAR, False))
			if self.__prevCameraLocation is not None:
				g_hangarSpace.space.setCameraLocation(**self.__prevCameraLocation)
				self.__prevCameraLocation = None
				
	def showPresetInHangar(self, id):
		
		preset = self.findPresetByID(id)
		
		if preset is not None:
				
			try:
				vDesc = g_hangarSpace.space._ClientHangarSpace__vAppearance._VehicleAppearance__vDesc
				vState = g_hangarSpace.space._ClientHangarSpace__vAppearance._VehicleAppearance__vState	
			except:
				return
			
			try:
				
				
				if self.__oldCustomization is None:
					self.__oldCustomization = [vDesc.playerInscriptions, vDesc.playerEmblems, vDesc.camouflages]
				
				if self.__prevCameraLocation is None:
					self.__prevCameraLocation = g_hangarSpace.space.getCameraLocation()
				
				
				old = vDesc.playerInscriptions
				
				
				adv = preset['advert']
				if vDesc.name in self.config["advert_fix"]:
					vDesc.playerInscriptions = (
						(self.settingParser(old, adv[0], 0, 0), 0, 0, 1), 
						(self.settingParser(old, adv[0], 1, 0), 0, 0, 1), 
						(self.settingParser(old, adv[1], 2, 0), 0, 0, 0), 
						(self.settingParser(old, adv[1], 3, 0), 0, 0, 0)
					)
				else:
					vDesc.playerInscriptions = (
						(self.settingParser(old, adv[0], 0, 0), 0, 0, 1), 
						(self.settingParser(old, adv[1], 1, 0), 0, 0, 1), 
						(self.settingParser(old, adv[0], 2, 0), 0, 0, 0), 
						(self.settingParser(old, adv[1], 3, 0), 0, 0, 0)
					)
				
				old = vDesc.playerEmblems
				
				
				logo = [preset['logotype'], self.findMirroredLogo(preset['logotype'])]
				
				if vDesc.name in self.config["logo_fix_1"]:
					vDesc.playerEmblems = (
						(self.settingParser(old, logo[0], 0, 1), 0, 0), 
						(self.settingParser(old, logo[1], 1, 1), 0, 0), 
						(self.settingParser(old, logo[1], 2, 1), 0, 0), 
						(self.settingParser(old, logo[1], 3, 1), 0, 0)
					)	
				elif vDesc.name in self.config["logo_fix_2"]:
					vDesc.playerEmblems = (
						(self.settingParser(old, logo[1], 0, 1), 0, 0), 
						(self.settingParser(old, logo[1], 1, 1), 0, 0), 
						(self.settingParser(old, logo[1], 2, 1), 0, 0), 
						(self.settingParser(old, logo[1], 3, 1), 0, 0)
					)	
				else:
					vDesc.playerEmblems = (
						(self.settingParser(old, logo[0], 0, 1), 0, 0), 
						(self.settingParser(old, logo[1], 1, 1), 0, 0), 
						(self.settingParser(old, logo[0], 2, 1), 0, 0), 
						(self.settingParser(old, logo[1], 3, 1), 0, 0)
					)
				
				old = vDesc.camouflages
				
				
				camo = preset['camouflage']
				vDesc.camouflages = (
					(self.settingParser(old, camo, 0, 2), 0, 0), 
					(self.settingParser(old, camo, 1, 2), 0, 0), 
					(self.settingParser(old, camo, 2, 2), 0, 0)
				)
				
				vDesc._VehicleAppearance__emblemsAlpha = 1.0
				
				g_hangarSpace.space.recreateVehicle(vDesc, vState)
				g_eventBus.handleEvent(LobbySimpleEvent(LobbySimpleEvent.HIDE_HANGAR, True))
				g_hangarSpace.space.locateCameraToPreview()
				
			except:
				pass
				
	def __hooked_start(self, baseClass, baseFunc, vehicle, prereqs):
		
		def customizeVehicle(preset, apperence,  clear = False):
			
			if self.__oldCustomization is not None:
				self.__oldCustomization = None
			
			old = apperence._CompoundAppearance__typeDesc.playerInscriptions
			adv = preset['advert']
			if apperence._CompoundAppearance__typeDesc.name in self.config["advert_fix"]:
				apperence._CompoundAppearance__typeDesc.playerInscriptions = (
					(None if clear else self.settingParser(old, adv[0], 0, 0), 13068864000, 0, 0), 
					(None if clear else self.settingParser(old, adv[0], 1, 0), 1306886400, 0, 0), 
					(None if clear else self.settingParser(old, adv[1], 2, 0), 1306886400, 0, 1), 
					(None if clear else self.settingParser(old, adv[1], 3, 0), 1306886400, 0, 1)
				)
			else:
				apperence._CompoundAppearance__typeDesc.playerInscriptions = (
					(None if clear else self.settingParser(old, adv[0], 0, 0), 1306886400, 0, 0), 
					(None if clear else self.settingParser(old, adv[1], 1, 0), 1306886400, 0, 0), 
					(None if clear else self.settingParser(old, adv[0], 2, 0), 1306886400, 0, 1), 
					(None if clear else self.settingParser(old, adv[1], 3, 0), 1306886400, 0, 1)
				)
			
			old = apperence._CompoundAppearance__typeDesc.playerEmblems
			logo = [preset['logotype'], self.findMirroredLogo(preset['logotype'])]
			
			if apperence._CompoundAppearance__typeDesc.name in self.config["logo_fix_1"]:
				apperence._CompoundAppearance__typeDesc.playerEmblems = (
					(None if clear else self.settingParser(old, logo[0], 0, 1), 1306886400, 0), 
					(None if clear else self.settingParser(old, logo[1], 1, 1), 1306886400, 0), 
					(None if clear else self.settingParser(old, logo[1], 2, 1), 1306886400, 0), 
					(None if clear else self.settingParser(old, logo[1], 3, 1), 1306886400, 0)
				)	
			elif apperence._CompoundAppearance__typeDesc.name in self.config["logo_fix_2"]:
				apperence._CompoundAppearance__typeDesc.playerEmblems = (
					(None if clear else self.settingParser(old, logo[1], 0, 1), 1306886400, 0), 
					(None if clear else self.settingParser(old, logo[1], 1, 1), 1306886400, 0), 
					(None if clear else self.settingParser(old, logo[1], 2, 1), 1306886400, 0), 
					(None if clear else self.settingParser(old, logo[1], 3, 1), 1306886400, 0)
				)	
			else:
				apperence._CompoundAppearance__typeDesc.playerEmblems = (
					(None if clear else self.settingParser(old, logo[0], 0, 1), 1306886400, 0), 
					(None if clear else self.settingParser(old, logo[1], 1, 1), 1306886400, 0), 
					(None if clear else self.settingParser(old, logo[0], 2, 1), 1306886400, 0), 
					(None if clear else self.settingParser(old, logo[1], 3, 1), 1306886400, 0)
				)
			
			old = apperence._CompoundAppearance__typeDesc.camouflages
			camo = preset['camouflage']
			apperence._CompoundAppearance__typeDesc.camouflages = (
				(None if clear else self.settingParser(old, camo, 0, 2), 1306886400, 0), 
				(None if clear else self.settingParser(old, camo, 1, 2), 1306886400, 0), 
				(None if clear else self.settingParser(old, camo, 2, 2), 1306886400, 0)
			)
			
			apperence._CompoundAppearance__typeDesc._VehicleAppearance__emblemsAlpha = 1.0
		
		if self.config['UIType'] == 2:
			if self.config['onlyOnMyTank']:
				preset = self.findPresetByID(self.config['current'][0])
				if preset is not None:
					if vehicle.isPlayerVehicle:
						customizeVehicle(preset, baseClass)
					else:
						customizeVehicle(preset, baseClass, True)
			else:
				import BigWorld
				isPlayerTeam = BigWorld.player().team == int(vehicle.publicInfo['team'])
				if isPlayerTeam:
					preset = self.findPresetByID(self.config['current'][0])
				else:
					preset = self.findPresetByID(self.config['current'][1])
				if preset is not None:
					customizeVehicle(preset, baseClass)
		else:
			team = int(vehicle.publicInfo['team'])
			if team not in [1, 2]:
				return baseFunc(baseClass, vehicle, prereqs)
			preset = self.findPresetByID(self.config['current'][team - 1])
			if preset is not None:
				customizeVehicle(preset, baseClass)
				
		return baseFunc(baseClass, vehicle, prereqs)
	
	def findMirroredLogo(self, id):
		for logotype in self.config['logotypes']:
			if logotype['id'] == id:
				return logotype['mirrored_id']
		return -1 if id == -1 else 0
	
	def findPresetByID(self, id): 
		for preset in self.config['presets']:
			if preset['id'] == id:
				return preset
		return None

	def settingParser(self, old, adv, idx, type): 
		if self.__oldCustomization is not None:
			old = self.__oldCustomization[type]
		if adv == -1: 
			return None
		elif adv == 0: 
			return old[idx][0]
		else: 
			return adv
	
	def pushSystemMessageOperator(self):
		name_1 = self.findPresetByID(self.config['current'][0])
		name_1 = name_1['name'] if name_1 is not None else "Unknown"
		
		name_2 = self.findPresetByID(self.config['current'][1])
		name_2 = name_2['name'] if name_2 is not None else "Unknown"
		
		SystemMessages.pushMessage('Team #1 style: "' + name_1 + '" <br>Team #2 style: "' + name_2 + '"', type=SystemMessages.SM_TYPE.Warning)
	
	def pushSystemMessagePlayer(self):
		
		if self.config['current'][1] != -1:
			
			name_1 = self.findPresetByID(self.config['current'][0])
			name_1 = name_1['name'] if name_1 is not None else "Unknown"
			
			name_2 = self.findPresetByID(self.config['current'][1])
			name_2 = name_2['name'] if name_2 is not None else "Unknown"
			
			SystemMessages.pushMessage('Branding for both teams<br><b><font color="#00FF00">' + name_1 + '</font> vs <font color="#FF0000">' + name_2 + '</font></b>', type=SystemMessages.SM_TYPE.Warning)
			
		else:
		
			name_1 = self.findPresetByID(self.config['current'][0])
			name_1 = name_1['name'] if name_1 is not None else "Unknown"
			
			SystemMessages.pushMessage('Branding for your vehicle<br><b><font color="#00FF00">' + name_1 + '</font></b>', type=SystemMessages.SM_TYPE.Warning)



class brandingOperator(AbstractWindowView):
	
	def _populate(self):
		super(brandingOperator, self)._populate()
		if self._isDAAPIInited():
			presets = []
			for preset in g_branding.config['presets']:
				presets.append(preset['name'])	
			settings = [g_branding.config['current'], presets]
			self.flashObject.as_syncData(settings)
		
	def onWindowClose(self):
		g_branding.restoreHangarVehicle()
		self.destroy()

	def onTryClosing(self):
		return True

	def as_isModalS(self):
		if self._isDAAPIInited():
			return False
	
	def py_onSettings(self, settings):
		
		g_branding.config['current'] = [int(settings[0]), int(settings[1])]
		g_branding.pushSystemMessageOperator()
		
		with codecs.open('/'.join([WOT_INFO.GUI_MODS, 'mod_branding', 'brandingConfig.json']), 'w+', 'utf-8-sig') as fh:
			fh.write(json.dumps(g_branding.config, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True))
		g_branding.restoreHangarVehicle()
		
	def py_onShowPreset(self, id):
		g_branding.showPresetInHangar(int(id))



class brandingPlayer(AbstractWindowView):
	
	def _populate(self):
		super(brandingPlayer, self)._populate()
		
		def get_image(path):
			with open('/'.join([WOT_INFO.GUI_MODS, 'mod_branding', 'resources', path]), 'rb') as fh:
				return fh.read().encode("base64").replace('\n', '')
			return None
		
		if self._isDAAPIInited():
			presets = []
			for preset in g_branding.config['presets']:
				if preset["preview"]["enable"]:
					presets.append({
						"id": preset["id"],
						"name": preset["name"],
						"icon": get_image(preset["preview"]["image"])
					})	
			self.flashObject.as_syncData(presets, g_branding.onlyOnMyTank)
		
	def onWindowClose(self):
		g_branding.restoreHangarVehicle()
		self.destroy()
		
	def py_onFinish(self, settings):
		g_branding.config['current'] = [int(settings[0]), int(settings[1])]
		g_branding.config['onlyOnMyTank'] = bool(settings[2])
		g_branding.pushSystemMessagePlayer()
		
		with codecs.open('/'.join([WOT_INFO.GUI_MODS, 'mod_branding', 'brandingConfig.json']), 'w+', 'utf-8-sig') as fh:
			fh.write(json.dumps(g_branding.config, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True))
		
		g_branding.restoreHangarVehicle()
		
		self.onWindowClose()

	def onTryClosing(self):
		return True

	def as_isModalS(self):
		if self._isDAAPIInited():
			return False
	
	def py_onSettings(self, settings):
		
		g_branding.config['current'] = [int(settings[0]), int(settings[1])]
		g_branding.config['onlyOnMyTank'] = bool(settings[2])
		g_branding.pushSystemMessage()
		
		with codecs.open('/'.join([WOT_INFO.GUI_MODS, 'mod_branding', 'brandingConfig.json']), 'w+', 'utf-8-sig') as fh:
			fh.write(json.dumps(g_branding.config, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True))
		
		g_branding.restoreHangarVehicle()
		
	def debugLogS(self, *args):
		print '[DEBUG] brandingPlayer ' + ' '.join([str(arg) for arg in args])



g_branding = branding()



print "[NOTE] package loaded: mod_branding"


