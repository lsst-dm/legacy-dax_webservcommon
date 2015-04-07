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
Implementation of Response specifications for REST APIs.
@author  Brian Van Klaveren, SLAC
"""

class Response(object):
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return other.__dict__ == self.__dict__

class ScalarResponse(Response):
    _SLOTS = ["result", "metadata"]

    def __init__(self, result, metadata=None):
        self.result = result
        self.metadata = metadata

class VectorResponse(Response):
    _SLOTS = ["results", "metadata"]

    def __init__(self, results, metadata=None, pagination=None):
        self.results = results
        self.pagination = pagination
        self.metadata = metadata

class ErrorResponse(Response):
    _SLOTS = ["exception", "message", "cause"]

    def __init__(self, exception, message=None, cause=None):
        self.exception = exception
        self.message = message
        self.cause = cause
