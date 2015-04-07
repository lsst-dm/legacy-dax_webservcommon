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
Decoders for type-based decoding for python objects.
@author  Brian Van Klaveren, SLAC
"""

import json
from .response import ScalarResponse, VectorResponse, ErrorResponse

class TypeDecoder(json.JSONDecoder):
    """
    A JSONDecoder which allows subclasses to notify if they can decode a type.
    """
    def __init__(self, **kwargs):
        super(TypeDecoder, self).__init__(object_hook=self.object_hook, **kwargs)

    def decode_object(self, obj):
        return obj

    def can_decode(self, obj):
        return False

    def object_hook(self, obj):
        if self.can_decode(obj):
            return self.decode_object(obj)
        return obj

class ScalarResponseDecoder(TypeDecoder):
    def __init__(self, **kwargs):
        super(ScalarResponseDecoder, self).__init__(**kwargs)

    def can_decode(self, obj):
        return u"result" in obj.keys()

    def decode_object(self, obj):
        return ScalarResponse(obj["result"])

class VectorResponseDecoder(TypeDecoder):
    def __init__(self, **kwargs):
        super(VectorResponseDecoder, self).__init__(**kwargs)

    def can_decode(self, obj):
        return u"results" in obj.keys()

    def decode_object(self, obj):
        return VectorResponse(obj["results"])

class ErrorResponseDecoder(TypeDecoder):
    def __init__(self, **kwargs):
        super(ErrorResponseDecoder, self).__init__()

    def can_decode(self, obj):
        return u"exception" in obj.keys()

    def decode_object(self, obj):
        return ErrorResponse(exception=obj["exception"])

class MixInDecoder(TypeDecoder):
    def __init__(self, decoders, **kwargs):
        """
        MixInDecoder takes a list of TypeDecoders as it's only parameter. It will iterate through the list
        of TypeDecoders and search for a TypeDecoder which can decode the object, then decode it with that
        TypeDecoder
        :param Decoders: List of TypeDecoders
        """
        super(MixInDecoder, self).__init__(**kwargs)
        self._decoders = decoders

    def decode_object(self, obj):
        decoder = self.get_decoder(obj)
        return decoder.decode_object(obj) if decoder else json.JSONDecoder.decode(obj)

    def can_decode(self, obj):
        return self.get_decoder(obj) is not None

    def get_decoder(self, obj):
        for decoder in self._decoders:
            if decoder.can_decode(obj):
                return decoder
        return None

class ResponseDecoder(MixInDecoder):
    def __init__(self, **kwargs):
        super(ResponseDecoder, self).__init__([ScalarResponseDecoder(**kwargs),
                                               VectorResponseDecoder(**kwargs),
                                               ErrorResponseDecoder(**kwargs)], **kwargs)
