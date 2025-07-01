# PyAES Package

**File**: `gluon/contrib/pyaes/__init__.py`  
**Type**: Python AES Encryption Library Package  
**Framework**: Web2py Gluon Framework  
**License**: MIT License  
**Author**: Richard Moore

## Overview

PyAES is a pure-Python implementation of the Advanced Encryption Standard (AES) algorithm and common AES modes of operation. This package provides secure encryption and decryption capabilities for Web2py applications without requiring external C libraries.

## Package Information

### Version
- **Current Version**: 1.3.0
- **License**: MIT License (Copyright 2014 Richard Moore)
- **Implementation**: Pure Python (no C dependencies)

### Key Features
- **Pure Python**: No external dependencies or C compilation required
- **Multiple Key Sizes**: 128-bit, 192-bit, and 256-bit AES encryption
- **Multiple Modes**: ECB, CBC, CFB, OFB, and CTR modes of operation
- **Stream Support**: Encrypt/decrypt data streams with automatic padding
- **Web2py Integration**: Seamlessly integrated into Web2py framework

## Supported Algorithms

### Key Sizes
- **AES-128**: 128-bit keys (16 bytes)
- **AES-192**: 192-bit keys (24 bytes) 
- **AES-256**: 256-bit keys (32 bytes)

### Modes of Operation

**ECB (Electronic Codebook)**
- Simplest mode, each block encrypted independently
- Not recommended for production due to pattern visibility
- Useful for testing and simple applications

**CBC (Cipher-Block Chaining)**
- Each block XORed with previous ciphertext block
- Requires initialization vector (IV)
- Most common mode for file encryption

**CFB (Cipher Feedback)**
- Turns block cipher into stream cipher
- Processes data in segments smaller than block size
- Good for real-time applications

**OFB (Output Feedback)**
- Similar to CFB but encrypts output of cipher
- Does not propagate transmission errors
- Suitable for error-prone environments

**CTR (Counter)**
- Converts block cipher to stream cipher
- Highly parallelizable
- Modern recommended mode

## Module Exports

### Core Classes
```python
from .aes import (
    AES,                        # Core AES algorithm
    AESModeOfOperationCTR,      # Counter mode
    AESModeOfOperationCBC,      # Cipher-Block Chaining
    AESModeOfOperationCFB,      # Cipher Feedback
    AESModeOfOperationECB,      # Electronic Codebook
    AESModeOfOperationOFB,      # Output Feedback
    AESModesOfOperation,        # Mode enumeration
    Counter                     # Counter for CTR mode
)
```

### Stream Processing
```python
from .blockfeeder import (
    decrypt_stream, Decrypter,  # Stream decryption
    encrypt_stream, Encrypter,  # Stream encryption
    PADDING_NONE,              # No padding
    PADDING_DEFAULT           # PKCS#7 padding
)
```

## Usage Examples

### Basic Encryption
```python
import pyaes

# AES-256 encryption
key = b"This_key_for_demo_purposes_only!"  # 32-byte key
plaintext = b"Text may be any length you wish, no padding is required"

# CBC mode with random IV
aes = pyaes.AESModeOfOperationCBC(key)
ciphertext = aes.encrypt(plaintext)
```

### Stream Encryption
```python
# For large files or streaming data
encrypter = pyaes.Encrypter(
    pyaes.AESModeOfOperationCTR(key, pyaes.Counter())
)

ciphertext = b''
ciphertext += encrypter.feed(plaintext[:16])
ciphertext += encrypter.feed(plaintext[16:32])
ciphertext += encrypter.feed()  # Finalize
```

### Web2py Integration
```python
# In Web2py controller
def encrypt_data():
    from gluon.contrib import pyaes
    
    key = session.encryption_key
    data = request.vars.sensitive_data
    
    aes = pyaes.AESModeOfOperationCBC(key)
    encrypted = aes.encrypt(data.encode('utf-8'))
    
    return dict(encrypted=encrypted.hex())
```

## Security Considerations

### Key Management
- **Strong Keys**: Use cryptographically secure random keys
- **Key Storage**: Never hardcode keys in source code
- **Key Rotation**: Regularly rotate encryption keys
- **Key Derivation**: Use proper key derivation functions (PBKDF2, scrypt)

