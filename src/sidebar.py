# sidebar.py
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

@Gtk.Template(resource_path='/net/jeena/jnotes/ui/sidebar.ui')
class Sidebar(Gtk.ScrolledWindow):
    __gtype_name__ = 'Sidebar'

    calendar_set = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_calendars(self, calendars):
        self.calendar_set.bind_model(calendars, self.create_item_widget)

    def create_item_widget(self, calendar):
        return Gtk.Label(label=calendar.displayname, halign="start",
            hexpand=True, ellipsize=3)

