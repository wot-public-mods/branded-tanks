# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2024 Andrii Andrushchyshyn

import json
import os

from .events import g_eventsManager
from .lang import l10n
from .utils import byteify, vfs_file_read
from ._constants import SETTINGS_FILE

__all__ = ('g_dataHolder', )

class DataHolder(object):

	@property
	def cache(self):
		return self.__cache

	@property
	def config(self):
		return self.__config

	def __init__(self):

		# embedded in a package
		self.__config = byteify(json.loads(vfs_file_read('mods/net.wargaming.branding/config.json')))

		for idx, preset in enumerate(self.__config['presets']):
			if 'l10n:' in preset['name']:
				self.__config['presets'][idx]['name'] = l10n(preset['name'].replace('l10n:', ''))

		self.__cache = {
			'currentSetup': [1, 2],
			'onlyOnMyTank': False
		}

		self.__loadCache()

		g_eventsManager.onAppFinish += self.__saveCache

	def __loadCache(self):
		settings_dir = os.path.dirname(SETTINGS_FILE)
		if not os.path.isdir(settings_dir):
			os.makedirs(settings_dir)
		if os.path.isfile(SETTINGS_FILE):
			with open(SETTINGS_FILE, 'rb') as fh:
				self.__cache = byteify(json.loads(fh.read()))

	def __saveCache(self):
		with open(SETTINGS_FILE, 'wb') as fh:
			fh.write(json.dumps(self.__cache))

g_dataHolder = DataHolder()
