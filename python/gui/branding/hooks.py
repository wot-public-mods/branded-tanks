
from gui.app_loader.loader import _AppLoader
from gui.branding.events import g_eventsManager
from gui.branding.utils import override
from gui.customization.elements import Element
from vehicle_systems.CompoundAppearance import CompoundAppearance
from VehicleStickers import VehicleStickers

__all__ = ( )

@override(CompoundAppearance, 'start')
def test(baseMethod, baseInstance, prereqs):
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
