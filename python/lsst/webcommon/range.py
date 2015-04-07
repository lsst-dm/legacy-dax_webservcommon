# LSST Data Management System
# Copyright 2015 AURA/LSST.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
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
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.

"""
Implementation of several Range specifications for REST APIs.
@author  Brian Van Klaveren, SLAC
"""


class Range(object):
    def __init__(self, type):
        self.type = type

class StartStopSlice(Range):
    def __init__(self, start, stop, length=None):
        super(StartStopSlice, self).__init__("start_stop")
        self.start = start
        self.stop = stop
        if length:
            self.length = length

class OffsetMaxSlice(Range):
    def __init__(self, offset, max, length=None):
        super(StartStopSlice, self).__init__("offset_max")
        self.offset = offset
        self.max = max
        if length:
            self.length = length


class OffsetLimitSlice(Range):
    def __init__(self, offset, limit, length=None):
        super(StartStopSlice, self).__init__("offset_limit")
        self.offset = offset
        self.limit = limit
        if length:
            self.length = length

