import json
import datetime
from bson import ObjectId
from models import User


class JSONEncoder(json.JSONEncoder):
    """Маленький сериалайзер"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        if isinstance(o, User):
            return {'id': o.id, 'login': o.login}
        return json.JSONEncoder.default(self, o)
