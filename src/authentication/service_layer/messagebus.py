from __future__ import annotations
import re
from typing import (
    Callable,
    Dict,
    List,
    Union,
    Type,
    TYPE_CHECKING
)

from authentication.domain import commands, events

if TYPE_CHECKING:
    from . import unit_of_work

Message = Union[commands.Command, events.Event]


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable]
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        results = []
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, commands.Command):
                cmd_result = self.handle_command(message)
                results.append(cmd_result)
            elif isinstance(message, events.Event):
                self.handle_event(message)
            else:
                raise TypeError(f"Unknown message type: {type(message)}")
        return results

    def handle_command(self, command: commands.Command):
        try:
            handler = self.command_handlers[type(command)]
            result = handler(command)
            self.queue.extend(self.uow.collect_new_events())
            return result
        except Exception:
            raise

    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                continue
