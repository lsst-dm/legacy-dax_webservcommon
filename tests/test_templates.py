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

from lsst.dax.webservcommon import render_response, render_table_response

result = [i for i in range(2)]
results = [result for i in range(3)]


class RenderTemplateTest(unittest.TestCase):

    def test_vector(self):
        response = dict(results=results)
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
        html = render_response(response=response, status_code=200)
        expected = [line.strip() for line in expected.splitlines(1)]
        html = [line.strip() for line in html.splitlines(1)]
        self.assertEqual(expected, html, "Vector response incorrect")

    def test_scalar(self):
        response = dict(result=result)
        expected = """\
<!doctype html>
<html>
  <head><title>Found Object(s)</title></head>
  <body>
    <div class="result">

    <table>
      <tbody>
          <tr><td>0</td><td>1</td></tr>
      </tbody>
    </table>
    </div>
</body>
</html>"""
        html = render_response(response=response, status_code=200)
        expected = [line.strip() for line in expected.splitlines(1)]
        html = [line.strip() for line in html.splitlines(1)]
        self.assertEquals(expected, html, "Scalar response incorrect")

    def test_error(self):
        response = dict(error="NotFoundException")
        expected = """\
<!doctype html>
<html>
  <head><title>404 - An Error occurred</title></head>
  <body>
    <div class="error">
      Error: NotFoundException
    </div></body>
</html>"""
        html = render_response(response=response, status_code=404)
        self.assertAlmostEqual(expected, html, "Scalar response incorrect")

    def test_table(self):
        response = {
            "result": {
                "table": {
                    "metadata": {
                        "elements": [
                            {"name": "deepForcedSourceId", "datatype": "long"},
                            {"name": "scienceCcdExposureId", "datatype": "long"}
                        ]
                    },
                    "data": [
                        [8404051561545729, 125230127],
                        [8404051561545730, 125230127]
                    ]
                }
            }
        }

        expected = """\
<!doctype html>
<html>
  <head><title>Found Object(s)</title></head>
  <body>
    <div class="result">


    <table>
      <thead>
        <tr><th data-datatype="long">deepForcedSourceId</th><th data-datatype="long">scienceCcdExposureId</th>
        </tr>
      </thead>
      <tbody>
          <tr><td>8404051561545729</td><td>125230127</td></tr>
          <tr><td>8404051561545730</td><td>125230127</td></tr>
      </tbody>
    </table>
    </div>
</body>
</html>"""

        html = render_response(response=response, status_code=200)
        expected = [line.strip() for line in expected.splitlines(1)]
        html = [line.strip() for line in html.splitlines(1)]
        self.assertEqual(expected, html, "Table response incorrect")
