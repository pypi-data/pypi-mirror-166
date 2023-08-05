"""
Crypto helper.

"""
import logging
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
# from web3.auto.infura.mainnet import w3
from web3.exceptions import TransactionNotFound
import pickle
import sys

logger = logging.getLogger(__name__)

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
  # 'et_main': {  # not tested
  #   'rpc_url': 'https://rpc.ankr.com/eth',  # https://rpc.info/
  #   'chain_id': '1',
  #   'currency': 'ETH',
  #   'explorer_url': 'https://etherscan.io',
  #   'w3_client': w3  # still some issues iwth compatibility
  # }
}
for k, v in networks.items():
    if k.endswith(''):
        v['w3_client'].middleware_onion.inject(geth_poa_middleware, layer=0)


def check_transactions_by_wallet(blockchain_address: str, network: str = 'bnb_main', Logger: object=None):
    # NOTE: WIP code. We are not sure when and how to use this method.
    w3 = networks[network]['w3_client']

    # request the latest block number
    ending_blocknumber = w3.eth.blockNumber

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


def check_transaction_status(transaction_hash: str, network: str = 'bnb_main') -> bool:
    w3 = networks[network]['w3_client']
    minimal_confirm = networks[network]['minimal_confirm']
    try:
        transaction = w3.eth.get_transaction(transaction_hash=transaction_hash)
        last_block = w3.eth.get_block_number()
        print(f"Received Tranasction, {transaction}, last_block: {last_block}")
        if last_block - transaction.get('blockNumber', sys.maxsize) >= minimal_confirm:
          return True
        else:
          logger.info(f"Transaction {transaction_hash} is available now but still needs more confirmation.")
          return False
    except TransactionNotFound:
        logger.info(f"Transaction {transaction_hash} not found yet.")
        return False


if __name__ == '__main__':
    print(check_transaction_status('0x393baaae506524538a729f26307c3e289d934c642660b7a65bab7cc5e56314a6', network='bnb_test'))
