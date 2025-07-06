# test-referral-device-id.js Technical Documentation

## Purpose

Unit test suite for device ID validation in the referral system, ensuring proper device tracking to prevent referral fraud and abuse through device-based validation.

## Core Functionality

### Device ID Validation

#### Purpose
- **Fraud Prevention**: Ensure referrals come from legitimate devices
- **Abuse Detection**: Prevent multiple accounts from same device
- **Data Integrity**: Maintain referral system reliability

#### Validation Rules
1. **User Device ID**: Referring user must have valid device_id or register_device_id
2. **Sender Device ID**: Referral sender must have valid device_id or register_device_id
3. **Cross-Validation**: Both parties must have proper device tracking

## Test Architecture

### Test Structure
```javascript
describe('Referral Service - senderTokenData', () => {
  let sandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();
  });

  afterEach(() => {
    sandbox.restore();
  });
});
```

### Mock Strategy
```javascript
// Mock AuthUsers model
sandbox.stub(AuthUsers, 'query').callsFake(() => ({
  select: sinon.stub().returns({
    findById: sinon.stub().resolves(userData)
  }),
  findById: sinon.stub().resolves(senderData)
}));

// Mock ReferralHistory model  
sandbox.stub(ReferralHistory, 'query').returns({
  where: sinon.stub().returnsThis(),
  first: sinon.stub().resolves(null)
});
```

## Error Scenarios

### User Device ID Missing
```javascript
it('should throw ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST if user device ID is missing', async () => {
  const inputData = {
    userId: 1,
    referral_code: 'testcode',
    reward_type: 'token',
  };

  const referralHash = new Hashids('projectTitle', 10);
  const senderId = referralHash.decode(inputData.referral_code)[0] || 0;

  // Mock user with missing device IDs
  sandbox.stub(AuthUsers, 'query').callsFake(() => ({
    select: sinon.stub().returns({
      findById: sinon.stub().resolves({
        created_on: new Date(),
        registration_latitude: 29.0,
        registration_longitude: -95.0,
        device_id: null,              // Missing device ID
        register_device_id: null,     // Missing register device ID
        is_debug: false,
      }),
    }),
    findById: sinon.stub().resolves({
      id: senderId,
      device_id: null,
      register_device_id: null,
    }),
  }));

  try {
    await ReferralService.create(inputData);
  } catch (error) {
    expect(error.message).to.equal('ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST');
    expect(error.httpStatus).to.equal(400);
  }
});
```

### Sender Device ID Missing
```javascript
it('should throw ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST if sender device ID is missing', async () => {
  const inputData = {
    userId: 1,
    referral_code: 'testcode',
    reward_type: 'token',
  };

  // Mock user with device ID, sender without
  sandbox.stub(AuthUsers, 'query').callsFake(() => ({
    select: sinon.stub().returns({
      findById: sinon.stub().resolves({
        created_on: new Date(),
        registration_latitude: 29.0,
        registration_longitude: -95.0,
        device_id: 'has device_id',    // Valid device ID
        register_device_id: null,
        is_debug: false,
      }),
    }),
    findById: sinon.stub().resolves({
      id: senderId,
      device_id: null,               // Missing sender device ID
      register_device_id: null,      // Missing sender register device ID
    }),
  }));

  try {
    await ReferralService.create(inputData);
  } catch (error) {
    expect(error.message).to.equal('ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST');
    expect(error.httpStatus).to.equal(400);
  }
});
```

## Device ID Sources

### Primary Device ID
- **Field**: `device_id`
- **Source**: Device UUID from mobile app
- **Purpose**: Primary device identification

### Registration Device ID
- **Field**: `register_device_id`
- **Source**: Device ID captured during registration
- **Purpose**: Backup device identification

### Validation Logic
```javascript
const hasValidDeviceId = (user) => {
  return user.device_id || user.register_device_id;
};

const validateDeviceIds = (user, sender) => {
  if (!hasValidDeviceId(user)) {
    throw new Error('ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST');
  }
  
  if (!hasValidDeviceId(sender)) {
    throw new Error('ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST');
  }
};
```

## Error Types

### ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST
- **Code**: Custom error type
- **HTTP Status**: 400 (Bad Request)
- **Trigger**: Missing device ID on user or sender
- **Purpose**: Prevent referrals without proper device tracking

## Data Structure

