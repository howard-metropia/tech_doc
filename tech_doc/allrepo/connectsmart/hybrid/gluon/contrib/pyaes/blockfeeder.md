# PyAES Block Feeder Module

**File**: `gluon/contrib/pyaes/blockfeeder.py`  
**Type**: Stream Processing and Padding Module  
**Framework**: Web2py Gluon Framework  
**License**: MIT License

## Overview

This module provides stream-oriented encryption and decryption capabilities for PyAES, allowing processing of data that doesn't fit neatly into 16-byte AES blocks. It handles padding, stream processing, and provides convenient high-level interfaces for encrypting/decrypting data of arbitrary length.

## Core Components

### Padding Constants
```python
PADDING_NONE = 'none'        # No padding applied
PADDING_DEFAULT = 'default'  # PKCS#7 padding (recommended)
```

### Stream Classes

**Encrypter Class**
- Handles incremental encryption of data streams
- Automatically manages padding for final blocks
- Buffers incomplete blocks until sufficient data available

**Decrypter Class**  
- Handles incremental decryption of data streams
- Automatically strips padding from final blocks
- Manages block boundaries during stream processing

## Key Features

### Stream Processing
- **Incremental Processing**: Handle data in chunks of any size
- **Memory Efficient**: Process large files without loading entirely into memory
- **Automatic Buffering**: Internal buffering for incomplete blocks
- **Padding Management**: Automatic PKCS#7 padding and removal

### Padding Support
- **PKCS#7 Padding**: Industry-standard padding scheme
- **Automatic Application**: Applied during encryption finalization
- **Automatic Removal**: Stripped during decryption finalization
- **None Option**: For pre-padded data or stream ciphers

## Usage Examples

### Stream Encryption
```python
from gluon.contrib import pyaes

# Setup
key = b"This_key_for_demo_purposes_only!"  # 32-byte key
plaintext = b"This is a long message that spans multiple AES blocks and needs to be encrypted in streaming fashion."

# Create stream encrypter (CTR mode)
counter = pyaes.Counter()
mode = pyaes.AESModeOfOperationCTR(key, counter=counter)
encrypter = pyaes.Encrypter(mode)

# Encrypt in chunks
ciphertext = b''
chunk_size = 64  # Process 64 bytes at a time

for i in range(0, len(plaintext), chunk_size):
    chunk = plaintext[i:i+chunk_size]
    ciphertext += encrypter.feed(chunk)

# Finalize encryption (important!)
ciphertext += encrypter.feed()  # Final call with no arguments
```

### Stream Decryption
```python
# Create stream decrypter (same mode and key)
counter = pyaes.Counter()  # Reset counter for decryption
mode = pyaes.AESModeOfOperationCTR(key, counter=counter) 
decrypter = pyaes.Decrypter(mode)

# Decrypt in chunks
decrypted = b''
chunk_size = 64

for i in range(0, len(ciphertext), chunk_size):
    chunk = ciphertext[i:i+chunk_size]
    decrypted += decrypter.feed(chunk)

# Finalize decryption
decrypted += decrypter.feed()  # Final call
```

### File Encryption Example
```python
def encrypt_file_stream(input_file_path, output_file_path, key):
    from gluon.contrib import pyaes
    import os
    
    # Generate random IV for CBC mode
    iv = os.urandom(16)
    mode = pyaes.AESModeOfOperationCBC(key, iv=iv)
    encrypter = pyaes.Encrypter(mode, padding=pyaes.PADDING_DEFAULT)
    
    with open(input_file_path, 'rb') as infile, \
         open(output_file_path, 'wb') as outfile:
        
        # Write IV to beginning of encrypted file
        outfile.write(iv)
        
        # Encrypt file in chunks
        while True:
            chunk = infile.read(8192)  # 8KB chunks
            if not chunk:
                break
                
            encrypted_chunk = encrypter.feed(chunk)
            if encrypted_chunk:
                outfile.write(encrypted_chunk)
        
        # Finalize and write last block
        final_chunk = encrypter.feed()
        if final_chunk:
            outfile.write(final_chunk)
```

### File Decryption Example
```python
def decrypt_file_stream(input_file_path, output_file_path, key):
    from gluon.contrib import pyaes
    
    with open(input_file_path, 'rb') as infile, \
         open(output_file_path, 'wb') as outfile:
        
        # Read IV from beginning of file
        iv = infile.read(16)
        mode = pyaes.AESModeOfOperationCBC(key, iv=iv)
        decrypter = pyaes.Decrypter(mode, padding=pyaes.PADDING_DEFAULT)
        
        # Decrypt file in chunks
        while True:
            chunk = infile.read(8192)  # 8KB chunks
            if not chunk:
                break
                
            decrypted_chunk = decrypter.feed(chunk)
            if decrypted_chunk:
                outfile.write(decrypted_chunk)
        
        # Finalize and write last block
        final_chunk = decrypter.feed()
        if final_chunk:
            outfile.write(final_chunk)
```

## High-Level Functions

### encrypt_stream()
```python
def encrypt_stream(mode, data, padding=PADDING_DEFAULT):
    # Convenience function for one-shot stream encryption
    encrypter = Encrypter(mode, padding=padding)
    ciphertext = encrypter.feed(data)
    ciphertext += encrypter.feed()  # Finalize
    return ciphertext
```

