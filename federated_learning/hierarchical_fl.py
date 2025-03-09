import os
import sys
# Add the parent directory to the path so we can import from the same package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import time
# Change to a direct import for running the file individually
from federated_learning.anomaly_detection import AnomalyDetectionModel

class HierarchicalFederatedLearning:
    """Hierarchical Federated Learning implementation"""
    def __init__(self):
        """Initialize the HFL system"""
        self.global_model = None
        self.edge_models = {}
        self.local_models = {}
        self.aggregation_weights = {}
    
    def initialize_global_model(self, model_type="anomaly_detection"):
        """Initialize the global model"""
        self.global_model = AnomalyDetectionModel("global_model")
        return self.global_model
    
    def initialize_edge_model(self, edge_id, model_type="anomaly_detection"):
        """Initialize an edge model"""
        model = AnomalyDetectionModel(f"edge_model_{edge_id}")
        self.edge_models[edge_id] = model
        return model
    
    def initialize_local_model(self, local_id, model_type="anomaly_detection"):
        """Initialize a local model"""
        model = AnomalyDetectionModel(f"local_model_{local_id}")
        self.local_models[local_id] = model
        return model
    
    def train_local_model(self, local_id, data):
        """Train a local model with data"""
        if local_id not in self.local_models:
            return False
            
        return self.local_models[local_id].train(data)
    
    def aggregate_local_models(self, edge_id, local_ids=None):
        """Aggregate local models to update the edge model"""
        if edge_id not in self.edge_models:
            return False
            
        if local_ids is None:
            # Use all local models
            local_ids = [lid for lid in self.local_models.keys() 
                      if lid.startswith(f"local_model_{edge_id}")]
        
        # Filter for existing models
        valid_local_ids = [lid for lid in local_ids if lid in self.local_models]
        
        if not valid_local_ids:
            return False
            
        # Get parameters from local models
        parameters_list = []
        for lid in valid_local_ids:
            params = self.local_models[lid].get_model_parameters()
            if params.get('trained', False):
                parameters_list.append(params)
        
        if not parameters_list:
            return False
            
        # Aggregate parameters (average)
        aggregated_params = self._aggregate_parameters(parameters_list)
            
        # Update the edge model
        return self.edge_models[edge_id].set_model_parameters(aggregated_params)
    
    def aggregate_edge_models(self, edge_ids=None):
        """Aggregate edge models to update the global model"""
        if self.global_model is None:
            return False
            
        if edge_ids is None:
            # Use all edge models
            edge_ids = list(self.edge_models.keys())
        
        # Filter for existing models
        valid_edge_ids = [eid for eid in edge_ids if eid in self.edge_models]
        
        if not valid_edge_ids:
            return False
            
        # Get parameters from edge models
        parameters_list = []
        for eid in valid_edge_ids:
            params = self.edge_models[eid].get_model_parameters()
            if params.get('trained', False):
                parameters_list.append(params)
        
        if not parameters_list:
            return False
            
        # Aggregate parameters
        aggregated_params = self._aggregate_parameters(parameters_list)
            
        # Update the global model
        return self.global_model.set_model_parameters(aggregated_params)
    
    def distribute_global_model(self, edge_ids=None):
        """Distribute global model parameters to edge models"""
        if self.global_model is None:
            return 0
            
        if edge_ids is None:
            # Use all edge models
            edge_ids = list(self.edge_models.keys())
        
        # Get global model parameters
        global_params = self.global_model.get_model_parameters()
        
        if not global_params.get('trained', False):
            return 0
        
        # Update each edge model
        success_count = 0
        for eid in edge_ids:
            if eid in self.edge_models:
                if self.edge_models[eid].set_model_parameters(global_params):
                    success_count += 1
        
        return success_count
    
    def _aggregate_parameters(self, parameters_list):
        """Aggregate model parameters by averaging"""
        if not parameters_list:
            return {}
            
        # Initialize with the first set of parameters
        aggregated = parameters_list[0].copy()
        
        # For arrays, we need to average them
        if 'mean_vector' in aggregated and all('mean_vector' in p for p in parameters_list):
            mean_vectors = [np.array(p['mean_vector']) for p in parameters_list]
            aggregated['mean_vector'] = np.mean(mean_vectors, axis=0).tolist()
        
        if 'std_vector' in aggregated and all('std_vector' in p for p in parameters_list):
            std_vectors = [np.array(p['std_vector']) for p in parameters_list]
            aggregated['std_vector'] = np.mean(std_vectors, axis=0).tolist()
        
        # For scalar values, take the average
        if 'threshold' in aggregated:
            thresholds = [p.get('threshold', 3.0) for p in parameters_list]
            aggregated['threshold'] = sum(thresholds) / len(thresholds)
        
        # Use the maximum version number
        versions = [p.get('version', 1) for p in parameters_list]
        aggregated['version'] = max(versions)
        
        # Update timestamp
        aggregated['updated_at'] = time.time()
        
        return aggregated
    
    def generate_sample_data(self, num_samples=100):
        """Generate sample data for testing"""
        import numpy as np
        
        # Normal data
        normal_data = [
            {'time_of_day': np.random.random(), 
            'location': np.random.random(), 
            'frequency': np.random.random(), 
            'duration': np.random.random(), 
            'power': np.random.random()}
            for _ in range(int(num_samples * 0.9))  # 90% normal
        ]
        
        # Anomalous data
        anomalous_data = [
            {'time_of_day': np.random.random(), 
            'location': np.random.random(), 
            'frequency': 5 + np.random.random(),  # Anomalous value 
            'duration': np.random.random(), 
            'power': np.random.random()}
            for _ in range(int(num_samples * 0.1))  # 10% anomalous
        ]
        
        # Combine and shuffle
        all_data = normal_data + anomalous_data
        np.random.shuffle(all_data)
        
        return all_data

