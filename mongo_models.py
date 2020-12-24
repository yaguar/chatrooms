from datetime import datetime


class Users():
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
                await self.collection.update_one({'user': user}, {'$set': {'chats': user_chats['chats']}})
            else:
                await self.collection.insert_one({'user': user, 'chats': [{'id': chat_id, 'name': name}, ]})


class Chats():
    """
        Объект чата в монге

        'name': name,
        'users': users,
        'create_time': time
    """

    def __init__(self, collection):
        self.collection = collection

    async def create_chat(self, name, users):
        """Создаем новый чат"""

        time = datetime.now()
        result = await self.collection.insert_one({'name': name, 'users': users, 'create_time': time})
        return result
