import time
from operator import itemgetter
from collections import namedtuple
from typing import Any, List, Tuple

from authentication import config, exceptions as exc
from authentication.domain import events, commands
from authentication.adapters import codec
from authentication.enums import TokenTypes


ACCESS_TOKEN_EXP_TIME = config.get_login_exp_time()[
    'access_token_exp'
]
REFRESH_TOKEN_EXP_TIME = config.get_login_exp_time()[
    'refresh_token_exp'
]
EMAIL_VERIFICATION_TOKEN_EXP_TIME = config.get_email_verification_expiration_time()


def make_user_email_verification_notification(
    event: events.NeedEmailVerification,
    codec: codec.AbstractCodec
) -> Tuple[None, List[events.Event]]:
    token = codec.encode(
        {
            'user_id': event.id,
            'token_type': TokenTypes.VERIFICATION_EMAIL,
            'exp': time.time() + EMAIL_VERIFICATION_TOKEN_EXP_TIME,
        }
    )
    return (
        None,
        events.EmailVerificationNotificationMade(
            email=event.email,
            token=token,
        )
    )


def generate_user_access_token(
    event: events.UserLoggedIn | events.RefreshTokenVerified,
    codec: codec.AbstractCodec
) -> Tuple[Any, List[events.Event]]:
    access_token = codec.encode(
        {
            'user_id': event.id,
            'token_type': TokenTypes.LOGIN_ACCESS,
            'exp': time.time() + ACCESS_TOKEN_EXP_TIME,
        }
    )
    refresh_token = codec.encode(
        {
            'user_id': event.id,
            'token_type': TokenTypes.LOGIN_REFRESH,
            'exp': time.time() + REFRESH_TOKEN_EXP_TIME,
        }
    )

    tokens = namedtuple('Tokens', ['access_token', 'refresh_token'])(
        access_token,
        refresh_token,
    )
    return (
        tokens,
        []
    )


def refresh_tokens(
    cmd: commands.RefreshTokens,
    codec: codec.AbstractCodec,
) -> List[events.Event]:
    user_id, token_type, exp_time = itemgetter(
        'user_id', 'token_type', 'exp')(codec.decode(cmd.refresh_token))

    if token_type != TokenTypes.REFRESH_TOKEN:
        raise exc.VerificationError(f'Invalid token type')

    if time.time() > exp_time:
        raise exc.VerificationError(f'Token expired')

    return [
        events.RefreshTokenVerified(
            id=user_id,
        )
    ]
