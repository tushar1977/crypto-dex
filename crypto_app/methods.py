import secrets
from eth_account import Account
from flask import session
from flask_login.login_manager import LoginManager
from flask_login.utils import current_app
from mnemonic import Mnemonic
from .models import User_Wallet_info

from hashlib import sha256

mnemo = Mnemonic()


def create_wallet():
    mnemonic_phrase = mnemo.generate(strength=256)
    seed = mnemo.to_seed(mnemonic_phrase)
    private_key = sha256(seed).hexdigest()
    acct = Account.from_key(private_key)

    return private_key, acct.address, mnemonic_phrase


def import_wallet(private_key):
    acct = Account.from_key(private_key)

    return acct.address


def get_phase(private_key):
    return mnemo.to_mnemonic(bytes.fromhex(private_key[2:]))
