from http.client import FORBIDDEN


class HttpStatusCodes:
    OK_200 = 200
    CREATED_201 = 201
    BAD_REQUEST_400 = 400
    FORBIDDEN_403 = 403
    NOT_FOUND_404 = 404


class TokenTypes:
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'
    VERIFY_EMAIL = 'verify_email'
    REPETITIVE_VERIFY_EMAIL = 'repetitive_verify_email'
