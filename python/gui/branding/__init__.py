__author__ = "Andruschyshyn Andrey"
__copyright__ = "Copyright 2020, poliroid"
__credits__ = ["Andruschyshyn Andrey"]
__license__ = "CC BY-NC-SA 4.0"
__version__ = "4.1"
__maintainer__ = "Andruschyshyn Andrey"
__email__ = "p0lir0id@yandex.ru"
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
