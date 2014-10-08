#!/usr/bin/env python

import os
import gtk
import shutil

import gettext
from gettext import gettext as _
gettext.textdomain('xdiagnose')

from application import Application
from utils.debug import dbg
from utils.execute import execute


class XDiagnoseApplication(Application):
    def __init__(self):
        Application.__init__(self)
        self.xorg_conf_path = "/etc/X11/xorg.conf"
        self.xorg_conf_d_path = "/etc/X11/xorg.conf.d"
        self.xorg_conf_backup_path = "%s-backup" %(self.xorg_conf_path)
        self.xorg_conf_d_backup_path = "%s-backup" %(self.xorg_conf_d_path)

        self.pages['welcome'] = self.create_welcome_page()
        self.pages['actions'] = self.create_actions_page()
        self.pages['reconfigure'] = self.create_reconfigure_page()
        self.pages['troubleshoot'] = self.create_troubleshoot_page()

        # Refresh
        self.update_frame()
        self.window.show_all()
        self.on_page(None, 'welcome')

    def create_welcome_page(self):
        page = self.create_page(
            '<big>The system is running in low-graphics mode</big>\n\n' +
            'Your graphics and input devices could not be detected correctly.  You will need to configure these yourself.')
        nav_bar = self.create_nav_bar(next_page="actions")
        page.pack_end(nav_bar, expand=False)
        return page

    def create_actions_page(self):
        page = self.create_page("What would you like to try?")

        hbox = gtk.HBox()

        button1 = self.create_button("Run in low-graphics mode",
                                      "Use low-graphics for just one session")
        button1.connect("clicked", self.on_low_res_mode)
        button2 = self.create_button("Reconfigure",
                                      "Try to automatically fix the problem")
        button2.connect("clicked", self.on_page, "reconfigure")
        button3 = self.create_button("Troubleshoot",
                                      "Review errors, configs, and logs")
        button3.connect("clicked", self.on_page, "troubleshoot")
        button4 = self.create_button("Console",
                                      "Exit to the console login")
        button4.connect("clicked", self.on_exit_to_console)

        table = gtk.Table(rows=4, columns=3, homogeneous=False)
        table.set_border_width(0)
        table.attach(gtk.Label(''), 0, 1, 0, 1, xoptions=gtk.EXPAND)
        table.attach(button1, 1, 2, 0, 1)
        table.attach(button2, 1, 2, 1, 2)
        table.attach(button3, 1, 2, 2, 3)
        table.attach(button4, 1, 2, 3, 4)
        table.attach(gtk.Label(''), 2, 3, 0, 1, xoptions=gtk.EXPAND)
        page.pack_start(table, expand=False)

        nav_bar = self.create_nav_bar(prev_page="welcome")
        page.pack_end(nav_bar, expand=False)
        return page

    def create_reconfigure_page(self):
        page = self.create_page("How would you like to reconfigure your display?")

        hbox = gtk.HBox()

        button1 = self.create_button("Reset to defaults",
                                      "Use default (generic) configuration")
        button1.connect("clicked", self.on_reset_to_default_xorg_conf)
        button2 = self.create_button("Generate xorg.conf",
                                      "Creates a new configuration for this hardware")
        button2.connect("clicked", self.on_generate_xorg_conf)
        button3 = self.create_button("Restore backup",
                                      "Use your backed-up configuration")
        button3.connect("clicked", self.on_restore_backup)

        table = gtk.Table(rows=3, columns=3, homogeneous=False)
        table.set_border_width(0)
        table.attach(gtk.Label(''), 0, 1, 0, 1, xoptions=gtk.EXPAND)
        table.attach(button1, 1, 2, 0, 1)
        table.attach(button2, 1, 2, 1, 2)
        table.attach(button3, 1, 2, 2, 3)
        table.attach(gtk.Label(''), 2, 3, 0, 1, xoptions=gtk.EXPAND)
        page.pack_start(table, expand=False)

        nav_bar = self.create_nav_bar(prev_page="actions")
        page.pack_end(nav_bar, expand=False)
        return page

    def create_troubleshoot_page(self):
        page = self.create_page("What information would you like to review?")

        hbox = gtk.HBox()

        button1 = self.create_button("X server log",
                                      "Review the failed session Xorg.0.log")
        button1.connect("clicked", self.on_view_file, "/var/log/Xorg.0.log")
        button2 = self.create_button("lightdm's X startup log",
                                      "Review the display manager log")
        button2.connect("clicked", self.on_view_file, "/var/log/lightdm/x-0.log")
        button3 = self.create_button("Edit X Config",
                                      "Edit xorg.conf configuration file")
        button3.connect("clicked", self.on_edit_file, "/etc/X11/xorg.conf")
        button4 = self.create_button("Archive",
                                      "Package up configuration and logs for sharing")
        button4.connect("clicked", self.on_make_archive)

        table = gtk.Table(rows=4, columns=3, homogeneous=False)
        table.set_border_width(0)
        table.attach(gtk.Label(''), 0, 1, 0, 1, xoptions=gtk.EXPAND)
        table.attach(button1, 1, 2, 0, 1)
        table.attach(button2, 1, 2, 1, 2)
        table.attach(button3, 1, 2, 2, 3)
        table.attach(button4, 1, 2, 3, 4)
        table.attach(gtk.Label(''), 2, 3, 0, 1, xoptions=gtk.EXPAND)
        page.pack_start(table, expand=False)

        nav_bar = self.create_nav_bar(prev_page="actions")
        page.pack_end(nav_bar, expand=False)
        return page

    def has_backup(self):
        if (os.path.exists(self.xorg_conf_backup_path) or
            os.path.exists(self.xorg_conf_d_backup_path)):
            return True
        return False

    def backup_xorg_conf(self):
        '''Backs up xorg.conf and xorg.conf.d, overwriting any pre-existing backups'''
        if os.path.exists(self.xorg_conf_path):
            if os.path.exists(self.xorg_conf_backup_path):
                shutil.rm(self.xorg_conf_backup_path)
            shutil.copy(self.xorg_conf_path, self.xorg_conf_backup_path)
        if os.path.exists(self.xorg_conf_d_path):
            if os.path.exists(self.xorg_conf_d_backup_path):
                shutil.rmtree(self.xorg_conf_d_backup_path)
            shutil.copytree(self.xorg_conf_d_path, self.xorg_conf_d_backup_path)

    def update_frame(self):
        self.window.ensure_style()
        style = self.window.get_style()
        color = style.bg[gtk.STATE_SELECTED]
        self.frame.modify_bg(gtk.STATE_NORMAL, color)

        self.page_title.modify_fg(gtk.STATE_NORMAL, color)

    def on_page(self, widget, page_name):
        new_page = self.pages[page_name]
        if self.current_page is not None:
            self.frame.remove(self.current_page)
        if page_name == "welcome":
            self.page_title.set_markup("<big>Failsafe-X</big>")
        else:
            self.page_title.set_markup("<big>Failsafe-X: %s</big>" %(page_name.capitalize()))
        self.frame.add(new_page)
        self.current_page = new_page
        self.frame.show_all()

    def on_low_res_mode(self, widget):
        pass

    def on_exit_to_console(self, widget):
        pass

    def on_reset_to_default_xorg_conf(self, widget):
        if not self.backup_xorg_conf():
            dbg("Error: Could not backup the config")
            return
        shutils.rm(self.xorg_conf)
        shutils.rmtree(self.xorg_conf_d)

    def on_generate_xorg_conf(self, widget):
        if not self.backup_xorg_conf():
            dbg("Error: Could not backup the config")
            return
        pass

    def on_restore_backup(self, widget):
        pass

    def on_view_file(self, widget, filename):
        execute("zenity --text-info --filename=%s --width=640 --height=480" %(filename))

    def on_edit_file(self, widget, filename):
        if not os.path.exists(self.xorg_conf_path):
            # TODO: Stub in an xorg.conf
            pass
        execute("zenity --text-info --editable --filename=%s --width=640 --height=480" %(self.xorg_conf_path))

    def on_make_archive(self, widget):
        xorg_backup_name = "failsafeX-backup-${timestamp}"
        xorg_backup_dir  = "/tmp" # TODO: $(mktemp -d -t ${xorg_backup_name}.XXX)
        xorg_backup_file = "/var/log/%s.tar" %(xorg_backup_name)

        shutils.copy("/etc/X11/xorg.conf", xorg_backup_dir)
        shutils.copy("/var/log/Xorg.0.log", xorg_backup_dir)
        shutils.copy("/var/log/Xorg.0.log.old", xorg_backup_dir)
        shutils.copytree("/var/log/gdm", xorg_backup_dir)
        shutils.copytree("/var/log/lightdm", xorg_backup_dir)
        execute("lspci -vvnn > %s/lspci-vvnn.txt" %(xorg_backup_dir))
        execute("xrandr --verbose > %s/xrandr-verbose.txt" %(xorg_backup_dir))
        execute("tar -cf %s %s" %(xorg_backup_file, xorg_backup_dir))
        shutils.rmtree(xorg_backup_dir)


if __name__ == "__main__":
    import sys

    dbg("main:  Starting program")
    app = XDiagnoseApplication()
    gtk.main()

    dbg("main:  Ending program")
    sys.exit(0)


