from aiohttp import web
from mongo_models import Chats, Users
from serializers import JSONEncoder
from models import User


class NewChat(web.View):
    """Вьюха для создания нового чата"""

    async def post(self):
        """
            1. Создать в монге чат
            2. Добавить в монге каждому пользователю список чатов
        """

        data = await self.request.json()
        # transaction
        chats = Chats(self.request.app['mongo']['chats'])
        chat = await chats.create_chat(data['name'], data['users'])
        users = Users(self.request.app['mongo']['users'])
        await users.add_chat_in_users(data['users'], str(chat.inserted_id), data['name'])
        return web.Response(status=201)


class MainInfo(web.View):
    """Вьюха для получения основной информации пользователя из постгрес (id, логин)"""

    async def get(self):
        """Отдать информацию о пользователе"""

        request = self.request
        # pydantic
        return web.Response(status=200, body=JSONEncoder().encode({'id': request.id, 'login': request.login}))


class LoginList(web.View):
    """Вьюха списка полизователей и чатов"""

    async def get(self):
        """Отдать список пользователей"""
        search = self.request.rel_url.query['q']
        users = await User.query.where(User.login.contains(search)).gino.all()
        return web.Response(status=200, body=JSONEncoder().encode(users[:10]))
