"""
Comprehensive LQAP System Test Script
This script tests the interaction between all major components
"""
import os
import sys
import time
import random
import numpy as np
from datetime import datetime

# Import LQAP components
from lqap_protocol.protocol import LQAPProtocol
from federated_learning.hierarchical_fl import HierarchicalFederatedLearning

def run_system_test():
    """Run a comprehensive system test"""
    print("Starting LQAP System Test...")
    
    # Initialize protocol
    protocol = LQAPProtocol()
    protocol.start()
    
    try:
        print("\n1. Entity Creation and Registration")
        print("------------------------------------")
        # Register entities
        ev_ids = []
        cs_ids = []
        for i in range(3):
            ev_id = protocol.register_entity("EV", f"test-ev-{i+1}")
            ev_ids.append(ev_id)
            print(f"Registered EV: {ev_id}")
        
        for i in range(2):
            cs_id = protocol.register_entity("CS", f"test-cs-{i+1}")
            cs_ids.append(cs_id)
            print(f"Registered CS: {cs_id}")
        
        en_id = protocol.register_entity("EN", "test-en-1")
        print(f"Registered EN: {en_id}")
        
        esp_id = protocol.register_entity("ESP", "test-esp-1")
        print(f"Registered ESP: {esp_id}")
        
        # Check entity status
        print("\nEntity Status:")
        for ev_id in ev_ids:
            status, _ = protocol.get_entity_status("EV", ev_id)
            print(f"  {ev_id}: {status.get('charging_status', 'Unknown')}")
        
        print("\n2. Credential Issuance")
        print("----------------------")
        # Issue credentials
        for ev_id in ev_ids:
            credential, message = protocol.issue_verifiable_credential(ev_id, en_id)
            print(f"Credential issued to {ev_id}: {message}")
        
        print("\n3. Intra-Domain Authentication")
        print("------------------------------")
        # Perform intra-domain authentication
        session_ids = []
        for i, ev_id in enumerate(ev_ids[:2]):  # Only authenticate 2 EVs
            cs_id = cs_ids[i % len(cs_ids)]
            success, result = protocol.intra_domain_authentication(ev_id, cs_id)
            if success:
                session_id = result['session_id']
                session_ids.append(session_id)
                print(f"Authentication successful: {ev_id} -> {cs_id}, Session: {session_id}")
            else:
                print(f"Authentication failed: {ev_id} -> {cs_id}, Reason: {result}")
        
        # Check blockchain status
        blocks = len(protocol.blockchain.blocks)
        pending = len(protocol.blockchain.pending_transactions)
        print(f"\nBlockchain status: {blocks} blocks, {pending} pending transactions")
        
        print("\n4. Cross-Domain Authentication")
        print("------------------------------")
        # Perform cross-domain authentication
        ev_id = ev_ids[2]  # Use the remaining EV
        cs_id = cs_ids[0]
        success, result = protocol.cross_domain_authentication(ev_id, cs_id, en_id)
        if success:
            session_id = result['session_id']
            session_ids.append(session_id)
            print(f"Cross-domain authentication successful: {ev_id} -> {cs_id}, Session: {session_id}")
        else:
            print(f"Cross-domain authentication failed: {ev_id} -> {cs_id}, Reason: {result}")
        
        print("\n5. Federated Learning Model Update")
        print("----------------------------------")
        # Generate some log data for FL model training
        log_data = []
        for i in range(20):
            data_point = {
                'time_of_day': random.random(),
                'location': random.random(),
                'frequency': random.normalvariate(0.5, 0.1),
                'duration': random.normalvariate(0.3, 0.05),
                'power': random.normalvariate(0.4, 0.1)
            }
            log_data.append(data_point)
        
        # Add some anomalous data
        for i in range(5):
            data_point = {
                'time_of_day': random.random(),
                'location': random.random(),
                'frequency': random.normalvariate(0.9, 0.1),  # Anomalous frequency
                'duration': random.normalvariate(0.8, 0.05),  # Anomalous duration
                'power': random.normalvariate(0.9, 0.1)       # Anomalous power
            }
            log_data.append(data_point)
        
        # Update FL model
        success, message = protocol.update_fl_model(log_data, en_id)
        print(f"FL model update: {message}")
        
        # Wait for model to be trained
        print("Waiting for model training...")
        time.sleep(2)
        
        # Check EN status
        status, _ = protocol.get_entity_status("EN", en_id)
        print(f"EN status: {status}")
        
        print("\n6. End Authentication Sessions")
        print("------------------------------")
        # End sessions
        for session_id in session_ids:
            success, message = protocol.end_session(session_id)
            print(f"Session {session_id} ended: {message}")
        
        # Print final system status
        print("\n7. Final System Status")
        print("----------------------")
        status = protocol.get_system_status()
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        print("\nLQAP System Test Completed Successfully!")
    
    finally:
        # Stop the protocol
        protocol.stop()
        print("Protocol stopped")

if __name__ == "__main__":
    run_system_test()