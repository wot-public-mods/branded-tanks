__author__ = "Andrii Andrushchyshyn"
__copyright__ = "Copyright 2022, poliroid"
__credits__ = ["Andrii Andrushchyshyn"]
__license__ = "CC BY-NC-SA 4.0"
__version__ = "4.2.1"
__maintainer__ = "Andrii Andrushchyshyn"
__email__ = "contact@poliroid.me"
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
