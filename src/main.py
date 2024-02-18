# main.py
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

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import JnotesWindow
from .preferences import PreferencesWindow
from .sidebar import Sidebar
from .sync import Sync
from .notes_list import NotesList
from .note_edit import NoteEditWindow


class JnotesApplication(Adw.Application):
    """The main application singleton class."""

    calendar_set = None

    def __init__(self):
        super().__init__(application_id='net.jeena.jnotes',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = JnotesWindow(application=self)
            win.sidebar.calendar_set.connect('row-selected', self.on_calendar_selected)
            win.notes_list.notes_list.connect('row-selected', self.on_note_selected)
        win.present()

        def callback(calendar_set):
            self.calendar_set = calendar_set
            if not self.calendar_set:
                self.on_preferences_action(win, False)
            else:
                win.sidebar.set_calendars(self.calendar_set)

        Sync.set_spinner(win.sidebar.spinner)
        Sync.get_calendar_set(callback)

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='jnotes',
                                application_icon='net.jeena.jnotes',
                                developer_name='Jeena',
                                version='0.1.0',
                                developers=['Jeena'],
                                copyright='© 2024 Jeena')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        preferences_window = PreferencesWindow(transient_for=self.props.active_window)
        preferences_window.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def on_calendar_selected(self, container, row):
        notes_list = self.props.active_window.notes_list
        Sync.get_calenndar_notes(
            self.calendar_set[row.get_index()],
            lambda calendar: notes_list.set_calendar(calendar)
        )

    def on_note_selected(self, container, row):
        calendar = self.props.active_window.notes_list.calendar
        note = calendar[row.get_index()]
        edit_dialog = NoteEditWindow(transient_for=self.props.active_window)
        edit_dialog.set_note(note)
        edit_dialog.present()


def main(version):
    """The application's entry point."""
    app = JnotesApplication()
    return app.run(sys.argv)
