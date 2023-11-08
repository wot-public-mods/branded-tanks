
from gui.Scaleform.framework import g_entitiesFactories, ViewSettings, ScopeTemplates
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.shared.personality import ServicesLocator
from frameworks.wulf import WindowLayer

from ..data import g_dataHolder
from ..events import g_eventsManager
from ..utils import getParentWindow
from .._constants import BRANDING_OPERATOR_WINDOW_UI, BRANDING_PLAYER_WINDOW_UI, UI_TYPE
from .operatorView import BrandingOperatorView
from .playerView import BrandingPlayerView

def getViewSettings():
	viewSettings = []
	viewSettings.append(ViewSettings(BRANDING_OPERATOR_WINDOW_UI, BrandingOperatorView, 'brandingOperator.swf',
			WindowLayer.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE))
	viewSettings.append(ViewSettings(BRANDING_PLAYER_WINDOW_UI, BrandingPlayerView, 'brandingPlayer.swf',
			WindowLayer.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE))
	return viewSettings

for settings in getViewSettings():
	g_entitiesFactories.addSettings(settings)

def showUI():
	app = ServicesLocator.appLoader.getDefLobbyApp()
	if g_dataHolder.config['UIType'] == UI_TYPE.OPERATOR:
		g_dataHolder.cache['onlyOnMyTank'] = False
		app.loadView(SFViewLoadParams(BRANDING_OPERATOR_WINDOW_UI, parent=getParentWindow()))
	elif g_dataHolder.config['UIType'] == UI_TYPE.PLAYER:
		app.loadView(SFViewLoadParams(BRANDING_PLAYER_WINDOW_UI, parent=getParentWindow()))

g_eventsManager.showUI += showUI
