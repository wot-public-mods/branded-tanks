__author__ = "Andruschyshyn Andrey"
__copyright__ = "Copyright 2019, Wargaming"
__credits__ = ["Andruschyshyn Andrey"]
__license__ = "CC BY-NC-SA 4.0"
__version__ = "3.7"
__maintainer__ = "Andruschyshyn Andrey"
__email__ = "prn.a_andruschyshyn@wargaming.net"
__status__ = "Production"

from gui.branding.data import *
from gui.branding.hooks import *
from gui.branding.controllers import g_controllers
from gui.branding.views import *
from gui.branding.events import g_eventsManager

__all__ = ('init', 'fini')

def init():
	g_controllers.init()

def fini():
	g_eventsManager.onAppFinish()
