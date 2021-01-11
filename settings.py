import os

POSTGRES = {
    'user': os.getenv('PG_USER', 'username'),
    'password': os.getenv('PG_PASSWORD', 'password'),
    'host': os.getenv('PG_HOST', '0.0.0.0'),
    'port': os.getenv('PG_PORT', '5432'),
    'database': 'chat_db'
}

MONGO = {
    'login': os.getenv('MONGO_LOGIN', 'root'),
    'password': os.getenv('MONGO_PASSWORD', 'example'),
    'host': os.getenv('MONGO_HOST', '0.0.0.0'),
    'port': os.getenv('MONGO_PORT', '27017'),
}

MONGO_URL = f'mongodb://{MONGO["login"]}:{MONGO["password"]}@{MONGO["host"]}:{MONGO["port"]}'
