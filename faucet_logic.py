

from nacl.signing import SigningKey
import hashlib
import requests
import time
from typing import Any, Dict, Optional

TESTNET_URL = "https://fullnode.devnet.aptoslabs.com"
FAUCET_URL = "https://faucet.devnet.aptoslabs.com"

#:!:>section_1
class RestClient:
    """A wrapper around the Aptos-core Rest API"""

    def __init__(self, url: str) :#-> None:
        self.url = url

    def account(self, account_address: str):# -> Dict[str, str]:
        """Returns the sequence number and authentication key for an account"""

        response = requests.get(f"{self.url}/accounts/{account_address}")
        assert response.status_code == 200, f"{response.text} - {account_address}"
        return response.json()

    def account_resources(self, account_address: str):# -> Dict[str, Any]:
        """Returns all resources associated with the account"""

        response = requests.get(f"{self.url}/accounts/{account_address}/resources")
        assert response.status_code == 200, response.text
        return response.json()

    def transaction_pending(self, txn_hash: str):# -> bool:
        response = requests.get(f"{self.url}/transactions/{txn_hash}")
        if response.status_code == 404:
            return True
        assert response.status_code == 200, f"{response.text} - {txn_hash}"
        return response.json()["type"] == "pending_transaction"

    def wait_for_transaction(self, txn_hash: str):# -> None:
        """Waits up to 10 seconds for a transaction to move past pending state."""

        count = 0
        while self.transaction_pending(txn_hash):
            assert count < 10, f"transaction {txn_hash} timed out"
            time.sleep(1)
            count += 1

    def account_balance(self, account_address: str) :# -> Optional[int]:
        """Returns the test coin balance associated with the account"""

        resources = self.account_resources(account_address)
        for resource in resources:
            if resource["type"] == "0x1::TestCoin::Balance":
                return int(resource["data"]["coin"]["value"])
        return None

#<:!:section_1


#:!:>section_2
class FaucetClient:
    """Faucet creates and funds accounts. This is a thin wrapper around that."""

    def __init__(self, url: str, rest_client: RestClient) :#-> None:
        self.url = url
        self.rest_client = rest_client

    def fund_account(self, address: str, amount: int):# -> None:
        """This creates an account if it does not exist and mints the specified amount of
        coins into that account."""
        txns = requests.post(f"{self.url}/mint?amount={amount}&address={address}")
        assert txns.status_code == 200, txns.text
        for txn_hash in txns.json():
            self.rest_client.wait_for_transaction(txn_hash)
#<:!:section_2

rest_client = RestClient(TESTNET_URL)
faucet_client = FaucetClient(FAUCET_URL, rest_client)

# my_address = '45b44793724a5ecc6ad85fa60949d0824cfc7f61d6bd74490b13598379313141'
# #len = 64

# #amount max 20_000
# faucet_client.fund_account(my_address, 20000)
# print(f"My balance: {rest_client.account_balance(my_address)}")

