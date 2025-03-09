"""
LQAP Performance Benchmarking Tool
This script evaluates the performance of key LQAP components
"""
import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import gc

# Import LQAP components
from crypto_components.xmss import XMSS
from crypto_components.puf_simulator import PUFSimulator
from lqap_protocol.protocol import LQAPProtocol

def run_benchmark(iterations=100):
    """Run performance benchmarks on key components"""
    print("LQAP Performance Benchmark")
    print("-------------------------")
    
    results = {}
    
    # 1. Benchmark XMSS operations
    print("\n1. XMSS Cryptographic Operations")
    
    # Key generation
    times = []
    for i in range(iterations):
        xmss = XMSS()
        start_time = time.time()
        public_key, private_key = xmss.key_gen()
        elapsed = time.time() - start_time
        times.append(elapsed)
        
        # Clean up to prevent memory issues
        del xmss
        gc.collect()
    
    results['xmss_keygen'] = times
    print(f"  Key Generation: {np.mean(times)*1000:.2f} ms (avg), {np.min(times)*1000:.2f} ms (min), {np.max(times)*1000:.2f} ms (max)")
    
    # Signing
    xmss = XMSS()
    public_key, private_key = xmss.key_gen()
    message = b"Test message for benchmarking"
    
    times = []
    for i in range(iterations):
        start_time = time.time()
        signature = xmss.sign(message, private_key)
        elapsed = time.time() - start_time
        times.append(elapsed)
    
    results['xmss_sign'] = times
    print(f"  Signature Generation: {np.mean(times)*1000:.2f} ms (avg), {np.min(times)*1000:.2f} ms (min), {np.max(times)*1000:.2f} ms (max)")
    
    # Verification
    times = []
    for i in range(iterations):
        start_time = time.time()
        result = xmss.verify(message, signature, public_key)
        elapsed = time.time() - start_time
        times.append(elapsed)
    
    results['xmss_verify'] = times
    print(f"  Signature Verification: {np.mean(times)*1000:.2f} ms (avg), {np.min(times)*1000:.2f} ms (min), {np.max(times)*1000:.2f} ms (max)")
    
    # Clean up
    del xmss
    gc.collect()
    
    # 2. Benchmark PUF operations
    print("\n2. PUF Simulator Operations")
    
    # Challenge-response
    puf = PUFSimulator()
    challenge = "benchmark_challenge"
    
    times = []
    for i in range(iterations):
        start_time = time.time()
        response = puf.challenge(challenge)
        elapsed = time.time() - start_time
        times.append(elapsed)
    
    results['puf_challenge'] = times
    print(f"  Challenge-Response: {np.mean(times)*1000:.2f} ms (avg), {np.min(times)*1000:.2f} ms (min), {np.max(times)*1000:.2f} ms (max)")
    
    # Verification
    times = []
    for i in range(iterations):
        start_time = time.time()
        result = puf.verify(challenge, response)
        elapsed = time.time() - start_time
        times.append(elapsed)
    
    results['puf_verify'] = times
    print(f"  PUF Verification: {np.mean(times)*1000:.2f} ms (avg), {np.min(times)*1000:.2f} ms (min), {np.max(times)*1000:.2f} ms (max)")
    
    # Clean up
    del puf
    gc.collect()
    
    # 3. Benchmark Authentication Process
    print("\n3. Authentication Process")
    
    # Initialize protocol
    protocol = LQAPProtocol()
    protocol.start()
    
    try:
        # Register entities
        ev_id = protocol.register_entity("EV", "bench-ev")
        cs_id = protocol.register_entity("CS", "bench-cs")
        en_id = protocol.register_entity("EN", "bench-en")
        
        # Issue credential
        protocol.issue_verifiable_credential(ev_id, en_id)
        
        # Intra-domain authentication
        times = []
        for i in range(5):  # Fewer iterations for complete authentication
            start_time = time.time()
            success, result = protocol.intra_domain_authentication(ev_id, cs_id)
            elapsed = time.time() - start_time
            times.append(elapsed)
            
            # End the session
            if success:
                protocol.end_session(result['session_id'])
        
        results['intra_auth'] = times
        print(f"  Intra-Domain Authentication: {np.mean(times)*1000:.2f} ms (avg), {np.min(times)*1000:.2f} ms (min), {np.max(times)*1000:.2f} ms (max)")
        
        # Cross-domain authentication
        times = []
        for i in range(5):  # Fewer iterations for complete authentication
            start_time = time.time()
            success, result = protocol.cross_domain_authentication(ev_id, cs_id, en_id)
            elapsed = time.time() - start_time
            times.append(elapsed)
            
            # End the session
            if success:
                protocol.end_session(result['session_id'])
        
        results['cross_auth'] = times
        print(f"  Cross-Domain Authentication: {np.mean(times)*1000:.2f} ms (avg), {np.min(times)*1000:.2f} ms (min), {np.max(times)*1000:.2f} ms (max)")
    
    finally:
        # Stop the protocol
        protocol.stop()
    
    # Generate visualization
    plt.figure(figsize=(15, 10))
    
    # Plot XMSS operations
    plt.subplot(2, 2, 1)
    plt.boxplot([results['xmss_keygen'], results['xmss_sign'], results['xmss_verify']], 
                labels=['Key Generation', 'Signing', 'Verification'])
    plt.title('XMSS Operations (ms)')
    plt.ylabel('Time (ms)')
    plt.yscale('log')
    plt.grid(True)
    
    # Plot PUF operations
    plt.subplot(2, 2, 2)
    plt.boxplot([results['puf_challenge'], results['puf_verify']], 
                labels=['Challenge', 'Verification'])
    plt.title('PUF Operations (ms)')
    plt.ylabel('Time (ms)')
    plt.grid(True)
    
    # Plot Authentication
    plt.subplot(2, 2, 3)
    plt.boxplot([results['intra_auth'], results['cross_auth']], 
                labels=['Intra-Domain', 'Cross-Domain'])
    plt.title('Authentication Process (ms)')
    plt.ylabel('Time (ms)')
    plt.grid(True)
    
    # Plot Operation Counts
    plt.subplot(2, 2, 4)
    operations = ['XMSS Key Gen', 'XMSS Sign', 'XMSS Verify', 'PUF Challenge', 'PUF Verify', 
                 'Intra-Auth', 'Cross-Auth']
    op_counts = [iterations, iterations, iterations, iterations, iterations, 5, 5]
    plt.bar(operations, op_counts)
    plt.title('Benchmark Operation Counts')
    plt.ylabel('Number of Operations')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the visualization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"lqap_benchmark_{timestamp}.png"
    plt.savefig(filename)
    print(f"\nBenchmark results saved to {filename}")
    
    # Show the plot (if running in GUI environment)
    plt.show()
    
    return results

if __name__ == "__main__":
    try:
        run_benchmark(iterations=50)  # Reduced iterations for faster execution
    except Exception as e:
        print(f"Error: {e}")