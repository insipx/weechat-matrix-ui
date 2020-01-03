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

import logging

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now: http://www.weechat.org")
    import_ok = False

# Matrix Buffer Object. Manages Matrix Buffer Names.
# Map Buffer Hash to Human-Readable name
class Buffer:
    # needs buffer and buffer pointer
    # creates a buffer object
    def __init__(self, buffer, opts):
        # Global weechat options
        self.opts = opts
        # General Buffer Shenanigans
        self.plugin = weechat.buffer_get_string(buffer, "plugin")
        self.name = weechat.buffer_get_string(buffer, "name")
        self.full_name = weechat.buffer_get_string(buffer, "full_name")
        self.short_name = weechat.buffer_get_string(buffer, "short_name")
        logging.debug("FULL_NAME: %s, SHORT_NAME: %s" % (self.full_name, self.short_name))
        self.title = weechat.buffer_get_string(buffer, "title")
        # Local Variables
        self.script_name = weechat.buffer_get_string(buffer, "localvar_script_name")
        self.type = weechat.buffer_get_string(buffer, "localvar_type")
        self.keep_alive = False

    def get_pointer(self):
        buf = weechat.buffer_search("==", self.full_name)
        if not buf:
            weechat.prnt("", "[WUI] ERROR: POINTER TO BUFFER: %s NOT FOUND" % self.short_name)
        return buf
   
    def get_notify_level(self):
        return weechat.buffer_get_integer(self.get_pointer(), "notify")

    def hide(self): # may cause segfault because infolist was freed
        weechat.buffer_set(self.get_pointer(), "hidden", "1")

    def show(self):
        weechat.buffer_set(self.get_pointer(), "hidden", "0")

    def set_alive(self):
        self.keep_alive = True

    def unset_alive(self):
        self.keep_alive = False

    # TODO: possibly Make 'matrix' buffer different class
    def is_matrix(self):
        return self.script_name == "matrix"

    def is_private(self):
        return self.type == "private"

    def is_alive(self):
        if self.get_notify_level() > 0 and self.keep_alive:
            return True
        else:
            return False

    # The buffer may be hidden if it's not the current or server buffer
    def is_hideable(self):

        if self.type == "server":
            logging.debug("not hiding because buffer is a server")
            return False

        if self.full_name == "core.weechat":
            logging.debug("Not hiding because buffer is core.weechat")
            return False

        if self.short_name in self.opts.get_favorites():
            logging.debug("not hiding because buffer is in favorites")
            return False

        if self.keep_alive:
            logging.debug("Not hiding because buffer needs to be kept alive")
            return False

        if not self.is_matrix():
            logging.debug("Not hiding because buffer is not matrix")
            return False

        if self.get_pointer() == weechat.current_buffer():
            logging.debug("Not hiding because buffer is current")
            return False

        return True
