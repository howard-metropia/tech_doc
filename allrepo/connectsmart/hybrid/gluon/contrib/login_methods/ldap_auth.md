# gluon/contrib/login_methods/ldap_auth.py

## Overview

The ldap_auth.py module provides comprehensive LDAP (Lightweight Directory Access Protocol) authentication integration for Web2py applications. This module supports authentication against LDAP servers including Microsoft Active Directory, OpenLDAP, and other directory services, with advanced features like group management, SSL/TLS support, and user profile synchronization.

## Key Components

### Main Function: ldap_auth()
```python
def ldap_auth(server='ldap',
              port=None,
              base_dn='ou=users,dc=domain,dc=com',
              mode='uid',
              secure=False,
              self_signed_certificate=None,
              cert_path=None,
              cert_file=None,
              cacert_path=None,
              cacert_file=None,
              key_file=None,
              bind_dn=None,
              bind_pw=None,
              filterstr='objectClass=*',
              username_attrib='uid',
              custom_scope='subtree',
              allowed_groups=None,
              manage_user=False,
              user_firstname_attrib='cn:1',
              user_lastname_attrib='cn:2',
              user_mail_attrib='mail',
              manage_groups=False,
              manage_groups_callback=[],
              db=None,
              group_dn=None,
              group_name_attrib='cn',
              group_member_attrib='memberUid',
              group_filterstr='objectClass=*',
              group_mapping={},
              tls=False,
              logging_level='error'):
```

### Dependencies
```python
import sys
import logging
import ldap
import ldap.filter

# Configure LDAP options
ldap.set_option(ldap.OPT_REFERRALS, 0)
```

## Configuration Parameters

### Server Connection
- **server**: LDAP server hostname or IP
- **port**: LDAP port (389 for LDAP, 636 for LDAPS)
- **secure**: Enable LDAPS (SSL/TLS)
- **tls**: Use StartTLS for secure connection

### Authentication Settings
- **base_dn**: Base Distinguished Name for user searches
- **mode**: Authentication mode ('uid', 'cn', 'mail', etc.)
- **bind_dn**: DN for binding to LDAP server
- **bind_pw**: Password for binding account
- **filterstr**: Additional LDAP filter for user searches

### SSL/TLS Configuration
- **cert_path**: Path to client certificate directory
- **cert_file**: Client certificate file
- **cacert_path**: CA certificate directory path
- **cacert_file**: CA certificate file
- **key_file**: Private key file
- **self_signed_certificate**: Path to self-signed certificate

## Authentication Modes

### User ID Mode (uid)
```python
# Authentication using uid attribute
ldap_auth(mode='uid', 
          base_dn='ou=users,dc=company,dc=com',
          username_attrib='uid')
```

### Email Mode
```python
# Authentication using email address
ldap_auth(mode='mail',
          base_dn='ou=users,dc=company,dc=com', 
          username_attrib='mail')
```

### Active Directory Mode
```python
# Active Directory authentication
ldap_auth(server='ad.company.com',
          mode='domainname\\',
          base_dn='OU=Users,DC=company,DC=com',
          filterstr='objectClass=person')
```

## User Management Features

### Automatic User Creation
```python
def ldap_auth_with_user_management():
    return ldap_auth(
        server='ldap.company.com',
        manage_user=True,
        user_firstname_attrib='givenName',
        user_lastname_attrib='sn',
        user_mail_attrib='mail',
        db=db  # Web2py database instance
    )
```

### User Profile Synchronization
```python
def sync_user_profile(ldap_user_data, web2py_user):
    """Synchronize LDAP user data with Web2py user profile"""
    # Update user fields from LDAP
    web2py_user.first_name = ldap_user_data.get('givenName', [''])[0]
    web2py_user.last_name = ldap_user_data.get('sn', [''])[0]
    web2py_user.email = ldap_user_data.get('mail', [''])[0]
    
    # Custom attribute mapping
    if 'department' in ldap_user_data:
        web2py_user.department = ldap_user_data['department'][0]
```

## Group Management

### Group Authorization
```python
# Restrict access to specific LDAP groups
ldap_auth(server='ldap.company.com',
          allowed_groups=['web2py_users', 'developers'],
          group_dn='ou=groups,dc=company,dc=com',
          group_name_attrib='cn',
          group_member_attrib='memberUid')
```

