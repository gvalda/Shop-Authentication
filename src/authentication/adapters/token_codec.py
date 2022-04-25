import abc

import jwt

from authentication import config


class AbstractCodec(abc.ABC):
    def __init__(self, secret: str = config.get_jwt_secret(), algorithm: str = 'HS256'):
        self.secret = secret
        self.algorithm = algorithm

    @abc.abstractmethod
    def encode(self, payload: dict) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, token: str,) -> dict:
        raise NotImplementedError


class JwtCodec(AbstractCodec):
    def encode(self, payload: dict,) -> str:
        return jwt.encode(
            payload,
            self.secret,
            self.algorithm
        )

    def decode(self, token: str,) -> dict:
        return jwt.decode(
            token,
            self.secret,
            self.algorithm
        )
