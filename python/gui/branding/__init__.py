
__all__ = ( )

# initialization
from gui.branding.data import *
from gui.branding.hooks import *
from gui.branding.controllers import *
from gui.branding.views import *

# firing init for controllers
g_controllers.init()

# for modsListApi
from gui.modsListApi import g_modsListApi
from gui.branding.lang import l10n
from gui.branding.events import g_eventsManager
g_modsListApi.addModification(
	id = 'branding',
	name = l10n('modsListApi.name'),
	description = l10n('modsListApi.description'),
	icon = 'gui/maps/icons/brandingIcon.png',
	enabled = True,
	login = True,
	lobby = True,
	callback = g_eventsManager.showUI
)