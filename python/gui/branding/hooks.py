
from gui.app_loader.loader import _AppLoader
from gui.modsListApi import g_modsListApi
from vehicle_systems.CompoundAppearance import CompoundAppearance

from gui.branding.events import g_eventsManager
from gui.branding.lang import l10n
from gui.branding.utils import override, readBrandingItem

__all__ = ( )

@override(CompoundAppearance, '_CompoundAppearance__applyVehicleOutfit')
def applyVehicleOutfit(baseMethod, baseInstance):
	from gui.branding.controllers import g_controllers
	baseOutfit = baseInstance._CompoundAppearance__outfit
	baseInstance._CompoundAppearance__outfit = g_controllers.vehicle.getVehicleOutfit(baseInstance, baseOutfit)
	return baseMethod(baseInstance)

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

# new customization inject
from items.vehicles import g_cache
from items.components.c11n_components import CamouflageItem, DecalItem
cache = g_cache.customization20()
readBrandingItem(CamouflageItem, 'camouflage', cache, cache.camouflages)
readBrandingItem(DecalItem, 'decal', cache, cache.decals)
