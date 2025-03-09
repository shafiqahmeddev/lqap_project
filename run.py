import time
import argparse
from lqap_protocol.protocol import LQAPProtocol

def main():
    """Main entry point for the LQAP system"""
    parser = argparse.ArgumentParser(description='LQAP System')
    parser.add_argument('--mode', default='development', choices=['development', 'production', 'simulation'],
                        help='Execution mode')
    args = parser.parse_args()
    
    print("Lightweight Quantum-Resistant Authentication Protocol (LQAP)")
    print("-----------------------------------------------------------")
    print(f"Running in {args.mode} mode")
    
    # Initialize LQAP protocol
    protocol = LQAPProtocol()
    
    try:
        # Start the protocol
        protocol.start()
        
        # Register some test entities
        ev_id = protocol.register_entity("EV", "test-ev-1")
        cs_id = protocol.register_entity("CS", "test-cs-1")
        en_id = protocol.register_entity("EN", "test-en-1")
        esp_id = protocol.register_entity("ESP", "test-esp-1")
        
        print(f"Registered entities: EV={ev_id}, CS={cs_id}, EN={en_id}, ESP={esp_id}")
        
        # Issue a credential to the EV
        credential, message = protocol.issue_verifiable_credential(ev_id, en_id)
        print(f"Credential issuance: {message}")
        
        # Perform intra-domain authentication
        print("\nPerforming intra-domain authentication...")
        success, result = protocol.intra_domain_authentication(ev_id, cs_id)
        
        if success:
            session_id = result['session_id']
            print(f"Authentication successful: {session_id}")
            
            # End the session after a short delay
            time.sleep(2)
            protocol.end_session(session_id)
            print("Session ended")
        else:
            print(f"Authentication failed: {result}")
        
        # Perform cross-domain authentication
        print("\nPerforming cross-domain authentication...")
        success, result = protocol.cross_domain_authentication(ev_id, cs_id, en_id)
        
        if success:
            session_id = result['session_id']
            print(f"Cross-domain authentication successful: {session_id}")
        else:
            print(f"Cross-domain authentication failed: {result}")
        
        # Update the FL model with some sample data
        print("\nUpdating federated learning model...")
        log_data = [
            {'time_of_day': 0.5, 'location': 0.5, 'frequency': 0.5, 'duration': 0.5, 'power': 0.5}
            for _ in range(10)
        ]
        success, message = protocol.update_fl_model(log_data, en_id)
        print(f"FL model update: {message}")
        
        # Get system status
        print("\nSystem status:")
        status = protocol.get_system_status()
        for category, data in status.items():
            print(f"  {category}: {data}")
        
        # Keep running for a while to allow blockchain mining
        print("\nRunning for 30 seconds...")
        time.sleep(30)
        
        # Final system status
        print("\nFinal system status:")
        status = protocol.get_system_status()
        for category, data in status.items():
            print(f"  {category}: {data}")
        
        print("\nLQAP system test completed successfully")
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        # Stop the protocol
        protocol.stop()

if __name__ == "__main__":
    main()