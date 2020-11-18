LOCALHOST = '127.0.0.1'

USER_APP_HOST = LOCALHOST
USER_APP_PORT = 5001

OFFERS_APP_HOST = LOCALHOST
OFFERS_APP_PORT = 5002

DB_CONFIG = {
    'postgres_host': 'localhost',
    'postgres_port': 5432,
    'user': 'napoleon',
    'password': 'password',
    'database': 'napoleon_db',
    'models': ['db.models'],
}

SALT = 'NAPOLEON'
