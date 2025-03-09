from entity_models.base_entity import BaseEntity

class ElectricVehicle(BaseEntity):
    """Electric Vehicle (EV) entity"""
    def __init__(self, ev_id=None):
        """Initialize an Electric Vehicle entity"""
        super().__init__(ev_id, "EV")
        
        # EV-specific attributes
        self.battery_level = 100.0  # Percentage
        self.charging_status = "idle"  # idle, charging, discharging
        self.verifiable_credential = None
    
    def update_battery_level(self, new_level):
        """Update the battery level"""
        if 0 <= new_level <= 100:
            self.battery_level = new_level
            return True
        return False
    
    def start_charging(self):
        """Start charging the vehicle"""
        if self.charging_status == "idle":
            self.charging_status = "charging"
            return True
        return False
    
    def stop_charging(self):
        """Stop charging the vehicle"""
        if self.charging_status == "charging":
            self.charging_status = "idle"
            return True
        return False

# Simple test
if __name__ == "__main__":
    ev = ElectricVehicle("test-ev")
    print(f"EV created with ID: {ev.id}")
    print(f"Battery level: {ev.battery_level}%")
    ev.start_charging()
    print(f"Charging status: {ev.charging_status}")