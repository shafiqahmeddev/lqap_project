from entity_models.base_entity import BaseEntity

class ChargingStation(BaseEntity):
    """Charging Station (CS) entity"""
    def __init__(self, cs_id=None):
        """Initialize a Charging Station entity"""
        super().__init__(cs_id, "CS")
        
        # CS-specific attributes
        self.available_power = 50.0  # kW
        self.connected_evs = []
        self.active_charging_sessions = {}
    
    def connect_ev(self, ev_id):
        """Connect an EV to the charging station"""
        if ev_id not in self.connected_evs:
            self.connected_evs.append(ev_id)
            return True
        return False
    
    def disconnect_ev(self, ev_id):
        """Disconnect an EV from the charging station"""
        if ev_id in self.connected_evs:
            self.connected_evs.remove(ev_id)
            
            # End any active charging session
            if ev_id in self.active_charging_sessions:
                del self.active_charging_sessions[ev_id]
                
            return True
        return False
    
    def start_charging_session(self, ev_id, power_request=10.0):
        """Start a charging session for an EV"""
        if ev_id not in self.connected_evs:
            return False, "EV not connected"
        
        if ev_id in self.active_charging_sessions:
            return False, "EV already has an active charging session"
        
        if power_request > self.available_power:
            return False, "Insufficient power available"
        
        # Allocate power
        self.available_power -= power_request
        
        # Record the session
        self.active_charging_sessions[ev_id] = {
            'start_time': __import__('time').time(),
            'power_allocated': power_request
        }
        
        return True, "Charging session started"
    
    def verify_authentication_request(self, auth_request):
        """Verify an authentication request from an EV"""
        # For simplicity, we'll just return True
        # In a real implementation, this would verify the request signature
        return True, "Authentication successful"

# Simple test
if __name__ == "__main__":
    cs = ChargingStation("test-cs")
    print(f"CS created with ID: {cs.id}")
    print(f"Available power: {cs.available_power} kW")
    
    # Connect an EV
    result = cs.connect_ev("ev-1")
    print(f"Connected EV-1: {result}")
    
    # Start charging session
    success, message = cs.start_charging_session("ev-1", 15.0)
    print(f"Charging session result: {message}")
    print(f"Available power after session: {cs.available_power} kW")