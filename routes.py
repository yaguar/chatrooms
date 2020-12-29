from views.pages import Registration, RoomMessages, Login
from views.rest import MainInfo, ChatList, NewChat, Messages, WebSocket

routes = [
    ('GET', '/', RoomMessages, 'room_messages'),
    ('GET', '/main_info', MainInfo, 'main_info'),
    ('GET', '/chat_list', ChatList, 'chat_list'),
    ('POST', '/new_chat', NewChat, 'new_chat'),
    ('*', '/messages/{chat_id}', Messages, 'messages'),
    ('*', '/login', Login, 'login'),
    ('*', '/registration', Registration, 'registration'),
    ('GET', '/ws', WebSocket, 'socket_message')
]
