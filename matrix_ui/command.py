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

from .globals import (
    SCRIPT_COMMAND,
    CONFIG_FILE_NAME,
    OPTIONS,
    BUFFERS
)

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org/")
    import_ok = False

def wui_cmd(data, buffer, args):
    """Callback for /buffer_autoset command."""
    args = args.strip()
    if args == "":
        weechat.command("", "/set %s.buffer.*" % CONFIG_FILE_NAME)
        return weechat.WEECHAT_RC_OK
    argv = args.split(None, 3)
    if len(argv) > 0:
        if argv[0] == "add":
            if len(argv) < 2:
                weechat.command("", "/help %s" % SCRIPT_COMMAND)
                return weechat.WEECHAT_RC_OK
            OPTIONS.add_favorite(argv[1])
        elif argv[0] == "del":
            if len(argv) < 2:
                weechat.command("", "/help %s" % SCRIPT_COMMAND)
                return weechat.WEECHAT_RC_OK
            OPTIONS.del_favorite(argv[1])
        elif argv[0] == "list":
            if len(argv) > 1:
                weechat.command("", "/help %s" % SCRIPT_COMMAND)
                return weechat.WEECHAT_RC_OK
            OPTIONS.list_favorites()
        elif argv[0] == "refresh":
            if len(argv) > 1:
                weechat.command("", "help %s" % SCRIPT_COMMAND)
                return weechat.WEECHAT_RC_OK
            BUFFERS.refresh()
        else:
            weechat.command("", "/help %s" % SCRIPT_COMMAND)
            return weechat.WEECHAT_RC_OK
    return weechat.WEECHAT_RC_OK


def completion_current_buffer_cb(data, completion_item, buffer,
                                     completion):
    """
    Complete with current buffer name (plugin.name),
    for command '/buffer_autoset'.
    """
    name = "%s.%s" % (weechat.buffer_get_string(buffer, "plugin"),
                      weechat.buffer_get_string(buffer, "name"))
    weechat.hook_completion_list_add(completion, name,
                                     0, weechat.WEECHAT_LIST_POS_BEGINNING)
    return weechat.WEECHAT_RC_OK


def completion_options_cb(data, completion_item, buffer, completion):
    """Complete with config options, for command '/buffer_autoset'."""
    options = weechat.infolist_get("option", "",
                                   "%s.buffer.*" % CONFIG_FILE_NAME)
    if options:
        while weechat.infolist_next(options):
            weechat.hook_completion_list_add(
                completion,
                weechat.infolist_string(options, "option_name"),
                0, weechat.WEECHAT_LIST_POS_SORT)
        weechat.infolist_free(options)
    return weechat.WEECHAT_RC_OK
