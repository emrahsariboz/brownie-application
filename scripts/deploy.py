from brownie import config, accounts, MockV3Aggregator, StorageContract, network
from scripts.helpfulscripts import (
    get_account,
    deploy_mock,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        network_now = network.show_active()
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        print(network_now)
    else:
        deploy_mock()
        price_feed_address = MockV3Aggregator[-1].address
        print("Mocks Deployed at", price_feed_address)

    contract = StorageContract.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    print(f"Contract deployed at {contract.address}")
    return contract


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy()
