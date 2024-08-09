from dataclasses import dataclass

from flask_login import UserMixin
from sqlalchemy.orm import Mapped
from . import db
import enum


class WalletType(enum.Enum):
    IMPORTED_WALLET = "imported_wallet"
    NEW_WALLET = "new_wallet"


@dataclass
class User_Wallet_info(UserMixin, db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    wallet_address: Mapped[str] = db.Column(db.String(42), nullable=False)
    wallet_private_key: Mapped[str] = db.Column(db.String(1000), nullable=False)
    wallet_mnemonic: Mapped[str] = db.Column(db.String(1000))
    wallet_type: Mapped[str] = db.Column(db.Enum(WalletType))
