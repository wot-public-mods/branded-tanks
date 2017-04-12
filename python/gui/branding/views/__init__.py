
from gui.Scaleform.framework import g_entitiesFactories, ViewSettings, ViewTypes, ScopeTemplates

from gui.branding.branding_constants import BRANDING_OPERATOR_WINDOW_UI, BRANDING_PLAYER_WINDOW_UI
from gui.branding.views.operatorView import BrandingOperatorView
from gui.branding.views.playerView import BrandingPlayerView

def getViewSettings():
	return ( ViewSettings(BRANDING_OPERATOR_WINDOW_UI, BrandingOperatorView, 'brandingOperator.swf', ViewTypes.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE ), 
			 ViewSettings(BRANDING_PLAYER_WINDOW_UI, BrandingPlayerView, 'brandingPlayer.swf', ViewTypes.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE ), )

for settings in getViewSettings():
	g_entitiesFactories.addSettings(settings)
