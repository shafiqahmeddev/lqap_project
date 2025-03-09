import time
from entity_models.base_entity import BaseEntity

class EdgeNode(BaseEntity):
    """Edge Node (EN) entity"""
    def __init__(self, en_id=None):
        """Initialize an Edge Node entity"""
        super().__init__(en_id, "EN")
        
        # EN-specific attributes
        self.connected_charging_stations = []
        self.fl_model = None  # Will hold a federated learning model
        self.connection_logs = {}  # For anomaly detection
        
    def register_charging_station(self, cs_id):
        """Register a charging station with this edge node"""
        if cs_id not in self.connected_charging_stations:
            self.connected_charging_stations.append(cs_id)
            return True
        return False
    
    def issue_verifiable_credential(self, ev_id, validity_hours=24):
        """Issue a short-lived verifiable credential for an EV"""
        # Create a simple credential
        expiry = time.time() + (validity_hours * 3600)
        
        credential = {
            'subject_id': ev_id,
            'issuer_id': self.id,
            'issued_at': time.time(),
            'expiry': expiry,
            'type': 'cross-domain-auth'
        }
        
        # Sign the credential (simple string representation for now)
        credential_bytes = str(credential).encode()
        signature = self.xmss.sign(credential_bytes, self.private_key)
        
        return {
            'credential': credential,
            'signature': signature
        }
    
    def log_connection(self, ev_id, cs_id, timestamp=None):
        """Log a connection for anomaly detection"""
        if timestamp is None:
            timestamp = time.time()
            
        if ev_id not in self.connection_logs:
            self.connection_logs[ev_id] = []
            
        self.connection_logs[ev_id].append({
            'cs_id': cs_id,
            'timestamp': timestamp,
            'type': 'authentication'
        })
        
        return len(self.connection_logs[ev_id])
    
    def evaluate_anomaly_score(self, ev_id):
        """Evaluate an anomaly score for an EV based on its connection patterns"""
        # For simplicity, return a random score between 0 and 1
        # In a real implementation, this would use the FL model
        import random
        return random.random()

# Simple test
if __name__ == "__main__":
    en = EdgeNode("test-en")
    print(f"EN created with ID: {en.id}")
    
    # Register a charging station
    result = en.register_charging_station("cs-1")
    print(f"Registered CS-1: {result}")
    
    # Issue a credential
    credential = en.issue_verifiable_credential("ev-1")
    print(f"Issued credential for EV-1 with expiry: {credential['credential']['expiry']}")
    
    # Log some connections
    en.log_connection("ev-1", "cs-1")
    en.log_connection("ev-1", "cs-2")
    print(f"Connection logs for EV-1: {len(en.connection_logs['ev-1'])}")
    
    # Get anomaly score
    score = en.evaluate_anomaly_score("ev-1")
    print(f"Anomaly score for EV-1: {score}")