from debug_utils import LOG_ERROR
from gui.branding.events import g_eventsManager
from gui.branding.lang import l10n
from gui.branding.utils import override, readBrandingItem
from items.vehicles import g_cache
from items.components.c11n_components import CamouflageItem, DecalItem, PaintItem
from vehicle_systems.CompoundAppearance import CompoundAppearance

__all__ = ()

@override(CompoundAppearance, '_prepareOutfit')
def applyVehicleOutfit(baseMethod, baseInstance, outfitCD):
	from gui.branding.controllers import g_controllers
	outfit = g_controllers.vehicle.getVehicleOutfit(baseInstance, baseInstance.outfit)
	return outfit or baseMethod(baseInstance, outfitCD)

# modsListApi
g_modsListApi = None
try:
	from gui.modsListApi import g_modsListApi
except ImportError:
	LOG_ERROR('modsListApi not installed')
if g_modsListApi:
	g_modsListApi.addModification(id='branding', name=l10n('modslist.name'), enabled=True,
		description=l10n('modslist.description'), icon='gui/maps/icons/brandingIcon.png',
		login=True, lobby=True, callback=g_eventsManager.showUI)

# new customization inject
cache = g_cache.customization20()
readBrandingItem(CamouflageItem, 'camouflage', cache, cache.camouflages)
readBrandingItem(DecalItem, 'decal', cache, cache.decals)
readBrandingItem(PaintItem, 'paint', cache, cache.paints)
