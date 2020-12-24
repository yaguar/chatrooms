from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session

from utils import check_pass, set_session, create_user

from models import User


class RoomMessages(web.View):
    """Вьюха основной страницы"""

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        """Отдали шаблон"""
        pass


class Login(web.View):
    """Вьюха страница логина"""

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        """Отдали шаблон"""
        pass

    async def post(self):
        """Проверка логина и пароля"""

        data = await self.request.json()
        user = await User.query.where(User.login == data['login']).gino.first()
        if user and await check_pass(data['login'], data['password']):
            session = await get_session(self.request)
            set_session(session, user.id, user.login, data['password'])
        return web.Response(status=400, text='Неправильный логин или пароль')


class Registration(web.View):
    """Вьюха страницы регистрации"""

    @aiohttp_jinja2.template('registration.html')
    async def get(self):
        """Отдали шаблон"""
        pass

    async def post(self):
        """Регистрируем нового пользователя"""

        data = await self.request.json()
        user = await User.query.where(User.login == data['login']).gino.first()
        if not user and data['password']:
            id_ = await create_user(data['login'], data['password'])
            session = await get_session(self.request)
            set_session(session, id_, data['login'], data['password'])
        return web.Response(status=400, text='Данный логин уже существует')
