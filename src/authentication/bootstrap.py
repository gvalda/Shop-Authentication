import inspect
import logging

from authentication.adapters.notifications import AbstractNotification, EmailNotification
from authentication.adapters.publications import AbstractPublication, RedisPublication
from authentication.adapters.codec import AbstractCodec, JwtCodec
from authentication.service_layer import unit_of_work, messagebus, handlers
from authentication.adapters import orm


def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
    notifications: AbstractNotification = None,
    publish: AbstractPublication = None,
    codec: AbstractCodec = None
) -> messagebus.MessageBus:

    if notifications is None:
        try:
            notifications = EmailNotification()
        except Exception as e:
            logging.error(f"Failed to initialize email notifications: {e}")

    if publish is None:
        publish = RedisPublication()

    if codec is None:
        codec = JwtCodec()

    if start_orm:
        orm.start_mappers()

    dependencies = {
        'uow': uow,
        'notifications': notifications,
        'codec': codec,
        'publish': publish
    }

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
