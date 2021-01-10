
import pytest
from app import init_app


@pytest.fixture
async def client(aiohttp_client):
    app = await init_app(True)
    return await aiohttp_client(app)
