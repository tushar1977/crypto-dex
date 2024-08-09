from flask import Blueprint, flash, render_template, request, url_for, session
from eth_account import Account
from flask.helpers import redirect
from flask_login import current_user, logout_user
from flask_login.utils import login_required
from .methods import create_wallet, get_phase, import_wallet
from .models import User_Wallet_info
from . import db
import bcrypt
from werkzeug.security import generate_password_hash

r = Blueprint("r", __name__)

Account.enable_unaudited_hdwallet_features()

salt = bcrypt.gensalt(rounds=15)


@r.route("/", methods=["GET"])
def index():
    if current_user.wallet_private_key:
        return render_template("profile.html")
    return render_template("index.html")


@r.route("/api/logout")
@login_required
def logout():
    logout_user()
    session.pop("wallet_private_key", None)
    return redirect(url_for("index"))


@r.route("/api/wallet_manager", methods=["POST"])
def create_import():
    print("hello")
    if "create_wallet" in request.form:
        print("create")
        try:
            private_key, acc_address, phase = create_wallet()
            hashed_private_key = bcrypt.hashpw(private_key.encode("utf-8"), salt)
            hashed_mnemonic = generate_password_hash(phase)
            if not private_key or acc_address:
                flash("Internal Error")

            wallet = User_Wallet_info(
                wallet_address=acc_address,
                wallet_private_key=hashed_private_key.decode("utf-8"),
                wallet_mnemonic=hashed_mnemonic,
                wallet_type="new_wallet",
            )

            db.session.add(wallet)
            db.session.commit()
            print("done")
            session["wallet_private_key"] = private_key
            session["wallet_address"] = acc_address
            flash("wallet created")
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error occured :- {str(e)}")
            return redirect(url_for("index"))
    elif "import_wallet" in request.form:
        priv_key = request.form.get("private_key")
        if not priv_key:
            flash("PRovdie private key")

        try:
            acc = import_wallet(priv_key)
            if not acc:
                flash("invalid private key")
            hashed_key = bcrypt.hashpw(priv_key.encode("utf-8"), salt)

            imp_wallet = User_Wallet_info(
                wallet_address=acc,
                wallet_private_key=hashed_key.decode("utf-8"),
                wallet_type="imported_wallet",
                wallet_mnemonic="",
            )

            db.session.add(imp_wallet)
            db.session.commit()
            session["wallet_private_key"] = priv_key

            session["wallet_address"] = acc
            flash("Imported!")
            return redirect(url_for("r.index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error :- {str(e)}")
            return redirect(url_for("r.index"))
