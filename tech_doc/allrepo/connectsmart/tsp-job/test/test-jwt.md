# JWT Helper Test Suite

## Overview
Test suite for the JWT (JSON Web Token) helper module that validates token creation, decoding, and database integration for user authentication and authorization in the TSP job system.

## File Location
`/test/test-jwt.js`

## Dependencies
- `@maas/core/bootstrap` - Application initialization
- `chai` - Assertion library with expect interface
- `@app/src/models/AuthUserTokens` - User token database model
- `@app/src/models/AuthUsers` - User authentication model
- `@app/src/helpers/jwt` - JWT helper functions

## Test Architecture

### JWT Helper Functions Under Test
```javascript
const jwtHelper = require('@app/src/helpers/jwt');
```

### Core Functions Tested
- `createAccessToken(userId)` - Creates new JWT access tokens
- `decodeToken(token)` - Decodes and validates JWT tokens

### Database Models
- **AuthUserTokens**: Manages user token records
- **AuthUsers**: Manages user authentication data

## Test Configuration

### Test User Setup
```javascript
const userId = 1003;
```
- **Purpose**: Consistent test user ID for all JWT operations
- **Selection**: Uses existing test user in database
- **Scope**: All tests operate on this single user

## Access Token Creation Testing

### Token Generation Test
```javascript
it('should create access token', async () => {
  const token = await jwtHelper.createAccessToken(userId);
  expect(token).to.be.a('string');
});
```

#### Token Validation
- **Type Check**: Verifies token is returned as string
- **Format**: JWT tokens are base64-encoded strings with dot separators
- **Structure**: Follows JWT standard format (header.payload.signature)

### Token Decoding Validation
```javascript
const decoded = jwtHelper.decodeToken(token);
expect(decoded).to.be.an('object');
expect(decoded.user.id).to.equal(userId);
```

#### Decoded Token Structure
- **Object Type**: Decoded token returns JavaScript object
- **User Information**: Contains user data in payload
- **ID Verification**: User ID matches the requesting user

### Database Integration Testing

#### Token Storage Verification
```javascript
const tokenInDb = await AuthUserTokens.query()
  .where({ user_id: userId, disabled: false })
  .orderBy('id', 'desc')
  .first();
  
expect(tokenInDb).to.be.an('object');
expect(tokenInDb.access_token).to.equal(token);
```

#### Database Query Logic
- **User Filter**: Queries tokens for specific user
- **Status Filter**: Only retrieves active (non-disabled) tokens
- **Ordering**: Gets most recent token (highest ID)
- **Token Match**: Verifies stored token matches generated token

#### User Record Update Verification
```javascript
const authUser = await AuthUsers.query().findById(userId);
expect(authUser).to.be.an('object');
expect(authUser.access_token).to.equal(token);
```

## JWT Token Structure

### Standard JWT Components
1. **Header**: Algorithm and token type information
2. **Payload**: User data and claims
3. **Signature**: Cryptographic signature for verification

### Expected Payload Structure
```javascript
{
  user: {
    id: 1003,           // User identifier
    // Additional user claims
  },
  iat: timestamp,       // Issued at time
  exp: timestamp,       // Expiration time
  // Additional standard claims
}
```

## Database Schema Integration

### AuthUserTokens Table
- **user_id**: Foreign key to users table
- **access_token**: JWT token string
- **disabled**: Boolean flag for token status
- **created_at**: Token creation timestamp
- **updated_at**: Token update timestamp

### AuthUsers Table
- **id**: Primary key (user identifier)
- **access_token**: Current active token
- **Additional fields**: User authentication data

## Security Considerations

### Token Management
- **Single Active Token**: User has one active token at a time
- **Token Replacement**: New token creation invalidates previous tokens
- **Database Consistency**: Token stored in both tables for different purposes

### Authentication Flow
1. **Token Creation**: Generate JWT for authenticated user
2. **Database Storage**: Store token in AuthUserTokens table
3. **User Update**: Update user record with current token
4. **Token Validation**: Decode and verify token on subsequent requests

## Error Handling

### Token Creation Failures
- **Database Errors**: Handle database connection issues
- **Cryptographic Errors**: Manage JWT signing failures
- **User Validation**: Verify user exists before token creation

