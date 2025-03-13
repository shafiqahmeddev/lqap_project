import numpy as np
from federated_learning.base_model import FederatedLearningModel
from scipy.stats import chi2

class AnomalyDetectionModel(FederatedLearningModel):
    """Simple anomaly detection model using statistical methods"""
    def __init__(self, model_id):
        """Initialize the anomaly detection model"""
        super().__init__(model_id, "anomaly_detection")
        
        # Initialize model parameters
        self.mean_vector = None
        self.cov_matrix = None  # Added covariance matrix
        self.std_vector = None
        self.threshold = 0.95  # Changed to use percentile
        self.feature_names = ['time_of_day', 'location', 'frequency', 'duration', 'power']
    
    def _extract_features(self, data):
        """Extract features from raw data"""
        if not data:
            return np.array([])
            
        features = []
        for record in data:
            base_features = [
                record.get('time_of_day', 0),
                record.get('location', 0),
                record.get('frequency', 0),
                record.get('duration', 0),
                record.get('power', 0)
            ]
            # Add derived features
            power_freq_ratio = base_features[4] / (base_features[2] + 1e-10)
            duration_power = base_features[3] * base_features[4]
            features.append(base_features + [power_freq_ratio, duration_power])
            
        return np.array(features)

    def train(self, data):
        """Train the model on local data"""
        features = self._extract_features(data)
        
        if features.size == 0:
            return False
        
        # Calculate mean vector and covariance matrix
        self.mean_vector = np.mean(features, axis=0)
        self.cov_matrix = np.cov(features, rowvar=False)
        self.std_vector = np.std(features, axis=0)
        
        # Handle numerical stability
        self.cov_matrix += np.eye(self.cov_matrix.shape[0]) * 1e-6
        self.std_vector[self.std_vector < 1e-6] = 1.0
        
        # Calculate Mahalanobis distances for training data
        train_scores = self._compute_mahalanobis(features)
        
        # Set threshold based on chi-square distribution
        self.threshold = chi2.ppf(0.95, df=features.shape[1])
        
        self.updated_at = __import__('time').time()
        self.version += 1
        
        return True
        
    def _compute_mahalanobis(self, features):
        # Calculate Mahalanobis distance for each point
        diff = features - self.mean_vector
        inv_cov = np.linalg.inv(self.cov_matrix)
        left = np.dot(diff, inv_cov)
        mahalanobis = np.sqrt(np.sum(left * diff, axis=1))
        return mahalanobis
        
    def predict(self, data):
        """Predict anomaly scores
        Returns a score for each record, higher = more anomalous
        """
        if self.mean_vector is None or self.cov_matrix is None:
            return np.array([1.0] * len(data))  # Untrained model
        
        features = self._extract_features(data)
        
        if features.size == 0:
            return np.array([])
        
        # Compute Mahalanobis distances
        distances = self._compute_mahalanobis(features)
        
        # Normalize scores to [0,1] range
        scores = distances / self.threshold
        scores = np.clip(scores, 0, 1)
        
        return scores
        
    def get_model_parameters(self):
        """Get the model parameters"""
        if self.mean_vector is None or self.cov_matrix is None:
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
            'cov_matrix': self.cov_matrix.tolist(),
            'std_vector': self.std_vector.tolist(),
            'threshold': self.threshold
        }
    
    def set_model_parameters(self, parameters):
        """Update model with new parameters"""
        if not parameters.get('trained', False):
            return False
        
        if 'mean_vector' in parameters:
            self.mean_vector = np.array(parameters['mean_vector'])
        
        if 'cov_matrix' in parameters:
            self.cov_matrix = np.array(parameters['cov_matrix'])
        
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