# Gluon Contrib PBKDF2 Module

## Overview
Password-Based Key Derivation Function 2 (PBKDF2) implementation for secure password hashing. Provides a pure Python implementation using only standard library components, offering a secure alternative to bcrypt without requiring C extensions.

## Module Information
- **Module**: `gluon.contrib.pbkdf2`
- **Author**: Armin Ronacher
- **License**: BSD
- **Dependencies**: `hmac`, `hashlib`, `struct`, `operator`, `itertools`
- **Purpose**: Secure password hashing and key derivation

## Key Features
- **Secure Hashing**: PBKDF2 algorithm for password protection
- **Configurable Iterations**: Adjustable computational cost
- **Multiple Hash Functions**: Support for various hash algorithms
- **Pure Python**: No C extensions required
- **Constant Time Comparison**: Timing attack protection
- **Salt Support**: Proper salt handling for security

## Main Functions

### pbkdf2_hex()
Generate PBKDF2 hash in hexadecimal format.

**Signature:**
```python
def pbkdf2_hex(data, salt, iterations=1000, keylen=24, hashfunc=None)
```

**Parameters:**
- `data`: Password or data to hash (string)
- `salt`: Salt value (string or bytes)
- `iterations`: Number of iterations (default: 1000)
- `keylen`: Desired key length in bytes (default: 24)
- `hashfunc`: Hash function to use (default: hashlib.sha1)

**Returns:**
- Hexadecimal string representation of derived key

**Example:**
```python
from gluon.contrib.pbkdf2 import pbkdf2_hex

# Basic usage
hash_hex = pbkdf2_hex('password123', 'random_salt')
print(hash_hex)  # 'fa7cc8a2b0a932f8e6ea42f9787e9d36e592e0c222ada6a9'

# With custom parameters
hash_hex = pbkdf2_hex('password123', 'random_salt', 
                     iterations=10000, keylen=32)
```

### pbkdf2_bin()
Generate PBKDF2 hash in binary format.

**Signature:**
```python
def pbkdf2_bin(data, salt, iterations=1000, keylen=24, hashfunc=None)
```

**Parameters:**
- Same as `pbkdf2_hex()`

**Returns:**
- Binary string representation of derived key

**Example:**
```python
from gluon.contrib.pbkdf2 import pbkdf2_bin

# Binary output
hash_bin = pbkdf2_bin('password123', 'random_salt')
```

## Secure Implementation Patterns

### Constant Time Comparison
```python
def safe_str_cmp(a, b):
    """Constant time string comparison to prevent timing attacks"""
    if len(a) != len(b):
        return False
    rv = 0
    for x, y in zip(a, b):
        rv |= ord(x) ^ ord(y)
    return rv == 0

# Usage for password verification
stored_hash = 'fa7cc8a2b0a932f8e6ea42f9787e9d36e592e0c222ada6a9'
input_hash = pbkdf2_hex('user_password', 'stored_salt')

if safe_str_cmp(stored_hash, input_hash):
    print("Password correct")
else:
    print("Password incorrect")
```

### Secure Salt Generation
```python
import os

def generate_salt(length=16):
    """Generate cryptographically secure random salt"""
    return os.urandom(length)

# Usage
salt = generate_salt()
password_hash = pbkdf2_hex('user_password', salt, iterations=10000)
```

### Complete Password Storage System
```python
import os
import base64
from gluon.contrib.pbkdf2 import pbkdf2_hex

class SecurePassword:
    def __init__(self, iterations=10000, keylen=32, algorithm='PBKDF2-SHA1'):
        self.iterations = iterations
        self.keylen = keylen
        self.algorithm = algorithm
    
    def hash_password(self, password):
        """Hash password with random salt"""
        salt = os.urandom(16)
        hash_value = pbkdf2_hex(password, salt, self.iterations, self.keylen)
        
        # Store as: algorithm$salt:iterations$hash
        salt_b64 = base64.b64encode(salt).decode('ascii')
        return '%s$%s:%d$%s' % (self.algorithm, salt_b64, 
                               self.iterations, hash_value)
    
    def verify_password(self, password, stored_hash):
        """Verify password against stored hash"""
        try:
            algorithm, salt_iterations, hash_value = stored_hash.split('$')
            salt_b64, iterations = salt_iterations.split(':')
            
            salt = base64.b64decode(salt_b64.encode('ascii'))
            iterations = int(iterations)
            
            # Compute hash with same parameters
            computed_hash = pbkdf2_hex(password, salt, iterations, self.keylen)
            
            # Constant time comparison
            return safe_str_cmp(hash_value, computed_hash)
        except:
            return False

# Usage
pwd_manager = SecurePassword()

# Hash password
stored = pwd_manager.hash_password('user_password_123')
print(stored)  # 'PBKDF2-SHA1$cmFuZG9tc2FsdA==:10000$deadbeef...'

# Verify password
is_valid = pwd_manager.verify_password('user_password_123', stored)
print(is_valid)  # True
```

