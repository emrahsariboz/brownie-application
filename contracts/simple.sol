// SPDX-License-Identifier: MIT
pragma solidity ^0.6.7;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract StorageContract {
    using SafeMathChainlink for uint256;

    address[] public funders;
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    mapping(address => uint256) public addressToAmoundFunded;

    AggregatorV3Interface priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        // 50$
        uint256 minimumUSD = 50 * 10**18;
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more money"
        );
        addressToAmoundFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() external view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();

        // Returned Price: 345278793257
        // which is already multiplied by 10^8 to remove decimal.
        // Actual price of 1 ETH is: 3452.78793257 $

        // 1 ETH is 10^18 WEI. We already have 10^8 multiplied.
        // We multiply again with 10^10.
        // We just wanna have same decimal for every unit!

        // Returned ETH / DOLLAR RATE has 18 decimal point!
        return uint256(answer * 10000000000);
    }

    // GWEI TO USD!
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        // = (3452289226890000000000 * 10 ^-18 )  * (1000000000)
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 10000000000;
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
    }
}
