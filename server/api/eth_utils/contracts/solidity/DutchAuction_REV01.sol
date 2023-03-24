// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
/*
1. Seller of NFT deploys this contract setting a starting price for the NFT.
2. Auction lasts for 7 days.
3. Price of NFT decreases over time.
4. Participants can buy by depositing ETH greater than the current price computed by the smart contract.
5. Auction ends when a buyer buys the NFT.
*/
//import "./lib/openzepplin/contracts/token/ERC20/IERC20.sol";

interface IERC721 {
    function transferFrom(
        address _from,
        address _to,
        uint _nftId
    ) external;
}


contract DutchAuction {
    uint private constant DURATION = 7 days;

    IERC721 public immutable nft;
    uint public immutable nftId;

    mapping(address => bool) public tokenApproved;


    address payable public immutable seller;
    uint public immutable startingPrice;
    uint public immutable startAt;
    uint public immutable expiresAt;
    uint public immutable discountRate;

    constructor(
        uint _startingPrice,
        uint _discountRate,
        address _nft,
        uint _nftId
    ) {
        seller = payable(msg.sender);
        startingPrice = _startingPrice;
        startAt = block.timestamp;
        expiresAt = block.timestamp + DURATION;
        discountRate = _discountRate;

        // Approved token addresses to transact with (USDC, DAI, USDT)
        //tokenApproved[0x07865c6E87B9F70255377e024ace6630C1Eaa37F] = true; // GOERLI USDC
        //tokenApproved[0x11fE4B6AE13d2a6055C8D9cF65c55bac32B5d844] = true; // GOERLI DAI

        require(_startingPrice >= _discountRate * DURATION, "starting price < min");

        nft = IERC721(_nft);
        nftId = _nftId;
    }

    function getPrice() public view returns (uint) {
        uint timeElapsed = block.timestamp - startAt;
        uint discount = discountRate * timeElapsed;
        return startingPrice - discount;
    }

    // Placeholder... Use functionality in buy() function to force buyer to pay in tokens cited in tokenApproved mapping
    /*
    function receiveTokens(address token, uint amount) public {
        require(tokenApproved[token], "We don't accept those");
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        emit Received(msg.sender, token, amount);
    }
    */
    function buy() external payable {
        require(block.timestamp < expiresAt, "auction expired");

        uint price = getPrice();
        require(msg.value >= price, "ETH < price");

        nft.transferFrom(seller, msg.sender, nftId);
        uint refund = msg.value - price;
        if (refund > 0) {
            payable(msg.sender).transfer(refund);
        }
        selfdestruct(seller);
    }
}