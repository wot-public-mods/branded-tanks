import types
import ResMgr

__all__ = ('byteify', 'override', 'readFromVFS', 'getFashionValue', 'parseLangFields', 'getHangarVehicle',
		'getIconPatch', 'readBrandingItem', )

def override(holder, name, wrapper=None, setter=None):
	"""Override methods, properties, functions, attributes
	:param holder: holder in which target will be overrided
	:param name: name of target to be overriden
	:param wrapper: replacement for override target
	:param setter: replacement for target property setter"""
	if wrapper is None:
		return lambda wrapper, setter=None: override(holder, name, wrapper, setter)
	target = getattr(holder, name)
	wrapped = lambda *a, **kw: wrapper(target, *a, **kw)
	if not isinstance(holder, types.ModuleType) and isinstance(target, types.FunctionType):
		setattr(holder, name, staticmethod(wrapped))
	elif isinstance(target, property):
		prop_getter = lambda *a, **kw: wrapper(target.fget, *a, **kw)
		prop_setter = target.fset if not setter else lambda *a, **kw: setter(target.fset, *a, **kw)
		setattr(holder, name, property(prop_getter, prop_setter, target.fdel))
	else:
		setattr(holder, name, wrapped)

def byteify(data):
	"""Encodes data with UTF-8
	:param data: Data to encode"""
	result = data
	if isinstance(data, dict):
		result = {byteify(key): byteify(value) for key, value in data.iteritems()}
	elif isinstance(data, (list, tuple, set)):
		result = [byteify(element) for element in data]
	elif isinstance(data, unicode):
		result = data.encode('utf-8')
	return result

def parseLangFields(langFile):
	"""split items by lines and key value by ':'
	like yaml format"""
	result = {}
	langData = readFromVFS(langFile)
	if langData:
		for item in langData.splitlines():
			if ': ' not in item:
				continue
			key, value = item.split(": ", 1)
			result[key] = value
	return result

def readFromVFS(path):
	"""using for read files from VFS"""
	file = ResMgr.openSection(path)
	if file is not None and ResMgr.isFile(path):
		return str(file.asBinary)
	return None

def getFashionValue(current, saved, custom, index, type, isClean=False):
	"""generation value by data for vehicle fashion:
	camouflages, emblems, inscriptions"""
	if saved is not None:
		current = saved[type]
	result = custom
	if custom == -1 or isClean:
		result = None
	elif custom == 0:
		result = current[index][0]
	return result

def getHangarVehicle():
	from helpers import dependency
	from skeletons.gui.shared.utils import IHangarSpace
	try:
		hangarSpace = dependency.instance(IHangarSpace)
		appereance = hangarSpace.space._ClientHangarSpace__vAppearance
		vDesc = appereance._VehicleAppearance__vDesc
		vState = appereance._VehicleAppearance__vState
	except: #NOSONAR
		vDesc, vState = None, None
	return vDesc, vState

def getIconPatch(preset):
	if preset['preview']['enable']:
		return '/'.join(['mods', 'net.wargaming.branding', preset['preview']['image']])
	return None

def readBrandingItem(itemCls, itemName, cache, storage):
	from gui.branding._constants import XML_FILE_PATH
	from items.readers.c11n_readers import _readItems
	itemsFileName = XML_FILE_PATH % itemName
	dataSection = ResMgr.openSection(itemsFileName)
	try:
		_readItems(cache, itemCls, (None, 'branding_%ss.xml' % itemName), dataSection, itemName, storage)
	finally:
		ResMgr.purge(itemsFileName)
