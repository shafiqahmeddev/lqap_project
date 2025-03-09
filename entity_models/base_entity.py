import uuid
import time
from crypto_components.xmss import XMSS

class BaseEntity:
    """Base class for all V2G entities"""
    def __init__(self, entity_id, entity_type):
        """
        Initialize a base entity
        entity_id: Unique identifier for the entity
        entity_type: Type of entity (EV, CS, EN, ESP)
        """
        self.id = entity_id if entity_id else f"{entity_type}-{uuid.uuid4()}"
        self.entity_type = entity_type
        self.xmss = XMSS()
        self.public_key, self.private_key = self.xmss.key_gen()
        self.certificate = None
        self.created_at = time.time()
    
    def create_authentication_request(self, timestamp=None):
        """Create a basic authentication request"""
        if timestamp is None:
            timestamp = time.time()
            
        # Create request data
        request = {
            'id': self.id,
            'type': self.entity_type,
            'timestamp': timestamp,
            'certificate': self.certificate
        }
        
        # Convert to bytes for signing (simple string conversion for now)
        request_bytes = str(request).encode()
        
        # Sign the request
        signature = self.xmss.sign(request_bytes, self.private_key)
        
        return {
            'request': request,
            'signature': signature
        }

# Simple test
if __name__ == "__main__":
    entity = BaseEntity("test-entity", "TEST")
    request = entity.create_authentication_request()
    print(f"Entity created with ID: {entity.id}")
    print(f"Authentication request created with timestamp: {request['request']['timestamp']}")