import json
from aiohttp import web, WSMsgType
from mongo_models import MongoChats, MongoUsers
from serializers import JSONEncoder
from utils.views_utils import get_chats, create_chat, get_logins, get_messages, post_message


class MainInfo(web.View):
    """Вьюха для получения основной информации пользователя из постгрес (id, логин)"""

    async def get(self):
        """Отдать информацию о пользователе"""

        request = self.request
        # pydantic
        return web.Response(status=200, body=JSONEncoder().encode({'id': request.id, 'login': request.login}))


class NewChat(web.View):
    """Вьюха для создания нового чата"""

    async def post(self):
        """
            1. Создать в монге чат
            2. Добавить в монге каждому пользователю список чатов
        """

        data = await self.request.json()
        login = self.request.login
        chats = MongoChats(self.request.app['mongo']['chats'])
        users = MongoUsers(self.request.app['mongo']['users'])
        await create_chat(login, data, {'users': users, 'chats': chats})
        return web.Response(status=201)


class ChatList(web.View):
    """Вьюха списка полизователей и чатов"""

    async def get(self):
        """Отдать список пользователей и чатов"""
        search = self.request.rel_url.query['q']
        login = self.request.login
        chat_list = await get_chats(search, login, self.request.app['mongo'])
        return web.Response(status=200, body=JSONEncoder().encode(chat_list))


class LoginList(web.View):
    """Вьюха списка полизователей и чатов"""

    async def get(self):
        """Отдать список пользователей"""
        search = self.request.rel_url.query['q']
        login = self.request.login
        login_list = await get_logins(search, login)
        return web.Response(status=200, body=JSONEncoder().encode(login_list[:10]))


class Messages(web.View):
    """Вьюха для работы с сообщениями"""

    async def get(self):
        """Метод для выдачи списка сообщений у конкретного чата"""

        chat_id = self.request.match_info.get('chat_id', None)
        users = MongoUsers(self.request.app['mongo']['users'])
        chats = MongoChats(self.request.app['mongo']['chats'])
        login = self.request.login
        messages = await get_messages(chat_id, login, {'users': users, 'chats': chats})
        return web.Response(status=200, body=JSONEncoder().encode(messages))

    async def post(self):
        """Метод для обработки сообщения в чате"""

        chat_id = self.request.match_info.get('chat_id', None)
        req_id = self.request.id
        login = self.request.login
        ws = self.request.app['websockets']
        data = await self.request.json()
        users, obj_msg = await post_message(chat_id, req_id, login, data, self.request.app['mongo'])
        for user in users:
            if user in ws:
                await ws[user].send_json(obj_msg)

        return web.Response(status=201)


class WebSocket(web.View):
    """Класс для работы с websockets"""

    async def get(self):
        """Создаем пул вебсокетов"""

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        req_id = self.request.id
        login = self.request.login
        self.request.app['websockets'][login] = ws

        # Обязательная конструкция
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    data = json.loads(msg.data)
                    if data['type'] == 'GET_CHATS':
                        chat_list = await get_chats(data['search'], login, self.request.app['mongo'])
                        await ws.send_json({'type': 'GET_CHATS', 'chats': JSONEncoder().encode(chat_list)})
                    elif data['type'] == 'CREATE_CHAT':
                        users, chat = await create_chat(login, data['chat'], {
                            'users': MongoUsers(self.request.app['mongo']['users']),
                            'chats': MongoChats(self.request.app['mongo']['chats'])
                        })
                        for user in users:
                            if user in self.request.app['websockets']:
                                await self.request.app['websockets'][user].send_json({
                                    'type': 'NEW_CHAT', 'chat': JSONEncoder().encode(chat)
                                })
                    elif data['type'] == 'GET_LOGINS':
                        login_list = await get_logins(data['search'], login)
                        await ws.send_json({'type': 'GET_LOGINS', 'logins': JSONEncoder().encode(login_list)})
                    elif data['type'] == 'GET_MESSAGES':
                        messages = await get_messages(str(data['chat_id']), login, {
                            'users': MongoUsers(self.request.app['mongo']['users']),
                            'chats': MongoChats(self.request.app['mongo']['chats'])
                        })
                        await ws.send_json({'type': 'GET_MESSAGES', 'msgs': JSONEncoder().encode(messages)})
                    elif data['type'] == 'POST_MESSAGE':
                        users, obj_msg = await post_message(
                            str(data['chat_id']),
                            req_id,
                            login, data,
                            self.request.app['mongo']
                        )
                        for user in users:
                            if user in self.request.app['websockets']:
                                await self.request.app['websockets'][user].send_json(obj_msg)

            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        del self.request.app['websockets'][login]
        return ws
