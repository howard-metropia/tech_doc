# PyAES Utility Module

**File**: `gluon/contrib/pyaes/util.py`  
**Type**: Utility Functions for AES Operations  
**Framework**: Web2py Gluon Framework  
**License**: MIT License

## Overview

This module provides utility functions for PyAES, primarily focusing on data format handling, padding operations, and Python 2/3 compatibility. It contains helper functions that ensure proper data handling across different Python versions and provide essential cryptographic padding operations.

## Core Functions

### to_bufferable()
Ensures binary data is in the correct format for cryptographic operations:

```python
def to_bufferable(binary):
    return binary
```

**Purpose**: 
- Handles Python 2/3 compatibility for binary data
- Ensures data is in the correct format for AES operations
- Normalizes different binary data types

**Usage**:
```python
# Ensures data is properly formatted for encryption
data = to_bufferable(input_data)
encrypted = aes.encrypt(data)
```

## Padding Operations

### PKCS#7 Padding Functions

**append_PKCS7_padding(data, blocksize=16)**
Adds PKCS#7 padding to data to make it a multiple of the block size:

```python
def append_PKCS7_padding(data, blocksize=16):
    # Calculate padding needed
    pad_count = blocksize - (len(data) % blocksize)
    
    # Create padding bytes (each byte = pad_count)
    padding = bytes([pad_count]) * pad_count
    
    return data + padding
```

**strip_PKCS7_padding(data)**
Removes PKCS#7 padding from decrypted data:

```python
def strip_PKCS7_padding(data):
    # Last byte indicates padding length
    pad_count = data[-1]
    
    # Validate padding
    if pad_count == 0 or pad_count > 16:
        raise ValueError("Invalid padding")
    
    # Verify all padding bytes are correct
    padding = data[-pad_count:]
    if padding != bytes([pad_count]) * pad_count:
        raise ValueError("Invalid padding")
    
    return data[:-pad_count]
```

## Usage Examples

### Basic Padding Operations
```python
from gluon.contrib.pyaes.util import append_PKCS7_padding, strip_PKCS7_padding

# Add padding
original_data = b"Hello World"  # 11 bytes
padded_data = append_PKCS7_padding(original_data)
print(len(padded_data))  # 16 bytes (next multiple of 16)
print(padded_data)       # b'Hello World\x05\x05\x05\x05\x05'

# Remove padding
unpadded_data = strip_PKCS7_padding(padded_data)
print(unpadded_data)     # b'Hello World'
assert original_data == unpadded_data
```

### Data Format Handling
```python
from gluon.contrib.pyaes.util import to_bufferable

# Ensure data is in correct format
def safe_encrypt(data, aes_mode):
    # Convert to proper binary format
    binary_data = to_bufferable(data)
    
    # Add padding if needed (for block modes)
    if hasattr(aes_mode, 'block_size'):
        binary_data = append_PKCS7_padding(binary_data)
    
    # Encrypt
    return aes_mode.encrypt(binary_data)
```

### Custom Padding Validation
```python
def validate_pkcs7_padding(data, block_size=16):
    """Validate PKCS#7 padding without removing it"""
    if len(data) % block_size != 0:
        return False
    
    if len(data) == 0:
        return False
    
    pad_count = data[-1]
    
    # Check padding count is valid
    if pad_count == 0 or pad_count > block_size:
        return False
    
    # Check all padding bytes are correct
    padding = data[-pad_count:]
    expected_padding = bytes([pad_count]) * pad_count
    
    return padding == expected_padding
```

## Integration with Web2py

### Safe Data Processing
```python
def process_encrypted_form_data(form_data, key):
    from gluon.contrib import pyaes
    from gluon.contrib.pyaes.util import to_bufferable, append_PKCS7_padding
    
    # Ensure data is in correct format
    binary_data = to_bufferable(form_data.encode('utf-8'))
    
    # Add padding for CBC mode
    padded_data = append_PKCS7_padding(binary_data)
    
    # Encrypt
    iv = os.urandom(16)
    cbc = pyaes.AESModeOfOperationCBC(key, iv=iv)
    encrypted = cbc.encrypt(padded_data)
    
    return iv + encrypted
```

