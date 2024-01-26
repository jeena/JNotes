# sync.py
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

import caldav
import logging, requests
from gi.repository import Gtk, Gio, GObject
from threading import Thread
from typing import Callable
from .gsettings import GSettings

def threaded(function: Callable):
    """
    Decorator to run function in thread.
    Use GLib.idle_add(func) as callback at the end of threaded function
    if you need to change UI from thread.
    It's needed to be called to make changes in UI thread safe.
    """

    def wrapper(*args, **kwargs):
        Thread(target=function, args=args, kwargs=kwargs, daemon=True).start()

    return wrapper

class Sync():
    client = None
    principal = None

    @classmethod
    @threaded
    def test_connection(self, server_url, username, password, callback):
        try:
            client = caldav.DAVClient(server_url, username=username, password=password)
            client.principal()
            callback(True)
        except caldav.lib.error.AuthorizationError as e:
            logging.warning(e)
            callback(False, e)
        except requests.exceptions.ConnectionError as e:
            logging.warning(e)
            callback(False, e)

    @classmethod
    def init(self):
        server_url = GSettings.get("server-url")
        username = GSettings.get("username")
        password = GSettings.get_secret("CalDAV")

        try:
            self.client = caldav.DAVClient(server_url, username=username, password=password)
            self.principal = self.client.principal()
        except caldav.lib.error.AuthorizationError as e:
            logging.warning(e)
        except requests.exceptions.ConnectionError as e:
            logging.warning(e)

    @classmethod
    def get_calendar_set(self):
        calendar_set = CalendarSet()
        if not self.client:
            self.init()
        if self.principal:
            remote_calendars = self.principal.calendars()
            for remote_calendar in remote_calendars:
                if "VJOURNAL" in remote_calendar.get_supported_components():
                    calendar = Calendar(remote_calendar.get_display_name(), remote_calendar.url)
                    for journal in remote_calendar.journals():
                        summary = journal.icalendar_component.get("summary", "")
                        description = journal.icalendar_component.get("description", "")
                        calendar.add_note(Note(calendar, summary, description))
                    calendar_set.add_calendar(calendar)

        return calendar_set

class CalendarSet(Gio.ListStore):
    def add_calendar(self, calendar):
        self.append(calendar)

    def remove_calendar(self, calendar):
        self.remove(calendar)

class Calendar(Gio.ListStore):
    displayname = None
    cal_id = None

    def __init__(self, displayname, cal_id):
        super().__init__()
        self.displayname = displayname
        self.cal_id = cal_id

    def add_note(self, note):
        self.append(note)

class Note(GObject.GObject):
    uid = None
    calendar = None
    summary = None
    description = None

    def __init__(self, calendar, summary, description):
        super().__init__()
        self.calendar = calendar
        self.summary = summary
        self.description = description