### User Data Requirements
```javascript
const userData = {
  created_on: 'timestamp',
  registration_latitude: 'decimal',
  registration_longitude: 'decimal',
  device_id: 'string',           // Required: Primary device ID
  register_device_id: 'string', // Alternative: Registration device ID
  is_debug: 'boolean'
};
```

### Sender Data Requirements
```javascript
const senderData = {
  id: 'integer',
  device_id: 'string',           // Required: Primary device ID
  register_device_id: 'string'  // Alternative: Registration device ID
};
```

## Service Integration

### ReferralService.create()
```javascript
const inputData = {
  userId: 'integer',
  referral_code: 'string',
  reward_type: 'string'
};

// Validate device IDs before processing referral
const result = await ReferralService.create(inputData);
```

### Hashids Integration
```javascript
const Hashids = require('hashids');
const referralHash = new Hashids('projectTitle', 10);
const senderId = referralHash.decode(inputData.referral_code)[0] || 0;
```

## Mock Configuration

### Successful Scenario Mock
```javascript
const validUserData = {
  created_on: new Date(),
  registration_latitude: 29.0,
  registration_longitude: -95.0,
  device_id: 'valid-device-uuid',
  register_device_id: 'backup-device-id',
  is_debug: false
};

const validSenderData = {
  id: senderId,
  device_id: 'sender-device-uuid',
  register_device_id: 'sender-backup-id'
};
```

### Failed Scenario Mock
```javascript
const invalidUserData = {
  // ... other fields
  device_id: null,
  register_device_id: null
};

const invalidSenderData = {
  id: senderId,
  device_id: null,
  register_device_id: null
};
```

## Security Implications

### Fraud Prevention
- **Device Fingerprinting**: Unique device identification
- **Multiple Account Detection**: Prevent same device creating multiple accounts
- **Referral Abuse**: Stop self-referrals from same device

### Privacy Considerations
- **Device ID Anonymization**: Hash device IDs for privacy
- **Data Retention**: Limit device ID storage duration
- **User Consent**: Ensure proper consent for device tracking

## Business Rules

### Device ID Requirements
1. **New Users**: Must have device ID from registration
2. **Existing Users**: Must have device ID from login/update
3. **Referrers**: Must have valid device tracking history
4. **Cross-Platform**: Support iOS and Android device IDs

### Validation Timing
- **Pre-Referral**: Validate before processing referral
- **Registration**: Capture device ID during signup
- **Login**: Update device ID on each login

## Error Handling

### Missing Device ID Flow
1. **Detection**: Check for null/empty device IDs
2. **Error Creation**: Create specific error type
3. **HTTP Response**: Return 400 with error message
4. **Logging**: Log device ID validation failures

### Recovery Strategies
- **Device ID Update**: Prompt user to update app
- **Alternative Validation**: Use other fraud detection methods
- **Manual Review**: Flag for manual verification

## Testing Strategy

### Unit Test Isolation
```javascript
beforeEach(() => {
  sandbox = sinon.createSandbox();
});

afterEach(() => {
  sandbox.restore();
});
```

### Mock Data Consistency
- **Realistic IDs**: Use UUID-format device IDs
- **Consistent Data**: Ensure related data consistency
- **Edge Cases**: Test null, empty, and malformed IDs

## Integration Points

### Mobile Applications
- **Device ID Collection**: Capture unique device identifiers
- **Registration Flow**: Store device ID during signup
- **API Communication**: Include device ID in referral requests

### Backend Services
- **Device Tracking**: Store and validate device IDs
- **Fraud Detection**: Cross-reference device patterns
- **Analytics**: Track device-based metrics

## Usage Examples

### Valid Referral Processing
```javascript
const inputData = {
  userId: 1,
  referral_code: 'ABCDE12345',
  reward_type: 'token'
};

try {
  const result = await ReferralService.create(inputData);
  console.log('Referral processed successfully');
} catch (error) {
  if (error.message === 'ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST') {
    console.log('Device ID validation failed');
  }
}
```

### Device ID Validation
```javascript
const validateReferralDevices = async (userId, referralCode) => {
  const user = await AuthUsers.query().findById(userId);
  const senderId = referralHash.decode(referralCode)[0];
  const sender = await AuthUsers.query().findById(senderId);
  
  if (!user.device_id && !user.register_device_id) {
    throw new Error('User device ID missing');
  }
  
  if (!sender.device_id && !sender.register_device_id) {
    throw new Error('Sender device ID missing');
  }
};
```

This test suite ensures the referral system maintains device-based fraud prevention, validating that both referring users and referral senders have proper device tracking to maintain system integrity.