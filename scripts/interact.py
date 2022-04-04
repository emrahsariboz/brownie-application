from brownie import StorageContract, accounts, config, network
from scripts.helpfulscripts import get_account


def fund():
    fund_me = StorageContract[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()

    print(entrance_fee)
    print(f"Current entry fee is {entrance_fee}")
    print("Funding....")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = StorageContract[-1]
    account = get_account()

    fund_me.withdraw({"from": account})


def main():
    fund()
