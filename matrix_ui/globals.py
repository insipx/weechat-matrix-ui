#!/usr/bin/env python3

import_ok = True
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
SCRIPT_DESC = "Hide Matrix Buffers on inactvity, and put private messages in merge buffer"
SCRIPT_COMMAND = "wui"
CONFIG_FILE_NAME = "weechat-matrix-ui"
