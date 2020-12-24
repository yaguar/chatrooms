import base64
import logging
import aiohttp_jinja2
import jinja2
from cryptography import fernet
from aiohttp import web
from motor import motor_asyncio as ma
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from routes import routes
from models import db
from middleware import authorization


async def init_app():
    """Запуск различных баз"""
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    middle = [
        session_middleware(EncryptedCookieStorage(secret_key)),
        authorization,
        db
    ]
    app = web.Application(middlewares=middle)
    app['config'] = {}
    app['config']['gino'] = {'user': 'username', 'password': 'password', 'host': '0.0.0.0', 'port': '5433',
                             'database': 'chat_db'}
    client = ma.AsyncIOMotorClient('mongodb://root:example@0.0.0.0:27017')
    mongo = client['chat_db']
    app['mongo'] = mongo

    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    # change path
    app.router.add_static('/static', '/home/python/chatrooms/static', name='static')

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('/home/python/chatrooms/templates'))
    db.init_app(app)

    return app


async def shutdown(app):
    """Функция вызывается при остановке приложения"""

    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()


def main():
    """Функция запуска"""
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    web.run_app(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
