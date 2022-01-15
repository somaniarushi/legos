import hashlib
import json
from time import time

class Blockchain(object):
    '''
    Represents a block chain in our system.
    '''
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.__genesis()

    def __genesis(self):
        '''
        Starts the chain with a block.
        '''
        self.add_block(previous_hash=1, proof=100)

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

