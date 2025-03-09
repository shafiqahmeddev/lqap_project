import time
from crypto_components.xmss import XMSS
from entity_models.electric_vehicle import ElectricVehicle

def main():
    """Main entry point for the LQAP system"""
    print("Lightweight Quantum-Resistant Authentication Protocol (LQAP)")
    print("-----------------------------------------------------------")
    
    # Create a simple test environment
    xmss = XMSS()
    public_key, private_key = xmss.key_gen()
    print(f"Generated XMSS keys")
    
    # Create an EV
    ev = ElectricVehicle()
    print(f"Created Electric Vehicle with ID: {ev.id}")
    
    # Create an authentication request
    auth_request = ev.create_authentication_request()
    print(f"Created authentication request at: {auth_request['request']['timestamp']}")
    
    # Simulate simple operations
    print("\nSimulating EV operations:")
    print(f"Initial battery level: {ev.battery_level}%")
    
    print("Starting charging...")
    ev.start_charging()
    print(f"Charging status: {ev.charging_status}")
    
    print("Updating battery level...")
    ev.update_battery_level(85)
    print(f"New battery level: {ev.battery_level}%")
    
    print("Stopping charging...")
    ev.stop_charging()
    print(f"Final charging status: {ev.charging_status}")
    
    print("\nLQAP system test completed successfully")

if __name__ == "__main__":
    main()