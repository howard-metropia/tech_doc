# Bank Account Controller API Documentation

## Overview
The Bank Account Controller manages user banking information for the MaaS platform's wallet system. It provides secure storage and retrieval of bank account details for payment processing and fund transfers within the mobility ecosystem.

**File Path:** `/allrepo/connectsmart/hybrid/applications/portal/controllers/bank_account.py`

**Controller Type:** Authenticated Portal Controller

**Authentication:** JWT token required

## Features
- Secure bank account information storage
- UTF-8 encoding support for international characters
- Account creation and updates
- User-specific account management
- Comprehensive error handling and validation

## API Endpoints

### Bank Account Management
**Endpoint:** `/bank_account/bank_account`
**Methods:** GET, PUT
**Authentication:** JWT token required

#### GET - Retrieve Bank Account
Retrieves the current user's bank account information.

**Parameters:** None

**Response Format:**
```json
{
  "success": true,
  "data": {
    "bank_account_number": "1234567890",
    "bank_code": "001",
    "bank_user_name": "John Doe",
    "bank_name": "First National Bank",
    "id_number": "A123456789",
    "bank_branch": "Main Branch",
    "address": "123 Main St, City",
    "residence_address": "456 Home Ave, City"
  }
}
```

**Status Codes:**
- `200`: Success (returns account data or empty object if no account)

#### PUT - Update Bank Account
Creates or updates the user's bank account information.

**Required Fields:**
- `bank_account_number`: Bank account number
- `bank_code`: Bank institution code
- `bank_user_name`: Account holder name
- `bank_name`: Bank institution name
- `id_number`: User identification number
- `bank_branch`: Bank branch name
- `address`: Bank address
- `residence_address`: Account holder's address

**Request Example:**
```json
{
  "bank_account_number": "1234567890",
  "bank_code": "001",
  "bank_user_name": "張三",
  "bank_name": "第一銀行",
  "id_number": "A123456789",
  "bank_branch": "總行營業部",
  "address": "台北市中正區重慶南路一段30號",
  "residence_address": "台北市信義區信義路五段7號"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "bank_account_number": "1234567890",
    "bank_code": "001",
    "bank_user_name": "張三",
    "bank_name": "第一銀行",
    "id_number": "A123456789",
    "bank_branch": "總行營業部",
    "address": "台北市中正區重慶南路一段30號",
    "residence_address": "台北市信義區信義路五段7號"
  }
}
```

**Status Codes:**
- `200`: Successfully updated/created
- `400`: Invalid parameters or update failure

## Data Model

### Bank Account Structure
```python
{
    "bank_account_number": str,    # Bank account number
    "bank_code": str,              # Bank institution code
    "bank_user_name": str,         # Account holder name (UTF-8)
    "bank_name": str,              # Bank institution name (UTF-8)
    "id_number": str,              # User identification number
    "bank_branch": str,            # Bank branch name (UTF-8)
    "address": str,                # Bank address (UTF-8)
    "residence_address": str       # Account holder address (UTF-8)
}
```

## Database Schema

### Table: wallet_user_bank_account
- `user_id` (FOREIGN KEY): Reference to user
- `bank_account_number`: Account number
- `bank_code`: Bank institution identifier
- `bank_user_name`: Account holder name
- `bank_name`: Bank institution name
- `id_number`: User identification
- `bank_branch`: Bank branch information
- `address`: Bank address
- `residence_address`: Account holder residence address

## Authentication & Security

### JWT Authentication
- `@auth.allows_jwt()`: Enables JWT token authentication
- `@jwt_helper.check_token()`: Validates token integrity
- User identification through `auth.user.id`

### Data Security
- UTF-8 encoding for international character support
- Parameter validation and type checking
- SQL injection prevention through ORM
- User-scoped data access (user can only access own account)

## Implementation Details

### Helper Functions

#### `__get_bank_account(user_id)`
Private function that retrieves bank account data for a specific user.

**Parameters:**
- `user_id`: User identifier

**Returns:**
- `row`: Database row object or None
- `result`: Dictionary with account data or empty dict

### UTF-8 Encoding Handling
The controller specifically handles UTF-8 encoding for text fields:
```python
bank_user_name = str(fields['bank_user_name'].encode('utf-8'))
bank_name = str(fields['bank_name'].encode('utf-8'))
bank_branch = str(fields['bank_branch'].encode('utf-8'))
address = str(fields['address'].encode('utf-8'))
residence_address = str(fields['residence_address'].encode('utf-8'))
```

### Database Operations
- **SELECT**: Retrieves existing account information
- **INSERT**: Creates new bank account record
- **UPDATE**: Modifies existing account information
- Uses `update_or_insert` pattern for flexibility

## Error Handling

### Exception Types
- `ValueError`: Invalid parameter types or values
- `TypeError`: Incorrect parameter types
- `KeyError`: Missing required parameters
- `Exception`: General database or processing errors

### Error Response Format
```json
{
  "success": false,
  "error_code": "ERROR_BAD_REQUEST_PARAMS",
  "message": "Invalid parameters"
}
```

### Error Logging
Comprehensive error logging for debugging:
```python
logger.error('[Bank account] Update bank account failure reason: %s' % e)
```

## Usage Examples

### Retrieve Bank Account
```bash
curl -X GET /bank_account/bank_account \
  -H "Authorization: Bearer <jwt_token>"
```

### Update Bank Account
```bash
curl -X PUT /bank_account/bank_account \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "bank_account_number": "1234567890",
    "bank_code": "001",
    "bank_user_name": "John Doe",
    "bank_name": "First National Bank",
    "id_number": "A123456789",
    "bank_branch": "Main Branch",
    "address": "123 Main St, City",
    "residence_address": "456 Home Ave, City"
  }'
```

## Integration Points

### Wallet System
- Links to user wallet functionality
- Enables fund transfers and payments
- Supports payment processing workflows

### Payment Processing
- Bank account verification
- ACH transfers and direct deposits
- Withdrawal and refund operations

### User Management
- Tied to authenticated user sessions
- User profile completion workflows
- KYC (Know Your Customer) compliance

## International Support

### Character Encoding
- Full UTF-8 support for names and addresses
- Handles Chinese, Japanese, Korean characters
- Supports special characters and accents

### Localization Considerations
- Bank name and branch internationalization
- Address format flexibility
- ID number format variations by country

## Security Considerations

### Data Protection
- Sensitive financial information handling
- User access isolation (users can only access own data)
- Secure parameter validation
- Database transaction safety

### Privacy Compliance
- Minimal data storage approach
- User consent mechanisms
- Data retention policies
- Audit trail capabilities

## Performance Optimization

### Database Efficiency
- User-scoped queries for performance
- Minimal data transfer with selective fields
- Efficient upsert operations

### Caching Considerations
- Sensitive data should not be cached
- Database connection pooling
- Optimized query patterns

## Troubleshooting

### Common Issues
1. **UTF-8 Encoding Errors**: Check character encoding in requests
2. **Missing Parameters**: Ensure all required fields are provided
3. **Authorization Failures**: Verify JWT token validity
4. **Database Errors**: Check table structure and constraints

### Debug Information
- Error logging with specific failure reasons
- Parameter validation feedback
- Database operation status tracking

## Compliance Notes

### Financial Regulations
- Bank account information handling
- Anti-money laundering (AML) considerations
- Customer identification requirements
- Transaction monitoring capabilities

### Data Governance
- Sensitive data classification
- Access control and audit trails
- Data retention and deletion policies
- Cross-border data transfer compliance