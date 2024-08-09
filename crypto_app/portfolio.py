from flask import Flask, Blueprint, jsonify, session
from dotenv import load_dotenv
import os
from web3 import Web3
from alchemy import Alchemy, Network
from concurrent.futures import ThreadPoolExecutor, as_completed

alchemy = Alchemy()
load_dotenv()
p = Blueprint("p", __name__)

api_key = os.getenv("API")
network = Network.ETH_MAINNET
alchemy = Alchemy(api_key, network, max_retries=3)


def format_balance(balance):
    return Web3.from_wei(int(balance, 16), "ether")


def get_token_data(token):
    balance = format_balance(token.token_balance)
    if abs(balance) <= 1.0:
        return None

    metadata = alchemy.core.get_token_metadata(token.contract_address)
    return {
        "symbol": metadata.symbol if len(str(metadata.symbol)) <= 7 else "Unknown",
        "token_balance": "{:.3f}".format(balance),
    }


@p.route("/get_balancer", methods=["GET"])
def get_balance():
    address = "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C"

    all_tokens = alchemy.core.get_token_balances(address)
    balance_wei = alchemy.core.get_balance(address, "latest")

    # Convert balance from Wei to Ether
    balance_eth = balance_wei / 10**18

    formatted_tokens = []
    with ThreadPoolExecutor(max_workers=30) as executor:
        future_to_token = {
            executor.submit(get_token_data, token): token
            for token in all_tokens["token_balances"]
        }
        for future in as_completed(future_to_token):
            token_data = future.result()
            if token_data:
                formatted_tokens.append(token_data)
    formatted_tokens.sort(key=lambda x: x["token_balance"], reverse=True)

    result = {
        "address": address,
        "eth_balance": "{:.5f}".format(balance_eth),
        "token_balances": formatted_tokens,
    }

    return jsonify(result)
