#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''High level package information'''
PROGNAME = 'xdiagnose'
URL = 'http://launchpad.net/xdiagnose'
EMAIL = 'bryce@canonical.com'
VERSION = None
DATE_STARTED = '2010-11-04'
DATE_COPYRIGHT = '2011'
LICENSE_URL = 'http://www.gnu.org/copyleft/gpl.html'

SHORT_DESCRIPTION = 'Analysis tools for troubleshooting X.org problems'

DESCRIPTION = """
This package is a friendly GUI application for diagnosing several
common X.org problems.
"""

class _contributor:
    '''Information about a person contributing to this project'''
    def __init__(self, name, email, started=None, roles=None, translating=None):
        self.name = name
        self.email = email
        self.started = started
        if roles is None:
            self.roles = []
        elif type(roles) is not list:
            self.roles = [roles]
        else:
            self.roles = roles
        self.translation_languages = translating
        return

    def to_dict(self):
        '''Returns the object in a dict suitable for json'''
        return self.__dict__

    @property
    def display_email(self):
        '''Formatted string version of email address'''
        if self.email:
            return '<%s>' % self.email
        else:
            return ''

    @property
    def display_roles(self):
        '''Formatted string version of roles list'''
        if self.roles:
            return '[%s]' % ','.join(self.roles)
        else:
            return ''

LEAD_DEVELOPER = _contributor(
    'Bryce Harrington', 'bryce@canonical.com', started='2010-11-04',
    roles=['lead', 'developer'], translating=None,
    )

CONTRIBUTORS = [
    _contributor(
        'Gabor Kelemen', 'kelemeng@ubuntu.com', started='2012-01-21',
        roles=['developer', 'translator'], translating=None),
]


if __name__ == "__main__":
    print PROGNAME, VERSION, URL
    print "Copyright (C) %s %s <%s>" % (
        DATE_COPYRIGHT, LEAD_DEVELOPER.name, LEAD_DEVELOPER.email)
    print
    for contributor in CONTRIBUTORS:
        print "%s %s %s" % (
            contributor.name,
            contributor.display_email,
            contributor.display_roles)
