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

from matrix_ui.buffer.buffer import Buffer
import logging

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org")
    import_ok = False

class Buffers:
    def __init__(self, opts):
        self.buffers = dict()
        self.hotlist = dict()
        self.opts = opts
        # List of buffers that need to be hidden as soon as possible
        self.to_hide = list()
        # self.hotlist_infolist = str

    # Accepts a function that takes a buffer object and returns a boolean
    def get_buffer(self, fun):
        return list(filter(lambda b: fun(b), self.buffers.values()))[0]

    # Get all buffres
    def get_buffers(self):
        logging.debug("{}".format(self.buffers.values()))
        return self.buffers.values()

    # Buffers that are not private
    def get_channels(self):
        return list(filter(lambda b: not b.is_private(), self.buffers.values()))

    def get_pm_buffers(self):
        return list(filter(lambda b: b.is_private(), self.buffers.values()))

    def get_matrix_buffers(self):
        return list(filter(lambda b: b.is_matrix(), self.buffers.values()))

    # accepts a buffer object that will be hidden as soon as it is hideable
    def set_to_hide(self, buffer):
        self.to_hide.append(buffer)

    # `buffer` must be buffer pointer
    def on_buffer_kill(self, buffer):
        try:
            self.buffers.pop(full_name(buffer))
        except KeyError:
            print("Key not in Buffers")

    # `buffer` must be buffer pointer
    def on_buffer_open(self, buffer):
        self.buffers[full_name(buffer)] = Buffer(buffer, self.opts)
        self.try_hide(self.buffers[full_name(buffer)])

    # buffer must be buffer pointer
    # argument passed to on_hotlist_changed may be null, so need to
    # refresh entire list
    def on_hotlist_changed(self, buffer):
        self.refresh_hotlist()

    # just refresh hotlist
    def on_buffer_switch(self, buffer):
        name = full_name(buffer)
        if name == "core.weechat":
            return
        else:
            buffer = self.buffers[full_name(buffer)]
            for b in self.to_hide:
                self.try_hide(b)
   
    # Refresh the classes internal state
    def refresh(self):
        self.refresh_buffers()
        self.refresh_hotlist()


    # refresh internal list of the hotlist
    def refresh_hotlist(self):

        hotlist_buffers = weechat.infolist_get("hotlist", "", "")
        if not hotlist_buffers:
            logging.debug("NO MORE HOTLIST!!!!!!!!!!!!!!!!!!!!!!!")
            return weechat.WEECHAT_RC_OK

        new_hotlist = dict()
        while weechat.infolist_next(hotlist_buffers):
            buffer = full_name(weechat.infolist_pointer(hotlist_buffers, "buffer_pointer"))
            if buffer == "core.weechat":
                continue
            new_hotlist[buffer] = self.buffers[buffer]
            buffer = new_hotlist[buffer]
            if buffer.is_matrix():
                buffer.show()
                buffer.set_alive()

        # Check if a value has been removed from the old hotlist
        # hide it if it has (means that it has been checked)
        removed = set(self.hotlist) - set(new_hotlist)
        logging.debug("REMOVED: {}".format(list(map(lambda x: self.buffers[x].short_name, removed))))
        for b in removed:
            buf = self.buffers[b]
            buf.unset_alive()
            self.to_hide.append(buf)

        weechat.infolist_free(hotlist_buffers)

        self.hotlist = new_hotlist

    # refresh internal list of all buffers
    def refresh_buffers(self):
        self.buffers.clear()
        hdata = weechat.hdata_get("buffer")
        buffer = weechat.hdata_get_list(hdata, "gui_buffers")

        if not hdata or not buffer:
            return weechat.WEECHAT_RC_OK
        while True:
            buffer = weechat.hdata_move(hdata, buffer, 1)
            if not buffer:
                break
            else:
                buf = self.buffers[full_name(buffer)] = Buffer(buffer, self.opts)
                logging.debug("Hideable: {}".format(buf.is_hideable()))
                self.try_hide(self.buffers[full_name(buffer)])

    # `buffer` must be buffer object
    def try_hide(self, buffer):
        if buffer.is_matrix() and buffer.is_hideable():
            buffer.hide()
        else:
            buffer.show()

    def try_hide_all(self):
        for buf in self.buffers:
            self.hide(buf)

def full_name(buffer):
    return weechat.buffer_get_string(buffer, "full_name")

def short_name(buffer):
    return weechat.buffer_get_string(buffer, "short_name")
