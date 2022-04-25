from dataclasses import dataclass
import uuid


class Command:
    pass


@dataclass
class CreateUser(Command):
    username: str
    password: str
    email: str


@dataclass
class LoginUser(Command):
    username: str
    password: str


@dataclass
class UpdateUserPassword(Command):
    username: str
    password: str


@dataclass
class UpdateUserEmail(Command):
    username: str
    email: str


@dataclass
class SendUserVerificationEmail(Command):
    username: str


@dataclass
class VerifyUserEmail(Command):
    token: str


@dataclass
class BanUser(Command):
    username: str


@dataclass
class UnbanUser(Command):
    username: str


@dataclass
class DeleteUser(Command):
    username: str
