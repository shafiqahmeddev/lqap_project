from entity_models.base_entity import BaseEntity

class ElectricServiceProvider(BaseEntity):
    """Electric Service Provider (ESP) entity"""
    def __init__(self, esp_id=None):
        """Initialize an Electric Service Provider entity"""
        super().__init__(esp_id, "ESP")
        
        # ESP-specific attributes
        self.edge_nodes = []
        self.energy_prices = {'buy': 0.15, 'sell': 0.10}  # $ per kWh
        self.global_fl_model = None  # Will hold the global federated learning model
        
    def register_edge_node(self, en_id):
        """Register an edge node with this ESP"""
        if en_id not in self.edge_nodes:
            self.edge_nodes.append(en_id)
            return True
        return False
    
    def update_energy_prices(self, buy_price, sell_price):
        """Update energy prices"""
        if buy_price > 0 and sell_price > 0:
            self.energy_prices = {'buy': buy_price, 'sell': sell_price}
            return True
        return False
    
    def update_global_fl_model(self, model_updates):
        """Update the global federated learning model"""
        # For simplicity, we'll just log the update
        # In a real implementation, this would aggregate model updates
        print(f"Received {len(model_updates)} model updates")
        
        # Set a simple placeholder model
        self.global_fl_model = "updated_model"
        
        return True, "Global model updated"
    
    def distribute_global_model(self):
        """Distribute the global model to edge nodes"""
        # In a real implementation, this would send the model to edge nodes
        return self.global_fl_model

# Simple test
if __name__ == "__main__":
    esp = ElectricServiceProvider("test-esp")
    print(f"ESP created with ID: {esp.id}")
    
    # Register edge nodes
    esp.register_edge_node("en-1")
    esp.register_edge_node("en-2")
    print(f"Registered edge nodes: {esp.edge_nodes}")
    
    # Update energy prices
    esp.update_energy_prices(0.18, 0.12)
    print(f"Updated energy prices: {esp.energy_prices}")
    
    # Update global model
    result, message = esp.update_global_fl_model(["model1", "model2"])
    print(f"Global model update: {message}")