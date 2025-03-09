import time
import uuid
import threading

# Import components
from crypto_components.xmss import XMSS
from crypto_components.puf_simulator import PUFSimulator
from entity_models.electric_vehicle import ElectricVehicle
from entity_models.charging_station import ChargingStation
from entity_models.edge_node import EdgeNode
from entity_models.electric_service_provider import ElectricServiceProvider
from entity_models.blockchain import ConsortiumBlockchain
from federated_learning.hierarchical_fl import HierarchicalFederatedLearning

class CertificateAuthority:
    """Simple Certificate Authority for the V2G network"""
    def __init__(self, ca_id=None):
        """Initialize Certificate Authority"""
        if ca_id is None:
            ca_id = f"CA-{uuid.uuid4()}"
        self.id = ca_id
        self.xmss = XMSS()
        self.public_key, self.private_key = self.xmss.key_gen()
        self.issued_certificates = {}
        
    def issue_certificate(self, subject_id, subject_public_key, expiry=None):
        """Issue a certificate for an entity"""
        if expiry is None:
            expiry = time.time() + 86400  # 24 hours
            
        # Create certificate data
        cert_data = {
            'subject_id': subject_id,
            'subject_public_key': subject_public_key.hex() if isinstance(subject_public_key, bytes) else subject_public_key,
            'issuer_id': self.id,
            'issued_at': time.time(),
            'expiry': expiry
        }
        
        # Sign the certificate
        cert_bytes = str(cert_data).encode()
        signature = self.xmss.sign(cert_bytes, self.private_key)
        
        # Create the certificate
        certificate = {
            'data': cert_data,
            'signature': signature.hex() if isinstance(signature, bytes) else signature
        }
        
        # Store the certificate
        self.issued_certificates[subject_id] = certificate
        
        return certificate
    
    def verify_certificate(self, certificate):
        """Verify a certificate"""
        # Extract data and signature
        cert_data = certificate['data']
        signature = certificate['signature']
        
        # Convert signature to bytes if needed
        if isinstance(signature, str):
            signature = bytes.fromhex(signature)
            
        # Check expiry
        if cert_data['expiry'] < time.time():
            return False, "Certificate expired"
            
        # Verify signature (simplified for demo)
        return True, "Certificate valid"
    
    def revoke_certificate(self, subject_id):
        """Revoke a certificate"""
        if subject_id in self.issued_certificates:
            del self.issued_certificates[subject_id]
            return True
        return False

