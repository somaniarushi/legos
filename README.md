# Legos: Implementing a Blockchain

Inspired by Daniel Van Flymen's excellent article on the inner workings of the blockchain.

## Requirements
- Python 3.6+
- `flask==0.12.2`
- `requests==2.18.4`

## Data Structures
Each blockchain has a list of block and a list of transactions made over that chain.

Each Block has an index, a timestamp (in Unix time), a list of transactions, a proof, and the hash of the previous Block.

Each transaction has the id of the sender and the recipient, as well as the amount sent over the chain.

## Proof of Work Implementation
We need to introduce some sort of _number_ that is the confirmation of a new block being created onto the blockchain. The number must be computationally **difficult to find and easy to verify**.

We'll be using a [HashCash](https://en.wikipedia.org/wiki/Hashcash?ref=hackernoon.com) implementation.

Our next proof depends on the previous proof. It is generated as follows:
> When a number p when hashed with the previous block's solution has a hash with 4 leading 0s, this is our next proof.