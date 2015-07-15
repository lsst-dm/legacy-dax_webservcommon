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

from lsst.dax.webservcommon import ScalarResponse, VectorResponse, ErrorResponse, renderObjectResponse

result = [i for i in range(2)]
results = [result for i in range(3)]

class RenderTemplateTest(unittest.TestCase):

    def test_vector(self):
        response = VectorResponse(results)
        expected = """\
<!doctype html>
<html>
  <head><title>Found Object(s)</title></head>
  <body>
    <div class="results">

    <table>
      <tbody>
          <tr><td>0</td><td>1</td></tr>
          <tr><td>0</td><td>1</td></tr>
          <tr><td>0</td><td>1</td></tr>
      </tbody>
    </table>
    </div>
</body>
</html>"""
        html = renderObjectResponse(response=response, status_code = 200)
        self.assertEqual(expected, html, "Vector response incorrect")

    def test_scalar(self):
        response = ScalarResponse(result)
        expected = """\
<!doctype html>
<html>
  <head><title>Found Object(s)</title></head>
  <body>
    <div class="results">

    <table>
      <tbody>
          <tr><td>0</td><td>1</td></tr>
          <tr><td>0</td><td>1</td></tr>
          <tr><td>0</td><td>1</td></tr>
      </tbody>
    </table>
    </div>
</body>
</html>"""
        html = renderObjectResponse(response=response, status_code = 200)
        self.assertEqual(expected, html, "Scalar response incorrect")

    def test_error(self):
        response = ErrorResponse("NotFoundException")
        expected = """\
<!doctype html>
<html>
  <head><title>404 - An Error occurred</title></head>
  <body>
    <div class="exception">
      Exception: NotFoundException
    </div></body>
</html>"""
        html = renderObjectResponse(response=response, status_code = 404)
        self.assertEqual(expected, html, "Scalar response incorrect")
