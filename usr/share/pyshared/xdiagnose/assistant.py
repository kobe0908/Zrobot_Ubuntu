#!/usr/bin/env python

import gtk
import os

class SetupActionGuide(gtk.Assistant):
    def __init__(self):
        gtk.Assistant.__init__(self)
        self.set_default_size( 400, 300 )

        self.connect('delete_event', self.cb_on_delete)
        self.connect('close', self.cb_close)
        self.connect('cancel', self.cb_close)
        self.connect('prepare', self.cb_prepare)

        # The first page - welcomes the user and changed the bluetooth connection to sixa mode.
        self.page1 = gtk.Label("This guide will go trough each step to have a connected gamepad.")
        self.page1.set_line_wrap(True)
        self.page1.show()
        self.append_page(self.page1)
        self.set_page_title(self.page1, 'Welcome to SixA Connection Guide!')
        self.set_page_type(self.page1, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_complete(self.page1, True )

        # The second page.
        self.page2 = gtk.Label("Press the PS (the middle) button and wait for the gamepad to connect.")
        self.page2.set_line_wrap(True)
        self.page2.show()
        self.append_page(self.page2)
        self.set_page_title(self.page2, 'Step 2: Pairing the gamepad.')
        self.set_page_type(self.page2, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_complete(self.page2, True)

        # The third page.
        self.page3 = gtk.Label("Looking for gamepads.")
        self.page3.set_line_wrap(True)
        self.page3.show()
        self.append_page(self.page3)
        self.set_page_title(self.page3, 'Step 3: Checks for connected gamepads.')
        self.set_page_type(self.page3, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_complete(self.page3, True)

        # The forth page.
        self.page4 = gtk.Label("When you click next, Bluetooth and gamepad will be configured!")
        self.page4.set_line_wrap(True)
        self.page4.show()
        self.append_page(self.page4)
        self.set_page_title(self.page4, 'Step 4: ')
        self.set_page_type(self.page4, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_complete(self.page4, True)


        # The fifth and final page.
        self.page5 = gtk.Label("Hello!")
        self.page5.set_line_wrap(True)
        self.page5.show()
        self.append_page(self.page5)
        self.set_page_title(self.page5, 'Step 5:')
        self.set_page_type(self.page5, gtk.ASSISTANT_PAGE_SUMMARY)


        self.show()

    def cb_on_delete(self, widget, event):
        gtk.main_quit()

    def cb_close(self, assistant):
        gtk.main_quit()

    def cb_prepare(self, assistant, page):
        if self.page1 == page:
            print 'sixa action setup part1'
        elif self.page2 == page:
            print 'sixa action setup part2'
        elif self.page3 == page:
            print 'sixa action setup part3'
        elif self.page4 == page:
            print 'sixa action setup part4'
        elif self.page5 == page:
            print 'sixa action setup part5'



if __name__ == '__main__':
    win = SetupActionGuide()
    win.show()
    gtk.main() 
