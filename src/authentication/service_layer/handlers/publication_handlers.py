from authentication.domain import events
from authentication.adapters import publications
from authentication.enums import PublishChannels as pc


def publish_user_created_event(
    event: events.UserCreated,
    publish: publications.AbstractPublication,
):
    publish(pc.USER_CREATED, event)


def publish_user_email_verified_event(
    event: events.UserVerified,
    publish: publications.AbstractPublication,
):
    publish(pc.USER_VERIFIED, event)


def publish_user_deactivated_event(
    event: events.UserDeactivated,
    publish: publications.AbstractPublication,
):
    publish(pc.USER_DEACTIVATED, event)


def publish_user_activated_event(
    event: events.UserActivated,
    publish: publications.AbstractPublication,
):
    publish(pc.USER_DEACTIVATED, event)
