# LQAP: Lightweight Quantum-Resistant Authentication Protocol

A secure authentication framework for Vehicle-to-Grid (V2G) networks using post-quantum cryptography, Physical Unclonable Functions (PUFs), and Federated Learning.

## Overview

LQAP provides a secure, efficient and quantum-resistant authentication solution for V2G environments. It combines several cutting-edge technologies:

- **Post-Quantum Cryptography**: XMSS and LMS signature schemes to resist quantum computing attacks
- **Physical Unclonable Functions (PUF)**: Hardware-based authentication for tamper-resistant identity verification
- **Zero-Knowledge Proofs (ZKP)**: Privacy-preserving cross-domain authentication
- **Hierarchical Federated Learning (HFL)**: Distributed anomaly detection for enhanced security
- **Blockchain Integration**: Immutable logging of authentication events

## System Components

The LQAP system consists of four main entity types:

1. **Electric Vehicles (EVs)**: Mobile entities that request charging services
2. **Charging Stations (CSs)**: Fixed infrastructure that provides charging services
3. **Edge Nodes (ENs)**: Regional aggregation points that issue credentials and manage local federated learning
4. **Electric Service Providers (ESPs)**: Top-level entities that coordinate edge nodes and maintain global models

## Features

- **Quantum-Resistant Authentication**: Secure against future quantum computing threats
- **Cross-Domain Authentication**: Seamless authentication across different administrative domains
- **Anomaly Detection**: Federated learning-based detection of suspicious authentication patterns
- **Privacy Preservation**: Zero-knowledge proofs for minimal information disclosure
- **Scalable Architecture**: Hierarchical design for efficient large-scale deployment

## Getting Started

### Prerequisites

- Python 3.10 or later
- Required packages: numpy, matplotlib, cryptography, etc.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shafiqahmeddev/lqap-implementation.git
   cd lqap-implementation

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Install the package in development mode:
    ```bash
    pip install -e .

### running the System:

1. Start the LQAP system:
    ```bash
    python run.py

2. Run the dashboard:
    ```bash
    python run_dashboard.py

3. Run a simulation:
    ```bash
    run_simulation.py

### Testing and Evaluation

1. Run the system test:
    ```bash
    python test_system.py

2. Visualize anomaly detection:
    ```bash
    python visualize_anomalies.py

3. Benchmark performance:
    ```bash
    python benchmark.py

## Acknowledgements
This project implements the architecture described in the paper "A Decentralized Blockchain-Based Federated Learning Architecture for Secure Multi-Domain V2G Networks" by Shafiq Ahmed and Mohammad Hossein Anisi.


## Future Development Areas

Now that you have a complete working LQAP system, here are some directions for further development:

1. **Performance Optimization**: Identify and optimize bottlenecks in the system
2. **Advanced UI**: Develop a more sophisticated dashboard with additional visualizations
3. **Hardware Integration**: Explore options for integrating with real PUF hardware
4. **Blockchain Enhancements**: Implement more sophisticated consensus mechanisms
5. **Advanced Federated Learning**: Develop more sophisticated anomaly detection models
6. **Mobile Application**: Create a mobile app for EV users
7. **Real-world Testing**: Test the system in a real V2G environment

Which of these areas would you like to explore next?