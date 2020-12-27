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

    async def test_get_chats_list(self, client):
        await client.post('/login', json={'login': 'admin', 'password': 'admin'})
        resp = await client.get('/chat_list?q=')
        assert resp.status == 200
        text = await resp.text()
        result = json.loads(text)
        assert 'id' in result[0]
        assert 'login' in result[0]

    async def test_add_new_chat_for_user(self, client):
        await client.post('/login', json={'login': 'admin112', 'password': 'admin'})
        resp = await client.post('/create_chat', json={'name': 'test_chat', 'users': ['admin112', 'admin11', 'admin']})
        assert resp.status == 201

    async def test_add_new_msg(self, client):
        await client.post('/login', json={'login': 'admin112', 'password': 'admin'})
        resp = await client.get('/chat_list?q=')
        text = await resp.text()
        result = json.loads(text)
        chat_id = result[0]['id']
        resp = await client.post(f'/messages/{chat_id}', json={"message": "тест"})
        assert resp.status == 201

    async def test_get_msgs(self, client):
        await client.post('/login', json={'login': 'admin112', 'password': 'admin'})
        resp = await client.get('/chat_list?q=')
        text = await resp.text()
        result = json.loads(text)
        chat_id = result[0]['id']
        resp = await client.get(f'/messages/{chat_id}')
        assert resp.status == 200
