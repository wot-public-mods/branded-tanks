# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2025 Andrii Andrushchyshyn

import BigWorld
import os
from external_strings_utils import unicode_from_utf8

# Language
LANGUAGE_FILES = 'mods/net.wargaming.branding/text'
LANGUAGE_DEFAULT = 'en'
LANGUAGE_FALLBACK = ('ru', 'be', 'kk', )

XML_FILE_PATH = 'mods/net.wargaming.branding/xml/%ss.xml'

DEFAULT_UI_LANGUAGE = 'ru'

BRANDING_OPERATOR_WINDOW_UI = 'brandingObserver'
BRANDING_PLAYER_WINDOW_UI = 'brandingPlayer'

class UI_TYPE:
	OPERATOR = 1
	PLAYER = 2

prefsFilePath = unicode_from_utf8(BigWorld.wg_getPreferencesFilePath())[1]
SETTINGS_FILE = os.path.normpath(os.path.join(os.path.dirname(prefsFilePath), 'mods', 'branding.json'))
