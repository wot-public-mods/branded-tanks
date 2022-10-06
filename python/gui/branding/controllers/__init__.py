from ..events import g_eventsManager

__all__ = ('g_controllers', )

class ControllersHolder():

	processor = None
	vehicle = None

	def init(self):
		from .processor import ProcessorController
		from .vehicle import VehicleController

		self.processor = ProcessorController()
		self.vehicle = VehicleController()

		g_eventsManager.onAppFinish += self.fini

	def fini(self):

		self.processor = None
		self.vehicle = None

g_controllers = ControllersHolder()
