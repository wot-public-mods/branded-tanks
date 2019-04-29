from gui.app_loader.loader import g_appLoader
from gui.branding.data import g_dataHolder
from gui.branding.branding_constants import BRANDING_OPERATOR_WINDOW_UI, BRANDING_PLAYER_WINDOW_UI, UI_TYPE
from gui.branding.events import g_eventsManager
from gui.branding.views.operatorView import BrandingOperatorView
from gui.branding.views.playerView import BrandingPlayerView
from gui.Scaleform.framework import g_entitiesFactories, ViewSettings, ViewTypes, ScopeTemplates
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams

def getViewSettings():
	viewSettings = []
	viewSettings.append(ViewSettings(BRANDING_OPERATOR_WINDOW_UI, BrandingOperatorView, 'brandingOperator.swf',
			ViewTypes.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE))
	viewSettings.append(ViewSettings(BRANDING_PLAYER_WINDOW_UI, BrandingPlayerView, 'brandingPlayer.swf',
			ViewTypes.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE))
	return viewSettings

for settings in getViewSettings():
	g_entitiesFactories.addSettings(settings)

def showUI():
	app = g_appLoader.getDefLobbyApp()
	if g_dataHolder.config['UIType'] == UI_TYPE.OPERATOR:
		g_dataHolder.cache['onlyOnMyTank'] = False
		app.loadView(SFViewLoadParams(BRANDING_OPERATOR_WINDOW_UI))
	elif g_dataHolder.config['UIType'] == UI_TYPE.PLAYER:
		app.loadView(SFViewLoadParams(BRANDING_PLAYER_WINDOW_UI))

g_eventsManager.showUI += showUI
