# Import dependencies
import os
import subprocess
import json
from pprint import pprint
from dotenv import load_dotenv

# Load and set environment variables
load_dotenv()
mnemonic = os.getenv("MNEMONIC")
# mnemonic = "culture toddler flock leisure judge fuel dwarf cram high phone fire east"

# Import constants.py and necessary functions from bit and web3
from constants import *
from bit import PrivateKeyTestnet
from bit import wif_to_key
from bit.network import NetworkAPI
from web3 import Web3
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from getpass import getpass

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Create a function called `derive_wallets`
def derive_wallets(coin, mnemonic, numderive):
    command = f'./derive -g --format=json --mnemonic="{mnemonic}" --coin="{coin}" --numderive={numderive} --cols=all'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
numderive = 3
coins = {
    BTCTEST: derive_wallets(BTCTEST, mnemonic, numderive),
    ETH: derive_wallets(ETH, mnemonic, numderive)
}
pprint(coins)

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    # Why am I passing in priv_key if I can call it from the coins dictionary?
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

# # Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin == ETH:
        value = w3.toWei(amount,"ether")
        gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": to, "value": value}
        )
        return {
            "to": to,
            "from": account.address,
            "value": value,
            "gas": gasEstimate,
            "gasPrice": w3.eth.gasPrice,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chaidID": w3.eth.chain_id
        }

    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, coin)])

# # Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    if coin == ETH:
        tx = create_tx(coin, account, to, amount)
        signed = account.sign_transaction(tx)
        return w3.eth.sendRawTransaction(signed.rawTransaction)

    if coin == BTCTEST:
        tx = create_tx(coin, account, to, amount)
        signed = account.send(tx)
        return NetworkAPI.broadcast_tx_testnet(signed)

print(priv_key_to_account(ETH, coins[ETH][0]['privkey']))
sender_account = priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey'])
receiver_account =  coins[BTCTEST][1]['address']

send_tx('btc-test', sender_account, receiver_account, .001)