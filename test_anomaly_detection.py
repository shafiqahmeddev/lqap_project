import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add the project root directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the anomaly detection model
from federated_learning.anomaly_detection import AnomalyDetectionModel

def test_anomaly_detection():
    """Test the anomaly detection functionality"""
    print("Testing Anomaly Detection Model...")
    
    # Create a model
    model = AnomalyDetectionModel("test-model")
    
    # Generate normal training data
    print("Generating training data...")
    np.random.seed(42)  # For reproducibility
    
    normal_data = []
    for i in range(100):
        data_point = {
            'time_of_day': np.random.uniform(0, 1),          # Time of day (normalized)
            'location': np.random.uniform(0, 1),             # Location (normalized)
            'frequency': np.random.normal(0.5, 0.1),         # Normal frequency around 0.5
            'duration': np.random.normal(0.3, 0.05),         # Normal duration around 0.3
            'power': np.random.normal(0.4, 0.1)              # Normal power around 0.4
        }
        normal_data.append(data_point)
    
    # Train the model
    print("Training model...")
    model.train(normal_data)
    print(f"Model trained (version {model.version})")
    
    # Create test data with both normal and anomalous patterns
    print("Generating test data...")
    test_normal = []
    for i in range(50):
        data_point = {
            'time_of_day': np.random.uniform(0, 1),          
            'location': np.random.uniform(0, 1),             
            'frequency': np.random.normal(0.5, 0.1),         
            'duration': np.random.normal(0.3, 0.05),         
            'power': np.random.normal(0.4, 0.1)              
        }
        test_normal.append(data_point)
    
    test_anomalous = []
    for i in range(20):
        # Create several types of anomalies
        anomaly_type = i % 4
        
        if anomaly_type == 0:
            # Anomaly in frequency
            data_point = {
                'time_of_day': np.random.uniform(0, 1),          
                'location': np.random.uniform(0, 1),             
                'frequency': np.random.normal(0.9, 0.1),  # Anomalous frequency
                'duration': np.random.normal(0.3, 0.05),         
                'power': np.random.normal(0.4, 0.1)              
            }
        elif anomaly_type == 1:
            # Anomaly in duration
            data_point = {
                'time_of_day': np.random.uniform(0, 1),          
                'location': np.random.uniform(0, 1),             
                'frequency': np.random.normal(0.5, 0.1),         
                'duration': np.random.normal(0.8, 0.05),  # Anomalous duration
                'power': np.random.normal(0.4, 0.1)              
            }
        elif anomaly_type == 2:
            # Anomaly in power
            data_point = {
                'time_of_day': np.random.uniform(0, 1),          
                'location': np.random.uniform(0, 1),             
                'frequency': np.random.normal(0.5, 0.1),         
                'duration': np.random.normal(0.3, 0.05),         
                'power': np.random.normal(0.9, 0.1)    # Anomalous power
            }
        else:
            # Multiple anomalies
            data_point = {
                'time_of_day': np.random.uniform(0, 1),          
                'location': np.random.uniform(0, 1),             
                'frequency': np.random.normal(0.7, 0.1),  # Slightly anomalous
                'duration': np.random.normal(0.7, 0.05),  # Slightly anomalous
                'power': np.random.normal(0.7, 0.1)       # Slightly anomalous
            }
            
        test_anomalous.append(data_point)
    
    # Combine test data (normal and anomalous)
    test_data = test_normal + test_anomalous
    expected_labels = [0] * len(test_normal) + [1] * len(test_anomalous)
    
    # Get predictions
    print("Evaluating model...")
    anomaly_scores = model.predict(test_data)
    
    # Print statistics
    print(f"Average score for normal data: {np.mean(anomaly_scores[:len(test_normal)]):.4f}")
    print(f"Average score for anomalous data: {np.mean(anomaly_scores[len(test_normal):]):.4f}")
    
    # Use a threshold of 0.5 to classify anomalies
    predicted_labels = (anomaly_scores > 0.5).astype(int)
    
    # Calculate accuracy
    accuracy = np.mean(predicted_labels == expected_labels)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    
    # Visualize results
    plt.figure(figsize=(10, 6))
    
    # Plot scores
    plt.subplot(2, 1, 1)
    normal_indices = range(len(test_normal))
    anomaly_indices = range(len(test_normal), len(test_data))
    
    plt.scatter(normal_indices, anomaly_scores[:len(test_normal)], 
                c='blue', label='Normal', alpha=0.7)
    plt.scatter(anomaly_indices, anomaly_scores[len(test_normal):], 
                c='red', label='Anomalous', alpha=0.7)
    
    plt.axhline(y=0.5, color='green', linestyle='--', label='Threshold')
    plt.title('Anomaly Scores')
    plt.xlabel('Data Point Index')
    plt.ylabel('Anomaly Score')
    plt.legend()
    plt.grid(True)
    
    # Plot feature distributions
    plt.subplot(2, 1, 2)
    
    # Extract features for visualization
    features = ['frequency', 'duration', 'power']
    normal_values = {feature: [point[feature] for point in test_normal] for feature in features}
    anomaly_values = {feature: [point[feature] for point in test_anomalous] for feature in features}
    
    positions = np.arange(len(features))
    width = 0.35
    
    plt.bar(positions - width/2, [np.mean(normal_values[f]) for f in features], 
            width, label='Normal', alpha=0.7, color='blue')
    plt.bar(positions + width/2, [np.mean(anomaly_values[f]) for f in features], 
            width, label='Anomalous', alpha=0.7, color='red')
    
    plt.title('Feature Comparison')
    plt.xticks(positions, features)
    plt.ylabel('Average Value')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    # Save the plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig(f"anomaly_detection_test_{timestamp}.png")
    print(f"Plot saved as anomaly_detection_test_{timestamp}.png")
    
    # Show the plot (comment this out if running on a headless server)
    plt.show()
    
    return model, anomaly_scores, accuracy

if __name__ == "__main__":
    test_anomaly_detection()