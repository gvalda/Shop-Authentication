from __future__ import annotations
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
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable]
    ):
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        results = []
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, commands.Command):
                self.handle_command(message)
            elif isinstance(message, events.Event):
                result = self.handle_event(message)
                if result:
                    results.append(result)
            else:
                raise TypeError(f"Unknown message type: {type(message)}")
        return results

    def handle_command(self, command: commands.Command):
        try:
            handler = self.command_handlers[type(command)]
            events = handler(command)
            if events:
                self.queue.extend(events)
        except Exception:
            raise

    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                result, events = handler(event)
                if events:
                    self.queue.extend(events)
                return result
            except Exception:
                continue
