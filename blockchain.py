import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests


class Blockchain(object):
    '''
    Represents a block chain in our system.
    '''
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set() # makes addition of new nodes idempotent, prevents duplication
        self.__genesis()

    def __genesis(self):
        '''
        Starts the chain with a block.
        '''
        self.add_block(previous_hash=1, proof=100)

    def register_node(self, address):
        '''
        Adds a new node to the blockchain.
        '''
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def add_block(self, proof, previous_hash=None):
        '''
        Creates a new block and adds it to the chain. Returns the new block.
        Uses the proof value given by the proof of work algorithm
        Optionally accepts the hash of the previous block. #TODO: why optional?
        '''
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # All current transactions have been added to the block, null out
        self.transactions = []

        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        '''
        Creates a new transaction and adds it to the list of
        transactions.
        Returns the index of the block that holds this transaction.
        This block is the next one to be mined.
        '''
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        '''
        Given last proof, return a number that when hashed with
        the previous block's solution has a hash with 4 leading 0s
        '''
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def valid_chain(self, chain, print_chain=True):
        '''
        Determine if given blockchain is valid, return True or False.
        '''
        prev_block = chain[0]
        idx = 1

        while idx < len(chain):
            block = chain[idx]

            if print_chain:
                print(f'{prev_block}')
                print(f'{block}')
                print("\n-----------\n")

            # check if hash is correct
            if block['previous_hash'] != self.hash(prev_block):
                return False

            # proof of work is correct
            if not self.valid_proof(prev_block['proof'], block['proof']):
                return False

            prev_block = block
            idx += 1
        return True

    def resolve_conflicts(self):
        '''
        Implements consensus algorithm, resolving conflicts
        by replacing self's chain with longest chain in netork.
        Returns true if chain was replaced, False otherwise.
        '''
        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbors:
            response = requests.get(f'https://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(self):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        else:
            return False


    @staticmethod
    def valid_proof(last_proof, proof):
        '''
        Validates a new proof based on given proof of work algorithm
        and returns True or False respectively.
        '''
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    @staticmethod
    def hash(block):
        '''
        Accepts a block on the chain and returns its hascodes.
        Hash algo: SHA256
        '''
        # Order the dictionary, then convert to JSON string
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        '''
        Returns the current last block on the chain
        '''
        return self.chain[-1]