### Token Decoding Failures
- **Invalid Format**: Handle malformed JWT tokens
- **Signature Verification**: Manage signature validation failures
- **Expired Tokens**: Handle token expiration scenarios

## Performance Considerations

### Database Operations
- **Efficient Queries**: Uses indexed lookups on user_id
- **Transaction Management**: Ensures consistent token updates
- **Connection Pooling**: Leverages connection pooling for performance

### Token Operations
- **Cryptographic Performance**: JWT operations are computationally lightweight
- **Memory Usage**: Tokens are stored as strings with minimal memory impact
- **Caching Opportunities**: Decoded tokens could be cached for performance

## Integration Points

### Authentication System
- **Login Process**: Token creation during user authentication
- **Session Management**: Token validation for protected endpoints
- **Logout Process**: Token invalidation and cleanup

### Authorization System
- **Permission Checking**: Token contains user role and permission data
- **Resource Access**: Token validation for protected resources
- **API Security**: Token-based API authentication

## Testing Best Practices

### Assertion Strategy
- **Type Validation**: Ensures correct data types returned
- **Value Verification**: Confirms expected values in token and database
- **Object Structure**: Validates expected object properties
- **Database Consistency**: Verifies data consistency across tables

### Test Isolation
- **User Selection**: Uses consistent test user for reproducibility
- **State Management**: Assumes clean database state
- **No Cleanup**: Relies on test user being in known state

## Quality Assurance

### Test Coverage Areas
1. **Token Generation**: Validates token creation process
2. **Token Structure**: Verifies JWT format and content
3. **Database Integration**: Confirms proper data storage
4. **User Association**: Ensures tokens are linked to correct users

### Validation Approaches
- **Functional Testing**: Tests actual JWT operations
- **Database Testing**: Validates database storage and retrieval
- **Integration Testing**: Confirms end-to-end token workflow

## Business Logic

### Token Lifecycle
1. **Creation**: Generate token for authenticated user
2. **Storage**: Persist token in database for tracking
3. **Usage**: Token used for subsequent API requests
4. **Expiration**: Token expires based on configured TTL
5. **Renewal**: New token creation for continued access

### User Session Management
- **Single Session**: One active token per user
- **Session Tracking**: Database records enable session management
- **Security Auditing**: Token history available for security analysis

## Maintenance Considerations

### Token Configuration
- **Signing Algorithm**: JWT algorithm selection and configuration
- **Expiration Time**: Token TTL configuration
- **Secret Management**: JWT signing secret rotation
- **Claim Structure**: Evolution of token payload structure

### Database Schema Evolution
- **Token Fields**: Additional token metadata requirements
- **Indexing**: Performance optimization for token lookups
- **Archival**: Long-term token storage and cleanup strategies

## Security Best Practices

### Token Security
- **Signing Secrets**: Secure management of JWT signing secrets
- **Token Transmission**: HTTPS-only token transmission
- **Token Storage**: Secure client-side token storage
- **Token Expiration**: Appropriate token lifetime configuration

### Database Security
- **Access Control**: Restricted database access for token tables
- **Audit Logging**: Token creation and usage logging
- **Data Encryption**: Encryption of sensitive token data
- **Backup Security**: Secure handling of token data in backups

## Error Scenarios

### Common Failure Cases
- **Invalid User ID**: Attempt to create token for non-existent user
- **Database Unavailable**: Handle database connection failures
- **Signing Key Issues**: Manage JWT signing key problems
- **Concurrent Access**: Handle concurrent token creation scenarios

### Recovery Procedures
- **Token Regeneration**: Process for creating new tokens after failures
- **Database Recovery**: Procedures for recovering token data
- **User Session Recovery**: Methods for restoring user sessions
- **Emergency Access**: Alternative authentication methods during failures

## Monitoring and Alerting

### Token Metrics
- **Creation Rate**: Monitor token generation frequency
- **Failure Rate**: Track token creation and validation failures
- **Token Lifetime**: Analyze token usage patterns
- **Database Performance**: Monitor token-related query performance

### Security Monitoring
- **Suspicious Activity**: Detect unusual token usage patterns
- **Failed Validations**: Monitor token validation failures
- **Token Abuse**: Identify potential token misuse
- **System Health**: Overall authentication system health monitoring