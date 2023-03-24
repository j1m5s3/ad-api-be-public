// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract NFTADSpace is ERC721, ERC721URIStorage, Ownable {

    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    constructor() ERC721("NFT AD Space", "NFTAS") {}

    address nftContractAddress;
    uint256 referencedNftTokenId;

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function _baseURI() internal pure override returns (string memory) {
        return "http://";
    }

    function safeMint(address to, string memory uri) public onlyOwner {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
    // Owner sets nft info to be referemced by web server
    function setNftAdInfo(address _nftContractAddress, uint256 _referencedNftTokenId) external onlyOwner{
        nftContractAddress = _nftContractAddress;
        referencedNftTokenId = _referencedNftTokenId;
    }

    // Function to get the info needed by web server
    function getNftAdInfo() external view returns (address, uint256){
        return (nftContractAddress, referencedNftTokenId);
    }

}
