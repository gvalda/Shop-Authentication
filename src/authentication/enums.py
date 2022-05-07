class HttpStatusCodes:
    OK_200 = 200
    CREATED_201 = 201
    BAD_REQUEST_400 = 400
    FORBIDDEN_403 = 403
    NOT_FOUND_404 = 404


class TokenTypes:
    LOGIN_ACCESS = 'access_token'
    LOGIN_REFRESH = 'refresh_token'
    VERIFICATION_EMAIL = 'verify_email'


class PublishChannels:
    USER_CREATED = 'user_created'
    USER_VERIFIED = 'user_verified'
    USER_DEACTIVATED = 'user_deactivated'
    USER_ACTIVATED = 'user_activated'
