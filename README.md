# Legos: Python Implementation of a Blockchain

## Requirements
- Python 3.6+
- `flask==0.12.2`
- `requests==2.18.4`

## Data Structures
Each blockchain has a list of block and a list of transactions made over that chain.

Each Block has an index, a timestamp (in Unix time), a list of transactions, a proof, and the hash of the previous Block.

Each transaction has the id of the sender and the recipient, as well as the amount sent over the chain.