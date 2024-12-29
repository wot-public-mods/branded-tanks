# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2024 Andrii Andrushchyshyn

import Event

__all__ = ('g_eventsManager', )

class EventsManager(object):

	def __init__(self):
		self.showUI = Event.Event()
		self.onAppFinish = Event.Event()

g_eventsManager = EventsManager()
