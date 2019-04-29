import types
import ResMgr

__all__ = ('byteify', 'override', 'readFromVFS', 'getFashionValue', 'parseLangFields', 'getHangarVehicle',
		'getIconPatch', 'readBrandingItem', )

def override(holder, name, target=None):
	"""using for override any staff"""
	if target is None:
		return lambda target: override(holder, name, target)
	original = getattr(holder, name)
	overrided = lambda *a, **kw: target(original, *a, **kw)
	if not isinstance(holder, types.ModuleType) and isinstance(original, types.FunctionType):
		setattr(holder, name, staticmethod(overrided))
	elif isinstance(original, property):
		setattr(holder, name, property(overrided))
	else:
		setattr(holder, name, overrided)

def byteify(data):
	"""using for convert unicode key/value to utf-8"""
	result = data
	if isinstance(data, types.DictType):
		result = {byteify(key): byteify(value) for key, value in data.iteritems()}
	elif isinstance(data, (set, tuple, types.ListType)):
		result = [byteify(element) for element in data]
	elif isinstance(data, types.UnicodeType):
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
	from gui.branding.branding_constants import XML_FILE_PATH
	from items.readers.c11n_readers import _readItems
	itemsFileName = XML_FILE_PATH % itemName
	dataSection = ResMgr.openSection(itemsFileName)
	try:
		_readItems(cache, itemCls, (None, 'branding_%ss.xml' % itemName), dataSection, itemName, storage)
	finally:
		ResMgr.purge(itemsFileName)
