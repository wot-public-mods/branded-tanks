
from gui.app_loader.loader import _AppLoader
from gui.branding.events import g_eventsManager
from gui.branding.lang import l10n
from gui.branding.utils import override
from gui.customization.elements import Element
from gui.modsListApi import g_modsListApi
from items.vehicles import VehicleDescriptor
from vehicle_systems.CompoundAppearance import CompoundAppearance
from VehicleStickers import VehicleStickers

__all__ = ( )

@override(VehicleDescriptor, 'makeCompactDescr')
def makeCompactDescr(baseMethod, baseInstance):
	
	savedCamouflages = tuple(baseInstance.camouflages)
	if hasattr(baseInstance, 'backup_camouflages'):
		baseInstance.camouflages = baseInstance.backup_camouflages
	else:
		savedCamouflages = None
	
	savedInscriptions = tuple(baseInstance.playerInscriptions)
	if hasattr(baseInstance, 'backup_inscriptions'):
		baseInstance.playerInscriptions = baseInstance.backup_inscriptions
	else:
		savedInscriptions = None
	
	savedEmblems = tuple(baseInstance.playerEmblems)
	if hasattr(baseInstance, 'backup_emblems'):
		baseInstance.playerEmblems = baseInstance.backup_emblems
	else:
		savedEmblems = None
	
	base = baseMethod(baseInstance)
	
	if savedCamouflages:
		baseInstance.camouflages = savedCamouflages
	
	if savedInscriptions:
		baseInstance.playerInscriptions = savedInscriptions
	
	if savedEmblems:
		baseInstance.playerEmblems = savedEmblems 
	
	return base

@override(CompoundAppearance, 'start')
def start(baseMethod, baseInstance, prereqs):
	from gui.branding.controllers import g_controllers
	g_controllers.vehicle.processCompoundAppearance(baseInstance)
	return baseMethod(baseInstance, prereqs)

@override(Element, '__init__')
def init(baseMethod, baseInstance, params):
	if params['itemID'] >= 5000: 
		params["allowedVehicles"] = ["ussr:MS-1_bot"]
	baseMethod(baseInstance, params)

@override(Element, 'getPrice')
def getPrice(baseMethod, baseInstance, duration):
	try: 
		return int(round(baseInstance._getPrice(duration) * baseInstance._getVehiclePriceFactor() * baseInstance._getPriceFactor()))
	except: 
		return 0

@override(VehicleStickers, '__init__')
def init(baseMethod, baseInstance, vehicleDesc, insigniaRank = 0):
	baseMethod(baseInstance, vehicleDesc, insigniaRank)
	baseInstance._VehicleStickers__defaultAlpha = 1.0

@override(VehicleStickers, 'setClanID')
def setClanID(baseMethod, baseInstance, clanID):
	pass

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