import os

from authentication.utils import convert_timestr_to_sec


def get_postgres_uri():
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', 5432)
    user = os.environ.get('DB_USER', 'admin')
    password = os.environ.get('DB_PASSWORD', 'abc123')
    db_name = os.environ.get('DB_NAME', 'db_backend')
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'


def get_email_host_and_port():
    host = os.environ.get('EMAIL_HOST', 'localhost')
    port = os.environ.get('EMAIL_PORT', 25)
    sender = os.environ.get('EMAIL_SENDER_ADDRESS', 'example@mail.com')
    password = os.environ.get('EMAIL_SENDER_PASSWORD', 'password')

    return {
        'host': host,
        'port': port,
        'sender_address': sender,
        'sender_password': password
    }


def get_jwt_config():
    secret = os.environ.get('JWT_SECRET', 'secret')
    algorithm = os.environ.get('JWT_ALGORITHM', 'HS256')
    return {
        'secret': secret,
        'algorithm': algorithm,
    }


def get_login_exp_time():
    access_token_exp = convert_timestr_to_sec(
        os.environ.get('LOGIN_ACCESS_TOKEN_EXP_TIME', '1h')
    )
    refresh_token_exp = convert_timestr_to_sec(
        os.environ.get('LOGIN_REFRESH_TOKEN_EXP_TIME', '1d')
    )
    return {
        'access_token_exp': access_token_exp,
        'refresh_token_exp': refresh_token_exp,
    }


def get_email_verification_expiration_time():
    return convert_timestr_to_sec(
        os.environ.get('EMAIL_VERIFICATION_EXP_TIME', '1d')
    )


def get_redis_host_and_port():
    host = os.environ.get('REDIS_HOST', 'localhost')
    port = os.environ.get('REDIS_PORT', 6379)
    return {
        'host': host,
        'port': port,
    }