### Group Synchronization
```python
def ldap_auth_with_groups():
    return ldap_auth(
        server='ldap.company.com',
        manage_groups=True,
        group_dn='ou=groups,dc=company,dc=com',
        group_mapping={
            'web2py_admins': 'administrators',
            'web2py_users': 'users',
            'developers': 'developers'
        },
        manage_groups_callback=[update_user_roles]
    )

def update_user_roles(user_id, groups):
    """Callback to update user roles based on LDAP groups"""
    for group in groups:
        if group == 'administrators':
            auth.add_membership('admin', user_id)
        elif group == 'developers':
            auth.add_membership('developer', user_id)
```

## SSL/TLS Security

### LDAPS Configuration
```python
# Secure LDAP over SSL
ldap_auth(server='ldaps.company.com',
          port=636,
          secure=True,
          cacert_file='/path/to/ca-cert.pem')
```

### StartTLS Configuration
```python
# LDAP with StartTLS
ldap_auth(server='ldap.company.com',
          port=389,
          tls=True,
          cert_file='/path/to/client-cert.pem',
          key_file='/path/to/client-key.pem')
```

### Certificate Validation
```python
def configure_ldap_certificates():
    """Configure LDAP certificate validation"""
    import ldap
    
    # Set certificate validation
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
    ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, '/path/to/ca-cert.pem')
    ldap.set_option(ldap.OPT_X_TLS_CERTFILE, '/path/to/client-cert.pem')
    ldap.set_option(ldap.OPT_X_TLS_KEYFILE, '/path/to/client-key.pem')
```

## Advanced LDAP Operations

### Complex LDAP Filters
```python
def advanced_ldap_filter():
    """Create complex LDAP filter for user authentication"""
    filter_components = [
        'objectClass=person',
        'accountStatus=active',
        '(!(userAccountControl:1.2.840.113556.1.4.803:=2))'  # AD: not disabled
    ]
    
    return ldap_auth(
        filterstr='(&' + ''.join(f'({f})' for f in filter_components) + ')',
        server='ad.company.com'
    )
```

### Multi-Domain Support
```python
def multi_domain_ldap():
    """Support authentication across multiple LDAP domains"""
    domains = [
        {
            'server': 'ldap1.company.com',
            'base_dn': 'ou=users,dc=company,dc=com',
            'bind_dn': 'cn=service,dc=company,dc=com'
        },
        {
            'server': 'ldap2.partner.com', 
            'base_dn': 'ou=people,dc=partner,dc=com',
            'bind_dn': 'cn=web2py,dc=partner,dc=com'
        }
    ]
    
    auth_methods = []
    for domain in domains:
        auth_methods.append(ldap_auth(**domain))
    
    return auth_methods
```

## Error Handling and Logging

### Connection Error Handling
```python
def robust_ldap_auth():
    """LDAP authentication with comprehensive error handling"""
    try:
        return ldap_auth(
            server='ldap.company.com',
            logging_level='info'
        )
    except ldap.SERVER_DOWN:
        logging.error("LDAP server unavailable")
        return None
    except ldap.INVALID_CREDENTIALS:
        logging.warning("LDAP bind credentials invalid")
        return None
    except Exception as e:
        logging.error(f"LDAP configuration error: {e}")
        return None
```

### Authentication Logging
```python
def ldap_auth_with_logging():
    """Enhanced LDAP authentication with detailed logging"""
    def log_authentication(username, success, details=None):
        if success:
            logging.info(f"LDAP authentication successful for {username}")
        else:
            logging.warning(f"LDAP authentication failed for {username}: {details}")
    
    # Configure logging level
    logging.basicConfig(level=logging.INFO)
    
    return ldap_auth(
        server='ldap.company.com',
        logging_level='info'
    )
```

## Performance Optimization

### Connection Pooling
```python
import ldap.ldapobject

class LDAPConnectionPool:
    """Simple LDAP connection pool for performance"""
    
    def __init__(self, server, bind_dn, bind_pw, pool_size=5):
        self.server = server
        self.bind_dn = bind_dn
        self.bind_pw = bind_pw
        self.pool = []
        self.pool_size = pool_size
    
    def get_connection(self):
        if self.pool:
            return self.pool.pop()
        else:
            conn = ldap.initialize(self.server)
            conn.simple_bind_s(self.bind_dn, self.bind_pw)
            return conn
    
    def return_connection(self, conn):
        if len(self.pool) < self.pool_size:
            self.pool.append(conn)
        else:
            conn.unbind_s()
```

