# Copyright 2017-2019 Parity Technologies (UK) Ltd.
# This file is part of weechat-matrix-ui.

# weechat-matrix-ui is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# weechat-matrix-ui is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with weechat-matrix-ui.  If not, see <http://www.gnu.org/licenses/>.

import_ok = True

from .options import WeechatOptions
from .buffers import Buffers
from .rofi import FuzzySelect

try:
    import weechat
except ImportError:
    print("Script must be run under WeeChat.")
    import_ok = False

keep_alive_channels = []
SCRIPT_NAME = "matrix-ui"
SCRIPT_AUTHOR = "Andrew Plaza <dev@andrewplaza.dev>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Hide Matrix Buffers on inactivity, and put private messages in merge buffer"
SCRIPT_SHORT_HELP = "[add <buffer>] | [del <buffer>] | [buffer <list [matrix, irc]> | [select <buffer, matrix, pm, channel>]]"
SCRIPT_COMMAND = "wui"
CONFIG_FILE_NAME = "weechat-matrix-ui"
LOG_LEVEL="DEBUG"
SCRIPT_HELP =   ("    add: Add a buffer to favorites\n"
                "    del: Delete a buffer from favorites\n" +
                "    buffer: List all buffers, or just matrix and irc buffers\n" +
                "    select: Select a any buffer, or a specific matrix, irc or private buffer with rofi\n" +
                "    Examples:\n" +
                "    list all buffer short names: full name:\n" +
                "       /" + SCRIPT_COMMAND + " buffer list\n" +
                "    list only matrix buffer short names: full names(matrix ID):\n" +
                "       /" + SCRIPT_COMMAND + " buffer list matrix\n" +
                "    select from all buffers with rofi:\n" +
                "       /" + SCRIPT_COMMAND + " select buffer\n" +
                "    select only private channels with rofi:\n" +
                "       /" + SCRIPT_COMMAND + " select pm\n" +
                "    add a buffer to favorites:\n" +
                "       /" + SCRIPT_COMMAND + " add #weechat-matrix\n" +
                "    delete a buffer from favorites:\n" +
                "       /" + SCRIPT_COMMAND + " del #weechat-matrix\n" +
                "     list buffers in favorites:\n" +
                "       /" + SCRIPT_COMMAND + " buffer list favorites\n")

glob_map = {
    'SCRIPT_NAME': SCRIPT_NAME,
    'SCRIPT_AUTHOR': SCRIPT_AUTHOR,
    'SCRIPT_VERSION': SCRIPT_VERSION,
    'SCRIPT_LICENSE': SCRIPT_LICENSE,
    'SCRIPT_DESC': SCRIPT_DESC,
    'SCRIPT_SHORT_HELP': SCRIPT_SHORT_HELP,
    'SCRIPT_HELP': SCRIPT_HELP,
    'SCRIPT_COMMAND': SCRIPT_COMMAND,
    'LOG_LEVEL': LOG_LEVEL,
    'CONFIG_FILE_NAME': CONFIG_FILE_NAME
}

# Global Classes. Manage state within the class rather than stand-alone functions.
# Class is exposed to callbacks or whatever needs them
OPTIONS = WeechatOptions(glob_map)
BUFFERS = Buffers(OPTIONS)
FUZZY_SELECT = FuzzySelect(BUFFERS, OPTIONS)
