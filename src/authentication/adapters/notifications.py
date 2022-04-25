import abc

import smtplib

from authentication import config


class AbstractNotification(abc.ABC):
    @abc.abstractmethod
    def send(self, destination, message):
        raise NotImplementedError


DEFAULT_HOST = config.get_email_host_and_port()["host"]
DEFAULT_PORT = config.get_email_host_and_port()["port"]
DEFAULT_SENDER = config.get_email_host_and_port()['sender']


class EmailNotification(AbstractNotification):
    def __init__(
        self,
        smtp_host=DEFAULT_HOST,
        smtp_port=DEFAULT_PORT,
        sender=DEFAULT_SENDER
    ):
        self.server = smtplib.SMTP(smtp_host, smtp_port)
        self.sender = sender

    def send(self, destination, message,):
        self.server.sendmail(
            from_addr=self.sender,
            to_addrs=[destination],
            msg=message
        )
