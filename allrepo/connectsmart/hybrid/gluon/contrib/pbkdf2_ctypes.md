# Gluon Contrib PBKDF2 CTypes Module

## Overview
High-performance PBKDF2 implementation using ctypes to interface with native crypto libraries (OpenSSL or CommonCrypto). Provides faster password hashing by leveraging optimized C implementations while maintaining the same API as the pure Python version.

## Module Information
- **Module**: `gluon.contrib.pbkdf2_ctypes`
- **Author**: Michele Comitini
- **License**: LGPLv3
- **Version**: 0.99.4
- **Dependencies**: ctypes, platform-specific crypto libraries

## Key Features
- **High Performance**: Native C library implementation
- **Cross-Platform**: Support for OpenSSL and macOS CommonCrypto
- **API Compatible**: Drop-in replacement for pbkdf2.py
- **Multiple Hash Functions**: SHA-1, SHA-224, SHA-256, SHA-384, SHA-512
- **Automatic Detection**: Detects available crypto libraries

## Main Functions

### pkcs5_pbkdf2_hmac()
Core PBKDF2 function using native crypto libraries.

### pbkdf2_bin()
Generate binary PBKDF2 hash using native implementation.

### pbkdf2_hex()
Generate hexadecimal PBKDF2 hash using native implementation.

## Platform Support

### OpenSSL (Linux/Windows)
- Automatically detects OpenSSL library
- Uses EVP_PBKDF2_HMAC for optimal performance
- Supports all standard hash functions

### CommonCrypto (macOS)
- Native macOS crypto framework
- CCKeyDerivationPBKDF function
- Hardware-accelerated when available

### Fallback Behavior
- Falls back to pure Python implementation if native libraries unavailable
- Maintains consistent API across platforms
- Graceful degradation for compatibility

## Usage Examples

### Basic Usage
```python
from gluon.contrib.pbkdf2_ctypes import pbkdf2_hex, pbkdf2_bin

# Same API as pure Python version
hash_hex = pbkdf2_hex('password', 'salt', 10000, 32)
hash_bin = pbkdf2_bin('password', 'salt', 10000, 32)
```

### Performance Comparison
```python
import time
from gluon.contrib.pbkdf2 import pbkdf2_hex as py_pbkdf2
from gluon.contrib.pbkdf2_ctypes import pbkdf2_hex as c_pbkdf2

password = 'test_password'
salt = b'test_salt'
iterations = 100000

# Pure Python timing
start = time.time()
py_hash = py_pbkdf2(password, salt, iterations)
py_time = time.time() - start

# Native library timing
start = time.time()
c_hash = c_pbkdf2(password, salt, iterations)
c_time = time.time() - start

print(f"Python: {py_time:.3f}s")
print(f"Native: {c_time:.3f}s")
print(f"Speedup: {py_time/c_time:.1f}x")
```

## Integration

### Drop-in Replacement
```python
# Replace import for immediate performance boost
# from gluon.contrib.pbkdf2 import pbkdf2_hex
from gluon.contrib.pbkdf2_ctypes import pbkdf2_hex

# All existing code works unchanged
password_hash = pbkdf2_hex('user_password', salt, 10000, 32)
```

### Conditional Import
```python
try:
    from gluon.contrib.pbkdf2_ctypes import pbkdf2_hex, pbkdf2_bin
    USING_NATIVE = True
except ImportError:
    from gluon.contrib.pbkdf2 import pbkdf2_hex, pbkdf2_bin
    USING_NATIVE = False

print(f"Using native PBKDF2: {USING_NATIVE}")
```

This module provides significant performance improvements for password hashing operations while maintaining full compatibility with the pure Python implementation.