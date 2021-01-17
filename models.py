from gino.ext.aiohttp import Gino

db = Gino()


class User(db.Model):
    """Модель пользователя в postgres"""

    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), autoincrement=True, primary_key=True)
    login = db.Column(db.Unicode(), default='noname')
    passwd = db.Column(db.Unicode(), default='noname')


async def init_db():
    """Инициализация postgres"""

    async with db.set_bind('postgres://username:password@0.0.0.0:5432/chat_db'):
        await db.gino.create_all()
