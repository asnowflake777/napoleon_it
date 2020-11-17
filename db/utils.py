from tortoise import Tortoise
from tortoise.contrib.sanic import register_tortoise

from settings import DB_CONFIG
from db.exceptions import DBConfigurationError


required_params = ('postgres_host', 'postgres_port', 'user', 'password', 'database', 'models')
provided_params = [DB_CONFIG.get(param) for param in required_params]

if not all(provided_params):
    not_provided_params = [name for name, value in zip(required_params, provided_params) if not value]
    raise DBConfigurationError('{} were not mentioned in settings.py'.format(', '.join(not_provided_params)))

db_host, db_port, user, password, database, models = provided_params

db_url = f'postgres://{user}:{password}@{db_host}:{db_port}/{database}'
models = {"models": models}


async def init_connection():
    return await Tortoise.init(
        db_url=db_url,
        modules=models,
    )


async def generate_schemas():
    await init_connection()
    await Tortoise.generate_schemas()


def connect_to_db(app):
    register_tortoise(
        app=app,
        db_url=db_url,
        modules=models,
        generate_schemas=True
    )
