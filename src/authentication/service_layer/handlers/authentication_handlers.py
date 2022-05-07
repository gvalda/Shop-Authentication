from operator import itemgetter
from typing import List

from authentication import exceptions as exc
from authentication.domain import commands, events
from authentication.service_layer import unit_of_work
from authentication.adapters import codec
from authentication.enums import TokenTypes


def create_user(
    cmd: commands.CreateUser,
    uow: unit_of_work.AbstractUnitOfWork,
) -> List[events.Event]:
    with uow:
        user = uow.users.get(cmd.username)

        if user is not None:
            raise exc.RegistrationError("User already exists")

        user = uow.users.create(
            cmd.username,
            cmd.password,
            cmd.email
        )
        uow.commit()

    return [
        events.UserCreated(
            id=user.id,
            email=user.email,
        ),
        events.NeedEmailVerification(
            id=user.id,
            email=user.email,
        ),
    ]


def login_user(
    cmd: commands.LoginUser,
    uow: unit_of_work.AbstractUnitOfWork,
) -> List[events.Event]:
    with uow:
        user = uow.users.get(cmd.username)
        if user is None:
            raise exc.AuthenticationError("User not found")
        user.login(cmd.password)

    return [
        events.UserLoggedIn(
            id=user.id,
            email=user.email,
        ),
    ]


def verify_user_email(
    cmd: commands.VerifyUserEmail,
    uow: unit_of_work.AbstractUnitOfWork,
    codec: codec.AbstractCodec,
) -> List[events.Event]:
    with uow:
        user_id, token_type = itemgetter(
            'user_id', 'exp')(codec.decode(cmd.token))

        if token_type != TokenTypes.VERIFICATION_EMAIL:
            raise exc.VerificationError(f'Invalid token type')

        user = uow.users.get(user_id)
        if user is None:
            raise exc.AuthenticationError("User not found")

        user.verify(cmd.token, codec.decode)
        uow.commit()

    return [
        events.UserVerified(
            id=user.id,
        )
    ]


def ban_user(
    cmd: commands.BanUser,
    uow: unit_of_work.AbstractUnitOfWork,
) -> List[events.Event]:
    with uow:
        user = uow.users.get(cmd.username)
        if user is None:
            raise exc.AuthenticationError("User not found")
        user.ban()
        uow.commit()

    return [
        events.UserDeactivated(
            id=user.id,
        )
    ]


def unban_user(
    cmd: commands.UnbanUser,
    uow: unit_of_work.AbstractUnitOfWork,
) -> List[events.Event]:
    with uow:
        user = uow.users.get(cmd.username)
        if user is None:
            raise exc.AuthenticationError("User not found")
        user.unban()
        uow.commit()

    return [
        events.UserActivated(
            id=user.id,
        )
    ]


def delete_user(
    cmd: commands.DeleteUser,
    uow: unit_of_work.AbstractUnitOfWork,
) -> List[events.Event]:
    with uow:
        user = uow.users.get(cmd.username)
        if user is None:
            raise exc.AuthenticationError("User not found")
        user.delete()

    return [
        events.UserDeactivated(
            id=user.id,
        )
    ]


def update_user_password(
    cmd: commands.UpdateUserPassword,
    uow: unit_of_work.AbstractUnitOfWork,
) -> None:
    raise NotImplementedError


def update_user_email(
    cmd: commands.UpdateUserEmail,
    uow: unit_of_work.AbstractUnitOfWork,
) -> None:
    raise NotImplementedError