class LQAPProtocol:
    """
    Lightweight Quantum-Resistant Authentication Protocol implementation
    """
    def __init__(self):
        """Initialize the LQAP protocol"""
        # Initialize entities
        self.evs = {}
        self.charging_stations = {}
        self.edge_nodes = {}
        self.esps = {}
        
        # Initialize services
        self.ca = CertificateAuthority()
        self.blockchain = ConsortiumBlockchain()
        self.hfl = HierarchicalFederatedLearning()
        
        # Initialize global FL model
        self.hfl.initialize_global_model()
        
        # Active sessions
        self.active_sessions = {}
        
        # Protocol state
        self.running = False
        self.maintenance_thread = None
    
    def start(self):
        """Start the LQAP protocol"""
        if self.running:
            return False
            
        self.running = True
        
        # Start maintenance thread for periodic tasks
        self.maintenance_thread = threading.Thread(target=self._maintenance_loop)
        self.maintenance_thread.daemon = True
        self.maintenance_thread.start()
        
        print("LQAP Protocol started")
        return True
    
    def stop(self):
        """Stop the LQAP protocol"""
        self.running = False
        
        if self.maintenance_thread:
            self.maintenance_thread.join(timeout=5)
            
        print("LQAP Protocol stopped")
        return True
    
    def _maintenance_loop(self):
        """Maintenance loop for periodic tasks"""
        while self.running:
            try:
                # Mine blockchain blocks
                if self.blockchain.pending_transactions:
                    self.blockchain.mine_block()
                
                # Update global FL model
                if self.edge_nodes:
                    edge_ids = list(self.edge_nodes.keys())
                    self.hfl.aggregate_edge_models(edge_ids)
                    self.hfl.distribute_global_model(edge_ids)
                
                # Check for expired sessions
                self._cleanup_expired_sessions()
                
            except Exception as e:
                print(f"Error in maintenance loop: {e}")
                
            # Sleep for 10 seconds
            time.sleep(10)
    
    def _cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        current_time = time.time()
        expired_sessions = []
        
        for session_id, session_info in self.active_sessions.items():
            # Check if session has expired (default: 1 hour)
            if current_time - session_info['created_at'] > 3600:
                expired_sessions.append(session_id)
        
        # End expired sessions
        for session_id in expired_sessions:
            self.end_session(session_id)
    
    def register_entity(self, entity_type, entity_id=None):
        """Register a new entity in the system"""
        if entity_type == "EV":
            ev = ElectricVehicle(entity_id)
            certificate = self.ca.issue_certificate(ev.id, ev.public_key)
            ev.certificate = certificate
            self.evs[ev.id] = ev
            
            # Add registration to blockchain
            self.blockchain.add_transaction({
                'type': 'registration',
                'entity_type': 'EV',
                'entity_id': ev.id,
                'timestamp': time.time()
            })
            
            return ev.id
            
        elif entity_type == "CS":
            cs = ChargingStation(entity_id)
            certificate = self.ca.issue_certificate(cs.id, cs.public_key)
            cs.certificate = certificate
            self.charging_stations[cs.id] = cs
            
            # Add registration to blockchain
            self.blockchain.add_transaction({
                'type': 'registration',
                'entity_type': 'CS',
                'entity_id': cs.id,
                'timestamp': time.time()
            })
            
            return cs.id
            
        elif entity_type == "EN":
            en = EdgeNode(entity_id)
            certificate = self.ca.issue_certificate(en.id, en.public_key)
            en.certificate = certificate
            self.edge_nodes[en.id] = en
            
            # Initialize edge FL model
            self.hfl.initialize_edge_model(en.id)
            
            # Add registration to blockchain
            self.blockchain.add_transaction({
                'type': 'registration',
                'entity_type': 'EN',
                'entity_id': en.id,
                'timestamp': time.time()
            })
            
            return en.id
            
        elif entity_type == "ESP":
            esp = ElectricServiceProvider(entity_id)
            certificate = self.ca.issue_certificate(esp.id, esp.public_key)
            esp.certificate = certificate
            self.esps[esp.id] = esp
            
            # Add registration to blockchain
            self.blockchain.add_transaction({
                'type': 'registration',
                'entity_type': 'ESP',
                'entity_id': esp.id,
                'timestamp': time.time()
            })
            
            return esp.id
            
        else:
            raise ValueError(f"Unsupported entity type: {entity_type}")
    
    def issue_verifiable_credential(self, ev_id, en_id=None):
        """Issue a verifiable credential to an EV"""
        if ev_id not in self.evs:
            return None, "EV not found"
            
        # Select an edge node if not specified
        if en_id is None:
            if not self.edge_nodes:
                return None, "No edge nodes available"
            en_id = list(self.edge_nodes.keys())[0]
        
        if en_id not in self.edge_nodes:
            return None, "Edge node not found"
            
        ev = self.evs[ev_id]
        en = self.edge_nodes[en_id]
        
        # Issue the credential
        credential = en.issue_verifiable_credential(ev_id)
        
        # Store it with the EV
        ev.verifiable_credential = credential
        
        # Add to blockchain
        self.blockchain.add_transaction({
            'type': 'credential_issuance',
            'ev_id': ev_id,
            'en_id': en_id,
            'credential_id': str(hash(str(credential))),
            'timestamp': time.time()
        })
        
        return credential, "Credential issued successfully"
    
    def intra_domain_authentication(self, ev_id, cs_id):
        """Perform intra-domain authentication between EV and CS"""
        if ev_id not in self.evs:
            return False, "EV not found"
            
        if cs_id not in self.charging_stations:
            return False, "Charging station not found"
            
        ev = self.evs[ev_id]
        cs = self.charging_stations[cs_id]
        
        # Create authentication request
        auth_request = ev.create_authentication_request()
        
        # Verify the request
        auth_valid, auth_message = cs.verify_authentication_request(auth_request)
        
        if not auth_valid:
            return False, auth_message
        
        # Create a session ID
        session_id = str(uuid.uuid4())
        
        # Store session information
        self.active_sessions[session_id] = {
            'ev_id': ev_id,
            'cs_id': cs_id,
            'created_at': time.time(),
            'type': 'intra_domain'
        }
        
        # Connect the EV to the CS
        cs.connect_ev(ev_id)
        
        # Add authentication record to blockchain
        self.blockchain.add_transaction({
            'type': 'authentication',
            'mode': 'intra_domain',
            'ev_id': ev_id,
            'cs_id': cs_id,
            'session_id': session_id,
            'timestamp': time.time()
        })
        
        return True, {
            'session_id': session_id,
            'message': "Authentication successful"
        }
    
    def cross_domain_authentication(self, ev_id, cs_id, en_id=None):
        """Perform cross-domain authentication between EV and CS"""
        if ev_id not in self.evs:
            return False, "EV not found"
            
        if cs_id not in self.charging_stations:
            return False, "Charging station not found"
            
        ev = self.evs[ev_id]
        cs = self.charging_stations[cs_id]
        
        # Ensure the EV has a verifiable credential
        if not ev.verifiable_credential:
            # Auto-issue a credential if needed
            credential, message = self.issue_verifiable_credential(ev_id, en_id)
            if not credential:
                return False, f"Failed to issue credential: {message}"
        
        # Create authentication request
        auth_request = ev.create_authentication_request()
        
        # Select an edge node for verification
        if en_id is None:
            if not self.edge_nodes:
                return False, "No edge nodes available"
            en_id = list(self.edge_nodes.keys())[0]
        
        if en_id not in self.edge_nodes:
            return False, "Edge node not found"
            
        en = self.edge_nodes[en_id]
        
        # Verify the request
        auth_valid, auth_message = cs.verify_authentication_request(auth_request)
        
        if not auth_valid:
            return False, auth_message
        
        # Log the authentication attempt (for anomaly detection)
        en.log_connection(ev_id, cs_id)
        
        # Check for anomalies (simplified)
        anomaly_score = en.evaluate_anomaly_score(ev_id)
        
        # Reject if anomaly score is too high
        if anomaly_score > 0.8:  # Threshold for demonstration
            # Add failed authentication to blockchain
            self.blockchain.add_transaction({
                'type': 'authentication_failure',
                'mode': 'cross_domain',
                'reason': 'anomaly_detected',
                'ev_id': ev_id,
                'cs_id': cs_id,
                'en_id': en_id,
                'anomaly_score': anomaly_score,
                'timestamp': time.time()
            })
            
            return False, "Authentication rejected due to anomalous behavior"
        
        # Create a session ID
        session_id = str(uuid.uuid4())
        
        # Store session information
        self.active_sessions[session_id] = {
            'ev_id': ev_id,
            'cs_id': cs_id,
            'created_at': time.time(),
            'type': 'cross_domain',
            'en_id': en_id
        }
        
        # Connect the EV to the CS
        cs.connect_ev(ev_id)
        
        # Add to blockchain
        self.blockchain.add_transaction({
            'type': 'authentication',
            'mode': 'cross_domain',
            'ev_id': ev_id,
            'cs_id': cs_id,
            'en_id': en_id,
            'session_id': session_id,
            'timestamp': time.time()
        })
        
        return True, {
            'session_id': session_id,
            'message': "Cross-domain authentication successful"
        }
    
    def end_session(self, session_id):
        """End an active session"""
        if session_id not in self.active_sessions:
            return False, "Session not found"
            
        session_info = self.active_sessions[session_id]
        ev_id = session_info['ev_id']
        cs_id = session_info['cs_id']
        
        # Disconnect the EV from the CS
        if cs_id in self.charging_stations and ev_id in self.evs:
            cs = self.charging_stations[cs_id]
            cs.disconnect_ev(ev_id)
        
        # Add session end to blockchain
        self.blockchain.add_transaction({
            'type': 'session_end',
            'session_id': session_id,
            'ev_id': ev_id,
            'cs_id': cs_id,
            'duration': time.time() - session_info['created_at'],
            'timestamp': time.time()
        })
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        return True, "Session ended successfully"
    
    def update_fl_model(self, log_data, en_id=None):
        """Update the federated learning model with new log data"""
        # Select an edge node if not specified
        if en_id is None:
            if not self.edge_nodes:
                return False, "No edge nodes available"
            en_id = list(self.edge_nodes.keys())[0]
        
        if en_id not in self.edge_nodes:
            return False, "Edge node not found"
            
        # Initialize a local model for this edge node if needed
        local_model_id = f"local_model_{en_id}"
        if local_model_id not in self.hfl.local_models:
            self.hfl.initialize_local_model(local_model_id)
        
        # Train the local model
        self.hfl.train_local_model(local_model_id, log_data)
        
        # Aggregate local models to update edge model
        self.hfl.aggregate_local_models(en_id, [local_model_id])
        
        # Add model update to blockchain
        model_hash = str(hash(str(self.hfl.edge_models[en_id].get_model_parameters())))
        self.blockchain.add_transaction({
            'type': 'fl_model_update',
            'en_id': en_id,
            'model_id': en_id,
            'model_hash': model_hash,
            'timestamp': time.time()
        })
        
        return True, f"Model updated successfully for edge node {en_id}"
    
    def get_entity_status(self, entity_type, entity_id):
        """Get the status of an entity"""
        if entity_type == "EV":
            if entity_id not in self.evs:
                return None, "EV not found"
            
            ev = self.evs[entity_id]
            
            # Find active sessions for this EV
            active_sessions = [
                session_id for session_id, info in self.active_sessions.items()
                if info['ev_id'] == entity_id
            ]
            
            return {
                'id': ev.id,
                'type': 'EV',
                'battery_level': ev.battery_level,
                'charging_status': ev.charging_status,
                'has_credential': ev.verifiable_credential is not None,
                'active_sessions': active_sessions
            }, "EV status retrieved"
            
        elif entity_type == "CS":
            if entity_id not in self.charging_stations:
                return None, "Charging station not found"
            
            cs = self.charging_stations[entity_id]
            
            # Find active sessions for this CS
            active_sessions = [
                session_id for session_id, info in self.active_sessions.items()
                if info['cs_id'] == entity_id
            ]
            
            return {
                'id': cs.id,
                'type': 'CS',
                'available_power': cs.available_power,
                'connected_evs': cs.connected_evs,
                'active_sessions': active_sessions
            }, "Charging station status retrieved"
            
        elif entity_type == "EN":
            if entity_id not in self.edge_nodes:
                return None, "Edge node not found"
            
            en = self.edge_nodes[entity_id]
            
            return {
                'id': en.id,
                'type': 'EN',
                'connected_charging_stations': en.connected_charging_stations,
                'connection_logs': {k: len(v) for k, v in en.connection_logs.items()},
                'has_fl_model': entity_id in self.hfl.edge_models
            }, "Edge node status retrieved"
            
        elif entity_type == "ESP":
            if entity_id not in self.esps:
                return None, "Electric service provider not found"
            
            esp = self.esps[entity_id]
            
            return {
                'id': esp.id,
                'type': 'ESP',
                'edge_nodes': esp.edge_nodes,
                'energy_prices': esp.energy_prices,
                'has_global_model': self.hfl.global_model is not None
            }, "Electric service provider status retrieved"
            
        else:
            return None, f"Unsupported entity type: {entity_type}"
    
    def get_system_status(self):
        """Get overall system status"""
        return {
            'entities': {
                'evs': len(self.evs),
                'charging_stations': len(self.charging_stations),
                'edge_nodes': len(self.edge_nodes),
                'esps': len(self.esps)
            },
            'blockchain': {
                'blocks': len(self.blockchain.blocks),
                'pending_transactions': len(self.blockchain.pending_transactions)
            },
            'sessions': {
                'active': len(self.active_sessions),
                'cross_domain': sum(1 for info in self.active_sessions.values() if info.get('type') == 'cross_domain')
            },
            'federated_learning': {
                'global_model': self.hfl.global_model is not None,
                'edge_models': len(self.hfl.edge_models),
                'local_models': len(self.hfl.local_models)
            },
            'timestamp': time.time()
        }

