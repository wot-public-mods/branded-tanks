# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2024 Andrii Andrushchyshyn

__version__ = "4.3.1"

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
