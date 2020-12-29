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

    async def test_add_new_chat_for_user(self, client):
        await client.post('/login', json={'login': 'admin112', 'password': 'admin'})
        resp = await client.post('/new_chat', json={'chatName': 'test_chat', 'users': [
            {"id": 1, "login": "admin"},
            {"id": 228, "login": "admintest1"},
            {"id": 235, "login": "admin112"}
        ]})
        assert resp.status == 201

    async def test_get_chats_list(self, client):
        await client.post('/login', json={'login': 'admin', 'password': 'admin'})
        resp = await client.get('/chat_list?q=')
        assert resp.status == 200
        text = await resp.text()
        result = json.loads(text)
        assert 'id' in result[0]
        assert 'login' in result[0]

    async def test_get_msgs(self, client):
        await client.post('/login', json={'login': 'admin112', 'password': 'admin'})
        resp = await client.get('/chat_list?q=')
        text = await resp.text()
        result = json.loads(text)
        chat_id = result[0]['id']
        resp = await client.get(f'/messages/{chat_id}')
        assert resp.status == 200

    async def test_add_new_msg(self, client):
        await client.post('/login', json={'login': 'admin112', 'password': 'admin'})
        ws = await client.ws_connect('/ws')
        resp = await client.get('/chat_list?q=')
        text = await resp.text()
        result = json.loads(text)
        chat_id = result[0]['id']
        resp = await client.post(f'/messages/{chat_id}', json={"message": "тест2"})
        msg = await ws.receive()
        assert 'user' in msg.data
        assert 'msg' in msg.data
        assert 'time' in msg.data
        assert resp.status == 201

    # Добавить тест на несколько пользователей
