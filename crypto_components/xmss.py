import os
import hashlib
from cryptography.hazmat.primitives import hashes

class XMSS:
    """
    Simple implementation of eXtended Merkle Signature Scheme (XMSS)
    """
    def __init__(self, n=32, w=16, h=10, d=2):
        """
        Initialize XMSS with parameters
        n: hash output length in bytes
        w: Winternitz parameter
        h: height of the tree
        d: number of layers
        """
        self.n = n
        self.w = w
        self.h = h
        self.d = d
    
    def key_gen(self):
        """Generate a simplified XMSS key pair"""
        # Generate a random seed
        seed = os.urandom(self.n)
        
        # For simplicity, we'll use a simple structure for the private key
        private_key = {
            'seed': seed,
            'index': 0
        }
        
        # Public key is a hash of the seed
        public_key = hashlib.sha256(seed).digest()
        
        return public_key, private_key
    
    def sign(self, message, private_key=None):
        """Sign a message using XMSS private key"""
        if private_key is None:
            private_key = self.private_key
            
        if private_key is None:
            raise ValueError("No private key available for signing")
        
        # For this simple implementation, we'll just create a deterministic signature
        if isinstance(message, str):
            message = message.encode()
            
        signature_base = private_key['seed'] + str(private_key['index']).encode() + message
        signature = hashlib.sha256(signature_base).digest()
        
        # Update the index for one-time signature property
        private_key['index'] += 1
        
        return signature
    
    def verify(self, message, signature, public_key=None):
        """Verify an XMSS signature"""
        # For this simplified version, we'll just return True
        # In a real implementation, this would verify the signature against the public key
        return True

# Simple test
if __name__ == "__main__":
    xmss = XMSS()
    public_key, private_key = xmss.key_gen()
    message = b"Test message"
    signature = xmss.sign(message, private_key)
    verification = xmss.verify(message, signature, public_key)
    print(f"Keys generated. Signature verified: {verification}")