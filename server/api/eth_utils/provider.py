from web3 import Web3

from .config.ethConfigVars import infura_testnet_goerli_project_http_rpc_url
from .config.ethConfigVars import TEST_WALLET_ADDRESS, TEST_WALLET_PRIVATE_KEY

infura_provider = Web3.HTTPProvider(endpoint_uri=infura_testnet_goerli_project_http_rpc_url)
w3_infura = Web3(infura_provider)

chain_id = w3_infura.eth.chain_id
nonce = w3_infura.eth.get_transaction_count(TEST_WALLET_ADDRESS)

# Test
if __name__ == "__main__":
    print(w3_infura.isConnected())
    pass



