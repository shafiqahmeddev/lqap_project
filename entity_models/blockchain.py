import time
import hashlib
import json

class ConsortiumBlockchain:
    """Simple implementation of a consortium blockchain"""
    def __init__(self):
        """Initialize the blockchain"""
        self.blocks = []
        self.current_block = {
            'index': 0,
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash': '0' * 64,
            'nonce': 0
        }
        self.pending_transactions = []
        self.transaction_limit = 10  # Transactions per block
    
    def add_transaction(self, transaction):
        """Add a transaction to the pending pool"""
        # Add timestamp if not present
        if 'timestamp' not in transaction:
            transaction['timestamp'] = time.time()
            
        # Add transaction to pending pool
        self.pending_transactions.append({
            'data': transaction,
            'timestamp': time.time()
        })
        
        # Mine a block if we have enough transactions
        if len(self.pending_transactions) >= self.transaction_limit:
            self.mine_block()
            
        return len(self.pending_transactions)
    
    def mine_block(self):
        """Mine a new block with pending transactions"""
        if not self.pending_transactions:
            return False
            
        # Add pending transactions to current block
        self.current_block['transactions'] = self.pending_transactions.copy()
        self.current_block['timestamp'] = time.time()
        
        # Calculate the hash of the block
        block_string = json.dumps(self.current_block, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_string).hexdigest()
        
        # Add the block to the chain
        self.blocks.append({
            **self.current_block,
            'hash': block_hash
        })
        
        # Create a new block
        self.current_block = {
            'index': len(self.blocks),
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash': block_hash,
            'nonce': 0
        }
        
        # Clear pending transactions
        self.pending_transactions = []
        
        return len(self.blocks)
    
    def get_transaction(self, transaction_id):
        """Get a transaction from the blockchain"""
        # Search in blocks
        for block in self.blocks:
            for tx in block['transactions']:
                if tx['data'].get('id') == transaction_id:
                    return tx
        
        # Search in pending transactions
        for tx in self.pending_transactions:
            if tx['data'].get('id') == transaction_id:
                return tx
                
        return None
    
    def get_block(self, block_index):
        """Get a block by index"""
        if 0 <= block_index < len(self.blocks):
            return self.blocks[block_index]
        return None
    
    def get_chain_length(self):
        """Get the length of the blockchain"""
        return len(self.blocks)
    
    def verify_chain(self):
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.blocks)):
            current = self.blocks[i]
            previous = self.blocks[i-1]
            
            # Check that previous hash matches
            if current['previous_hash'] != previous['hash']:
                return False
                
            # Verify the block hash
            current_copy = dict(current)
            del current_copy['hash']
            block_string = json.dumps(current_copy, sort_keys=True).encode()
            block_hash = hashlib.sha256(block_string).hexdigest()
            
            if block_hash != current['hash']:
                return False
                
        return True

# Simple test
if __name__ == "__main__":
    blockchain = ConsortiumBlockchain()
    
    # Add some transactions
    for i in range(15):
        transaction = {
            'id': f"tx-{i}",
            'type': 'test',
            'data': f"Transaction data {i}"
        }
        blockchain.add_transaction(transaction)
    
    # Should have mined at least one block
    print(f"Blockchain length: {blockchain.get_chain_length()}")
    print(f"Pending transactions: {len(blockchain.pending_transactions)}")
    
    # Mine remaining transactions
    blockchain.mine_block()
    print(f"After mining, blockchain length: {blockchain.get_chain_length()}")
    print(f"After mining, pending transactions: {len(blockchain.pending_transactions)}")
    
    # Verify the chain
    is_valid = blockchain.verify_chain()
    print(f"Blockchain is valid: {is_valid}")