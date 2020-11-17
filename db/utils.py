from tortoise import Tortoise
from tortoise.contrib.sanic import register_tortoise

from settings import DB_URL, MODULES


async def init_connection():
    return await Tortoise.init(
        db_url=DB_URL,
        modules=MODULES,
    )


async def generate_schemas():
    await init_connection()
    await Tortoise.generate_schemas()


def connect_to_db(app):
    register_tortoise(
        app=app,
        db_url=DB_URL,
        modules=MODULES,
        generate_schemas=True
    )
