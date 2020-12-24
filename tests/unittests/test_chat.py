import json


class TestChat:

    async def test_get_main_info(self, client):
        await client.post('/login', json={'login': 'admin', 'password': 'admin'})
        resp = await client.get('/main_info')
        assert resp.status == 200
        text = await resp.text()
        result = json.loads(text)
        assert 'id' in result
        assert 'login' in result

    async def test_get_users_list(self, client):
        await client.post('/login', json={'login': 'admin', 'password': 'admin'})
        resp = await client.get('/login_list?q=')
        assert resp.status == 200
        text = await resp.text()
        result = json.loads(text)
        assert 'id' in result[0]
        assert 'login' in result[0]

    async def test_add_new_chat_for_user(self, client):
        await client.post('/login', json={'login': 'admin112', 'password': 'admin'})
        resp = await client.post('/create_chat', json={'name': 'test_chat', 'users': ['admin112', 'admin11', 'admin']})
        assert resp.status == 201
