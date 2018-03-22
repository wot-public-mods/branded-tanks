
import ResMgr
import types

__all__ = ('byteify', 'override', 'readFromVFS', 'getFashionValue', 'parseLangFields', 'getHangarVehicle', \
		'getIconPatch', )

def overrider(target, holder, name):
	"""using for override any staff"""
	original = getattr(holder, name)
	overrided = lambda *a, **kw: target(original, *a, **kw)
	if not isinstance(holder, types.ModuleType) and isinstance(original, types.FunctionType):
		setattr(holder, name, staticmethod(overrided))
	elif isinstance(original, property):
		setattr(holder, name, property(overrided))
	else:
		setattr(holder, name, overrided)
def decorator(function):
	def wrapper(*args, **kwargs):
		def decorate(handler):
			function(handler, *args, **kwargs)
		return decorate
	return wrapper
override = decorator(overrider)

def byteify(data):
	"""using for convert unicode key/value to utf-8"""
	if isinstance(data, types.DictType): 
		return { byteify(key): byteify(value) for key, value in data.iteritems() }
	elif isinstance(data, types.ListType) or isinstance(data, tuple) or isinstance(data, set):
		return [ byteify(element) for element in data ]
	elif isinstance(data, types.UnicodeType):
		return data.encode('utf-8')
	else: 
		return data

def parseLangFields(langFile):
	"""split items by lines and key value by ':'
	like yaml format"""
	result = {}
	langData = readFromVFS(langFile)
	if langData:
		for item in langData.splitlines():
			if ': ' not in item: continue
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
	if custom == -1 or isClean: 
		return None
	elif custom == 0: 
		return current[index][0]
	else: 
		return custom

def getHangarVehicle():
	from gui.shared.utils.HangarSpace import g_hangarSpace
	try:
		appereance = g_hangarSpace.space._ClientHangarSpace__vAppearance
		vDesc = appereance._VehicleAppearance__vDesc
		vState = appereance._VehicleAppearance__vState	
	except:
		vDesc, vState = None, None
	return (vDesc, vState)

def getIconPatch(preset):
	if preset['preview']['enable']:
		return '/'.join(['mods', 'net.wargaming.branding', preset['preview']['image']])
	return None