### decrypt_stream()
```python
def decrypt_stream(mode, data, padding=PADDING_DEFAULT):
    # Convenience function for one-shot stream decryption  
    decrypter = Decrypter(mode, padding=padding)
    plaintext = decrypter.feed(data)
    plaintext += decrypter.feed()  # Finalize
    return plaintext
```

## Padding Implementation

### PKCS#7 Padding
The default padding scheme adds bytes to make data multiple of block size:

```python
# Padding bytes = (16 - (data_length % 16))
# Each padding byte contains the padding length value

# Example: "Hello" (5 bytes) -> "Hello\x0b\x0b\x0b...\x0b" (16 bytes)
# 11 padding bytes, each with value 0x0b (11 in hex)
```

### Padding in Practice
```python
from gluon.contrib.pyaes.util import append_PKCS7_padding, strip_PKCS7_padding

# Add padding
data = b"Hello World"
padded = append_PKCS7_padding(data)
print(len(padded))  # 16 (next multiple of 16)

# Remove padding  
unpadded = strip_PKCS7_padding(padded)
print(unpadded)  # b"Hello World"
```

## Integration with Web2py

### Large File Upload Encryption
```python
def handle_encrypted_upload():
    from gluon.contrib import pyaes
    import os
    
    upload = request.vars.file
    if not upload:
        return dict(error="No file uploaded")
    
    # Generate encryption key (in practice, use proper key management)
    key = hashlib.sha256(session.user_id.encode()).digest()[:32]
    
    # Setup stream encryption
    iv = os.urandom(16)
    mode = pyaes.AESModeOfOperationCBC(key, iv=iv)
    encrypter = pyaes.Encrypter(mode)
    
    # Save encrypted file
    encrypted_filename = f"encrypted_{upload.filename}"
    filepath = os.path.join(request.folder, 'uploads', encrypted_filename)
    
    with open(filepath, 'wb') as outfile:
        outfile.write(iv)  # Store IV at beginning
        
        # Process upload in chunks
        while True:
            chunk = upload.file.read(8192)
            if not chunk:
                break
            encrypted = encrypter.feed(chunk)
            if encrypted:
                outfile.write(encrypted)
        
        # Finalize
        final = encrypter.feed()
        if final:
            outfile.write(final)
    
    return dict(message="File encrypted and saved", filename=encrypted_filename)
```

### Database BLOB Encryption
```python
def encrypt_blob_field(data, table_name, record_id):
    from gluon.contrib import pyaes
    import hashlib
    
    # Derive key from table and record (use proper key management in production)
    key_material = f"{table_name}_{record_id}_{current.app.config.secret_key}"
    key = hashlib.sha256(key_material.encode()).digest()[:32]
    
    # Encrypt using stream interface
    counter = pyaes.Counter()
    mode = pyaes.AESModeOfOperationCTR(key, counter=counter)
    
    encrypted = pyaes.encrypt_stream(mode, data)
    return encrypted

def decrypt_blob_field(encrypted_data, table_name, record_id):
    from gluon.contrib import pyaes
    import hashlib
    
    # Same key derivation
    key_material = f"{table_name}_{record_id}_{current.app.config.secret_key}"
    key = hashlib.sha256(key_material.encode()).digest()[:32]
    
    # Decrypt using stream interface
    counter = pyaes.Counter()
    mode = pyaes.AESModeOfOperationCTR(key, counter=counter)
    
    decrypted = pyaes.decrypt_stream(mode, encrypted_data)
    return decrypted
```

## Performance Considerations

### Memory Management
- **Streaming**: Processes data incrementally, not all at once
- **Buffering**: Internal buffers are small (typically one block)
- **Chunk Size**: Larger chunks = better performance, more memory usage

### Optimal Chunk Sizes
```python
# Good chunk sizes for different scenarios:
CHUNK_SIZE_SMALL = 1024      # 1KB - low memory usage
CHUNK_SIZE_MEDIUM = 8192     # 8KB - balanced performance
CHUNK_SIZE_LARGE = 65536     # 64KB - high performance
CHUNK_SIZE_MEMORY = 1048576  # 1MB - maximum performance
```

## Error Handling

### Common Issues
```python
def safe_stream_encrypt(data, key, mode_type='CBC'):
    try:
        from gluon.contrib import pyaes
        
        if mode_type == 'CBC':
            iv = os.urandom(16)
            mode = pyaes.AESModeOfOperationCBC(key, iv=iv)
            result_prefix = iv  # Include IV in result
        elif mode_type == 'CTR':
            mode = pyaes.AESModeOfOperationCTR(key, pyaes.Counter())
            result_prefix = b''
        else:
            raise ValueError(f"Unsupported mode: {mode_type}")
        
        encrypted = pyaes.encrypt_stream(mode, data)
        return result_prefix + encrypted
        
    except Exception as e:
        logger.error(f"Stream encryption failed: {str(e)}")
        raise
```

## Best Practices

### Stream Processing Guidelines
1. **Always finalize**: Call `feed()` with no arguments to complete processing
2. **Handle empty chunks**: Check for empty return values during processing
3. **Buffer management**: Don't assume immediate output for small inputs
4. **Error handling**: Wrap stream operations in try-catch blocks

### Security Considerations
1. **IV management**: Use unique IVs for each encryption operation
2. **Key derivation**: Use proper key derivation functions
3. **Padding oracles**: Be careful with padding error messages
4. **Memory cleanup**: Clear sensitive data from memory when possible

This module provides the essential streaming capabilities needed for practical encryption of large or arbitrary-sized data in Web2py applications, with careful attention to both performance and security requirements.