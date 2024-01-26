# preferences.py
#
# Copyright 2024 Jeena
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib
from .gsettings import GSettings
from urllib.parse import urlparse
from .sync import Sync

@Gtk.Template(resource_path='/net/jeena/jnotes/ui/preferences.ui')
class PreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'PreferencesWindow'

    server_url = Gtk.Template.Child()
    username = Gtk.Template.Child()
    password = Gtk.Template.Child()
    spinner = Gtk.Template.Child()
    test_connection_row = Gtk.Template.Child()
    test_connection = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        GSettings.bind("server-url", self.server_url, "text")
        GSettings.bind("username", self.username, "text")
        self.password.set_text(GSettings.get_secret("CalDAV"))

    @Gtk.Template.Callback()
    def on_test_connection_button_clicked(self, _btn):
        server_url = self.server_url.get_text()
        username = self.username.get_text()
        password = self.password.get_text()
        GLib.idle_add(self.spinner.start)
        GLib.idle_add(self.deactivate_test_button)
        Sync.test_connection(server_url, username, password, self.sync_ok_callback)

    @Gtk.Template.Callback()
    def on_validate(self, _lbl):
        server_url = urlparse(self.server_url.get_text())
        server_url_ok = bool(server_url.scheme and server_url.hostname)
        username_ok = len(self.username.get_text()) > 0
        password_ok = len(self.password.get_text()) > 0

        if (server_url_ok and username_ok and password_ok):
            self.activate_test_button()
        else:
            self.deactivate_test_button()

    def activate_test_button(self):
        self.test_connection.add_css_class("suggested-action")
        self.test_connection.set_sensitive(True)

    def deactivate_test_button(self):
        self.test_connection.remove_css_class("suggested-action")
        self.test_connection.set_sensitive(False)

    def sync_ok_callback(self, ok, e=None):
        self.activate_test_button()
        self.spinner.stop()
        if ok:
            self.test_connection_row.set_icon_name("emblem-ok-symbolic")
        else:
            self.test_connection_row.set_icon_name("network-error-symbolic")
            
