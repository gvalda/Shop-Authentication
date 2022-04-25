from dataclasses import asdict
import json
import abc

import redis

from authentication.domain import events
from authentication import config


class AbstractPublication(abc.ABC):
    @abc.abstractmethod
    def publish(self, chanel: str, event: events.Event):
        raise NotImplementedError


# TODO add system variables
DEFAULT_HOST = config.get_redis_host_and_port()["host"]
DEFAULT_PORT = config.get_redis_host_and_port()["port"]


class RedisPublication(AbstractPublication):
    def __init__(
        self,
        host=DEFAULT_HOST,
        port=DEFAULT_PORT
    ):
        self.r = redis.Redis(host, port)

    def publish(self, chanel: str, event: events.Event):
        self.r.publish(chanel, json.dumps(asdict(event)))
