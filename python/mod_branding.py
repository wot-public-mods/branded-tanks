

# using for convert unicode key/value to utf-8
def byteify(input):
	import types
	if isinstance(input, types.DictType): return { byteify(key): byteify(value) for key, value in input.iteritems() }
	elif isinstance(input, types.ListType): return [ byteify(element) for element in input ]
	elif isinstance(input, types.UnicodeType): return input.encode('utf-8')
	else: return input

# using for override any staff
def overrider(target, holder, name):
	import types
	original = getattr(holder, name)
	overrided = lambda *a, **kw: target(original, *a, **kw)
	if not isinstance(holder, types.ModuleType) and isinstance(original, types.FunctionType):
		setattr(holder, name, staticmethod(overrided))
	elif isinstance(original, property):
		setattr(holder, name, property(overrided))
	else:
		setattr(holder, name, overrided)
def decorator(function):
	def wrapper(*a, **kw):
		def decorate(handler):
			function(handler, *a, **kw)
		return decorate
	return wrapper
override = decorator(overrider)

# useing for read files from VFS
def readVFS(path):
	from ResMgr import openSection, isFile
	file = openSection(path)
	if file is not None and isFile(path):
		return str(file.asBinary)
	return None



import BigWorld
import time
import os
import json
from vehicle_systems.CompoundAppearance import CompoundAppearance
from VehicleStickers import VehicleStickers
from gui.modsListApi import g_modsListApi
from gui.app_loader.loader import g_appLoader
from gui.Scaleform.framework import g_entitiesFactories, ViewSettings, ViewTypes, ScopeTemplates
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.shared import g_eventBus
from gui.shared.events import LobbySimpleEvent
from gui.shared.utils.HangarSpace import g_hangarSpace
from gui import SystemMessages 
from gui.customization.elements import Element

class brandingController():
	
	def __init__(self):
		
		self.__oldCustomization = None
		self.__prevCameraLocation = None
		
		self.config = byteify(json.loads(readVFS('scripts/client/gui/mods/mod_branding/brandingConfig.json')))
		
		self.cache = {
			'current': [0, 1],
			'onlyOnMyTank': False
		}
		
		self.cacheFilePatch = os.path.join(os.path.dirname(unicode(BigWorld.wg_getPreferencesFilePath(), 'utf-8', errors='ignore')), 'branding.json')
		
		if os.path.isfile(self.cacheFilePatch):
			with open(self.cacheFilePatch, 'rb') as fh:
				self.cache = byteify(json.loads(fh.read()))
		
		if not self.findPresetByID(self.cache['current'][0]) or not self.findPresetByID(self.cache['current'][0]):
			self.cache['current'] = [0, 1]
			with open(self.cacheFilePatch, 'wb') as fh:
				fh.write(json.dumps(self.cache, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True))
			
			
		
		g_modsListApi.addModification(
			id = "mod_branding",
			#name = 'Брендированные танки', 
			name = 'Branded tanks', 
			#description = 'Подмена камуфляжей и надписей для команд', 
			description = 'Spoofing camouflage and inscriptions for teams', 
			icon = "scripts/client/gui/mods/mod_branding/brandingIcon.png", 
			enabled = True, 
			login = True, 
			lobby = True, 
			callback = self.loadUI
		)
		
		override(CompoundAppearance, "start")(self.__hooked_start)
		
		@override(VehicleStickers, "__init__")
		def hooked_init(baseMethod, baseObject, vehicleDesc, insigniaRank = 0):
			baseMethod(baseObject, vehicleDesc, insigniaRank)
			baseObject._VehicleStickers__defaultAlpha = 1.0
		
		VehicleStickers.setClanID = lambda *args: None
		
		@override(Element, "__init__")
		def hooked_init(baseMethod, baseObject, params):
			if params['itemID'] >= 5000: params["allowedVehicles"] = ["ussr:MS-1_bot"]
			baseMethod(baseObject, params)
		
		@override(Element, "getPrice")
		def hooked_getPrice(baseMethod, baseObject, duration):
			try: return int(round(baseObject._getPrice(duration) * baseObject._getVehiclePriceFactor() * baseObject._getPriceFactor()))
			except: return 0
		
		g_entitiesFactories.addSettings(ViewSettings('brandingOperator', brandingOperator, 'brandingOperator.swf', ViewTypes.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE))
		g_entitiesFactories.addSettings(ViewSettings('brandingPlayer', brandingPlayer, 'brandingPlayer.swf', ViewTypes.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE))
	
	def loadUI(self): 
		if self.config['UIType'] == 1:
			g_appLoader.getDefLobbyApp().loadView('brandingOperator')
			g_branding.cache['onlyOnMyTank'] = False
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
				
	def __hooked_start(self, baseMethod, baseObject, prereqs):
		
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
			if self.cache['onlyOnMyTank']:
				preset = self.findPresetByID(self.cache['current'][0])
				if preset is not None:
					if baseObject.id == BigWorld.player().playerVehicleID:
						customizeVehicle(preset, baseObject)
					else:
						customizeVehicle(preset, baseObject, True)
			else:
				vehicleInfo = BigWorld.player().arena.vehicles.get(baseObject.id)
				isPlayerTeam = BigWorld.player().team == int(vehicleInfo['team'])
				if isPlayerTeam:
					preset = self.findPresetByID(self.cache['current'][0])
				else:
					preset = self.findPresetByID(self.cache['current'][1])
				if preset is not None:
					customizeVehicle(preset, baseObject)
		else:
			vehicleInfo = BigWorld.player().arena.vehicles.get(baseObject.id)
			
			if vehicleInfo['team'] not in [1, 2]:
				return baseMethod(baseObject, prereqs)
			preset = self.findPresetByID(self.cache['current'][vehicleInfo['team'] - 1])
			if preset is not None:
				customizeVehicle(preset, baseObject)
				
		return baseMethod(baseObject, prereqs)
	
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
		name_1 = self.findPresetByID(self.cache['current'][0])
		name_1 = name_1['name'] if name_1 is not None else "Unknown"
		
		name_2 = self.findPresetByID(self.cache['current'][1])
		name_2 = name_2['name'] if name_2 is not None else "Unknown"
		
		SystemMessages.pushMessage('Team #1 style: "' + name_1 + '" <br>Team #2 style: "' + name_2 + '"', type=SystemMessages.SM_TYPE.Warning)
	
	def pushSystemMessagePlayer(self):
		
		if self.cache['current'][1] != -1:
			
			name_1 = self.findPresetByID(self.cache['current'][0])
			name_1 = name_1['name'] if name_1 is not None else "Unknown"
			
			name_2 = self.findPresetByID(self.cache['current'][1])
			name_2 = name_2['name'] if name_2 is not None else "Unknown"
			
			SystemMessages.pushMessage('Branding for both teams<br><b><font color="#00FF00">' + name_1 + '</font> vs <font color="#FF0000">' + name_2 + '</font></b>', type=SystemMessages.SM_TYPE.Warning)
			
		else:
		
			name_1 = self.findPresetByID(self.cache['current'][0])
			name_1 = name_1['name'] if name_1 is not None else "Unknown"
			
			SystemMessages.pushMessage('Branding for your vehicle<br><b><font color="#00FF00">' + name_1 + '</font></b>', type=SystemMessages.SM_TYPE.Warning)

