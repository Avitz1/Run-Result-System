import os
import configparser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

db = SQLAlchemy()
cache = Cache()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://user:password@localhost/db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

    db.init_app(app)
    cache.init_app(app)

    from backend.source.routes import main
    app.register_blueprint(main)

    return app
