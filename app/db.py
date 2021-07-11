from flask import current_app, g
from pymongo import MongoClient


def get_db():
    if 'db' not in g:
        g.db_client = MongoClient(
            host=current_app.config['DATABASE_ADD'],
            port=current_app.config['DATABASE_PORT'],
            username=current_app.config['DATABASE_USERNAME'],
            password=current_app.config['DATABASE_PASSWORD'],
            authSource=current_app.config['DATABASE_AUTHSOURCE'])
        g.db = g.db_client.get_database(
            current_app.config['DATABASE_AUTHSOURCE'])
    return g.db