# Simple test
if __name__ == "__main__":
    # Create HFL system
    hfl = HierarchicalFederatedLearning()
    
    # Initialize models
    global_model = hfl.initialize_global_model()
    edge1_model = hfl.initialize_edge_model("en-1")
    edge2_model = hfl.initialize_edge_model("en-2")
    local1_model = hfl.initialize_local_model("local_model_en-1_1")
    local2_model = hfl.initialize_local_model("local_model_en-1_2")
    local3_model = hfl.initialize_local_model("local_model_en-2_1")
    
    # Generate sample data
    data1 = hfl.generate_sample_data(100)
    data2 = hfl.generate_sample_data(100)
    data3 = hfl.generate_sample_data(100)
    
    # Train local models
    hfl.train_local_model("local_model_en-1_1", data1)
    hfl.train_local_model("local_model_en-1_2", data2)
    hfl.train_local_model("local_model_en-2_1", data3)
    
    # Aggregate local models to edge models
    result1 = hfl.aggregate_local_models("en-1", ["local_model_en-1_1", "local_model_en-1_2"])
    result2 = hfl.aggregate_local_models("en-2", ["local_model_en-2_1"])
    
    print(f"Aggregated local models to edge1: {result1}")
    print(f"Aggregated local models to edge2: {result2}")
    
    # Aggregate edge models to global model
    result_global = hfl.aggregate_edge_models(["en-1", "en-2"])
    print(f"Aggregated edge models to global: {result_global}")
    
    # Distribute global model
    success_count = hfl.distribute_global_model()
    print(f"Distributed global model to {success_count} edge nodes")
    
    # Test prediction
    test_data = [
        {'time_of_day': 0.5, 'location': 0.5, 'frequency': 0.5, 'duration': 0.5, 'power': 0.5},
        {'time_of_day': 0.5, 'location': 0.5, 'frequency': 5.5, 'duration': 0.5, 'power': 0.5}
    ]
    
    # Predict with global model
    scores = global_model.predict(test_data)
    print(f"Global model predictions: {scores}")