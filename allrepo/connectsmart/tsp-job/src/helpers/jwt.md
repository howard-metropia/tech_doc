# JWT Helper

## Overview
**File**: `src/helpers/jwt.js`  
**Type**: Authentication Utility  
**Purpose**: Manages JWT token creation and validation with key rotation support

## Core Functions

### Token Creation
```javascript
const createAccessToken = async (userId) => {
  // Check for existing valid tokens within refresh period
  // Create new token if needed
  // Update database records
}
```

### Token Decoding
```javascript
const decodeToken = (token) => {
  // Try current JWT key first
  // Fallback to rotation key if current fails
  // Mark payload with key age indicator
}
```

## Configuration

### Constants
- **MAX_EXPIRATION**: 30 days (token lifetime)
- **REFRESH_PERIOD**: 7 days (reuse window)

### Keys
- **JWT_KEY**: Current signing key (base64 encoded)
- **JWT_ROTATE_KEY**: Previous key for transition period

## Token Management

### Creation Logic
1. **Check Existing**: Look for valid tokens within refresh period
2. **Validate Key**: Ensure token uses current key
3. **Reuse or Create**: Use existing valid token or create new
4. **Database Update**: Store new token, disable old ones
5. **User Update**: Update user's access_token field

### Token Payload
```javascript
{
  iss: 'Metropia Auth',
  user: { id: userId },
  user_groups: { id: 1 },
  hmac_key: '',
  exp: // expiration timestamp
}
```

## Key Rotation Support

### Dual Key System
- **Primary Key**: Current active signing key
- **Rotation Key**: Previous key for backward compatibility
- **Transition**: Allows gradual key migration

### Decoding Strategy
```javascript
try {
  // Try current key first
  payload = jwt.verify(token, currentKey);
  payload.isOlder = false;
} catch (e) {
  // Fallback to rotation key
  payload = jwt.verify(token, rotationKey);
  payload.isOlder = true;
}
```

## Database Integration

### Models Used
- **AuthUsers**: User authentication records
- **AuthUserTokens**: Token storage and management

### Token Storage
```javascript
await AuthUserTokens.query().insert({
  user_id: userId,
  access_token: refreshToken,
});
```

### Token Cleanup
```javascript
// Disable old tokens
await AuthUserTokens.query()
  .where({ user_id: userId, disabled: false })
  .patch({ disabled: true });
```

## Usage Examples

### Create New Token
```javascript
const { createAccessToken } = require('./jwt');

const token = await createAccessToken(userId);
console.log('New token:', token);
```

### Decode Token
```javascript
const { decodeToken } = require('./jwt');

try {
  const payload = decodeToken(token);
  console.log('User ID:', payload.user.id);
  console.log('Is older key:', payload.isOlder);
} catch (error) {
  console.error('Invalid token:', error.message);
}
```

### Token Refresh Check
```javascript
// Check if token is from old key and needs refresh
const payload = decodeToken(existingToken);
if (payload.isOlder) {
  const newToken = await createAccessToken(payload.user.id);
  // Use new token for future requests
}
```

## Error Handling

### Token Errors
- **ERROR_TOKEN_REQUIRED**: Missing token
- **ERROR_TOKEN_EXPIRED**: Token past expiration
- **ERROR_TOKEN_CHANGED**: Token signature invalid
- **ERROR_TOKEN_FAILED**: General token validation failure
- **ERROR_USER_BLOCKED**: User account disabled

### Decoding Errors
- **JsonWebTokenError**: Invalid signature or format
- **TokenExpiredError**: Token past expiration date
- **NotBeforeError**: Token not yet valid

## Security Features

### Key Management
- **Base64 Encoding**: Keys stored in base64 format
- **Environment Variables**: Keys from secure configuration
- **Rotation Support**: Seamless key transitions

### Token Security
- **Signed Tokens**: Cryptographically signed
- **Expiration**: Built-in token expiration
- **Single Use**: Old tokens disabled on refresh

## Performance Optimization

### Token Reuse
- **Refresh Window**: 7-day reuse period
- **Database Query**: Efficient lookup of recent tokens
- **Conditional Creation**: Only create when necessary

### Database Efficiency
- **Indexed Queries**: Optimized user_id and date lookups
- **Batch Updates**: Efficient token disabling
- **Minimal Writes**: Reuse existing valid tokens

## Token Lifecycle

### Creation Flow
1. **Query Recent Tokens**: Check for reusable tokens
2. **Validate Key Usage**: Ensure current key usage
3. **Generate or Reuse**: Create new or use existing
4. **Database Updates**: Store and cleanup tokens
5. **Return Token**: Provide token to caller

### Validation Flow
1. **Try Current Key**: Attempt with active key
2. **Try Rotation Key**: Fallback if current fails
3. **Mark Key Age**: Flag older vs newer keys
4. **Return Payload**: Decoded token data

## Monitoring

### Logging
```javascript
logger.info(`Create new access token for userId:${userId}`);
logger.info(`[decodeToken] enter: ${token}`);
```

### Metrics to Track
- **Token Creation Rate**: New tokens per time period
- **Key Rotation Usage**: Old vs new key usage
- **Validation Failures**: Failed token attempts

## Integration Points

### Authentication Middleware
- **Token Validation**: Decode and validate tokens
- **User Context**: Extract user information
- **Permission Checking**: Use payload for authorization

### API Responses
- **Token Refresh**: Provide new tokens when needed
- **User Sessions**: Maintain user authentication state
- **Cross-Service**: Share tokens between services

## Configuration Requirements

### Environment Variables
```bash
JWT_KEY=base64_encoded_secret_key
JWT_ROTATE_KEY=base64_encoded_rotation_key
```

### Database Schema
```sql
-- auth_user_tokens table
user_id INT,
access_token TEXT,
disabled BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP
```

## Best Practices

### Key Rotation
- **Regular Rotation**: Rotate keys periodically
- **Gradual Transition**: Maintain overlap period
- **Monitoring**: Track key usage during transition

### Token Management
- **Reasonable Expiration**: Balance security and usability
- **Cleanup**: Regular cleanup of disabled tokens
- **Monitoring**: Track token creation and validation rates

## Testing Considerations

### Unit Tests
```javascript
// Mock JWT library
jest.mock('jsonwebtoken');

// Mock database models
jest.mock('@app/src/models/AuthUsers');
jest.mock('@app/src/models/AuthUserTokens');
```

### Test Scenarios
- **Token Creation**: Valid user scenarios
- **Key Rotation**: Old and new key validation
- **Error Cases**: Invalid tokens, expired tokens
- **Database Integration**: Token storage and retrieval