
import BigWorld
import os
from external_strings_utils import unicode_from_utf8

LANGUAGE_CODES = ('ru', 'uk', 'be', 'en', 'de', 'et', 'bg', 'da', 'fi', 'fil', 'fr', 'el', 'hu', 'id',
	'it', 'ja', 'ms', 'nl', 'no', 'pl', 'pt', 'pt_br', 'ro', 'sr', 'vi', 'zh_sg', 'zh_tw', 'hr', 'th',
	'lv', 'lt', 'cs', 'es_ar', 'tr', 'zh_cn', 'es', 'kk', 'sv', )

LANGUAGE_FILE_PATH = 'mods/net.wargaming.branding/text/%s.yml'

XML_FILE_PATH = 'mods/net.wargaming.branding/xml/%ss.xml'

DEFAULT_UI_LANGUAGE = 'ru'

BRANDING_OPERATOR_WINDOW_UI = 'brandingObserver'
BRANDING_PLAYER_WINDOW_UI = 'brandingPlayer'

class UI_TYPE:
	OPERATOR = 1
	PLAYER = 2

prefsFilePath = unicode_from_utf8(BigWorld.wg_getPreferencesFilePath())[1]
SETTINGS_FILE = os.path.normpath(os.path.join(os.path.dirname(prefsFilePath), 'mods', 'branding.json'))
