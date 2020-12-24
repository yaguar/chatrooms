from views.pages import Registration, RoomMessages, Login
from views.rest import MainInfo, LoginList, NewChat

routes = [
    ('GET', '/', RoomMessages, 'room_messages'),
    ('GET', '/main_info', MainInfo, 'main_info'),
    ('GET', '/login_list', LoginList, 'login_list'),
    ('POST', '/create_chat', NewChat, 'new_chat'),
    ('*', '/login', Login, 'login'),
    ('*', '/registration', Registration, 'registration'),
]