### Initialization Vectors
- **Unique IVs**: Use different IV for each encryption operation
- **Random IVs**: Generate IVs using secure random number generator
- **IV Storage**: Store IV alongside ciphertext for decryption

### Mode Selection
- **Avoid ECB**: Never use ECB mode for production encryption
- **Prefer CTR/CBC**: Use CTR or CBC modes for most applications
- **Authentication**: Consider authenticated encryption (AES-GCM)

## Performance Characteristics

### Pure Python Overhead
- **Speed**: Slower than C implementations (acceptable for most use cases)
- **Memory**: Higher memory usage than optimized libraries
- **Portability**: Runs anywhere Python runs

### Optimization Tips
- **Batch Processing**: Process larger blocks when possible
- **Mode Selection**: CTR mode offers best performance for parallel processing
- **Key Reuse**: Initialize AES objects once and reuse them

## Integration with Web2py

### Session Encryption
```python
# Encrypt sensitive session data
def encrypt_session_data(data):
    from gluon.contrib import pyaes
    key = current.app_key  # Application-specific key
    aes = pyaes.AESModeOfOperationCBC(key)
    return aes.encrypt(json.dumps(data).encode())
```

### Database Field Encryption
```python
# Custom field type for encrypted data
def encrypted_field():
    from gluon.contrib import pyaes
    
    def encrypt(value):
        if value:
            aes = pyaes.AESModeOfOperationCBC(app_key)
            return aes.encrypt(str(value).encode())
        return value
    
    def decrypt(value):
        if value:
            aes = pyaes.AESModeOfOperationCBC(app_key) 
            return aes.decrypt(value).decode()
        return value
    
    return Field.Lazy(lambda: dict(
        represent=decrypt,
        widget=lambda field, value, **attr: 
            INPUT(_value=decrypt(value) if value else '', **attr)
    ))
```

### File Upload Encryption
```python
def secure_upload():
    from gluon.contrib import pyaes
    
    def encrypt_file(file_content, filename):
        key = derive_file_key(filename)  # Derive unique key
        encrypter = pyaes.Encrypter(
            pyaes.AESModeOfOperationCTR(key, pyaes.Counter())
        )
        
        encrypted = b''
        for chunk in file_content:
            encrypted += encrypter.feed(chunk)
        encrypted += encrypter.feed()  # Finalize
        
        return encrypted
```

## Error Handling

### Common Exceptions
```python
try:
    aes = pyaes.AESModeOfOperationCBC(key)
    encrypted = aes.encrypt(data)
except ValueError as e:
    # Invalid key size or data format
    logger.error(f"Encryption error: {e}")
except Exception as e:
    # Other encryption errors
    logger.error(f"Unexpected encryption error: {e}")
```

### Input Validation
```python
def validate_encryption_params(key, data, mode='CBC'):
    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be 16, 24, or 32 bytes")
    
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    
    if mode == 'CBC' and len(data) % 16 != 0:
        raise ValueError("Data length must be multiple of 16 for CBC")
```

## Related Components

### Web2py Security
- **gluon.validators**: Input validation for encrypted fields
- **gluon.storage**: Secure storage containers
- **gluon.cache**: Encrypted caching mechanisms

### External Libraries
- **PyCrypto**: C-based crypto library (faster but requires compilation)
- **cryptography**: Modern Python crypto library
- **hashlib**: Standard library hashing functions

## Best Practices

### Development Guidelines
1. **Never log keys or plaintext**: Implement secure logging practices
2. **Use environment variables**: Store keys in environment, not code
3. **Test thoroughly**: Verify encryption/decryption round trips
4. **Document key management**: Maintain clear key lifecycle documentation

### Production Deployment
1. **Secure key storage**: Use dedicated key management systems
2. **Monitor performance**: Track encryption overhead in production
3. **Regular updates**: Keep PyAES updated for security patches
4. **Backup strategies**: Plan for encrypted data recovery

This package provides essential encryption capabilities for Web2py applications, offering a balance between security, portability, and ease of use through its pure-Python implementation.