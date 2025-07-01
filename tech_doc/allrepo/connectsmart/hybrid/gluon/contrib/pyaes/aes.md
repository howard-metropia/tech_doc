# PyAES Core AES Module

**File**: `gluon/contrib/pyaes/aes.py`  
**Type**: AES Encryption Algorithm Implementation  
**Framework**: Web2py Gluon Framework  
**License**: MIT License

## Overview

This module contains the core implementation of the Advanced Encryption Standard (AES) algorithm and its various modes of operation. It provides a pure Python implementation that supports 128-bit, 192-bit, and 256-bit encryption keys.

## Core Classes

### AES Class
The fundamental AES algorithm implementation:

```python
class AES:
    def __init__(self, key):
        # Initialize with 128, 192, or 256-bit key
        pass
    
    def encrypt(self, data):
        # Encrypt single 16-byte block
        pass
    
    def decrypt(self, data):  
        # Decrypt single 16-byte block
        pass
```

### Modes of Operation

**AESModeOfOperationECB**
- Electronic Codebook mode
- Simplest mode, encrypts each block independently
- **Warning**: Not secure for production use

**AESModeOfOperationCBC**
- Cipher-Block Chaining mode
- Each block XORed with previous ciphertext
- Requires initialization vector (IV)

**AESModeOfOperationCFB** 
- Cipher Feedback mode
- Converts block cipher to stream cipher
- Processes segments smaller than block size

**AESModeOfOperationOFB**
- Output Feedback mode
- Encrypts cipher output, not plaintext
- Error propagation resistant

**AESModeOfOperationCTR**
- Counter mode
- Modern stream cipher mode
- Highly parallelizable and secure

## Key Features

### Multiple Key Sizes
- **128-bit keys**: 16 bytes, 10 rounds
- **192-bit keys**: 24 bytes, 12 rounds
- **256-bit keys**: 32 bytes, 14 rounds

### Block Processing
- **Block Size**: 128 bits (16 bytes) for all key sizes
- **State Management**: Internal state tracking for modes
- **Round Functions**: SubBytes, ShiftRows, MixColumns, AddRoundKey

## Usage Examples

### Basic Block Encryption
```python
from gluon.contrib import pyaes

# 256-bit key (32 bytes)
key = b"This_key_for_demo_purposes_only!"
plaintext = b"A 16-byte block!"  # Must be exactly 16 bytes

# Create AES cipher
aes = pyaes.AES(key)

# Encrypt/decrypt single block
ciphertext = aes.encrypt(plaintext)
decrypted = aes.decrypt(ciphertext)
```

### CBC Mode with IV
```python
# Generate random IV (should be unique for each encryption)
import os
iv = os.urandom(16)

# CBC mode encryption
cbc = pyaes.AESModeOfOperationCBC(key, iv=iv)

# Encrypt multiple blocks
plaintext = b"This message is longer than 16 bytes and will span multiple blocks."
ciphertext = cbc.encrypt(plaintext)

# Decrypt (need same IV)
cbc_decrypt = pyaes.AESModeOfOperationCBC(key, iv=iv)
decrypted = cbc_decrypt.decrypt(ciphertext)
```

### CTR Mode (Recommended)
```python
# Counter mode - modern and secure
counter = pyaes.Counter()
ctr = pyaes.AESModeOfOperationCTR(key, counter=counter)

# Encrypt data of any length
plaintext = b"Counter mode can encrypt data of any length without padding!"
ciphertext = ctr.encrypt(plaintext)

# Decrypt with same counter
counter = pyaes.Counter()  # Reset counter
ctr_decrypt = pyaes.AESModeOfOperationCTR(key, counter=counter)
decrypted = ctr_decrypt.decrypt(ciphertext)
```

## Security Implementation

### Algorithm Components

**SubBytes Transformation**
- Non-linear substitution using S-box
- Provides confusion in the cipher
- Resistance against linear cryptanalysis

**ShiftRows Transformation**  
- Cyclic shifts of state rows
- Provides diffusion across columns
- Mixes data within state

