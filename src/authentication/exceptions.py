class InvalidUserCredentials(Exception):
    pass


class UserNotVerified(Exception):
    pass


class UserDeleted(Exception):
    pass


class UserBanned(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class InvalidToken(Exception):
    pass