## Web2py Integration

### User Authentication System
```python
# In models/db.py
db.define_table('auth_user',
    Field('email', 'string', unique=True),
    Field('password_hash', 'string'),
    Field('first_name', 'string'),
    Field('last_name', 'string'),
    Field('created_on', 'datetime', default=request.now)
)

# In models/auth.py
from gluon.contrib.pbkdf2 import pbkdf2_hex
import os
import base64

class PasswordManager:
    @staticmethod
    def hash_password(password):
        """Hash password using PBKDF2"""
        salt = os.urandom(16)
        hash_value = pbkdf2_hex(password, salt, iterations=10000, keylen=32)
        salt_b64 = base64.b64encode(salt).decode('ascii')
        return 'PBKDF2$%s$%s' % (salt_b64, hash_value)
    
    @staticmethod
    def verify_password(password, stored_hash):
        """Verify password against stored hash"""
        try:
            parts = stored_hash.split('$')
            if len(parts) != 3 or parts[0] != 'PBKDF2':
                return False
            
            salt = base64.b64decode(parts[1].encode('ascii'))
            stored_value = parts[2]
            
            computed_hash = pbkdf2_hex(password, salt, iterations=10000, keylen=32)
            return safe_str_cmp(stored_value, computed_hash)
        except:
            return False

# Custom auth table
auth.define_tables(username=True, signature=False)
auth.settings.table_user = db.auth_user
auth.settings.password_field = 'password_hash'
```

### Registration Controller
```python
def register():
    """User registration with PBKDF2 password hashing"""
    form = FORM(
        INPUT(_name='email', _placeholder='Email', requires=IS_EMAIL()),
        INPUT(_name='password', _type='password', _placeholder='Password', 
              requires=IS_STRONG()),
        INPUT(_name='confirm', _type='password', _placeholder='Confirm Password'),
        INPUT(_name='first_name', _placeholder='First Name'),
        INPUT(_name='last_name', _placeholder='Last Name'),
        INPUT(_type='submit', _value='Register')
    )
    
    if form.process().accepted:
        # Verify password confirmation
        if request.vars.password != request.vars.confirm:
            form.errors.confirm = 'Passwords do not match'
        else:
            # Hash password
            password_hash = PasswordManager.hash_password(request.vars.password)
            
            # Create user
            user_id = db.auth_user.insert(
                email=request.vars.email,
                password_hash=password_hash,
                first_name=request.vars.first_name,
                last_name=request.vars.last_name
            )
            
            session.flash = 'Registration successful'
            redirect(URL('login'))
    
    return dict(form=form)

def login():
    """User login with PBKDF2 password verification"""
    form = FORM(
        INPUT(_name='email', _placeholder='Email'),
        INPUT(_name='password', _type='password', _placeholder='Password'),
        INPUT(_type='submit', _value='Login')
    )
    
    if form.process().accepted:
        user = db(db.auth_user.email == request.vars.email).select().first()
        
        if user and PasswordManager.verify_password(request.vars.password, 
                                                   user.password_hash):
            session.user_id = user.id
            session.flash = 'Login successful'
            redirect(URL('index'))
        else:
            form.errors.email = 'Invalid email or password'
    
    return dict(form=form)
```

