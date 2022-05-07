import abc
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from authentication import config
from authentication.adapters.template_parser import TemplateParser


class AbstractNotification(abc.ABC):
    @abc.abstractmethod
    def send(self, destination: str, message: str):
        raise NotImplementedError


DEFAULT_HOST = config.get_email_host_and_port()["host"]
DEFAULT_PORT = config.get_email_host_and_port()["port"]
DEFAULT_SENDER_ADDRESS = config.get_email_host_and_port()['sender_address']
DEFAULT_SENDER_PASSWORD = config.get_email_host_and_port()['sender_password']


class EmailNotification(AbstractNotification):
    # TODO Create a separate service responsible for sending "official emails" with templates, tags, images etc.
    def __init__(
        self,
        smtp_host=DEFAULT_HOST,
        smtp_port=DEFAULT_PORT,
        sender_address=DEFAULT_SENDER_ADDRESS,
        sender_password=DEFAULT_SENDER_PASSWORD
    ):
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._sender_address = sender_address
        self._sender_password = sender_password

        self.connect()

    def connect(self):
        self.server = smtplib.SMTP(self._smtp_host, self._smtp_port)
        self.server.starttls()
        self.server.login(self._sender_address, self._sender_password)

    def send(self, destination, message):
        if not self.server:
            return
        msg = MIMEMultipart('alternative')
        message = TemplateParser.verification_email_template()
        part2 = MIMEText(message, 'html')
        msg.attach(part2)

        self.server.sendmail(
            from_addr=self._sender_address,
            to_addrs=[destination],
            msg=msg.as_string()
        )

    def reconnect(self):
        if self.server is not None:
            self.server.quit()
            self.server = None
        self.connect()
