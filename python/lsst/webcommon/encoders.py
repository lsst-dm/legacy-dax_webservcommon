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
Encoders to help type-based encoding for python objects.
@author  Brian Van Klaveren, SLAC
"""

import json
from .response import Response, ScalarResponse, VectorResponse, ErrorResponse

class TypeEncoder(json.JSONEncoder):
    """
    A JSONEncoder built for encoding specific objects.
    """
    def __init__(self, **kwargs):
        super(TypeEncoder, self).__init__(**kwargs)

    def can_encode(self, obj):
        """
        Determine if this encoder can encode the given object.
        :param obj: The object to be encoded.
        :return: True if we can encode the object
        """
        return False

class BaseResponseEncoder(TypeEncoder):
    def __init__(self, typ, **kwargs):
        super(BaseResponseEncoder, self).__init__(**kwargs)
        self._type = typ

    def can_encode(self, obj):
        return isinstance(obj, self._type)

    def default(self, obj):
        if isinstance(obj, Response):
            ret = {}
            for slot in obj._SLOTS:
                if hasattr(obj, slot) and getattr(obj, slot):
                    ret[slot] = getattr(obj, slot)
            return ret
        return json.JSONEncoder.default(self, obj)

class ScalarResponseEncoder(BaseResponseEncoder):
    def __init__(self, **kwargs):
        super(ScalarResponseEncoder, self).__init__(ScalarResponse, **kwargs)

class VectorResponseEncoder(BaseResponseEncoder):
    def __init__(self, **kwargs):
        super(VectorResponseEncoder, self).__init__(VectorResponse, **kwargs)

class ErrorResponseEncoder(BaseResponseEncoder):
    def __init__(self, **kwargs):
        super(ErrorResponseEncoder, self).__init__(ErrorResponse, **kwargs)

class MixInEncoder(TypeEncoder):
    def __init__(self, encoders, **kwargs):
        """
        MixInEncoder takes a list of TypeEncoders as it's only parameter. It will iterate through the list
        of TypeEncoders and search for a TypeEncoder which can encode the object, then encode it with that
        TypeEncoder
        :param encoders: List of TypeEncoders
        """
        super(MixInEncoder, self).__init__(**kwargs)
        self._encoders = encoders

    def default(self, obj):
        for encoder in self._encoders:
            if encoder.can_encode(obj):
                return encoder.default(obj)
        return json.JSONEncoder.default(self, obj)

    def can_encode(self, obj):
        for encoder in self._encoders:
            if encoder.can_encode(obj):
                return True
        return False

class ResponseEncoder(MixInEncoder):
    def __init__(self, **kwargs):
        super(ResponseEncoder, self).__init__([ScalarResponseEncoder(**kwargs),
                                               VectorResponseEncoder(**kwargs),
                                               ErrorResponseEncoder(**kwargs)
                                               ], **kwargs)

