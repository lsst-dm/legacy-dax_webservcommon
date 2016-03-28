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
    def decode_object(self, obj):
        """
        Subclasses should implement this and return the type of object they intend to decode.
        @param obj: Object to decode
        :return: Decoded object
        """
        return obj

    def can_decode(self, obj):
        """
        This method is called by the object hook to see if this encoder can decode it.
        It's exposed so the MixinEncoder can use it as well.
        This method should inspect the object (A python dictionary object) for some
        sort of signature that it recognizes.
        @param obj: Object to check if this TypeEncoder can decode it.
        @return: True if we can decode it.
        """
        return False

    def object_hook(self, obj):
        if self.can_decode(obj):
            return self.decode_object(obj)
        return obj


class MixInDecoder(TypeDecoder):
    def __init__(self, **kwargs):
        """
        MixInDecoder takes a list of TypeDecoders as it's only parameter. It will iterate through the list
        of TypeDecoders and search for a TypeDecoder which can decode the object, then decode it with that
        TypeDecoder
        @param decoders: List of TypeDecoders
        """
        self.decoders = kwargs.get("decoders", [])

    def decode_object(self, obj):
        decoder = self.get_decoder(obj)
        return decoder.decode_object(obj) if decoder else obj

    def can_decode(self, obj):
        return self.get_decoder(obj) is not None

    def get_decoder(self, obj):
        for decoder in self.decoders:
            if decoder.can_decode(obj):
                return decoder
        return None


class ScalarResponseDecoder(TypeDecoder):
    def can_decode(self, obj):
        return "result" in obj.keys()

    def decode_object(self, obj):
        return ScalarResponse(obj["result"])


class VectorResponseDecoder(TypeDecoder):
    def can_decode(self, obj):
        return "results" in obj.keys()

    def decode_object(self, obj):
        return VectorResponse(obj["results"])


class ErrorResponseDecoder(TypeDecoder):
    def can_decode(self, obj):
        return "error" in obj.keys()

    def decode_object(self, obj):
        return ErrorResponse(error=obj["error"])


class ResponseDecoder(MixInDecoder):
    def __init__(self, **kwargs):
        self.decoders = [ScalarResponseDecoder(**kwargs),
                         VectorResponseDecoder(**kwargs),
                         ErrorResponseDecoder(**kwargs)]

