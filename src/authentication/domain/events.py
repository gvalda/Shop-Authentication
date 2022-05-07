from dataclasses import dataclass
import uuid


class Event:
    pass


@dataclass
class UserCreated(Event):
    id: uuid.uuid4
    username: str


@dataclass
class NeedEmailVerification(Event):
    id: uuid.uuid4
    email: str


@dataclass
class UserLoggedIn(Event):
    id: uuid.uuid4


@dataclass
class EmailVerificationNotificationMade(Event):
    email: str
    token: str


@dataclass
class UserVerified(Event):
    id: uuid.uuid4


@dataclass
class EmailVerified(Event):
    id: uuid.uuid4


@dataclass
class UserDeactivated(Event):
    id: uuid.uuid4


@dataclass
class UserActivated(Event):
    id: uuid.uuid4


@dataclass
class RefreshTokenVerified(Event):
    id: uuid.uuid4
