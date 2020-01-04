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
from rofi import Rofi

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org")
    import_ok = False

class FuzzySelect:
    def __init__(self, buffers, opts):
        self.buffers = buffers
        self.opts = opts
        if not opts.rofi:
            self.rofi = Rofi(rofi_args=['-matching', 'fuzzy', '-levenshtein-sort', '-i', '-no-case-sensitive'])
        else:
            self.rofi = Rofi(self.opts.ROFI)

    # Accepts a predicate which returs list of buffers
    def select(self, bufs, name):
        buf_names = list(map(lambda x: x.short_name, bufs))
        logging.debug("Buf Names: {}".format(buf_names))
        index, key = self.rofi.select(name, buf_names,
                                      rofi_args=['-i'])
        if index == -1:
            return
        logging.debug("Index: {}, Key: {}".format(index, key))
        selected_buffer = self.buffers.get_buffer(lambda b: b.short_name == buf_names[index])
        selected_buffer.show()
        self.buffers.set_to_hide(selected_buffer)
        weechat.command("", "/buffer {}".format(selected_buffer.full_name))

    # TODO This code can be made much cleaner
    # Alt + t
    def select_any_buffer(self):
        self.select(self.buffers.get_buffers(), "Buffers")

    def select_channels(self):
        self.select(self.buffers.get_channels(), "Channels")

    def select_pms(self):
        self.select(self.buffers.get_pm_buffers(), "PM")

    def select_matrix(self):
        self.select(self.buffers.get_matrix_buffers(), "Matrix")
