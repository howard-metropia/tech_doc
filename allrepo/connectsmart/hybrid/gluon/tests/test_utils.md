# test_utils.py

## Overview
Unit tests for the utilities module in Web2py, covering cryptographic functions, string comparison, padding, secure serialization, and IP address validation.

## Imports
```python
import pickle
import unittest
from hashlib import md5
import gluon.utils
from gluon.utils import (compare, is_valid_ip_address, md5_hash, secure_dumps,
                         secure_loads, web2py_uuid)
from gluon.validators import get_digest, simple_hash
```

## Test Class: TestUtils

### String Comparison

#### test_compare()
Tests timing-safe string comparison to prevent timing attacks.

**Test Cases:**
- **Equal strings**: `compare("test123", "test123")` → `True`
- **Different strings**: `compare("test123", "test456")` → `False`
- **Type mismatch**: `compare("test123", ["test123", "test123"])` → `False`
- **String vs number**: `compare("123", 123)` → `False`

**Purpose:** The compare function provides constant-time string comparison to prevent timing-based cryptographic attacks.

### Hashing Functions

#### test_md5_hash()
Tests MD5 hash generation.
- Input: `"web2py rocks"`
- Expected output: `"79509f3246a2824dee64635303e99204"`

#### test_simple_hash()
Comprehensive testing of the `simple_hash` function with various algorithms.

**Test Cases:**

1. **Error Handling**: No algorithm specified raises `RuntimeError`

2. **MD5 Hashing**:
   - With md5 object: `simple_hash("web2py rocks!", digest_alg=md5)`
   - With string: `simple_hash("web2py rocks!", digest_alg="md5")`
   - Expected: `"37d95defba6c8834cb8cae86ee888568"`

3. **SHA Family Algorithms**:
   - **SHA1**: `"00489a46753d8db260c71542611cdef80652c4b7"`
   - **SHA224**: `"84d7054271842c2c17983baa2b1447e0289d101140a8c002d49d60da"`
   - **SHA256**: `"0849f224d8deb267e4598702aaec1bd749e6caec90832469891012a4be24af08"`
   - **SHA384**: `"3cffaf39371adbe84eb10f588d2718207d8e965e9172a27a278321b86977351376ae79f92e91d8c58cad86c491282d5f"`
   - **SHA512**: `"fa3237f594743e1d7b6c800bb134b3255cf4a98ab8b01e2ec23256328c9f8059964fdef25a038d6cc3fda1b2fb45d66461eeed5c4669e506ec8bdfee71348db7e"`

#### test_get_digest()
Tests digest algorithm validation.
- Invalid algorithm (`"123"`) raises `ValueError`

### Padding Functions

#### test_pad()
Tests padding and unpadding for cryptographic operations.

**Test Cases:**
```python
test_cases = [
    (16, b"mydata"),      # Basic padding
    (32, b"mydata "),     # Preserve trailing spaces
    (8, b"mydata\x01"),   # Handle existing padding bytes
    (4, b"mydata"),       # Multi-block behavior
    (2, b""),             # Empty string
]
```

**Validations:**
- Padded length is greater than original
- Padded length is multiple of block size
- Unpadding returns original data exactly

**Complex Object Test:**
- Pickles dictionary, pads result, unpads, unpickles
- Verifies data integrity through full cycle
- Tests default 32-byte block size

### Secure Serialization

#### test_secure_dumps_and_loads()
Tests secure object serialization with encryption and authentication.

**Basic Functionality:**
```python
testobj = {"a": 1, "b": 2}
testkey = "mysecret"
secured = secure_dumps(testobj, testkey)
original = secure_loads(secured, testkey)
```

**Validations:**
- Round-trip integrity (object → secured → object)
- Output is bytes with 2 colons (format validation)
- Backward compatibility with deprecated format (1 colon)

**Compression Testing:**
- Large object (1000 integers) with compression
- Compressed output is smaller than uncompressed
- Compression level parameter support

**Security Testing:**
- Custom hash parameter
- Wrong key returns `None`
- Wrong hash returns `None`
- Invalid data returns `None`

### UUID Generation

#### test_web2py_uuid()
Tests UUID generation.
- Generates UUID using `web2py_uuid()`
- Validates format using Python's UUID parser

### IP Address Validation

#### test_is_valid_ip_address()
Comprehensive IP address validation testing.

**IPv4 Testing:**
- **Valid**: `"127.0.0.1"`, `"localhost"`
- **Invalid**: `"unknown"`, `""` (empty string)

**IPv6 Testing:**
- **Loopback**: `"::1"`
- **Compressed formats**: `"::ffff:7f00:1"`, `"2001:660::1"`
- **Expanded formats**: `"0:0:0:0:0:ffff:7f00:1"`
- **Full addresses**: `"2607:fa48:6d50:69f1:21f:3cff:fe9d:9be3"`

**Note**: Some edge cases commented out due to platform-specific behavior on AppVeyor CI.

## Key Utility Functions

### Security Functions
- **compare()**: Timing-safe string comparison
- **secure_dumps/loads()**: Authenticated encryption
- **pad/unpad()**: Cryptographic padding

### Hashing Functions
- **md5_hash()**: MD5 digest
- **simple_hash()**: Multi-algorithm hashing
- **get_digest()**: Hash algorithm validation

### Network Functions
- **is_valid_ip_address()**: IPv4/IPv6 validation
- **web2py_uuid()**: Unique identifier generation

## Testing Patterns

### Cryptographic Testing
- Fixed test vectors for hash validation
- Round-trip testing for encryption
- Error condition testing

### Security Testing
- Invalid input handling
- Wrong key/hash detection
- Timing attack prevention

### Cross-Platform Testing
- Platform-specific IP validation differences
- CI environment considerations

## TODO Items
The file notes several functions that need test coverage:
- `test_AES_new()`
- `test_get_callable_argspec()`
- `test_initialize_urandom()`
- `test_fast_urandom16()`
- `test_is_loopback_ip_address()`
- `test_getipaddrinfo()`

## Notes
- Tests focus on security-critical functions
- Comprehensive hash algorithm coverage
- Platform-aware testing for network functions
- Backward compatibility validation for serialization
- Strong emphasis on cryptographic correctness