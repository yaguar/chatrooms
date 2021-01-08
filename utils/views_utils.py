from datetime import datetime
from models import User
from mongo_models import MongoChats, MongoUsers, MongoMessages


async def get_chats(search, login, mongo):
    """Отдаем список чатов"""

    chats = MongoUsers(mongo['users'])
    if search:

        chat_list = await chats.search_chat(login, search)
        for chat in chat_list:
            chat['login'] = chat.pop('name')
        chat_list = chat_list[:10]
        if len(chat_list) < 10:
            new_chat_list = await User.query.where(User.login.contains(search.replace('_', r'\_'))) \
                .where(User.login != login).gino.all()
            chat_list.extend(new_chat_list[:10-len(chat_list)])
    else:
        chat_list = await chats.get_chats(login)
        for chat in chat_list:
            chat['login'] = chat.pop('name')
    return chat_list


async def create_chat(login, data, mongo):
    """Создаем чат"""

    login_list = [user['login'] for user in data['users']]
    login_list.append(login)
    login_list = list(set(login_list))
    # transaction
    chats = mongo['chats']
    chat = await chats.create_chat(login_list, data['chatName'])
    users = mongo['users']
    await users.add_chat_in_users(login_list, str(chat.inserted_id), data['chatName'])
    return login_list, {'id': str(chat.inserted_id), 'login': data['chatName'], 'unread': 0}


async def get_logins(search, login):
    """Отдаем список логинов"""

    login_list = []
    if search:
        login_list = await User.query.where(User.login.contains(search.replace('_', r'\_'))) \
            .where(User.login != login).gino.all()
    return login_list


async def get_messages(chat_id, login, mongo):
    """Действия при отдаче сообщений"""

    if chat_id.isdigit():
        dialogs = await mongo['users'].get_dialogs(login)
        chat_id = dialogs.get(chat_id, None)
    if chat_id is not None:
        messages = await mongo['chats'].get_messages(chat_id)
    else:
        messages = []
    await mongo['users'].zero_unread(login, chat_id)
    return messages


async def post_message(*args):
    """Действия при отправке сообщения"""

    chat_id, req_id, login, data, mongo = args
    mongo = {
        'chats': MongoChats(mongo['chats']),
        'messages': MongoMessages(mongo['messages']),
        'users': MongoUsers(mongo['users'])
    }
    message = data['message']
    if chat_id.isdigit():
        dialogs = await mongo['users'].get_dialogs(login)
        dlg_id = chat_id
        if dialogs.get(chat_id, None) is None:
            login2 = await User.select('login').where(User.id == int(chat_id)).gino.scalar()
            chat_id = await mongo['chats'].create_chat([login, login2])
            chat_id = str(chat_id.inserted_id)
            await mongo['users'].create_dialog(login, dlg_id, chat_id)
            await mongo['users'].create_dialog(login2, req_id, chat_id)
            await mongo['users'].add_chat_in_users([login, ], chat_id, login2)
            await mongo['users'].add_chat_in_users([login2, ], chat_id, login)
    time = datetime.now()
    # Как то красиво завернуть
    obj_msg = {'user': login, 'msg': message, 'time': time}
    await mongo['chats'].add_msg(chat_id, obj_msg)
    users_from_this_chat = await mongo['chats'].get_users_from_chat(chat_id)
    users_from_this_chat.remove(login)
    for user in users_from_this_chat:
        await mongo['users'].add_msg(user, chat_id, message)
    await mongo['messages'].add_message(chat_id, obj_msg)

    # Раскидываем по вебсокетам
    obj_msg['time'] = str(obj_msg['time'])
    obj_msg['chat_id'] = chat_id
    users = await mongo['chats'].get_users_from_chat(chat_id)
    return users, {'type': 'POST_MESSAGE', **obj_msg}
