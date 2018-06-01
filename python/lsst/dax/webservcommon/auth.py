# LSST Data Management System
# Copyright 2018 AURA/LSST.
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
Authentication decorators for webserv Flask applications
"""

import json
from functools import wraps

import jwt
import requests
from flask import request, g
from jwt.algorithms import RSAAlgorithm

ALGORITHM = "RS256"


class DaxAuthException(Exception):
    pass


class JwtAuth:
    """JwtAuth is a thin wrapper around the PyJWT project.
    Parameters are best documented in that project.

    Parameters
    ----------
    key : RSAPublicKey
        Public key to verify RS256 signatures with
    issuer : str
        Domain of issuer, if applicable
    audience : str
        Audience of token, if applicable. If this is false or None,
        then the check is turned off
    options : dict
        Verification options to pass to PyJWT's decode function
    """

    def __init__(self, key, issuer=None, audience=None, options=None):
        if key is None:
            raise DaxAuthException("Need a valid public key for initialization")
        self.key = key
        self.issuer = issuer
        self.options = options or {}
        self.audience = audience
        if not self.audience and "verify_aud" not in self.options:
            self.options["verify_aud"] = False

    def jwt_required(self):
        """Flask decorator that requires a valid JWT token.
        Failures to authenticate raises exceptions.
        The REMOTE_USER request environment var will be set as well as
        valid JWT stored on success.

        Raises
        ------
        DaxAuthException
            If the Authorization header is missing or token is incorrect.
        InvalidTokenError
            If the token is invalid in some way
        """

        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                self._validate()
                return fn(*args, **kwargs)

            return decorator

        return wrapper

    def _validate(self):
        """Validate the token in the Flask request"""
        header = request.headers.get("Authorization", None)
        if not header:
            raise DaxAuthException("No Auth header")
        parts = header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise DaxAuthException("Not a bearer token")

        token = parts[1]
        decoded = jwt.decode(token, self.key, algorithm=ALGORITHM, audience=self.audience,
                             options=self.options)
        request.environ["REMOTE_USER"] = decoded["sub"]
        g.jwt = decoded


def demo_key():
    """This just returns a demo key from SciTokens"""
    jwk = requests.get("https://demo.scitokens.org/oauth2/certs").json()
    first_key = jwk["keys"][0]
    # arg... somebody issue a PR to PyJWT
    key_json = json.dumps(first_key)
    return RSAAlgorithm.from_jwk(key_json)
