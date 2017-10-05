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
Generic renderer for Responses
@author  Brian Van Klaveren, SLAC
"""

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('lsst.dax.webservcommon', 'templates'))

vector_template = env.get_template('vector_response.html')
scalar_template = env.get_template('scalar_response.html')
table_template = env.get_template('table_response.html')
error_template = env.get_template('error_response.html')


def render_response(response, status_code=None):
    if 'result' in response:
        if isinstance(response, dict):
            if 'table' in response["result"]:
                return render_table_response(response, status_code)
        return scalar_template.render(response=response, status_code=status_code)
    if 'results' in response:
        return vector_template.render(response=response, status_code=status_code)
    if 'error' in response:
        return error_template.render(response=response, status_code=status_code)


def render_table_response(response, status_code=None):
    return table_template.render(response=response, status_code=status_code)
