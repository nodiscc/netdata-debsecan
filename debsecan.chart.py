# -*- coding: utf-8 -*-
# Description: debsecan python.d module for netdata
# Author: nodiscc (nodiscc@gmail.com)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re

from bases.FrameworkServices.SimpleService import SimpleService

priority = 90000
update_every = 120

ORDER = [
    'status'
]

CHARTS = {
    'status': {
        'options': [None, 'CVEs by scope/urgency', 'CVEs', 'status', 'debsecan.status', 'stacked'],
        'lines': [
            ['high_remote', None, 'absolute'],
            ['high_local', None, 'absolute'],
            ['medium_remote', None, 'absolute'],
            ['medium_local', None, 'absolute'],
            ['low_remote', None, 'absolute'],
            ['low_local', None, 'absolute'],
            ['other', None, 'absolute'],
            ['error', None, 'absolute'],
        ]
    }
}

class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS

        self.data = dict()
        self.log_all_path = '/var/log/debsecan/debsecan.log'
        self.log_high_remote_path = '/var/log/debsecan/debsecan_high_remote.log'
        self.log_high_local_path = '/var/log/debsecan/debsecan_high_local.log'
        self.log_medium_remote_path = '/var/log/debsecan/debsecan_medium_remote.log'
        self.log_medium_local_path = '/var/log/debsecan/debsecan_medium_local.log'
        self.log_low_remote_path = '/var/log/debsecan/debsecan_low_remote.log'
        self.log_low_local_path = '/var/log/debsecan/debsecan_low_local.log'
        self.log_other_path = '/var/log/debsecan/debsecan_other.log'
        self.modtime = ''
        self.data['high_remote'] = 0
        self.data['high_local '] = 0
        self.data['medium_remote'] = 0
        self.data['medium_local'] = 0
        self.data['low_remote'] = 0
        self.data['low_local'] = 0
        self.data['other'] = 0
        self.data['error'] = 0

    def check(self):
        return True

    def get_data(self):
        if not is_readable(self.log_all_path):
            self.debug("{0} is unreadable".format(self.log_all_path))
            self.data['high_remote'] = 0
            self.data['high_local '] = 0
            self.data['medium_remote'] = 0
            self.data['medium_local'] = 0
            self.data['low_remote'] = 0
            self.data['low_local'] = 0
            self.data['other'] = 0
            self.data['error'] = 1
            return self.data
        else:
            self.data['error'] = 0

        try:
            if not self.is_changed():
                self.debug("{0} modification time is unchanged, returning previous values".format(self.log_all_path))
                return self.data
        except:
            self.error("Error while opening {0}".format(self.log_all_path))
            self.data['high_remote'] = 0
            self.data['high_local '] = 0
            self.data['medium_remote'] = 0
            self.data['medium_local'] = 0
            self.data['low_remote'] = 0
            self.data['low_local'] = 0
            self.data['other'] = 0
            self.data['error'] = 1
            return self.data

        self.modtime = os.path.getmtime(self.log_all_path)
        self.data['high_remote'] = line_count(self.log_high_remote_path)
        self.data['high_local '] = line_count(self.log_high_local_path)
        self.data['medium_remote'] = line_count(self.log_medium_remote_path)
        self.data['medium_local'] = line_count(self.log_medium_local_path)
        self.data['low_remote'] = line_count(self.log_low_remote_path)
        self.data['low_local'] = line_count(self.log_low_local_path)
        self.data['other'] = line_count(self.log_other_path)
        self.data['error'] = 0
        return self.data

    def is_changed(self):
        return self.modtime != os.path.getmtime(self.log_all_path)

def is_readable(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)

def line_count(filename):
    with open(filename) as file:
        for index, line in enumerate(file):
            pass
    return index + 1
