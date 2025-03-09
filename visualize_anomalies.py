"""
LQAP Anomaly Detection Visualization Tool
This script demonstrates the anomaly detection capabilities of LQAP
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import random

# Import FL components
from federated_learning.anomaly_detection import AnomalyDetectionModel
from federated_learning.hierarchical_fl import HierarchicalFederatedLearning

def generate_data(num_normal=100, num_anomalies=20):
    """Generate test data with normal and anomalous patterns"""
    # Normal data
    normal_data = []
    for i in range(num_normal):
        data_point = {
            'time_of_day': random.random(),
            'location': random.random(),
            'frequency': random.normalvariate(0.5, 0.1),
            'duration': random.normalvariate(0.3, 0.05),
            'power': random.normalvariate(0.4, 0.1)
        }
        normal_data.append(data_point)
    
    # Anomalous data
    anomalous_data = []
    for i in range(num_anomalies):
        # Create different types of anomalies
        anomaly_type = i % 4
        
        if anomaly_type == 0:
            # Anomaly in frequency
            data_point = {
                'time_of_day': random.random(),
                'location': random.random(),
                'frequency': random.normalvariate(0.9, 0.1),  # Anomalous
                'duration': random.normalvariate(0.3, 0.05),
                'power': random.normalvariate(0.4, 0.1)
            }
        elif anomaly_type == 1:
            # Anomaly in duration
            data_point = {
                'time_of_day': random.random(),
                'location': random.random(),
                'frequency': random.normalvariate(0.5, 0.1),
                'duration': random.normalvariate(0.8, 0.05),  # Anomalous
                'power': random.normalvariate(0.4, 0.1)
            }
        elif anomaly_type == 2:
            # Anomaly in power
            data_point = {
                'time_of_day': random.random(),
                'location': random.random(),
                'frequency': random.normalvariate(0.5, 0.1),
                'duration': random.normalvariate(0.3, 0.05),
                'power': random.normalvariate(0.9, 0.1)  # Anomalous
            }
        else:
            # Multiple anomalies
            data_point = {
                'time_of_day': random.random(),
                'location': random.random(),
                'frequency': random.normalvariate(0.8, 0.1),  # Anomalous
                'duration': random.normalvariate(0.7, 0.05),  # Anomalous
                'power': random.normalvariate(0.8, 0.1)  # Anomalous
            }
        
        anomalous_data.append(data_point)
    
    return normal_data, anomalous_data

def visualize_anomaly_detection():
    """Visualize the anomaly detection capabilities"""
    print("LQAP Anomaly Detection Visualization")
    print("------------------------------------")
    
    # Generate training and test data
    print("Generating training data...")
    train_normal, _ = generate_data(num_normal=200, num_anomalies=0)
    
    print("Generating test data...")
    test_normal, test_anomalous = generate_data(num_normal=50, num_anomalies=20)
    
    # Initialize the model
    print("Initializing anomaly detection model...")
    model = AnomalyDetectionModel("visualization_model")
    
    # Train the model
    print("Training model on normal data...")
    model.train(train_normal)
    
    # Predict anomalies
    print("Detecting anomalies in test data...")
    normal_scores = model.predict(test_normal)
    anomalous_scores = model.predict(test_anomalous)
    
    # Combine data for visualization
    all_data = test_normal + test_anomalous
    all_scores = np.concatenate([normal_scores, anomalous_scores])
    labels = np.array([0] * len(test_normal) + [1] * len(test_anomalous))
    
    # Print statistics
    print(f"\nStatistics:")
    print(f"  Average score for normal data: {np.mean(normal_scores):.4f}")
    print(f"  Average score for anomalous data: {np.mean(anomalous_scores):.4f}")
    print(f"  Score difference: {np.mean(anomalous_scores) - np.mean(normal_scores):.4f}")
    
    # Calculate accuracy using a threshold of 0.5
    predictions = (all_scores > 0.5).astype(int)
    accuracy = np.mean(predictions == labels)
    print(f"  Accuracy (threshold 0.5): {accuracy*100:.2f}%")
    
    # Calculate ROC curve
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, thresholds = roc_curve(labels, all_scores)
    roc_auc = auc(fpr, tpr)
    print(f"  Area Under ROC Curve: {roc_auc:.4f}")
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # 1. Anomaly scores plot
    plt.subplot(2, 2, 1)
    plt.scatter(range(len(test_normal)), normal_scores, label='Normal', alpha=0.7, color='blue')
    plt.scatter(range(len(test_normal), len(all_scores)), anomalous_scores, label='Anomalous', alpha=0.7, color='red')
    plt.axhline(y=0.5, color='green', linestyle='--', label='Threshold (0.5)')
    plt.title('Anomaly Scores')
    plt.xlabel('Sample Index')
    plt.ylabel('Anomaly Score')
    plt.legend()
    plt.grid(True)
    
    # 2. ROC curve
    plt.subplot(2, 2, 2)
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.grid(True)
    
    # 3. Feature distributions
    plt.subplot(2, 2, 3)
    features = ['frequency', 'duration', 'power']
    normal_means = [np.mean([point[f] for point in test_normal]) for f in features]
    anomalous_means = [np.mean([point[f] for point in test_anomalous]) for f in features]
    
    x = np.arange(len(features))
    width = 0.35
    
    plt.bar(x - width/2, normal_means, width, label='Normal', color='blue', alpha=0.7)
    plt.bar(x + width/2, anomalous_means, width, label='Anomalous', color='red', alpha=0.7)
    plt.xticks(x, features)
    plt.ylabel('Average Value')
    plt.title('Feature Comparison')
    plt.legend()
    plt.grid(True)
    
    # 4. Score distributions
    plt.subplot(2, 2, 4)
    plt.hist(normal_scores, bins=20, alpha=0.5, label='Normal', color='blue')
    plt.hist(anomalous_scores, bins=20, alpha=0.5, label='Anomalous', color='red')
    plt.axvline(x=0.5, color='green', linestyle='--', label='Threshold (0.5)')
    plt.title('Score Distributions')
    plt.xlabel('Anomaly Score')
    plt.ylabel('Count')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    # Save the visualization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"anomaly_detection_visualization_{timestamp}.png"
    plt.savefig(filename)
    print(f"\nVisualization saved to {filename}")
    
    # Show the plot (if running in GUI environment)
    plt.show()
    
    return model, normal_scores, anomalous_scores

if __name__ == "__main__":
    try:
        visualize_anomaly_detection()
    except Exception as e:
        print(f"Error: {e}")