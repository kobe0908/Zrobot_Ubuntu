#!/usr/bin/env python

# example basictreeview.py

from gi.repository import Gtk
import gettext
from gettext import gettext as _

class ErrorsTreeView(Gtk.Window):

    def __init__(self, data=[], top_level=False):
        self._is_top_level = top_level
        # Create a new window
        Gtk.Window.__init__(self)
        self.set_title(_("Xorg Error Messages"))
        self.set_size_request(500, 200)
        self.connect("delete-event", self.on_close)
        self.connect("destroy", self.on_close)

        # create a TreeStore with one string column to use as the model
        self.treestore = Gtk.TreeStore(str)

        for errormsg in data:
            self.treestore.append(None, [errormsg])

        # create the TreeView using treestore
        self.treeview = Gtk.TreeView()
        self.treeview.set_model(self.treestore)

        # create the TreeViewColumn to display the data
        self.tvcolumn = Gtk.TreeViewColumn(_("Error Message"))

        # add tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)

        # create a CellRendererText to render the data
        self.cell = Gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.add_attribute(self.cell, 'text', 0)

        # make it searchable
        self.treeview.set_search_column(0)

        # Allow sorting on the column
        self.tvcolumn.set_sort_column_id(0)

        # Allow drag and drop reordering of rows
        self.treeview.set_reorderable(True)

        self.add(self.treeview)
        self.show_all()

    # close the window
    def on_close(self, widget=None, event=None, data=None):
        if self._is_top_level:
            Gtk.main_quit()
            return False
        else:
            self.destroy()

if __name__ == "__main__":
    tvexample = ErrorsTreeView(top_level=True)
    Gtk.main()
