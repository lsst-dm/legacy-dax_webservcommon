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


import unittest
import json
from collections import OrderedDict
from lsst.webservcommon import ResponseEncoder, MixInEncoder, TypeEncoder, ResponseDecoder, TypeDecoder, MixInDecoder
from lsst.webservcommon import ScalarResponse, VectorResponse, ErrorResponse

class TestObject(object):
    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __eq__(self, other):
        if not type(other) == type(self):
            return False
        return other.__dict__ == self.__dict__

    def __str__(self):
        return "TestObject({},{})".format(self.a, self.b)

class ComplexEncoder(TypeEncoder):
    def can_encode(self, obj):
        return isinstance(obj, complex)

    def default(self, obj):
        return [obj.real, obj.imag]

class TestObjectEncoderDecoder(TypeEncoder, TypeDecoder):
    def can_encode(self, obj):
        return isinstance(obj, TestObject)

    def can_decode(self, obj):
        return "_type" in obj.keys() and obj["_type"] == "TestObject"

    def default(self, obj):
        ret = OrderedDict([("_type", "TestObject")])
        ret.update(obj.__dict__)
        return ret

    def decode_object(self, obj):
        return TestObject(obj["a"], obj["b"])

class TestResponseEncodingDecoding(unittest.TestCase):

    def test_object_response(self):
        result = {
            "a":1,
            "b":2
        }

        expected = {
            "result":{
                "a":1,
                "b":2
            }
        }

        actual = ScalarResponse(result)

        encoder = ResponseEncoder()
        decoder = ResponseDecoder()
        # Note: There's implicit guarantee "a" is before "b" in a hash-based dict.
        expected_str = json.dumps(expected)
        actual_str = encoder.encode(actual)

        expected_dict = json.loads(expected_str)
        actual_dict = json.loads(actual_str)
        self.assertEqual(actual_dict, expected_dict)

        expected_obj = decoder.decode(expected_str)
        actual_obj = decoder.decode(actual_str)
        self.assertEqual(actual_obj, expected_obj)


    def test_error_response(self):
        encoder = ResponseEncoder()
        decoder = ResponseDecoder()
        expected = ErrorResponse("SomeError")
        actual = decoder.decode(encoder.encode(ErrorResponse("SomeError")))
        self.assertEqual(actual, expected)

    def test_mixin_encoder(self):

        expected = {
            "results":[
                {
                    "_type": "TestObject",
                    "a":2,
                    "b":4
                },
                [2.0, 1.0]
            ]
        }

        actual = VectorResponse([TestObject(2, 4), 2+1j])

        resultsEncoder = MixInEncoder([ComplexEncoder(), TestObjectEncoderDecoder()])
        encoder = MixInEncoder([ResponseEncoder(), resultsEncoder])
        decoder = ResponseDecoder()

        expected_str = json.dumps(expected)
        actual_str = encoder.encode(actual)

        expected_dict = json.loads(expected_str)
        actual_dict = json.loads(actual_str)
        self.assertEqual(actual_dict, expected_dict)

        expected_obj = decoder.decode(expected_str)
        actual_obj = decoder.decode(actual_str)
        self.assertEqual(actual_obj, expected_obj)

    def test_mixin_decoder(self):
        expected = {
            "results":[
                {
                    "_type": "TestObject",
                    "a":2,
                    "b":4
                },
                [2.0, 1.0]
            ]
        }

        actual = VectorResponse([TestObject(2, 4), 2+1j])

        resultsEncoder = MixInEncoder([ComplexEncoder(), TestObjectEncoderDecoder()])
        encoder = MixInEncoder([ResponseEncoder(), resultsEncoder])
        decoder = MixInDecoder([ResponseDecoder(), TestObjectEncoderDecoder()])
        obj = decoder.decode(encoder.encode(ScalarResponse(TestObject(2, 4))))

        expected_str = json.dumps(expected)
        actual_str = encoder.encode(actual)

        expected_dict = json.loads(expected_str)
        actual_dict = json.loads(actual_str)
        self.assertEqual(actual_dict, expected_dict)

        expected_obj = decoder.decode(expected_str)
        actual_obj = decoder.decode(actual_str)
        self.assertEqual(actual_obj, expected_obj)

    def test_json_with_cls(self):
        expected_obj = ErrorResponse("SomeError")
        actual_str = json.dumps(ErrorResponse("SomeError"), cls=ResponseEncoder)
        actual_obj = json.loads(actual_str, cls=ResponseDecoder)
        self.assertEqual(actual_obj, expected_obj)
