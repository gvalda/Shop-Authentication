from authentication.domain import events, commands
from authentication.service_layer.handlers import (
    notification_handlers as ntf_h,
    publication_handlers as pub_h,
    authentication_handlers as auth_h,
    codec_handlers as codec_h,
)


EVENT_HANDLERS = {
    events.UserCreated: [
        pub_h.publish_user_created_event,
    ],
    events.UserLoggedIn: [
        codec_h.generate_user_access_token
    ],
    events.NeedEmailVerification: [
        codec_h.make_user_email_verification_notification,
    ],
    events.EmailVerified: [
        pub_h.publish_user_email_verified_event,
    ],
    events.RefreshTokenVerified: [
        codec_h.generate_user_access_token,
    ],
    events.EmailVerificationNotificationMade: [
        ntf_h.send_user_verification_token,
    ],
    events.UserDeactivated: [
        pub_h.publish_user_deactivated_event,
    ],
    events.UserActivated: [
        pub_h.publish_user_activated_event,
    ],
}

COMMAND_HANDLERS = {
    commands.CreateUser: auth_h.create_user,
    commands.LoginUser: auth_h.login_user,
    commands.RefreshTokens: codec_h.refresh_tokens,
    commands.VerifyUserEmail: auth_h.verify_user_email,
    commands.UpdateUserPassword: auth_h.update_user_password,
    commands.UpdateUserEmail: auth_h.update_user_email,
    commands.BanUser: auth_h.ban_user,
    commands.UnbanUser: auth_h.unban_user,
    commands.DeleteUser: auth_h.delete_user,
}
