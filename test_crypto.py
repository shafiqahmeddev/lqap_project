from crypto_components.xmss import XMSS

def test_xmss():
    """Test the XMSS implementation"""
    xmss = XMSS()
    public_key, private_key = xmss.key_gen()
    message = b"Hello, world!"
    
    # Sign the message
    signature = xmss.sign(message, private_key)
    
    # Verify the signature
    result = xmss.verify(message, signature, public_key)
    
    return result

if __name__ == "__main__":
    result = test_xmss()
    print(f"XMSS Test Result: {'Success' if result else 'Failure'}")