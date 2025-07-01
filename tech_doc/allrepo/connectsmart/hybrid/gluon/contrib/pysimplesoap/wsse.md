# PySimpleSOAP WS-Security Extensions Module

## Overview
This module implements Web Services Security (WS-Security) extensions for SOAP messages, providing authentication, message integrity, and security token management capabilities.

## Key Features

### Username Token Authentication
```python
class UsernameToken:
    """
    WS-Security Username Token implementation
    
    Features:
    - Plain text passwords
    - Password digest authentication
    - Nonce generation for replay protection
    - Timestamp-based token expiration
    """
```

### Security Namespaces
```python
# WS-Security specification namespaces
WSSE_URI = 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd'
WSU_URI = "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
XMLDSIG_URI = "http://www.w3.org/2000/09/xmldsig#"
X509v3_URI = "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3"
Base64Binary_URI = "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary"
PasswordDigest_URI = "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest"
```

### Cryptographic Utilities
```python
def randombytes(N):
    """Generate cryptographically secure random bytes for nonce generation"""
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits
    ) for _ in range(N))
```

### Authentication Methods

#### Plain Text Authentication
- **Username/Password**: Basic credential transmission
- **Timestamp Support**: Token lifetime management
- **Nonce Integration**: Replay attack prevention

#### Password Digest Authentication
- **SHA-1 Hashing**: Secure password transmission
- **Salt Generation**: Random nonce for each request
- **Timestamp Validation**: Token freshness verification

### Security Token Types

#### Username Tokens
- **Plain Text**: Direct password transmission
- **Digest**: Hashed password with nonce and timestamp
- **Binary Tokens**: Certificate-based authentication

#### X.509 Certificates
- **Certificate Embedding**: Direct certificate inclusion
- **Certificate References**: Indirect certificate referencing
- **Certificate Validation**: Trust chain verification

### Message Security

#### Digital Signatures
- **XML Digital Signatures**: Message integrity protection
- **Canonical XML**: Standardized XML representation
- **Signature Verification**: Message authenticity validation

#### Encryption Support
- **Message Encryption**: Confidentiality protection
- **Key Management**: Symmetric and asymmetric keys
- **Algorithm Selection**: Configurable encryption methods

### Integration with SOAP Headers

#### Security Header Creation
```python
# Example security header structure
security_header = {
    'Security': {
        '@xmlns:wsse': WSSE_URI,
        '@xmlns:wsu': WSU_URI,
        'UsernameToken': {
            '@wsu:Id': 'UsernameToken-1',
            'Username': username,
            'Password': {
                '@Type': PasswordDigest_URI,
                '#text': password_digest
            },
            'Nonce': {
                '@EncodingType': Base64Binary_URI,
                '#text': encoded_nonce
            },
            'Created': timestamp
        }
    }
}
```

### Timestamp Management

#### Token Lifetime
- **Creation Time**: Token generation timestamp
- **Expiration Time**: Token validity period
- **Timezone Handling**: UTC timestamp standardization

#### Replay Protection
- **Nonce Generation**: Unique request identifiers
- **Timestamp Validation**: Freshness verification
- **Token Caching**: Replay detection mechanisms

### Security Standards Compliance

#### OASIS WS-Security
- **Version 1.0**: Full specification compliance
- **Token Profiles**: Username, X.509, SAML tokens
- **Message Protection**: Signature and encryption

#### XML Security Standards
- **XML Digital Signature**: W3C specification compliance
- **XML Encryption**: Confidentiality protection
- **Canonical XML**: Standardized XML processing

### Error Handling and Security

#### Security Validation
- **Token Format Validation**: Proper token structure
- **Timestamp Verification**: Token freshness checks
- **Certificate Validation**: Trust chain verification

#### Error Management
- **Security Faults**: WS-Security specific error handling
- **Authentication Failures**: Invalid credential handling
- **Authorization Errors**: Access control violations

This module provides comprehensive WS-Security implementation for enterprise-grade SOAP web service security requirements.