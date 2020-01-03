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

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org/")
    import_ok = False

class WeechatOptions:

    # Gets options pertinent to wui
    def __init__(self, globs):
        # temp = weechat.config_get("%s.buffer.favorites")
        self.favorites = list()
        self.globs = globs
        self. rofi = ''

    # must be called before any methods
    def refresh(self):
        fav_pointer = weechat.config_get("%s.buffer.favorites" % self.globs["CONFIG_FILE_NAME"])
        self.favorites = weechat.config_string(fav_pointer).split(',')

    def get_favorites(self):
        if not self.favorites:
            self.refresh()
        return self.favorites

    # List favorites
    def list_favorites(self):
        if not self.favorites:
            self.refresh()
        weechat.prnt("", "Favorites: ")
        for fav in self.favorites:
            weechat.prnt("", "%s" % fav)

    def add_favorite(self, val):
        if not self.favorites:
            self.refresh()
        self.favorites.append(val)
        weechat.command("", "/set %s.buffer.favorites %s" % (self.globs["CONFIG_FILE_NAME"], ','.join(self.favorites)))

    def del_favorite(self, val):
        print(val)
        print(self.favorites)
        if not self.favorites:
            self.refresh()
        if val not in self.favorites:
            weechat.prnt("", "%s not in favorites" % val)
            return
        else:
            self.favorites.remove(val)
            if self.favorites == ['']:
                weechat.command("", "/set %s.buffer.favorites \"\"" % (self.globs["CONFIG_FILE_NAME"]))
            else:
                weechat.command("", "/set %s.buffer.favorites %s" % (self.globs["CONFIG_FILE_NAME"], ','.join(self.favorites)))
        return weechat.WEECHAT_RC_OK
