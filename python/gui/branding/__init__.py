__author__ = "Andruschyshyn Andrey"
__copyright__ = "Copyright 2019, Wargaming"
__credits__ = ["Andruschyshyn Andrey"]
__license__ = "CC BY-NC-SA 4.0"
__version__ = "3.6"
__maintainer__ = "Andruschyshyn Andrey"
__email__ = "prn.a_andruschyshyn@wargaming.net"
__status__ = "Production"

__all__ = ()

from gui.branding.data import *
from gui.branding.hooks import *
from gui.branding.controllers import g_controllers
from gui.branding.views import *

g_controllers.init()
