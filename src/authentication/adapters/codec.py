import abc

import jwt

from authentication import config

DEFAULT_SECRET = config.get_jwt_config()['secret']
DEFAULT_ALGORITHM = config.get_jwt_config()['algorithm']


class AbstractCodec(abc.ABC):
    def __init__(self, secret: str = DEFAULT_SECRET, algorithm: str = DEFAULT_ALGORITHM):
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
