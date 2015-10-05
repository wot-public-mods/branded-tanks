


# WOT_INFO ==> GUI_MODS MODS PATH VERSION
exec 'eJyNjk1vAiEQhu/7K+YGJAT7cdP00KZfHnSNa/VgjGGB3U7Lwgaw7c8vGzX22NszzPPOSxN8Bz6KXqZ3wK73IQFGjQFkBFk0w3\
pp4qwN563vjauMSujd4NRH5wHbjQ9Wn63vdt+atAheH1RamxBPelNouIOGMhF7i4kSTljR+AAK0EFNiRCj4S9R/HSWsC1ZDAPZiS9pDy\
ZSNi4AG5BUCRmrFNC1bAwm37w8TKAORn4WysoYYVOu9tP5c5mDs/KxyiYZEfHh0dGt4UCiCtinSDIqi8algTqvcymbwOJ+9ZojZgLrp2\
U1Led5oOgS1durHeNwxOsL3lzwdsfyhZe36f7/xe0B//YX2liQHGoOioPmkIPNL83ZhzY='.decode('base64').decode('zlib')



import Event
from constants import AUTH_REALM
from gui.Scaleform.framework import g_entitiesFactories, ViewSettings, GroupedViewSettings, ViewTypes, ScopeTemplates
from gui.Scaleform.framework.entities.View import View
from gui.Scaleform.framework.entities.abstract.AbstractPopOverView import AbstractPopOverView
from gui.Scaleform.framework.entities.abstract.AbstractViewMeta import AbstractViewMeta
from gui.app_loader.loader import g_appLoader
from gui.shared import events, g_eventBus

print "[NOTE] package loaded: mod_modsListAPI"


class ModsLauncherController(object):
	
	def __init__(self):
		
		# Mods collector
		self.mods = dict()
		
		# Lobby switcher
		self.isLobby = True
		
		# State and Cache Events
		self.onButtonBlinking = Event.Event()
		self.onListUpdated = Event.Event()
		
		# Lang Params
		if AUTH_REALM in ['RU', 'CT']:
			self.tooltipText = 'Список модификаций: удобный запуск, настройка и оповещение.'
			self.titleText = 'Список модификаций'
		else:
			self.tooltipText = 'Modifications list: comfortable run, setup and alert.'
			self.titleText = 'Modifications list'
	
	def addMod(self, id, name = None, description = None, icon = None, enabled = None, login = None, lobby = None, callback = None):
		
		# Update if exist
		if id in self.mods.keys(): 
			self.updateMod(id, name, description, icon, enabled, login, lobby, callback)
			return
		
		# Attr cheack
		if name is None or description is None or icon is None or enabled is None or login is None or lobby is None or callback is None:
			return
		
		# Adding to modslist
		self.mods[id] = {
			'id': id, 
			'name': name, 
			'icon': icon, 
			'description': description, 
			'enabled': enabled, 
			'login': login, 
			'lobby': lobby, 
			'callback': callback,
			'alert': False
		}
		
		# Updating List
		self.onListUpdated()
		
	def updateMod(self, id, name = None, description = None, icon = None, enabled = None, login = None, lobby = None, callback = None):
		
		# If not inited, return
		if id not in self.mods.keys(): 
			return
		
		# sheat copying
		old = dict(self.mods[id])
		
		# Updating mod attrs
		self.mods[id] = {
			'id': id, 
			'name': name if name is not None else old['name'], 
			'description': description if description is not None else old['description'], 
			'icon': icon if icon is not None else old['icon'], 
			'enabled': enabled if enabled is not None else old['enabled'], 
			'login': login if login is not None else old['login'], 
			'lobby': lobby if lobby is not None else old['lobby'], 
			'callback': callback if callback is not None else old['callback'],
			'alert': old['alert']
		}
		
		# Updating List
		self.onListUpdated() 

	def alertMod(self, id):
		
		# If not exist return
		if id not in self.mods.keys(): 
			return
		
		# Changing mod State
		self.mods[id]['alert'] = True
		
		# Updating List
		self.onListUpdated()
		
		# Button Blink
		self.onButtonState() 

	def clearAlert(self, id):
		
		# If not exist return
		if id not in self.mods.keys(): 
			return
		
		# Changing mod State
		self.mods[id]['alert'] = False
		
		# Updating List
		self.onListUpdated()
		
	def getModsList(self):
		
		# Generating mods list for views: hangar / login 
		result = list()
		for item in self.mods.values():
			if self.isLobby and item['lobby']: result.append(item)
			elif not self.isLobby and item['login']: result.append(item)
		return result
		
	def callMod(self, id):
		
		# If not exist return
		if id not in self.mods.keys(): 
			return
		
		# Calling callback
		func = self.mods[id]['callback']
		func()



class ModsListButton(View, AbstractViewMeta):

	def _populate(self):
		super(ModsListButton, self)._populate()
		g_modsListApi.onButtonBlinking += self.__handleButtonBlinking
		# Lang settings
		if self._isDAAPIInited():
			self.flashObject.as_setTooltipText(g_modsListApi.tooltipText)

	def _dispose(self):
		g_modsListApi.onButtonBlinking -= self.__handleButtonBlinking  
		super(ModsListButton, self)._dispose()	   
		
	def modsMenuButtonClickS(self):
		# Opening menu
		g_appLoader.getDefLobbyApp().loadView('modsListPopover')
			
	def fromLobbyS(self, isLobby):
		# Changing current view
		g_modsListApi.isLobby = isLobby
	
	def __handleButtonBlinking(self):
		if self._isDAAPIInited():
			return self.flashObject.as_handleModAlert()
	
	def onWindowClose(self):
		self.destroy()
		
	def onFocusIn(self, *args):
		if self._isDAAPIInited():
			return False						 



class ModsListPopover(AbstractPopOverView):
	
	def _populate(self):
		super(ModsListPopover, self)._populate()
		g_modsListApi.onListUpdated += self.__handleListUpdate				   
		if self._isDAAPIInited():
			self.flashObject.as_setTitleText(g_modsListApi.titleText)
	
	def _dispose(self):
		g_modsListApi.onListUpdated -= self.__handleListUpdate  
		super(ModsListPopover, self)._dispose()	   
		
	def __collectModsData(self):
		mods = g_modsListApi.getModsList()
		self.as_setDataS(mods)
		
	def __handleListUpdate(self):
		self.__collectModsData()
		
	def clearAlertS(self, id):
		g_modsListApi.clearAlert(id)
		
	def getModsListS(self):
		self.__collectModsData()  
		
	def callModS(self, id):
		g_modsListApi.callMod(id)
		
	def as_handleModAlertS(self, id):
		if self._isDAAPIInited():
			return self.flashObject.as_handleModAlert(id)
		
	def as_setDataS(self, data):
		if self._isDAAPIInited():
			return self.flashObject.as_setData(data)



g_modsListApi = ModsLauncherController()
_button = ViewSettings('modsListButton', ModsListButton, '../../scripts/client/gui/mods/modsListApi/button.swf', ViewTypes.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE)	  
_popover = GroupedViewSettings('modsListPopover', ModsListPopover, '../../scripts/client/gui/mods/modsListApi/popover.swf', ViewTypes.WINDOW, 'modsListPopover', 'modsListPopover', ScopeTemplates.DEFAULT_SCOPE)  
g_entitiesFactories.addSettings(_popover)
g_entitiesFactories.addSettings(_button)
g_eventBus.addListener(events.AppLifeCycleEvent.INITIALIZED, lambda *args : g_appLoader.getDefLobbyApp().loadView('modsListButton'))