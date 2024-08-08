from dataclasses import dataclass

from flask_login import UserMixin
from sqlalchemy.orm import Mapped
from . import db


@dataclass
class User_Wallet_info(UserMixin, db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    wallet_address: Mapped[str] = db.Column(db.String(42), nullable=False)
    wallet_private_key: Mapped[str] = db.Column(db.String(1000), nullable=False)
    wallet_mnemonic: Mapped[str] = db.Column(db.String(1000))

    def has_private_key(self):
        return self.wallet_private_key is not None and len(self.wallet_private_key) > 0

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
