# Test Helper - Authentication Token Generation

## Overview
A utility helper module for generating JWT authentication tokens specifically designed for testing environments. This module provides functionality to create and manage user authentication tokens for test scenarios.

## File Purpose
- **Primary Function**: Generate JWT tokens for test user authentication
- **Type**: Helper utility module
- **Role**: Supports testing by providing valid authentication tokens

## Key Functions

### `authToken(userId)`
Generates a JWT authentication token for a specified user ID.

**Parameters:**
- `userId` (number): The ID of the user for whom to generate the token

**Returns:**
- `Promise<string>`: JWT token string

**Functionality:**
- Creates JWT payload with 30-day expiration
- Manages token storage in AuthUserTokens table
- Updates existing tokens or creates new ones
- Handles token lifecycle management

## Implementation Details

### JWT Token Structure
```javascript
const payload = {
  iat: nowTimestamp,                    // Issued at timestamp
  exp: nowTimestamp + 60 * 60 * 24 * 30, // 30-day expiration
  iss: "Metropia Auth",                 // Issuer
  user: { id: userId },                 // User information
  user_groups: { id: 1 },               // User group assignment
  hmac_key: "",                         // HMAC key (empty for tests)
};
```

### Database Integration
- **Model Used**: `AuthUserTokens`
- **Operations**: 
  - Query existing tokens for user
  - Insert new token records
  - Update existing token records with new token and timestamp

### Token Management Logic
1. **Check Existing Token**: Queries for active (non-disabled) tokens for the user
2. **Create or Update**: 
   - If no existing token: Creates new token record
   - If existing token: Updates record with new token and timestamp
3. **Error Handling**: Comprehensive logging with error details and stack traces

## Dependencies

### External Dependencies
- `jsonwebtoken`: JWT token generation and signing
- `moment-timezone`: Timestamp formatting and timezone handling

### Internal Dependencies
- `@app/src/models/AuthUserTokens`: User token management model
- `@maas/core/log`: Centralized logging system

## Usage Examples

### Basic Token Generation
```javascript
const { authToken } = require('./test');

// Generate token for user ID 123
const token = await authToken(123);
console.log('Generated token:', token);
```

### Test Setup Integration
```javascript
// In test setup
beforeEach(async () => {
  const userToken = await authToken(testUserId);
  // Use token for authenticated API requests
});
```

## Technical Specifications

### Token Expiration
- **Duration**: 30 days (2,592,000 seconds)
- **Calculation**: `60 * 60 * 24 * 30` seconds from issued timestamp

### JWT Configuration
- **Algorithm**: Uses default JWT signing algorithm
- **Key**: Base64-encoded JWT_KEY environment variable
- **Issuer**: "Metropia Auth"

### Database Schema Integration
- **Table**: `auth_user_tokens`
- **Key Fields**: `user_id`, `access_token`, `disabled`, `created_at`

## Error Handling

### Exception Management
- Comprehensive try-catch block
- Error logging with message and stack trace
- Exception re-throwing for upstream handling

### Logging Integration
- Error-level logging for exceptions
- Warning-level logging for stack traces
- Structured logging through MaaS core logging system

## Security Considerations

### Token Security
- JWT keys loaded from environment variables
- Base64 encoding for key security
- 30-day token expiration limits exposure

### Test Environment Isolation
- Designed specifically for test environments
- Simplified authentication flow for testing
- No production security validations

## Testing Integration

### Test Support Features
- Simple API for token generation
- Database state management
- Consistent token format across tests

### Common Test Patterns
- User authentication setup
- API endpoint testing with valid tokens
- Authentication flow validation

## Maintenance Notes
- Token expiration period may need adjustment based on test requirements
- JWT key management should align with environment configuration
- Database schema changes may require model integration updates