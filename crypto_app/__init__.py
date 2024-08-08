from flask import Flask
from .config import Config as conf
from dotenv import load_dotenv
from flask_login.utils import session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


load_dotenv()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(conf)

    db.init_app(app)

    from .models import User_Wallet_info

    @login_manager.user_loader
    def load_user(user_id):
        user = User_Wallet_info()
        if "wallet_private_key" in session:
            user.wallet_private_key = session["wallet_private_key"]
        return user

    login_manager.init_app(app)
    login_manager.login_view = "login"

    Migrate(app, db)

    from .routes import r

    app.register_blueprint(r)

    return app
