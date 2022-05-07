import time
from uuid import uuid4
from operator import itemgetter
from typing import Callable, List

from authentication.domain import events
from authentication import exceptions as exc
from authentication.enums import TokenTypes


class BaseModel:
    pass


class User(BaseModel):
    def __init__(
            self,
            username: str,
            password: str,
            email: str,
            is_admin: bool = False,
            is_verified: bool = False,
            is_banned: bool = False,
            is_deleted: bool = False,
    ):
        self.id = uuid4()
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin
        self.is_verified = is_verified
        self.is_banned = is_banned
        self.is_deleted = is_deleted

    # Login user. If user is not verified send verification email.
    def login(self, password: str) -> None:
        if self.password != password:
            raise exc.AuthenticationError(f'Invalid user credentials')

        if self.is_banned:
            raise exc.AuthenticationError(f'User is banned')

        if self.is_deleted:
            raise exc.AuthenticationError(f'User is deleted')

        if not self.is_verified:
            self.events.append(events.NeedEmailVerification(
                id=self.id,
                email=self.email,
            ))
            raise exc.AuthenticationError(f'User is not verified')

    # Verifies user account, in case of repetitive verification raise VerificationError
    def verify(self, token: str, decoder: Callable) -> None:
        if self.is_verified:
            raise exc.VerificationError(f'User is already verified')

        exp, token_type = itemgetter('exp', 'token_type')(decoder(token))

        if token_type != TokenTypes.VERIFICATION_EMAIL:
            raise exc.VerificationError(f'Invalid token type')

        if time.time() > exp:
            raise exc.VerificationError(f'Token expired')

        self.is_verified = True

    def ban(self):
        self.is_banned = True

    def unban(self):
        self.is_banned = False

    def delete(self):
        self.is_deleted = True