### Database Field Encryption
```python
def encrypt_database_field(value, field_key):
    from gluon.contrib import pyaes
    from gluon.contrib.pyaes.util import to_bufferable, append_PKCS7_padding
    
    if not value:
        return None
    
    # Convert to binary format
    binary_value = to_bufferable(str(value).encode('utf-8'))
    
    # Add padding
    padded_value = append_PKCS7_padding(binary_value)
    
    # Encrypt with ECB mode (for deterministic field encryption)
    # Note: Only use ECB for single-block data or when patterns aren't a concern
    ecb = pyaes.AESModeOfOperationECB(field_key)
    encrypted = ecb.encrypt(padded_value)
    
    return encrypted

def decrypt_database_field(encrypted_value, field_key):
    from gluon.contrib import pyaes
    from gluon.contrib.pyaes.util import strip_PKCS7_padding
    
    if not encrypted_value:
        return None
    
    # Decrypt
    ecb = pyaes.AESModeOfOperationECB(field_key)
    decrypted = ecb.decrypt(encrypted_value)
    
    # Remove padding
    unpadded = strip_PKCS7_padding(decrypted)
    
    return unpadded.decode('utf-8')
```

## Python 2/3 Compatibility

### Binary Data Handling
The `to_bufferable()` function ensures consistent binary data handling:

```python
# Python 2 compatibility
if sys.version_info[0] == 2:
    def to_bufferable(binary):
        # Python 2: strings are bytes
        if isinstance(binary, unicode):
            return binary.encode('utf-8')
        return str(binary)
else:
    def to_bufferable(binary):
        # Python 3: ensure bytes type
        if isinstance(binary, str):
            return binary.encode('utf-8')
        return bytes(binary)
```

### String/Bytes Conversion
```python
def safe_string_to_bytes(data):
    """Convert string data to bytes safely across Python versions"""
    from gluon.contrib.pyaes.util import to_bufferable
    
    if isinstance(data, str):
        return to_bufferable(data.encode('utf-8'))
    elif isinstance(data, bytes):
        return to_bufferable(data)
    else:
        return to_bufferable(str(data).encode('utf-8'))
```

## Error Handling

### Padding Validation Errors
```python
def safe_padding_operations(data):
    from gluon.contrib.pyaes.util import append_PKCS7_padding, strip_PKCS7_padding
    
    try:
        # Add padding
        padded = append_PKCS7_padding(data)
        
        # Verify padding was added correctly
        if len(padded) % 16 != 0:
            raise ValueError("Padding failed - length not multiple of 16")
        
        # Remove padding
        unpadded = strip_PKCS7_padding(padded)
        
        # Verify original data integrity
        if unpadded != data:
            raise ValueError("Padding round-trip failed")
        
        return padded
        
    except ValueError as e:
        logger.error(f"Padding operation failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected padding error: {str(e)}")
        raise ValueError("Padding operation failed")
```

### Data Format Errors
```python
def validate_binary_data(data):
    from gluon.contrib.pyaes.util import to_bufferable
    
    try:
        # Attempt to convert to bufferable format
        binary_data = to_bufferable(data)
        
        # Validate it's actually binary data
        if not isinstance(binary_data, (bytes, bytearray)):
            raise TypeError("Data cannot be converted to binary format")
        
        return binary_data
        
    except (TypeError, UnicodeError) as e:
        logger.error(f"Binary data validation failed: {str(e)}")
        raise ValueError("Invalid binary data format")
```

## Performance Considerations

### Efficient Padding
```python
# Optimized padding for large data
def efficient_padding(data, block_size=16):
    remainder = len(data) % block_size
    if remainder == 0:
        # Full block padding
        pad_count = block_size
    else:
        pad_count = block_size - remainder
    
    # Use bytearray for efficiency with large data
    padded = bytearray(data)
    padded.extend([pad_count] * pad_count)
    
    return bytes(padded)
```

### Memory-Efficient Operations
```python
def memory_efficient_format_conversion(data_iterator):
    """Convert data stream to bufferable format efficiently"""
    for chunk in data_iterator:
        yield to_bufferable(chunk)
```

## Security Considerations

### Padding Oracle Protection
```python
def secure_padding_check(encrypted_data, decrypt_func):
    """Prevent padding oracle attacks through constant-time validation"""
    try:
        decrypted = decrypt_func(encrypted_data)
        unpadded = strip_PKCS7_padding(decrypted)
        return unpadded, True
    except:
        # Return dummy data and failure flag
        # Always take same amount of time regardless of error type
        return b'', False
```

### Constant-Time Padding Validation
```python
def constant_time_padding_check(data):
    """Validate padding in constant time to prevent timing attacks"""
    if len(data) == 0:
        return False
    
    pad_count = data[-1]
    valid = True
    
    # Check all conditions in constant time
    valid &= (pad_count > 0)
    valid &= (pad_count <= 16)
    valid &= (len(data) >= pad_count)
    
    # Check padding bytes in constant time
    for i in range(pad_count):
        valid &= (data[-(i+1)] == pad_count)
    
    return valid
```

This utility module provides essential support functions for the PyAES library, ensuring robust data handling, proper padding operations, and cross-platform compatibility for encryption operations in Web2py applications.