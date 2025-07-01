# Gluon Digest Module Technical Documentation

## Module: `digest.py`

### Overview
The `digest` module provides cryptographic hashing utilities for the Gluon web framework, specifically designed for security operations including password hashing, HMAC generation, and PBKDF2 implementation. It supports multiple hashing algorithms and provides a unified interface for digest operations.

### Table of Contents
1. [Dependencies](#dependencies)
2. [Constants](#constants)
3. [Functions](#functions)
4. [Supported Algorithms](#supported-algorithms)
5. [Usage Examples](#usage-examples)
6. [Security Best Practices](#security-best-practices)

### Dependencies
```python
import hashlib
import hmac
from gluon._compat import PY2, basestring, pickle, to_bytes, to_native, xrange
```

### Constants

#### `DIGEST_ALG_BY_SIZE`
Maps digest sizes (in bytes) to algorithm names:
```python
DIGEST_ALG_BY_SIZE = {
    128 // 4: "md5",      # 32 hex chars = 16 bytes
    160 // 4: "sha1",     # 40 hex chars = 20 bytes
    224 // 4: "sha224",   # 56 hex chars = 28 bytes
    256 // 4: "sha256",   # 64 hex chars = 32 bytes
    384 // 4: "sha384",   # 96 hex chars = 48 bytes
    512 // 4: "sha512",   # 128 hex chars = 64 bytes
}
```

### Functions

#### `pbkdf2_hex(data, salt, iterations=1000, keylen=24, hashfunc=None)`
Implements PBKDF2 (Password-Based Key Derivation Function 2) with hexadecimal output.

**Parameters:**
- `data` (str/bytes): Input data (typically password)
- `salt` (str/bytes): Salt value for key derivation
- `iterations` (int): Number of iterations (default: 1000)
- `keylen` (int): Desired key length in bytes (default: 24)
- `hashfunc` (callable): Hash function to use (default: sha1)

**Returns:**
- `str`: Hexadecimal string of derived key

**Example:**
```python
# Generate a secure key from password
password = "user_password"
salt = "random_salt_value"
key = pbkdf2_hex(password, salt, iterations=10000, keylen=32)
print(f"Derived key: {key}")
```

#### `simple_hash(text, key="", salt="", digest_alg="md5")`
Generates hash with the given text using the specified digest algorithm.

**Parameters:**
- `text` (str/bytes): Text to hash
- `key` (str/bytes): Optional key for HMAC (default: "")
- `salt` (str/bytes): Optional salt to append (default: "")
- `digest_alg` (str/callable): Algorithm name or callable (default: "md5")

**Returns:**
- `str`: Hexadecimal digest string

**Supported Formats:**
1. **Simple Hash**: `digest_alg` only
2. **HMAC**: With `key` parameter
3. **PBKDF2**: Format "pbkdf2(iterations,keylen,algorithm)"
4. **Custom**: Callable digest algorithm

**Examples:**
```python
# Simple MD5 hash
hash1 = simple_hash("hello world")

# SHA256 with salt
hash2 = simple_hash("password", salt="mysalt", digest_alg="sha256")

# HMAC-SHA256
hash3 = simple_hash("message", key="secret", digest_alg="sha256")

# PBKDF2 with SHA256
hash4 = simple_hash("password", salt="salt", digest_alg="pbkdf2(10000,32,sha256)")
```

#### `get_digest(value)`
Returns a hashlib digest algorithm from a string name.

**Parameters:**
- `value` (str/callable): Algorithm name or callable

**Returns:**
- `callable`: Hashlib digest algorithm

**Raises:**
- `ValueError`: If algorithm name is invalid

**Supported Algorithms:**
- `"md5"`
- `"sha1"`
- `"sha224"`
- `"sha256"`
- `"sha384"`
- `"sha512"`

**Example:**
```python
# Get SHA256 algorithm
sha256_func = get_digest("sha256")
hash_obj = sha256_func()
hash_obj.update(b"data")
print(hash_obj.hexdigest())
```

### Supported Algorithms

#### Standard Hash Algorithms
| Algorithm | Digest Size | Security Level |
|-----------|-------------|----------------|
| MD5       | 128 bits    | ⚠️ Deprecated  |
| SHA1      | 160 bits    | ⚠️ Weak        |
| SHA224    | 224 bits    | ✓ Moderate     |
| SHA256    | 256 bits    | ✓ Strong       |
| SHA384    | 384 bits    | ✓ Very Strong  |
| SHA512    | 512 bits    | ✓ Very Strong  |

#### PBKDF2 Configuration
Format: `pbkdf2(iterations,keylen,algorithm)`
- `iterations`: Number of rounds (minimum 1000, recommend 10000+)
- `keylen`: Output key length in bytes
- `algorithm`: Base hash algorithm (sha1, sha256, etc.)

### Usage Examples

#### Password Hashing
```python
def hash_password(password, salt=None):
    """Secure password hashing using PBKDF2"""
    if salt is None:
        import os
        salt = os.urandom(16).hex()
    
    # Use PBKDF2 with SHA256, 10000 iterations
    hashed = simple_hash(
        password,
        salt=salt,
        digest_alg="pbkdf2(10000,32,sha256)"
    )
    return f"{salt}${hashed}"

def verify_password(password, stored_hash):
    """Verify password against stored hash"""
    salt, hash_value = stored_hash.split('$')
    test_hash = simple_hash(
        password,
        salt=salt,
        digest_alg="pbkdf2(10000,32,sha256)"
    )
    return test_hash == hash_value
```

#### HMAC Authentication
```python
def create_api_signature(message, secret_key):
    """Create HMAC signature for API authentication"""
    return simple_hash(
        message,
        key=secret_key,
        digest_alg="sha256"
    )

def verify_api_signature(message, signature, secret_key):
    """Verify API message signature"""
    expected = create_api_signature(message, secret_key)
    # Use constant-time comparison
    return hmac.compare_digest(expected, signature)
```

#### File Integrity Checking
```python
def calculate_file_hash(filename, algorithm="sha256"):
    """Calculate hash of a file"""
    hash_func = get_digest(algorithm)()
    
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

# Usage
file_hash = calculate_file_hash("document.pdf", "sha256")
print(f"SHA256: {file_hash}")
```

#### Token Generation
```python
def generate_secure_token(user_id, timestamp):
    """Generate secure token for session/CSRF"""
    import time
    
    data = f"{user_id}:{timestamp}:{time.time()}"
    secret = "application_secret_key"
    
    return simple_hash(
        data,
        key=secret,
        salt=str(timestamp),
        digest_alg="sha256"
    )
```

### Security Best Practices

#### Password Storage
```python
# DO: Use PBKDF2 with high iterations
password_hash = simple_hash(
    password,
    salt=generate_salt(),
    digest_alg="pbkdf2(100000,32,sha256)"
)

# DON'T: Use simple hashes
bad_hash = simple_hash(password, digest_alg="md5")  # Insecure!
```

#### Salt Generation
```python
import os

def generate_salt(length=16):
    """Generate cryptographically secure salt"""
    return os.urandom(length).hex()

# Always use unique salts
salt = generate_salt()
```

#### Algorithm Selection
1. **Passwords**: Use PBKDF2 with SHA256+ and 10,000+ iterations
2. **HMAC**: Use SHA256 or stronger
3. **Checksums**: SHA256 for security, MD5 only for non-security
4. **Tokens**: Use HMAC-SHA256 with proper key management

### Error Handling

```python
def safe_hash(text, **kwargs):
    """Hash with comprehensive error handling"""
    try:
        # Validate algorithm
        alg = kwargs.get('digest_alg', 'sha256')
        if alg and not alg.startswith('pbkdf2'):
            get_digest(alg)  # Validates algorithm
        
        # Perform hashing
        return simple_hash(text, **kwargs)
    
    except ValueError as e:
        # Invalid algorithm
        raise ValueError(f"Invalid hash algorithm: {e}")
    
    except Exception as e:
        # Other errors
        raise RuntimeError(f"Hashing failed: {e}")
```

### Performance Considerations

#### Iteration Count Tuning
```python
def tune_pbkdf2_iterations(target_time=0.1):
    """Find iterations for target computation time"""
    import time
    
    test_password = "test_password"
    test_salt = "test_salt"
    iterations = 1000
    
    while True:
        start = time.time()
        pbkdf2_hex(test_password, test_salt, iterations=iterations)
        duration = time.time() - start
        
        if duration >= target_time:
            break
        
        iterations = int(iterations * (target_time / duration) * 1.2)
    
    return iterations
```

### Integration Examples

#### With Gluon Auth
```python
from gluon.tools import Auth

# Configure Auth to use PBKDF2
auth.settings.hmac_key = 'your-secret-key'
auth.settings.password_hash = lambda password: simple_hash(
    password,
    salt=auth.settings.hmac_key,
    digest_alg="pbkdf2(20000,32,sha512)"
)
```

#### Custom Validator
```python
from gluon.validators import Validator

class IS_STRONG_HASH(Validator):
    """Validate and create strong password hashes"""
    
    def __init__(self, iterations=10000, keylen=32):
        self.iterations = iterations
        self.keylen = keylen
    
    def __call__(self, value):
        salt = generate_salt()
        hashed = simple_hash(
            value,
            salt=salt,
            digest_alg=f"pbkdf2({self.iterations},{self.keylen},sha256)"
        )
        return (f"{salt}${hashed}", None)
```

### Migration Guide

#### Upgrading Hash Algorithms
```python
def upgrade_password_hash(user_id, password, old_hash):
    """Upgrade from old to new hash algorithm"""
    # Verify with old algorithm
    if verify_old_hash(password, old_hash):
        # Create new hash
        new_hash = hash_password(password)
        # Update database
        update_user_password(user_id, new_hash)
        return True
    return False
```

### Module Metadata

- **License**: LGPLv3
- **Part of**: web2py Web Framework
- **Thread Safety**: Yes
- **Cryptographic**: Yes
- **Python**: 2.7+, 3.x compatible