class brandingOperator(AbstractWindowView):
	
	def _populate(self):
		super(brandingOperator, self)._populate()
		if self._isDAAPIInited():
			presets = []
			for preset in g_branding.config['presets']:
				presets.append(preset['name'])	
			settings = [g_branding.cache['current'], presets]
			self.flashObject.as_syncData(settings)
		
	def onWindowClose(self):
		g_branding.restoreHangarVehicle()
		self.destroy()

	def onTryClosing(self):
		return True

	def as_isModalS(self):
		if self._isDAAPIInited():
			return False
	
	def onSettingsS(self, team1, team2):
		
		g_branding.cache['current'] = [int(team1), int(team2)]
		g_branding.cache['onlyOnMyTank'] = False
		g_branding.pushSystemMessageOperator()
		
		
		with open(g_branding.cacheFilePatch, 'wb') as fh:
			fh.write(json.dumps(g_branding.cache, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True))
		
		g_branding.restoreHangarVehicle()
		
	def onShowPresetS(self, id):
		g_branding.showPresetInHangar(int(id))

class brandingPlayer(AbstractWindowView):
	
	def _populate(self):
		super(brandingPlayer, self)._populate()
		
		def get_image_path(path):
			return '/'.join(['scripts', 'client', 'gui', 'mods', 'mod_branding', 'resources', path])
		
		if self._isDAAPIInited():
			presets = []
			for preset in g_branding.config['presets']:
				presets.append({
					"id": preset["id"],
					"name": preset["name"],
					"icon": get_image_path(preset["preview"]["image"]) if preset["preview"]["enable"] else None
				})
			self.flashObject.as_syncData(presets, g_branding.cache['onlyOnMyTank'])
		
	def onWindowClose(self):
		g_branding.restoreHangarVehicle()
		self.destroy()
		
	def finishSetupS(self, team1, team2, onlyOnMyTank):
		g_branding.cache['current'] = [int(team1), int(team2)]
		g_branding.cache['onlyOnMyTank'] = onlyOnMyTank
		g_branding.pushSystemMessagePlayer()
		
		with open(g_branding.cacheFilePatch, 'wb') as fh:
			fh.write(json.dumps(g_branding.cache, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True))
		
		g_branding.restoreHangarVehicle()
		
		self.onWindowClose()

	def onTryClosing(self):
		return True

	def as_isModalS(self):
		if self._isDAAPIInited():
			return False
	
g_branding = brandingController()
