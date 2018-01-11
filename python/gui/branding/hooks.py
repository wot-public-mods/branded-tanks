
from gui.app_loader.loader import _AppLoader
from gui.modsListApi import g_modsListApi
from vehicle_systems.CompoundAppearance import CompoundAppearance

from gui.branding.events import g_eventsManager
from gui.branding.lang import l10n
from gui.branding.utils import override

__all__ = ( )

@override(CompoundAppearance, '_CompoundAppearance__getVehicleOutfit')
def start(baseMethod, baseInstance):
	from gui.branding.controllers import g_controllers
	outfit = baseMethod(baseInstance)
	return g_controllers.vehicle.processVehicleOutfit(baseInstance, outfit)

@override(_AppLoader, 'fini')
def hooked_fini(baseMethod, baseObject):
	g_eventsManager.onAppFinish()
	baseMethod(baseObject)

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