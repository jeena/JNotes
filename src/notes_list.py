# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/net/jeena/jnotes/ui/notes_list.ui')
class NotesList(Gtk.ScrolledWindow):
    __gtype_name__ = 'NotesList'

    notes_list = Gtk.Template.Child()
    calendar = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_calendar(self, calendar):
        self.calendar = calendar
        self.notes_list.bind_model(self.calendar, self.create_item_widget)

    def create_item_widget(self, note):
        return Adw.ActionRow(title=note.summary, subtitle=note.description)

