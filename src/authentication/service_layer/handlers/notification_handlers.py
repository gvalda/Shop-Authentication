from authentication.domain import events
from authentication.adapters import notifications


def send_user_verification_token(
    event: events.EmailVerificationNotificationMade,
    notification: notifications.AbstractNotification,
):
    notification.send(event.email, "Verify your email" + event.token)
