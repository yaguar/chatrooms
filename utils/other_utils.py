"""Модуль с утилитами """

from time import time
from passlib.hash import pbkdf2_sha256
from aiohttp import web
from models import User


def set_session(session, id_, login, password):
    """Прописываем сессию полизователя, чтобы он мог авторизироваться"""

    session['id'] = str(id_)
    session['login'] = str(login)
    session['password'] = str(password)
    session['last_visit'] = time()
    raise web.HTTPFound('/')


def check_path(path):
    """Функция проверяет имеет ли право пользователь пройти по данному url"""

    return path not in ['/login', '/static/', '/signin', '/signout', '/registration']


async def create_user(login, password):
    """Создаем пользователя в postgres"""

    password_hash = pbkdf2_sha256.encrypt(password)
    user = await User.create(login=login, passwd=password_hash)
    return user.id


async def check_pass(login, password):
    """Аутентификация пользователя"""

    user = await User.query.where(User.login == login).gino.first()
    password_hash = user.passwd
    return pbkdf2_sha256.verify(password, password_hash)
