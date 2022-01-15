class Blockchain(object):
    '''
    Represents a block chain in our system.
    '''
    def __init__(self):
        self.chain = []
        self.transactions = []

    def add_block(self):
        '''
        Creates a new block and adds it to the chain
        '''
        pass

    def add_transaction(self):
        '''
        Creates a new transaction and adds it to the list of
        transactions.
        '''
        pass

    @staticmethod
    def hash(block):
        '''
        Accepts a block on the chain and
        returns its hascodes
        '''
        pass

    @property
    def last_block(self):
        '''
        Returns the current last block on the chain
        '''
        pass

