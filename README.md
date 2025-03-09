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