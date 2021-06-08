# Import dependencies
import os
import subprocess
import json
from pprint import pprint
from dotenv import load_dotenv

# Load and set environment variables
load_dotenv()
mnemonic = os.getenv("MNEMONIC")

# Import constants.py and necessary functions from bit and web3
from constants import *
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3 import Web3
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware
from eth_account import Account

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
            # "chaidID": w3.eth.chain_id
            # I had to comment this out, otherwise I was getting an error saying Transaction must not include unrecognized fields: {'chaidID'}
        }

    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to.address, amount, BTC)])

# # Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    if coin == ETH:
        tx = create_tx(coin, account, to, amount)
        signed = account.sign_transaction(tx)
        print(signed)
        return w3.eth.sendRawTransaction(signed.rawTransaction)

    if coin == BTCTEST:
        tx = create_tx(coin, account, to, amount)
        signed = account.sign_transaction(tx)
        print(signed)
        return NetworkAPI.broadcast_tx_testnet(signed)


# Set ETH variables and call send_tx function
eth_sender_account = priv_key_to_account(ETH, coins[ETH][1]['privkey'])
eth_reciever_account = coins[ETH][0]['address']
send_tx(ETH, eth_sender_account, eth_reciever_account, 5)

# Set BTCTEST variables and call send_tx function
btc_sender_account = priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey'])
btc_receiver_account = priv_key_to_account(BTCTEST, coins[BTCTEST][1]['privkey'])
send_tx(BTCTEST, btc_sender_account, btc_receiver_account, .0001)