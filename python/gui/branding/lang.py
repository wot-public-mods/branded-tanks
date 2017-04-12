
from constants import DEFAULT_LANGUAGE
from helpers import getClientLanguage

from gui.branding.branding_constants import DEFAULT_UI_LANGUAGE, LANGUAGE_CODES
from gui.branding.utils import parseLangFields

__all__ = ('l10n', )

_LANGUAGES = {}

for langCode in LANGUAGE_CODES:
	_LANGUAGES[langCode] = parseLangFields(langCode)

_CLIENT_LANGUAGE = getClientLanguage()
if _CLIENT_LANGUAGE in _LANGUAGES.keys():
	_LANGUAGE = _LANGUAGES[_CLIENT_LANGUAGE]
elif DEFAULT_LANGUAGE in _LANGUAGES.keys():
	_LANGUAGE = _LANGUAGES[DEFAULT_LANGUAGE]
else:
	_LANGUAGE = _LANGUAGES[DEFAULT_UI_LANGUAGE]

def l10n(key):
	'''returns localized value relative to key'''
	if key in _LANGUAGE:
		return _LANGUAGE[key]
	elif key in _LANGUAGES[DEFAULT_UI_LANGUAGE]:
		return _LANGUAGES[DEFAULT_UI_LANGUAGE][key]
	else:
		return key
	