import py
import pytest
from scripts.helpfulscripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    deploy_mock,
)
from scripts.deploy import deploy
from brownie import (
    accounts,
    StorageContract,
    config,
    network,
    MockV3Aggregator,
    exceptions,
)


def test_can_fund_and_withdraw():
    account = get_account()

    fund_me = deploy()

    entrance_fee = fund_me.getEntranceFee() + 100

    tx = fund_me.fund({"from": account, "value": entrance_fee})

    tx.wait(1)

    expected = fund_me.addressToAmoundFunded(account.address)

    assert expected == entrance_fee


def test_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")

    account = get_account()

    fund_me = deploy()

    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
