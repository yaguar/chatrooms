from aiohttp import web
from aiohttp.web import middleware
from aiohttp_session import get_session
from utils.other_utils import check_pass, check_path


@middleware
async def authorization(request, handler):
    """Авторизация"""

    session = await get_session(request)
    id_ = session.get('id')
    login = session.get('login')
    password = session.get('password')
    if not login and check_path(request.path) or login and not await check_pass(login, password):
        raise web.HTTPFound('/login')
    request.login = login
    request.id = id_
    return await handler(request)
