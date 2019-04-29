import json
import os

import BigWorld
from gui.branding.events import g_eventsManager
from gui.branding.lang import l10n
from gui.branding.utils import byteify, readFromVFS

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
		self.__config = byteify(json.loads(readFromVFS('mods/net.wargaming.branding/config.json')))

		for idx, preset in enumerate(self.__config['presets']):
			if 'l10n:' in preset['name']:
				self.__config['presets'][idx]['name'] = l10n(preset['name'].replace('l10n:', ''))

		# stored in appdata
		self.__cacheFilePatch = os.path.join(os.path.dirname(unicode(BigWorld.wg_getPreferencesFilePath(),
																	'utf-8', errors='ignore')), 'branding.json')

		self.__cache = {
			'currentSetup': [0, 1],
			'onlyOnMyTank': False
		}

		self.__loadCache()

		g_eventsManager.onAppFinish += self.__saveCache

	def __loadCache(self):
		if os.path.isfile(self.__cacheFilePatch):
			with open(self.__cacheFilePatch, 'rb') as fh:
				self.__cache = byteify(json.loads(fh.read()))

	def __saveCache(self):
		with open(self.__cacheFilePatch, 'wb') as fh:
			fh.write(json.dumps(self.__cache, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True))

g_dataHolder = DataHolder()