### Caching Strategies
```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def cached_ldap_user_lookup(username, cache_timestamp):
    """Cache LDAP user lookups for performance"""
    # Implementation would perform actual LDAP lookup
    pass

def ldap_auth_with_caching(cache_duration=300):
    """LDAP authentication with user lookup caching"""
    def auth_function(username, password):
        # Create cache key with time window
        cache_key = int(time.time() / cache_duration)
        
        # Check cached user data
        user_data = cached_ldap_user_lookup(username, cache_key)
        
        # Proceed with authentication
        return authenticate_with_cached_data(username, password, user_data)
    
    return auth_function
```

## Integration Examples

### Active Directory Integration
```python
def active_directory_auth():
    """Complete Active Directory integration example"""
    return ldap_auth(
        server='ad.company.com',
        port=389,
        base_dn='OU=Users,DC=company,DC=com',
        mode='domainname\\',
        bind_dn='CN=web2py-service,OU=Service Accounts,DC=company,DC=com',
        bind_pw='service_account_password',
        filterstr='(&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))',
        username_attrib='sAMAccountName',
        manage_user=True,
        user_firstname_attrib='givenName',
        user_lastname_attrib='sn',
        user_mail_attrib='mail',
        manage_groups=True,
        allowed_groups=['Web2py-Users'],
        group_dn='OU=Groups,DC=company,DC=com',
        group_name_attrib='cn',
        group_member_attrib='member',
        group_mapping={'Web2py-Admins': 'admin'},
        tls=True,
        logging_level='info'
    )
```

### OpenLDAP Integration
```python
def openldap_auth():
    """OpenLDAP server integration example"""
    return ldap_auth(
        server='openldap.company.com',
        port=389,
        base_dn='ou=people,dc=company,dc=com',
        mode='uid',
        bind_dn='cn=manager,dc=company,dc=com',
        bind_pw='manager_password',
        filterstr='objectClass=inetOrgPerson',
        username_attrib='uid',
        manage_user=True,
        user_firstname_attrib='givenName',
        user_lastname_attrib='sn',
        user_mail_attrib='mail',
        manage_groups=True,
        group_dn='ou=groups,dc=company,dc=com',
        group_name_attrib='cn',
        group_member_attrib='memberUid',
        tls=True
    )
```

## Testing and Validation

### LDAP Connection Testing
```python
def test_ldap_connection(server, bind_dn, bind_pw):
    """Test LDAP server connectivity and credentials"""
    try:
        conn = ldap.initialize(f'ldap://{server}')
        conn.simple_bind_s(bind_dn, bind_pw)
        conn.unbind_s()
        return True, "Connection successful"
    except ldap.INVALID_CREDENTIALS:
        return False, "Invalid bind credentials"
    except ldap.SERVER_DOWN:
        return False, "Server unavailable"
    except Exception as e:
        return False, f"Connection error: {e}"
```

### User Search Testing
```python
def test_user_search(server, base_dn, username):
    """Test LDAP user search functionality"""
    try:
        conn = ldap.initialize(f'ldap://{server}')
        conn.simple_bind_s()  # Anonymous bind
        
        search_filter = f'(uid={ldap.filter.escape_filter_chars(username)})'
        result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        
        conn.unbind_s()
        return len(result) > 0, f"Found {len(result)} user(s)"
    except Exception as e:
        return False, f"Search error: {e}"
```

## Best Practices

### Security Best Practices
1. **Use secure connections (LDAPS/StartTLS)**
2. **Validate server certificates**
3. **Use service accounts with minimal privileges**
4. **Implement proper error handling**
5. **Log authentication events for security monitoring**

### Performance Best Practices
1. **Implement connection pooling**
2. **Cache user lookups appropriately**
3. **Use efficient LDAP filters**
4. **Minimize attribute retrieval**
5. **Monitor LDAP server performance**

### Deployment Best Practices
1. **Test against actual LDAP servers**
2. **Document LDAP schema requirements**
3. **Plan for LDAP server maintenance**
4. **Implement fallback authentication**
5. **Regular security audits of LDAP integration**