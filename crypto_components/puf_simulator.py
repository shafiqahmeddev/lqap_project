import hashlib
import numpy as np

class PUFSimulator:
    """
    Simulates a Physical Unclonable Function (PUF) for hardware-based authentication
    """
    def __init__(self, challenge_length=128, response_length=128, noise_factor=0.05):
        """
        Initialize the PUF simulator
        challenge_length: Length of challenge in bits
        response_length: Length of response in bits
        noise_factor: Simulates noise in physical PUF responses
        """
        self.challenge_length = challenge_length
        self.response_length = response_length
        self.noise_factor = noise_factor
        
        # Secret mapping (unique to each device)
        # In a real PUF, this would be determined by physical characteristics
        self.secret = np.random.randint(0, 256, size=1024).astype(np.uint8)
    
    def challenge(self, challenge_input):
        """Generate a PUF response for a given challenge"""
        # Convert challenge to bytes if it's a string
        if isinstance(challenge_input, str):
            challenge_input = challenge_input.encode()
            
        # Hash the challenge to create a stable index
        challenge_hash = hashlib.sha256(challenge_input).digest()
        
        # Use the hash to select elements from the secret
        indices = np.frombuffer(challenge_hash, dtype=np.uint8).astype(np.int32)
        indices = indices % len(self.secret)
        
        # Generate a base response
        base_response = self.secret[indices]
        
        # Apply a hash function to get the final response
        response_hash = hashlib.sha256(bytes(base_response)).digest()
        
        # Convert to a bit array of the desired length
        bits = np.unpackbits(np.frombuffer(response_hash, dtype=np.uint8))
        response_bits = bits[:self.response_length]
        
        # Add simulated noise (flip bits with probability noise_factor)
        if self.noise_factor > 0:
            noise = np.random.random(len(response_bits)) < self.noise_factor
            response_bits = np.logical_xor(response_bits, noise).astype(np.uint8)
        
        # Convert back to bytes
        response_bytes = np.packbits(response_bits)
        
        return bytes(response_bytes)
    
    def verify(self, challenge, response, tolerance=0.9):
        """
        Verify a response against a challenge
        tolerance: Fraction of bits that must match (allows for noise)
        """
        # Generate the expected response
        expected_response = self.challenge(challenge)
        
        # Convert both to bit arrays
        expected_bits = np.unpackbits(np.frombuffer(expected_response, dtype=np.uint8))
        response_bits = np.unpackbits(np.frombuffer(response, dtype=np.uint8))
        
        # Limit to the response length
        expected_bits = expected_bits[:self.response_length]
        response_bits = response_bits[:self.response_length]
        
        # Calculate match ratio (fraction of matching bits)
        match_ratio = np.mean(expected_bits == response_bits)
        
        return match_ratio >= tolerance

# Simple test
if __name__ == "__main__":
    puf = PUFSimulator()
    
    # Generate response for a challenge
    challenge = "test_challenge"
    response = puf.challenge(challenge)
    print(f"Challenge: {challenge}")
    print(f"Response: {response.hex()}")
    
    # Verify the response
    verification = puf.verify(challenge, response)
    print(f"Verification result: {verification}")
    
    # Generate response for the same challenge again
    response2 = puf.challenge(challenge)
    print(f"Second response: {response2.hex()}")
    
    # Verify second response
    verification2 = puf.verify(challenge, response2)
    print(f"Second verification result: {verification2}")
    
    # Try with a different challenge
    challenge2 = "different_challenge"
    response3 = puf.challenge(challenge2)
    verification3 = puf.verify(challenge, response3)
    print(f"Different challenge verification: {verification3}")