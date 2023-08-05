"""
Crypto helper.

"""

from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from web3.auto.infura.mainnet import w3
from web3.exceptions import TransactionNotFound

import pickle
networks = {
  'bnb_test': {
    'rpc_url': 'https://data-seed-prebsc-1-s1.binance.org:8545/',
    'chain_id': '97',
    'currency': 'BNB',
    'explorer_url': 'https://testnet.bscscan.com',
    'w3_client': Web3(HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/')),
    'minimal_confirm': 2
  },
  'bnb_main': {
    'rpc_url': 'https://bsc-dataseed1.ninicoin.io',
    'chain_id': '56',
    'currency': 'BNB',
    'explorer_url': 'https://bscscan.com',
    'w3_client': Web3(HTTPProvider('https://bsc-dataseed1.ninicoin.io')),
    'minimal_confirm': 3
  },
  'et_main': {  # not tested
    'rpc_url': 'https://rpc.ankr.com/eth',  # https://rpc.info/
    'chain_id': '1',
    'currency': 'ETH',
    'explorer_url': 'https://etherscan.io',
    'w3_client': w3  # still some issues iwth compatibility
  }
}
for k, v in networks.items():
    if k.endswith(''):
        v['w3_client'].middleware_onion.inject(geth_poa_middleware, layer=0)


def check_transactions_by_wallet(blockchain_address: str, network: str = 'bnb_main'):
    w3 = networks[network]['w3_client']

    # request the latest block number
    ending_blocknumber = w3.eth.blockNumber
    ending_blocknumber = 20951990

    # latest block number minus 100 blocks
    starting_blocknumber = ending_blocknumber - 1

    # create an empty dictionary we will add transaction data to
    tx_dictionary = {}

    print(
        f"Started filtering through block number {starting_blocknumber} to {ending_blocknumber} for transactions involving the address - {blockchain_address}...")
    for x in range(starting_blocknumber, ending_blocknumber):
        block = w3.eth.getBlock(x, True)
        for transaction in block.transactions:
            # print(transaction)
            if str(transaction['to'].lower()) == blockchain_address or str(transaction['from'].lower()) == blockchain_address:
                print(transaction)
                with open("transactions.pkl", "wb") as f:
                    hashStr = transaction['hash'].hex()
                    tx_dictionary[hashStr] = transaction
                    pickle.dump(tx_dictionary, f)
                f.close()
    print(f"Finished searching blocks {starting_blocknumber} through {ending_blocknumber} and found {len(tx_dictionary)} transactions")


def check_transaction_status(transaction_hash: str, network: str = 'bnb_main', logger: object = None) -> bool:
    w3 = networks[network]['w3_client']
    minimal_confirm = networks[network]['minimal_confirm']
    try:
        result = w3.eth.get_transaction(transaction_hash=transaction_hash)
        if logger:
            logger.debug((f"Transaction-status: {result}"))
        return True
    except TransactionNotFound as e:
        print("Transaction not found, keep going")
        return None


if __name__ == '__main__':
    print(check_transaction_status('0x393baaae506524538a729f26307c3e289d934c642660b7a65bab7cc5e56314a6', network='bnb_test'))
