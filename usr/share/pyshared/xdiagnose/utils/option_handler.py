#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Command line options'''

from optparse import OptionParser

# TODO: re-run pylint on this
class OptionHandler(OptionParser):
    def __init__(self, opts, info):
        '''Creates an OptionParser instance for the options in this module'''
        self.options = opts
        option_list = []
        for item in self.options:
            option_list.append(item[0])
        OptionParser.__init__(
            self,
            option_list=option_list,
            version="%prog "+info.VERSION,
            epilog=info.SHORT_DESCRIPTION)


    def descriptions(self):
        '''Returns a list of dict objects mapping option name to description'''
        data = []
        for opt in self.options:
            opts = opt[0]._short_opts
            opts.extend(opt[0]._long_opts)
            item = {
                'opts': opts,
                'text': opt[1],
                }
            data.append(item)
        return data

    def parse_commandline(self):
        (opts, values) = self.parse_args()
        return opts

