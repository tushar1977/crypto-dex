from flask import Flask
from .config import Config as conf
from dotenv import load_dotenv
from flask_login.utils import session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


load_dotenv()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(conf)

    db.init_app(app)

    Migrate(app, db)

    from .routes import r

    app.register_blueprint(r)
    from .portfolio import p

    app.register_blueprint(p, url_prefix="/api/portfolio")

    return app
