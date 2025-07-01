# Gluon Utils Module

## Overview

The `utils.py` module provides security-focused utilities for the web2py Gluon framework, specifically handling cryptographic operations, secure data serialization, random number generation, and IP address validation. This module implements critical security functions including AES encryption, HMAC authentication, and secure UUID generation.

## Key Features

- **AES Encryption**: Secure symmetric encryption with fallback to pure Python implementation
- **Secure Serialization**: HMAC-authenticated pickle dumps/loads with compression support
- **UUID Generation**: Cryptographically strong UUID generation with machine-specific entropy
- **IP Validation**: IPv4/IPv6 address validation and loopback detection
- **Timing Attack Protection**: Constant-time string comparison functions
- **Random Number Generation**: Optimized secure random number generation

## Core Components

### Encryption Functions

#### `AES_new(key, IV=None)`
Creates a new AES cipher instance with optional initialization vector.

**Parameters:**
- `key`: Encryption key (must be properly padded to 32 bytes)
- `IV`: Initialization vector (auto-generated if None)

**Returns:** Tuple of (cipher_object, IV)

```python
cipher, iv = AES_new(key)
```

#### `AES_enc(cipher, data)` / `AES_dec(cipher, data)`
Encrypt/decrypt data using the provided cipher.

**Parameters:**
- `cipher`: AES cipher object from AES_new()
- `data`: Data to encrypt/decrypt

**Returns:** Encrypted/decrypted bytes

### Secure Data Serialization

#### `secure_dumps(data, encryption_key, hash_key=None, compression_level=None)`
Securely serializes data with encryption and HMAC authentication.

**Features:**
- Pickle serialization with highest protocol
- Optional zlib compression
- AES encryption with random IV
- HMAC-SHA256 authentication
- Base64 URL-safe encoding

**Parameters:**
- `data`: Object to serialize
- `encryption_key`: Key for AES encryption
- `hash_key`: Key for HMAC (derived from encryption_key if None)
- `compression_level`: Optional zlib compression level

**Returns:** Authenticated encrypted data string

```python
serialized = secure_dumps(data, "my_secret_key", compression_level=6)
```

#### `secure_loads(data, encryption_key, hash_key=None, compression_level=None)`
Deserializes and verifies secure data dumps.

**Security Features:**
- HMAC signature verification
- Timing attack resistant comparison
- Automatic fallback to deprecated format
- Exception handling for corrupted data

**Returns:** Deserialized object or None if verification fails

### UUID and Random Number Generation

#### `web2py_uuid(ctokens=UNPACKED_CTOKENS)`
Generates cryptographically strong UUIDs with machine-specific entropy.

**Features:**
- Uses os.urandom() when available
- XORs with machine-specific tokens
- Falls back to random module with warning
- Follows UUID4 format specification

**Returns:** UUID string

```python
unique_id = web2py_uuid()
```

#### `fast_urandom16()`
Optimized secure random number generation.

**Features:**
- 4x faster than repeated os.urandom(16) calls
- Prevents "too many files open" issues
- Thread-safe with RLock
- Bulk generation with local caching

**Returns:** 16 bytes of random data

### Utility Functions

#### `compare(a, b)`
Timing attack resistant string comparison.

**Features:**
- Uses hmac.compare_digest when available
- Custom constant-time implementation fallback
- Protection against timing-based attacks

**Returns:** Boolean indicating equality

#### `pad(s, n=32)` / `unpad(s, n=32)`
PKCS7v1.5 compliant padding operations.

**Features:**
- RFC 2315 compliant padding
- Secure unpadding with side-channel protection
- Default 32-byte block size for AES

#### `md5_hash(text)`
Generates MD5 hash of text (legacy support).

**Note:** MD5 is cryptographically broken; use only for non-security purposes.

### IP Address Validation

#### `is_valid_ip_address(address)`
Validates IPv4 and IPv6 addresses.

**Features:**
- Handles special cases (localhost, loopback)
- IPv4 validation using socket.inet_aton()
- IPv6 validation using socket.inet_pton()
- Regex fallback for systems without socket functions

**Examples:**
```python
is_valid_ip_address('127.0.0.1')        # True
is_valid_ip_address('2001:660::1')      # True
is_valid_ip_address('127.0')            # False
```

#### `is_loopback_ip_address(ip=None, addrinfo=None)`
Determines if an address is a loopback address.

**Features:**
- Supports both IPv4 and IPv6 loopback detection
- Handles various loopback representations
- Works with socket.getaddrinfo() results

#### `getipaddrinfo(host)`
Filters socket.getaddrinfo() results for valid IP addresses.

**Returns:** List of valid address info tuples

### HTTP Utilities

#### `unlocalised_http_header_date(data)`
Converts datetime to HTTP header format (RFC 7231).

**Features:**
- Locale-independent date formatting
- Latin1-encodable output for uWSGI compatibility
- Manual weekday/month name mapping

**Format:** "Sun, 06 Nov 1994 08:49:37 GMT"

## Security Considerations

### Cryptographic Strength
- Uses AES-256 in CBC mode with random IVs
- HMAC-SHA256 for authentication
- Secure random number generation with entropy seeding

### Backward Compatibility
- Maintains deprecated functions for existing data
- Automatic detection and handling of old formats
- Migration path from MD5 to SHA256 HMAC

### Side-Channel Protection
- Constant-time comparison functions
- Secure padding/unpadding operations
- Protection against timing attacks

## Dependencies

### Required Modules
- `hashlib`: Cryptographic hash functions
- `hmac`: Hash-based message authentication
- `base64`: Data encoding/decoding
- `struct`: Binary data packing
- `uuid`: UUID generation
- `socket`: Network address operations

### Optional Dependencies
- `Crypto.Cipher.AES`: Hardware-accelerated AES (preferred)
- `gluon.contrib.pyaes`: Pure Python AES fallback

## Error Handling

### Exception Management
- Graceful fallback for missing crypto libraries
- Silent failure for malformed data in secure_loads
- Comprehensive logging for security events

### Validation
- Input validation for all cryptographic operations
- Bounds checking for array operations
- Type checking for security-critical functions

## Performance Optimizations

### Bulk Operations
- Batch random number generation
- Efficient padding operations
- Optimized comparison functions

### Memory Management
- Minimal memory allocation in hot paths
- Proper cleanup of sensitive data
- Thread-safe operations with minimal locking

## Usage Examples

### Basic Encryption
```python
# Secure data storage
data = {"user_id": 123, "session_data": "sensitive"}
encrypted = secure_dumps(data, "encryption_key")
decrypted = secure_loads(encrypted, "encryption_key")
```

### UUID Generation
```python
# Generate unique identifiers
session_id = web2py_uuid()
request_id = web2py_uuid()
```

### IP Validation
```python
# Validate client addresses
if is_valid_ip_address(client_ip):
    if is_loopback_ip_address(client_ip):
        # Handle local connections
        pass
```

This module forms the security foundation of the web2py framework, providing essential cryptographic and validation utilities required for secure web application development.