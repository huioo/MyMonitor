#!/usr/bin/env python
# -*- coding: utf-8 -*-
# io
import re
import logging

from utils.subprocess_output import get_subprocess_output


logging.basicConfig(level=logging.DEBUG)

def parse_linux2(self, output):
    self.header_re = re.compile(r'([%\\/\-_a-zA-Z0-9]+)[\s+]?')
    self.item_re = re.compile(r'^([\-a-zA-Z0-9\/]+)')
    self.value_re = re.compile(r'\d+\.\d+')

    recentStats = output.split('Device:')[2].split('\n')
    header = recentStats[0]
    headerNames = re.findall(self.header_re, header)
    device = None

    ioStats = {}

    for statsIndex in range(1, len(recentStats)):
        row = recentStats[statsIndex]

        if not row:
            # Ignore blank lines.
            continue

        deviceMatch = self.item_re.match(row)

        if deviceMatch is not None:
            # Sometimes device names span two lines.
            device = deviceMatch.groups()[0]
        else:
            continue

        values = re.findall(self.value_re, row)

        if not values:
            # Sometimes values are on the next line so we encounter
            # instances of [].
            continue

        ioStats[device] = {}

        for headerIndex in range(len(headerNames)):
            headerName = headerNames[headerIndex]
            ioStats[device][headerName] = values[headerIndex]

    return ioStats


stdout, _, _ = get_subprocess_output(['iostat', '-d', '1', '2', '-x', '-k'], logging)

import UserDict
parse_linux2(UserDict.UserDict(), stdout)

