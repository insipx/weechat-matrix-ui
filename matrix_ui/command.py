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
    BUFFERS,
    FUZZY_SELECT
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
    argv = args.split(None, 3)
    if len(argv) > 0:
        if argv[0] == "add":
            OPTIONS.add_favorite(argv[1])
        elif argv[0] == "del":
            OPTIONS.del_favorite(argv[1])
        elif argv[0] == "list":
            OPTIONS.list_favorites()
        elif argv[0] == "refresh":
            BUFFERS.refresh()
        elif argv[0] == "buffer":
            if len(argv) < 2:
                weechat.command("", "/help %s" % SCRIPT_COMMAND)
                return weechat.WEECHAT_RC_OK
            elif argv[1] == "list":
                buflist = BUFFERS.get_buffers()
                if len(argv) == 2:
                    for b in buflist:
                        weechat.prnt("", "{}: {}".format(b.short_name, b.name))
                elif len(argv) < 3:
                    weechat.command("", "/help %s" % SCRIPT_COMMAND)
                    return weechat.WEECHAT_RC_OK
                elif argv[2] == "matrix":
                    for b in buflist:
                        if b.is_matrix():
                            weechat.prnt("", "{}: {}".format(b.short_name, b.name))
                elif argv[2] == "irc":
                    for b in buflist:
                        if not b.is_matrix():
                            weechat.prnt("", "{}: {}".format(b.short_name, b.name))
        elif argv[0] == "select":
            if len(argv) < 2:
                weechat.command("", "help %s" % SCRIPT_COMMAND)
                return weechat.WEECHAT_RC_OK
            if argv[1] == "buffer":
                FUZZY_SELECT.select_any_buffer()
            elif argv[1] == "channel":
                FUZZY_SELECT.select_channels()
            elif argv[1] == "pm":
                FUZZY_SELECT.select_pms()
            elif argv[1] == "matrix":
                FUZZY_SELECT.select_matrix()
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
