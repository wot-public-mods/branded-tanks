__author__ = "Andrii Andrushchyshyn"
__copyright__ = "Copyright 2023, poliroid"
__credits__ = ["Andrii Andrushchyshyn"]
__license__ = "CC BY-NC-SA 4.0"
__version__ = "4.2.5"
__maintainer__ = "Andrii Andrushchyshyn"
__email__ = "contact@poliroid.me"
__status__ = "Production"

from .data import *
from .hooks import *
from .controllers import g_controllers
from .views import *
from .events import g_eventsManager

__all__ = ('init', 'fini')

def init():
	g_controllers.init()

def fini():
	g_eventsManager.onAppFinish()
