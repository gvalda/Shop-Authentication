from operator import itemgetter
from typing import Dict
import uuid
import time

from authentication.service_layer import unit_of_work
from authentication.exceptions import (
    InvalidUserCredentials,
    UserAlreadyExists,
    UserNotVerified,
    UserDeleted,
    UserBanned,
    InvalidToken
)
from authentication.domain import model, commands, events
from authentication.adapters import token_codec, notifications, publications
from authentication.utils import convert_timestr_to_sec
from authentication.enums import TokenTypes
from authentication import config, enums


# TODO implement permission validation logic

def login_user(
    cmd: commands.LoginUser,
    uow: unit_of_work.AbstractUnitOfWork,
    codec: token_codec.AbstractCodec,
) -> Dict[str, str]:
    with uow:
        user = uow.users.get(cmd.username)
        if user is None or user.password != cmd.password:
            raise InvalidUserCredentials(
                f'Invalid user credentials {cmd.username}')

        if not user.is_verified:
            raise UserNotVerified(f'User {cmd.username} is not verified')

        if user.is_banned:
            raise UserBanned(f'User {cmd.username} is banned')

        if user.is_deleted:
            raise UserDeleted(f'User {cmd.username} is deleted')

        # TODO move exp time somewhere else
        # TODO now it breaks architecture
        access_token_exp, refresh_token_exp = config.get_expiration_times()

        access_token = codec.encode(
            {
                'user_id': user.id,
                'token_type': TokenTypes.ACCESS_TOKEN,
                'is_admin': user.is_admin,
                'is_verified': user.is_verified,
                'exp': time.time() + convert_timestr_to_sec(access_token_exp)
            })

        refresh_token = codec.encode({
            'user_id': user.id,
            'token_type': TokenTypes.REFRESH_TOKEN,
            'exp': time.time() + convert_timestr_to_sec(refresh_token_exp)
        })

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }


def create_user(
    cmd: commands.CreateUser,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        exists = uow.users.get(username=cmd.username) is not None
        if exists:
            raise UserAlreadyExists(f'User {cmd.username} already exists')
        user = model.User(
            id=uuid.uuid4(),
            username=cmd.username,
            password=cmd.password,
            email=cmd.email,
        )
        uow.users.add(user)
        uow.commit()


def verify_user_email(
    cmd: commands.VerifyUserEmail,
    uow: unit_of_work.AbstractUnitOfWork,
    codec: token_codec.AbstractCodec,
):
    with uow:
        user_id, exp, token_type = itemgetter(
            'user_id', 'exp', 'token_type')(codec.decode(cmd.token))

        user = uow.users.get_by_id(id=user_id)

        if user is None:
            raise InvalidToken(f'Invalid token {cmd.token}')

        # TODO make constants
        if token_type not in (TokenTypes.VERIFY_EMAIL, TokenTypes.REPETITIVE_VERIFY_EMAIL):
            raise InvalidToken(f'Invalid token type {token_type}')

        if time.time() > exp:
            raise InvalidToken(f'Expired token {cmd.token}')

        user.verify()
        uow.commit()


def publish_user_created_event(
    event: events.UserCreated,
    publish: publications.AbstractPublication,
):
    publish('user_created', event)


def send_user_created_email_verification(
    event: events.UserCreated,
    codec: token_codec.AbstractCodec,
    notification: notifications.AbstractNotification,
):
    # TODO MAKE CUSTOM FIRST VERIFICATION EMAIL TIME
    token = codec.encode(
        {
            'user_id': event.id,
            'token_type': TokenTypes.VERIFY_EMAIL,
            'exp': time.time() + convert_timestr_to_sec('1h'),
        }
    )
    # TODO make email verification template
    notification.send(event.email, "Verify your email" + token)


def send_user_email_verification(
    cmd: commands.SendUserVerificationEmail,
    uow: unit_of_work.AbstractUnitOfWork,
    codec: token_codec.AbstractCodec,
    notification: notifications.AbstractNotification,
):
    with uow:
        user = uow.users.get(cmd.username)

        if user is None:
            raise InvalidUserCredentials(
                f'Invalid user credentials {cmd.username}')

        # TODO MAKE CUSTOM VERIFICATION EMAIL TIME
        token = codec.encode(
            {
                'user_id': user.id,
                'token_type': TokenTypes.REPETITIVE_VERIFY_EMAIL,
                'exp': time.time() + convert_timestr_to_sec('1h'),
            }
        )
        # TODO make email verification template
        notification.send(user.email, "Verify your email" + token)


def publish_user_email_verified_event(
    event: events.UserEmailVerified,
    publish: publications.AbstractPublication,
):
    publish('user_verified', event)


def publish_user_banned_event(
    event: events.UserBanned,
    publish: publications.AbstractPublication,
):
    publish('user_banned', event)


def ban_user(
    cmd: commands.BanUser,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(cmd.username)

        if user is None:
            raise InvalidUserCredentials(
                f'Invalid user credentials {cmd.username}')

        user.ban()
        uow.commit()


def publish_user_unbanned_event(
    event: events.UserUnBanned,
    publish: publications.AbstractPublication,
):
    publish('user_unbanned', event)


def unban_user(
    cmd: commands.UnbanUser,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(cmd.username)

        if user is None:
            raise InvalidUserCredentials(
                f'Invalid user credentials {cmd.username}')

        user.unban()
        uow.commit()


def delete_user(
    cmd: commands.DeleteUser,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(cmd.username)

        if user is None:
            raise InvalidUserCredentials(
                f'Invalid user credentials {cmd.username}')

        user.delete()
        uow.commit()


def publish_user_deleted_event(
    event: events.UserDeleted,
    publish: publications.AbstractPublication,
):
    publish('user_deleted', event)


EVENT_HANDLERS = {
    events.UserCreated: [
        send_user_created_email_verification,
        publish_user_created_event,
    ],
    events.UserEmailVerified: [
        publish_user_email_verified_event,
    ],
    events.UserBanned: [
        publish_user_banned_event,
    ],
    events.UserUnBanned: [
        publish_user_unbanned_event,
    ],
    events.UserDeleted: [
        publish_user_deleted_event,
    ],
}

COMMAND_HANDLERS = {
    commands.CreateUser: create_user,
    commands.LoginUser: login_user,
    commands.UpdateUserPassword: None,
    commands.UpdateUserEmail: None,
    commands.SendUserVerificationEmail: send_user_email_verification,
    commands.VerifyUserEmail: verify_user_email,
    commands.BanUser: ban_user,
    commands.UnbanUser: unban_user,
    commands.DeleteUser: delete_user,
}