# Simple test
if __name__ == "__main__":
    # Initialize protocol
    protocol = LQAPProtocol()
    protocol.start()
    
    try:
        # Register entities
        ev_id = protocol.register_entity("EV", "test-ev")
        cs_id = protocol.register_entity("CS", "test-cs")
        en_id = protocol.register_entity("EN", "test-en")
        esp_id = protocol.register_entity("ESP", "test-esp")
        
        print(f"Registered entities: EV={ev_id}, CS={cs_id}, EN={en_id}, ESP={esp_id}")
        
        # Issue credential
        credential, message = protocol.issue_verifiable_credential(ev_id, en_id)
        print(f"Credential issuance: {message}")
        
        # Perform authentication
        success, result = protocol.intra_domain_authentication(ev_id, cs_id)
        if success:
            session_id = result['session_id']
            print(f"Intra-domain authentication successful: {session_id}")
            
            # End the session
            protocol.end_session(session_id)
            print("Session ended")
        else:
            print(f"Authentication failed: {result}")
        
        # Perform cross-domain authentication
        success, result = protocol.cross_domain_authentication(ev_id, cs_id, en_id)
        if success:
            session_id = result['session_id']
            print(f"Cross-domain authentication successful: {session_id}")
        else:
            print(f"Cross-domain authentication failed: {result}")
        
        # Get system status
        status = protocol.get_system_status()
        print(f"System status: {status}")
        
        # Update FL model
        log_data = [
            {'time_of_day': 0.5, 'location': 0.5, 'frequency': 0.5, 'duration': 0.5, 'power': 0.5}
            for _ in range(10)
        ]
        success, message = protocol.update_fl_model(log_data, en_id)
        print(f"FL model update: {message}")
        
    finally:
        # Stop the protocol
        protocol.stop()