**MixColumns Transformation**
- Linear transformation of state columns
- Maximum diffusion property
- Ensures each output bit depends on input bits

**AddRoundKey**
- XOR state with round key
- Key schedule expansion
- Combines plaintext with secret key

### Key Schedule
- Expands original key into round keys
- Different expansion for each key size
- Uses Rcon (round constants) for security

## Performance Considerations

### Pure Python Limitations
- **Speed**: ~10-100x slower than C implementations
- **Memory**: Higher memory usage for state management
- **CPU**: More CPU intensive than hardware AES

### Optimization Strategies
```python
# Reuse AES objects to avoid key schedule recalculation
aes = pyaes.AES(key)  # Calculate key schedule once
for block in blocks:
    encrypted = aes.encrypt(block)  # Reuse existing schedule

# Use CTR mode for parallel processing potential
ctr = pyaes.AESModeOfOperationCTR(key, counter)
# CTR mode can be parallelized (though not in this implementation)
```

## Mode Comparison

### Security Levels
1. **CTR**: Highly secure, modern recommendation
2. **CBC**: Secure with proper IV management
3. **CFB/OFB**: Secure for specific use cases
4. **ECB**: **NEVER use in production** - patterns visible

### Performance Characteristics
1. **CTR**: Best for stream processing
2. **ECB**: Fastest but insecure
3. **CBC**: Good balance of security/performance
4. **CFB/OFB**: Slower but good for real-time streams

## Integration with Web2py

### Database Encryption
```python
def encrypt_sensitive_field(value, key):
    from gluon.contrib import pyaes
    import os
    
    if not value:
        return None
        
    # Use CBC mode with random IV
    iv = os.urandom(16)
    cbc = pyaes.AESModeOfOperationCBC(key, iv=iv)
    
    # Pad value to block boundary
    padded = value.encode('utf-8')
    if len(padded) % 16:
        pad_len = 16 - (len(padded) % 16)
        padded += bytes([pad_len]) * pad_len
    
    encrypted = cbc.encrypt(padded)
    return iv + encrypted  # Store IV with ciphertext
```

### Session Security
```python
def secure_session_encrypt(session_data, app_secret):
    from gluon.contrib import pyaes
    import json
    import hashlib
    
    # Derive encryption key from app secret
    key = hashlib.sha256(app_secret.encode()).digest()[:32]
    
    # Use CTR mode for session encryption
    counter = pyaes.Counter()
    ctr = pyaes.AESModeOfOperationCTR(key, counter=counter)
    
    # Encrypt JSON-serialized session
    json_data = json.dumps(session_data).encode('utf-8')
    encrypted = ctr.encrypt(json_data)
    
    return encrypted
```

## Error Handling

### Common Issues
```python
def safe_aes_operation(key, data, mode='CBC'):
    try:
        if len(key) not in [16, 24, 32]:
            raise ValueError(f"Invalid key size: {len(key)}. Must be 16, 24, or 32 bytes.")
        
        if mode == 'CBC':
            aes = pyaes.AESModeOfOperationCBC(key)
        elif mode == 'CTR':
            aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter())
        else:
            raise ValueError(f"Unsupported mode: {mode}")
            
        return aes.encrypt(data)
        
    except Exception as e:
        logger.error(f"AES operation failed: {str(e)}")
        raise
```

## Best Practices

### Key Management
1. **Generate strong keys**: Use cryptographically secure random generators
2. **Key derivation**: Use PBKDF2, scrypt, or Argon2 for password-based keys
3. **Key storage**: Never store keys in source code or configuration files
4. **Key rotation**: Implement regular key rotation policies

### Mode Selection
1. **Prefer CTR or CBC**: Avoid ECB mode completely
2. **Unique IVs**: Always use unique IVs for each encryption
3. **Authentication**: Consider authenticated encryption modes
4. **Padding**: Handle padding correctly to prevent padding oracle attacks

This module provides the foundational cryptographic capabilities needed for secure data protection in Web2py applications, with careful attention to both security and practical implementation concerns.