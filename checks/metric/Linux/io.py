#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import logging

from checks.metric.tools import AgentCheck
from utils.subprocess_output import get_subprocess_output


logging.basicConfig(level=logging.DEBUG)


class IO(AgentCheck):
    def __init__(self):
        self.header_re = re.compile(r'([%\\/\-_a-zA-Z0-9]+)[\s+]?')  # [%\/- a-z A-Z 0-9]+[\s+]
        self.item_re = re.compile(r'^([\-a-zA-Z0-9\/]+)')               # [-/ a-z A-Z 0-9]+
        self.value_re = re.compile(r'\d+\.\d+')                             # [\d]+.[\d]+

    def parse_linux_io_stats(self, output):
        """
        :param output:  $ iostat -d 1 2 -x -k
    ubuntu:
    Linux 4.4.0-63-generic (heiniupiwik)    05/22/2018      _x86_64_        (4 CPU)

    Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    vda               0.00     1.48    6.55    3.58   195.03   226.93    83.38     0.14   13.40    4.94   28.87   0.93   0.94
    vdb               0.00    14.05  153.84    8.72  3065.93   257.29    40.89     0.06    0.37    0.09    5.30   0.56   9.02

    Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    vda               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
    vdb               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00

    centos:
    Linux 2.6.32-642.13.1.el6.x86_64 (iZ8vb1u6xle9fnu3sl1rljZ)      05/22/2018      _x86_64_        (8 CPU)

    Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    vda               0.03    11.86    0.15    2.77     3.35    58.54    42.30     0.01    3.75    1.06    3.90   0.80   0.23
    vdb               0.00     8.59    0.48   11.91    14.55    81.99    15.59     0.06    5.11    1.58    5.26   0.20   0.25
    vdc               0.07    20.88    0.43    0.34    39.05    84.88   321.58     0.15  188.35    3.20  428.17   2.28   0.18

    Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    vda               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
    vdb               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
    vdc               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
        :return:
        """
        recent_stats = output.split('Device:')[2].split('\n')
        header = recent_stats[0]
        header_names = re.findall(self.header_re, header)

        ioStats = {}

        for statsIndex in range(1, len(recent_stats)):
            row = recent_stats[statsIndex]
            if not row:
                continue

            device_match = self.item_re.match(row)
            if device_match is None:
                continue
            # Sometimes device names span two lines.
            device_name = device_match.groups()[0]

            values = re.findall(self.value_re, row)
            if not values:
                # Sometimes values are on the next line so we encounter
                # instances of [].
                continue

            ioStats[device_name] = {}

            for headerIndex in range(len(header_names)):
                header_name = header_names[headerIndex]
                ioStats[device_name][header_name] = values[headerIndex]

        return ioStats

    def aa(self):
        pass

    def check(self):
        pass



stdout, _, _ = get_subprocess_output(['iostat', '-d', '1', '2', '-x', '-k'], logging)






'''
BASIC_FORMAT = "%(levelname)s:%(name)s:%(message)s"

DEBUG:
    utils.subprocess_output:
        Popen(['iostat', '-d', '1', '2', '-x', '-k'], 
            stderr = <open file '<fdopen>', mode 'w+b' at 0x7f681204d930>, 
            stdout = <open file '<fdopen>', mode 'w+b' at 0x7f6812132810>
        ) 
called

'''
ioStats = {
    'vda': {
        'wrqm/s': '0.00',
        'avgrq-sz': '0.00',
        'r_await': '0.00',
        'rkB/s': '0.00',
        'await': '0.00',
        'w/s': '0.00',
        'avgqu-sz': '0.00',
        'svctm': '0.00',
        'wkB/s': '0.00',
        'rrqm/s': '0.00',
        'r/s': '0.00',
        '%util': '0.00',
        'w_await': '0.00'
    },
    'vdb': {
        'wrqm/s': '0.00',
        'avgrq-sz': '0.00',
        'r_await': '0.00',
        'rkB/s': '0.00',
        'await': '0.00',
        'w/s': '0.00',
        'avgqu-sz': '0.00',
        'svctm': '0.00',
        'wkB/s': '0.00',
        'rrqm/s': '0.00',
        'r/s': '0.00',
        '%util': '0.00',
        'w_await': '0.00'
    }
}