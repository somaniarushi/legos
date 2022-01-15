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

## API Endpoints
- Create new transaction: `/transactions/new`
- Mine a new block: `/mine`
- Return the full blockchain: `/chain`

## Consensus
With only the above parts in place, the blockchain is _not decentralized_. How do we ensure that all instances of the blockchain reflect the same chain? This requires the Consensus Algorithm.

Each node on our network must keep a registry of all other nodes on the network. Two endpoints are added for this:
- Accept a list of new nodes as URLS: `/nodes/register`
- Resolve any conflict and ensure that every node has correct chain: `/nodes/resolve`

The consensus algorithm works on a simple heuristic:
> The longest chain in the network is the de-facto one.

## Hash Quality
Typically, hash functions are considered **cryptographic** if they satisfy the following properties:
- Deterministic: The same input always yields the same
hash.
- Intractability: It’s infeasible to find the input for a
given hash except by exhaustion (trying a gargantuan
amount of possible inputs).
- Collision-safety: It’s infeasible to find two different
inputs which output the same hash.
- Avalanche effect: The smallest change in input should
yield a hash so different that the new hash appears
uncorrelated with the old hash.
- Speed: It’s computationally fast to generate a hash.
These hash functions are notoriously difficult to reverse.
