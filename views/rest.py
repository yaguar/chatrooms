from datetime import datetime
from aiohttp import web, WSMsgType
from aiohttp_session import get_session
from mongo_models import MongoChats, MongoUsers, MongoMessages
from serializers import JSONEncoder
from models import User


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
        session = await get_session(self.request)
        login = session.get('login')
        login_list = [user['login'] for user in data['users']]
        login_list.append(login)
        login_list = list(set(login_list))
        # transaction
        chats = MongoChats(self.request.app['mongo']['chats'])
        chat = await chats.create_chat(login_list, data['chatName'])
        users = MongoUsers(self.request.app['mongo']['users'])
        await users.add_chat_in_users(login_list, str(chat.inserted_id), data['chatName'])
        return web.Response(status=201)


class ChatList(web.View):
    """Вьюха списка полизователей и чатов"""

    async def get(self):
        """Отдать список пользователей и чатов"""
        search = self.request.rel_url.query['q']
        session = await get_session(self.request)
        login = session.get('login')
        if search:
            chat_list = await User.query.where(User.login.contains(search.replace('_', r'\_')))\
                .where(User.login != login).gino.all()
            chat_list = chat_list[:10]
            if len(chat_list) < 10:
                mongo = MongoChats(self.request.app['mongo']['chats'])

                new_chat_list = await mongo.search_chat(search)
                for chat in new_chat_list:
                    chat['id'] = str(chat.pop('_id'))
                    chat['login'] = chat.pop('name')
                chat_list.extend(new_chat_list)
        else:
            chats = MongoUsers(self.request.app['mongo']['users'])
            chat_list = await chats.get_chats(login)
            for chat in chat_list:
                chat['login'] = chat.pop('name')
        return web.Response(status=200, body=JSONEncoder().encode(chat_list))


class LoginList(web.View):
    """Вьюха списка полизователей и чатов"""

    async def get(self):
        """Отдать список пользователей"""
        search = self.request.rel_url.query['q']
        session = await get_session(self.request)
        login = session.get('login')
        login_list = []
        if search:
            login_list = await User.query.where(User.login.contains(search.replace('_', r'\_')))\
                .where(User.login != login).gino.all()
        return web.Response(status=200, body=JSONEncoder().encode(login_list[:10]))


class Messages(web.View):
    """Вьюха для работы с сообщениями"""

    async def get(self):
        """Метод для выдачи списка сообщений у конкретного чата"""

        chat_id = self.request.match_info.get('chat_id', None)
        users = MongoUsers(self.request.app['mongo']['users'])
        session = await get_session(self.request)
        login = session.get('login')
        if chat_id.isdigit():
            dialogs = await users.get_dialogs(login)
            chat_id = dialogs.get(chat_id, None)
        if chat_id is not None:
            mongo = MongoChats(self.request.app['mongo']['chats'])
            messages = await mongo.get_messages(chat_id)
        else:
            messages = []
        await users.zero_unread(login, chat_id)
        return web.Response(status=200, body=JSONEncoder().encode(messages))

    async def post(self):
        """Метод для обработки сообщения в чате"""

        # Записываем в базы
        chat_id = self.request.match_info.get('chat_id', None)
        session = await get_session(self.request)
        login = session.get('login')
        data = await self.request.json()
        message = data['message']
        mongo_chats = MongoChats(self.request.app['mongo']['chats'])
        users = MongoUsers(self.request.app['mongo']['users'])
        if chat_id.isdigit():
            dialogs = await users.get_dialogs(login)
            dlg_id = chat_id
            if dialogs.get(chat_id, None) is None:
                login2 = await User.select('login').where(User.id == int(chat_id)).gino.scalar()
                chat_id = await mongo_chats.create_chat([login, login2])
                chat_id = str(chat_id.inserted_id)
                await users.create_dialog(login, dlg_id, chat_id)
                await users.create_dialog(login2, session.get('id'), chat_id)
                await users.add_chat_in_users([login, ], chat_id, login2)
                await users.add_chat_in_users([login2, ], chat_id, login)
        time = datetime.now()
        # Как то красиво завернуть
        obj_msg = {'user': login, 'msg': message, 'time': time}
        await mongo_chats.add_msg(chat_id, obj_msg)
        users_from_this_chat = await mongo_chats.get_users_from_chat(chat_id)
        for user in users_from_this_chat:
            await users.add_msg(user, chat_id, message)
        mongo_msg = MongoMessages(self.request.app['mongo']['messages'])
        await mongo_msg.add_message(chat_id, obj_msg)

        # Раскидываем по вебсокетам
        obj_msg['time'] = str(obj_msg['time'])
        users = await mongo_chats.get_users_from_chat(chat_id)
        for user in users:
            if user in self.request.app['websockets']:
                await self.request.app['websockets'][user].send_json(obj_msg)

        return web.Response(status=201)


class WebSocket(web.View):
    """Класс для работы с websockets"""

    async def get(self):
        """Создаем пул вебсокетов"""

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        login = self.request.login
        self.request.app['websockets'][login] = ws

        # Обязательная конструкция
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        del self.request.app['websockets'][login]
        return ws
