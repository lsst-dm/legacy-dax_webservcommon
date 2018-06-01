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

    def __init__(self, key, issuer=None, audience=None, options=None):
        """
        JwtAuth is a thin wrapper around the PyJWT project. Parameters
        are best documented in that project.
        :param key: Public key to verify RS256 signatures with
        :param issuer: Domain of issuer, if applicable
        :param audience: Audience of token, if applicable. If this is
        false, then the check is turned off
        :param options: verification options to pass to decode
        """
        if key is None:
            raise DaxAuthException("Need a valid public key for initialization")
        self.key = key
        self.issuer = issuer
        self.options = options or {}
        self.audience = audience
        if not self.audience and "verify_aud" not in self.options:
            self.options["verify_aud"] = False

    def jwt_required(self):
        """View decorator that requires a valid JWT token and adds"""

        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                self._validate()
                return fn(*args, **kwargs)

            return decorator

        return wrapper

    def _validate(self):
        header = request.headers.get('Authorization', None)
        if not header:
            raise DaxAuthException("No Auth header")
        parts = header.split()

        if not parts or parts[0].lower() != "bearer" or len(parts) != 2:
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
