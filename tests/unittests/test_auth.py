from models import User 


class TestAuth:

    async def test_registration(self, client):
        user = await User.query.where(User.login == 'admin112').gino.first()
        if user:
            await user.delete()
        resp = await client.get('/registration')
        assert resp.status == 200
        resp = await client.post('/registration', json={'login': 'admin112', 'password':'admin'})
        assert resp.status == 200
        resp = await client.post('/registration', json={'login': 'admin112', 'password': 'admin'})
        assert resp.status == 400

    async def test_auth(self, client):
        resp = await client.get('/login')
        assert resp.status == 200
        resp = await client.post('/login', json={'login': 'admin112', 'password':'admin'})
        assert resp.status == 200