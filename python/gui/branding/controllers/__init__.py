
from gui.branding.events import g_eventsManager

__all__ = ('g_controllers', )

class ControllersHolder():
	
	processor = None
	vehicle = None
	
	def init(self):
		
		from gui.branding.controllers.processor import ProcessorController
		from gui.branding.controllers.vehicle import VehicleController
		
		self.processor = ProcessorController()
		self.vehicle = VehicleController()
		
		self.processor.init()
		self.vehicle.init()
		
		g_eventsManager.onAppFinish += self.fini
	
	def fini(self):
		
		self.processor.fini()
		self.vehicle.fini()
		
		self.processor = None
		self.vehicle = None
	
g_controllers = ControllersHolder()