### Password Change Functionality
```python
def change_password():
    """Change user password"""
    if not session.user_id:
        redirect(URL('login'))
    
    form = FORM(
        INPUT(_name='current_password', _type='password', 
              _placeholder='Current Password'),
        INPUT(_name='new_password', _type='password', 
              _placeholder='New Password', requires=IS_STRONG()),
        INPUT(_name='confirm_password', _type='password', 
              _placeholder='Confirm New Password'),
        INPUT(_type='submit', _value='Change Password')
    )
    
    if form.process().accepted:
        user = db.auth_user[session.user_id]
        
        # Verify current password
        if not PasswordManager.verify_password(request.vars.current_password,
                                             user.password_hash):
            form.errors.current_password = 'Incorrect current password'
        elif request.vars.new_password != request.vars.confirm_password:
            form.errors.confirm_password = 'Passwords do not match'
        else:
            # Update password
            new_hash = PasswordManager.hash_password(request.vars.new_password)
            user.update_record(password_hash=new_hash)
            
            session.flash = 'Password changed successfully'
            redirect(URL('index'))
    
    return dict(form=form)
```

## Security Configuration

### Iteration Count Guidelines
```python
# Choose iteration count based on security requirements
SECURITY_LEVELS = {
    'low': 1000,        # Fast, minimal security
    'medium': 10000,    # Balanced security/performance
    'high': 100000,     # High security, slower
    'critical': 1000000 # Maximum security, very slow
}

# Adaptive iteration count based on server capability
def calculate_iterations(target_time=0.1):
    """Calculate iterations for target computation time"""
    import time
    test_password = 'test_password'
    test_salt = os.urandom(16)
    
    iterations = 1000
    while True:
        start_time = time.time()
        pbkdf2_hex(test_password, test_salt, iterations)
        elapsed = time.time() - start_time
        
        if elapsed >= target_time:
            return iterations
        iterations *= 2
```

### Hash Function Selection
```python
import hashlib

# Different hash functions for different security levels
HASH_FUNCTIONS = {
    'sha1': hashlib.sha1,      # Fast, less secure
    'sha256': hashlib.sha256,  # Balanced
    'sha512': hashlib.sha512,  # Slower, more secure
}

def secure_pbkdf2(password, salt, hashfunc='sha256'):
    """PBKDF2 with configurable hash function"""
    hash_func = HASH_FUNCTIONS.get(hashfunc, hashlib.sha256)
    return pbkdf2_hex(password, salt, iterations=10000, 
                     keylen=32, hashfunc=hash_func)
```

## Performance Considerations

### Benchmarking
```python
import time

def benchmark_pbkdf2():
    """Benchmark PBKDF2 performance"""
    password = 'test_password'
    salt = os.urandom(16)
    
    iterations_list = [1000, 5000, 10000, 50000, 100000]
    
    for iterations in iterations_list:
        start_time = time.time()
        pbkdf2_hex(password, salt, iterations)
        elapsed = time.time() - start_time
        
        print("Iterations: %d, Time: %.3f seconds" % (iterations, elapsed))

# Run benchmark
benchmark_pbkdf2()
```

### Memory Usage
```python
def memory_efficient_pbkdf2(password, salt, iterations=10000):
    """Memory-efficient PBKDF2 for large-scale applications"""
    # Use smaller key length for reduced memory usage
    return pbkdf2_hex(password, salt, iterations, keylen=20)
```

## Testing

### Unit Tests
```python
def test_pbkdf2():
    """Test PBKDF2 implementation"""
    
    # Test basic functionality
    hash1 = pbkdf2_hex('password', 'salt')
    hash2 = pbkdf2_hex('password', 'salt')
    assert hash1 == hash2, "Same input should produce same output"
    
    # Test different salts
    hash3 = pbkdf2_hex('password', 'different_salt')
    assert hash1 != hash3, "Different salts should produce different outputs"
    
    # Test different passwords
    hash4 = pbkdf2_hex('different_password', 'salt')
    assert hash1 != hash4, "Different passwords should produce different outputs"
    
    # Test iteration sensitivity
    hash5 = pbkdf2_hex('password', 'salt', iterations=2000)
    assert hash1 != hash5, "Different iterations should produce different outputs"
    
    print("All PBKDF2 tests passed!")

# Run tests
test_pbkdf2()
```

This module provides robust password hashing capabilities for web2py applications, offering strong security without external dependencies while maintaining compatibility across different Python environments.