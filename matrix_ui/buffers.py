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

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org")
    import_ok = False

class Buffers:
    def __init__(self, globs):
        self.buffers = dict()
        self.keep_alive = list()
        self.globs = globs

    def refresh(self):
        print("hello")

# ==================================[ funcs ]==================================

def get_favorites(buffer):
    favorites = weechat.config_get("%s.buffer.favorites" % CONFIG_FILE_NAME)
    favorites = weechat.config_string(favorites)
    return favorites.split(',')

def apply_options_for_buffer(buffer):
    full_name = weechat.buffer_get_string(buffer, "full_name")
    short_name = weechat.buffer_get_string(buffer, "short_name")
    script_name = weechat.buffer_get_string(buffer, "localvar_script_name")
    buffer_type = weechat.buffer_get_string(buffer, "localvar_type")

    favorites = get_favorites(buffer)

    if short_name not in favorites and script_name == "matrix":
        maybe_hide_buffer(buffer)
    handle_hotlist

def maybe_hide_buffer(buffer):
    if buffer_is_hideable(buffer):
        # weechat.prnt("", "HIDING: %s" % weechat.buffer_get_string(buffer, "short_name"))
        weechat.buffer_set(buffer, "hidden", "1")

def buffer_is_hideable(buffer):
    """Check if passed buffer can be hidden.

    If configuration option ``hide_private`` is enabled,
    private buffers will become hidden as well.

    If the previous buffer name matches any of the exemptions defined in ``exemptions``,
    it will not become hidden.

    :param buffer: Buffer string representation
    """
    if buffer == weechat.current_buffer():
        return False

    buffer_type = weechat.buffer_get_string(buffer, "localvar_type")

    if buffer_type == "server":
        return False

    """
    buffer_type = weechat.buffer_get_string(buffer, 'localvar_type')

    if (buffer_type == "private"
            and weechat.config_get_plugin("hide_private") == "off"):
        return False
    """

    return True


def handle_hotlist():
    global keep_alive_channels
    hotlist_buffers = weechat.infolist_get("hotlist", "", "")

    if not hotlist_buffers:
        return weechat.WEECHAT_RC_OK

    while True:
        buffer = weechat.infolist_pointer(hotlist_buffers, "buffer_pointer")
        full_name = weechat.buffer_get_string(buffer, "full_name")
        short_name = weechat.buffer_get_string(buffer, "short_name")
        script_name = weechat.buffer_get_string(buffer, "localvar_script_name")
        if script_name == "matrix":
            weechat.buffer_set(buffer, "hidden", "0")
            keep_alive_channels.append(full_name)
            weechat.prnt("", "BUFFER: %s" % short_name)
        if not weechat.infolist_next(hotlist_buffers):
            break

    weechat.infolist_free(hotlist_buffers)
