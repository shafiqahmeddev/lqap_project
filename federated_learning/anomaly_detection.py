import os
import sys
# Add the parent directory to the path so we can import from the same package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import numpy as np
from federated_learning.base_model import FederatedLearningModel

class AnomalyDetectionModel(FederatedLearningModel):
    """Simple anomaly detection model using statistical methods"""
    def __init__(self, model_id):
        """Initialize the anomaly detection model"""
        super().__init__(model_id, "anomaly_detection")
        
        # Initialize model parameters
        self.mean_vector = None
        self.std_vector = None
        self.threshold = 3.0  # Number of standard deviations for anomaly
        self.feature_names = ['time_of_day', 'location', 'frequency', 'duration', 'power']
    
    def _extract_features(self, data):
        """Extract features from raw data"""
        if not data:
            return np.array([])
            
        features = []
        for record in data:
            # Extract features if available
            if isinstance(record, dict):
                feature_vector = [
                    record.get('time_of_day', 0),
                    record.get('location', 0),
                    record.get('frequency', 0),
                    record.get('duration', 0),
                    record.get('power', 0)
                ]
                features.append(feature_vector)
            else:
                # Use random features for testing
                features.append(np.random.random(5))
        
        return np.array(features)
    
    def train(self, data):
        """Train the model on local data"""
        features = self._extract_features(data)
        
        if features.size == 0:
            return False
        
        # Calculate mean and standard deviation for each feature
        self.mean_vector = np.mean(features, axis=0)
        self.std_vector = np.std(features, axis=0)
        
        # Handle zero standard deviations
        self.std_vector[self.std_vector == 0] = 1.0
        
        self.updated_at = __import__('time').time()
        self.version += 1
        
        return True
    
    def predict(self, data):
        """
        Predict anomaly scores
        Returns a score for each record, higher = more anomalous
        """
        if self.mean_vector is None or self.std_vector is None:
            return np.array([1.0] * len(data))  # Untrained model
        
        features = self._extract_features(data)
        
        if features.size == 0:
            return np.array([])
        
        # Calculate z-scores
        z_scores = np.abs((features - self.mean_vector) / self.std_vector)
        
        # Maximum z-score across features
        max_z_scores = np.max(z_scores, axis=1)
        
        # Normalize to 0-1 range
        anomaly_scores = max_z_scores / self.threshold
        anomaly_scores = np.clip(anomaly_scores, 0, 1)
        
        return anomaly_scores
    
    def get_model_parameters(self):
        """Get the model parameters"""
        if self.mean_vector is None or self.std_vector is None:
            return {
                'version': self.version,
                'updated_at': self.updated_at,
                'trained': False
            }
        
        return {
            'version': self.version,
            'updated_at': self.updated_at,
            'trained': True,
            'mean_vector': self.mean_vector.tolist(),
            'std_vector': self.std_vector.tolist(),
            'threshold': self.threshold
        }
    
    def set_model_parameters(self, parameters):
        """Update model with new parameters"""
        if not parameters.get('trained', False):
            return False
        
        if 'mean_vector' in parameters:
            self.mean_vector = np.array(parameters['mean_vector'])
        
        if 'std_vector' in parameters:
            self.std_vector = np.array(parameters['std_vector'])
        
        if 'threshold' in parameters:
            self.threshold = parameters['threshold']
        
        if 'version' in parameters:
            self.version = parameters['version']
        
        self.updated_at = __import__('time').time()
        
        return True

# Simple test
if __name__ == "__main__":
    # Create model
    model = AnomalyDetectionModel("test-model")
    
    # Generate some sample data
    np.random.seed(42)
    normal_data = [
        {'time_of_day': np.random.random(), 
         'location': np.random.random(), 
         'frequency': np.random.random(), 
         'duration': np.random.random(), 
         'power': np.random.random()}
        for _ in range(100)
    ]
    
    # Train the model
    model.train(normal_data)
    print(f"Model trained: Version {model.version}")
    
    # Generate test data - normal
    test_normal = [
        {'time_of_day': np.random.random(), 
         'location': np.random.random(), 
         'frequency': np.random.random(), 
         'duration': np.random.random(), 
         'power': np.random.random()}
        for _ in range(10)
    ]
    
    # Generate anomalous data - outliers
    test_anomalous = [
        {'time_of_day': np.random.random(), 
         'location': np.random.random(), 
         'frequency': 5 + np.random.random(),  # Anomalous value 
         'duration': np.random.random(), 
         'power': np.random.random()}
        for _ in range(5)
    ]
    
    # Score normal and anomalous data
    normal_scores = model.predict(test_normal)
    anomalous_scores = model.predict(test_anomalous)
    
    print(f"Average normal score: {np.mean(normal_scores)}")
    print(f"Average anomalous score: {np.mean(anomalous_scores)}")
    
    # Get model parameters
    params = model.get_model_parameters()
    print(f"Model parameters: {len(params)} items")