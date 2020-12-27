from datetime import datetime
from bson.objectid import ObjectId

class MongoUsers:
    """
        Объект пользователя в монге

        'user': логин
        'chats': [ {'id': chat_id, 'name': name} ] - список чатов для пользователя
    """

    def __init__(self, collection):
        self.collection = collection

    async def add_chat_in_users(self, users, chat_id, name):
        """Добавляем каждому пользователю новый чат"""

        for user in users:
            user_chats = await self.collection.find_one({'user': user})
            if user_chats:
                user_chats['chats'].append({'id': chat_id, 'name': name})
                _id = user_chats['_id']
                await self.collection.update_one({'_id': _id}, {'$set': {'chats': user_chats['chats']}})
            else:
                await self.collection.insert_one({'user': user, 'chats': [{'id': chat_id, 'name': name}, ]})

    async def get_chats(self, user):
        """Получить список чатов пользователя"""

        result = await self.collection.find_one({'user': user})
        return result['chats']


class MongoChats:
    """
        Объект чата в монге

        'name': name,
        'users': users,
        'create_time': time,
        'messages': [ {'login': login, 'msg': msg, 'time': time}, ]
    """

    def __init__(self, collection):
        self.collection = collection

    async def create_chat(self, name, users):
        """Создаем новый чат"""

        time = datetime.now()
        result = await self.collection.insert_one({'name': name, 'users': users, 'create_time': time})
        return result

    async def get_messages(self, chat_id):
        """Получаем список сообщений"""

        result = await self.collection.find_one({'_id': ObjectId(chat_id)})
        return result.get('messages', [])

    async def add_msg(self, chat_id, msg):
        """Создаем сообщение"""

        chat = await self.collection.find_one({'_id': ObjectId(chat_id)})
        msgs = chat.get('messages', [])
        if len(msgs) >= 100:
            msgs.pop(0)
        msgs.append(msg)
        await self.collection.update_one({'_id': ObjectId(chat_id)}, {'$set': {'messages': msgs}})


class MongoMessages:
    """
        Объект чата в монге

        'chat_id': id чата,
        'login': имя пользователя, который отправил сообщение,
        'time': время создания сообщения,
        'msg': текст сообщения
    """

    def __init__(self, collection):
        self.collection = collection

    async def add_message(self, chat_id, msg):
        """Добавляем новое сообщение"""

        result = await self.collection.insert_one({'chat_id': chat_id, **msg})
        return result
