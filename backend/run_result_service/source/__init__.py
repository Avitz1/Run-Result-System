import os
import configparser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

db = SQLAlchemy()
cache = Cache()


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name:
        app.config.from_object(config_name)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://user:password@localhost/db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["CACHE_TYPE"] = "simple"
        app.config["CACHE_DEFAULT_TIMEOUT"] = 1

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

    db.init_app(app)
    cache.init_app(app)

    from backend.run_result_service.source.routes import main
    app.register_blueprint(main)

    return app
