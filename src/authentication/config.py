import os


def get_postgres_uri():
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', 5432)
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user = os.environ.get('DB_USER', 'admin')
    db_name = os.environ.get('DB_NAME', 'db_backend')
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'


def get_email_host_and_port():
    host = os.environ.get('EMAIL_HOST', 'localhost')
    port = os.environ.get('EMAIL_PORT', 25)
    sender = os.environ.get('EMAIL_USER', 'authentication@example.com')
    return {
        'host': host,
        'port': port,
        'sender': sender,
    }


def get_jwt_secret():
    return os.environ.get('JWT_SECRET', 'secret')


def get_expiration_times():
    access_token_exp = os.environ.get('ACCESS_TOKEN_EXP', '1h')
    refresh_token_exp = os.environ.get('REFRESH_TOKEN_EXP', '1d')
    return {
        'access_token_exp': access_token_exp,
        'refresh_token_exp': refresh_token_exp,
    }


def get_email_verification_expiration_time():
    return os.environ.get('EMAIL_VERIFICATION_EXP', '1d')


def get_repetitive_email_verification_expiration_time():
    return os.environ.get('REPETITIVE_EMAIL_VERIFICATION_EXP', '1d')


def get_redis_host_and_port():
    host = os.environ.get('REDIS_HOST', 'localhost')
    port = os.environ.get('REDIS_PORT', 6379)
    return {
        'host': host,
        'port': port,
    }
