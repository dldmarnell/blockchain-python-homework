# Multi-Blockchain Wallet in Python

The following code uses a command line tool called hd-wallet-derive to create an HD wallet for Ethereum and Bitcoin Testnet.  Python then uses bit and web3 to create and send transactions over both networks. 

---

## Technologies

Language: Python, PHP

Programs: bit, web3

Developed with Visual Studio

---

## Installation

**HD Wallet Derive** - [Install HD Wallet Derive](https://github.com/dan-da/hd-wallet-derive)
- Install [Homebrew](https://brew.sh/)<br />
- Use the following command to update PHP to the full version:
![PHP_Install_Command](Resources/Images/install_php.png)
- Execute the following command if using a zsh shell:
![Execute_PHP_Command](Resources/Images/execute_command.png)
*Note: if using bash shell change .zshrc to .bash_profile*
- Verify the correct version of PHP was installed
- Clone and install HD Wallet Derive from the link above and using the following commands:
![Install_HD_Wallet_derive](Resources/Images/hd_wallet_clone.png)

**Go Ethereum** - [Install Go Ethereum](https://geth.ethereum.org/downloads/)
- *Please refer to [Testnet Documentation](Resources/testnet-documentation.pdf) to set up the Ethereum blockchain*

**MyCrypto** - [Install MyCrypto](https://download.mycrypto.com/)

---

## Instructions

**Ethereum:**</br>
- Add one of the ETH addresses to the pre-allocated accounts in the config json file from the Ethereum testnet you setup previously
![ETH_testnet_config](Resources/Images/testnet_config.png)
- Delete the geth folder in each node, then reinitialize using the command below. This will create a new chain and will prefund the account
![Reinitialize_nodes](Resources/Images/reinitialize_node.png)
- Since the w3.eth.generateGasPrice() function does not work with an empty chain, you must send a couple transactions using MyCrypto first. Print the coins dictionary and use an ETH address privkey to access the wallet in MyCrypto (*note: do not share your private key*)
![ETH_privkey](Resources/Images/coins_dict_eth.png)
- Run the code to send an ETH transaction
![ETH_send_tx](Resources/Images/eth_send_tx.png)
- Find the transaction ID 
![ETH_tx_hash](Resources/Images/eth_tx_hash.png)
- Open MyCrypto and check the transaction was successful
![ETH_tx_status](Resources/Images/eth_tx_status.png)


**Bitcoin Testnet:**
- Fund one of the BTCTEST addresses found in the coins dictionary using [this testnet faucet](https://testnet-faucet.mempool.co/)
![BTCTEST_address](Resources/Images/btctest_address.png)
- Run the code to send a BTCTEST transaction
![BTCTEST_send_tx](Resources/Images/btctest_send_tx.png)
- Enter the BTCTEST address into a [block explorer](https://tbtc.bitaps.com/) to watch the transaction
![BTCTEST_tx](Resources/Images/btctest_tx.png)

---

## Contributors

Drew Disbrow Marnell: dldmarnell@gmail.com

---

## License

MIT License
Copyright (c) 2021 Drew Disbrow Marnell