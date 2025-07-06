# Carpool API Test Suite

## Overview
Test suite for the Carpool API functionality, specifically testing the suggested price calculation endpoint. Validates pricing logic for carpooling services based on distance and geographic location.

## File Purpose
- **Primary Function**: Test carpool pricing functionality
- **Type**: Integration test suite
- **Role**: Validates carpool price calculation and API error handling

## Test Configuration

### Test Setup
- **Framework**: Mocha with Chai assertions
- **HTTP Testing**: Supertest for API endpoint testing
- **Authentication**: JWT token-based authentication
- **Test User**: User ID 1003
- **Timeout**: 10-second timeout for pricing calculations

### Dependencies
- `@maas/core/bootstrap`: Application bootstrapping
- `@maas/core/api`: API application factory
- `@maas/core`: Router and core utilities
- `AuthUsers`: User authentication model
- `supertest`: HTTP assertion library
- `chai`: Assertion library

## Test Scenarios

### GET /suggested_price - Price Calculation

#### Test Case 1: Basic Price Calculation
**Purpose**: Test suggested price calculation for carpool trips
**Input Parameters**:
```javascript
{
  meter: 1000,
  country: 'usa'
}
```

**Expected Response Structure**:
```javascript
{
  "result": "success",
  "data": {
    "meter": 1000,
    "total_price": number,
    "min_price": number,
    "max_price": number,
    "currency": "USD"
  }
}
```

**Validation Steps**:
1. Submit distance (1000 meters) and country (USA)
2. Verify successful response
3. Confirm response contains all required pricing fields
4. Validate meter value matches input
5. Confirm USD currency for USA

### Response Properties Validation

#### Required Fields
- **meter**: Distance in meters (matches input)
- **total_price**: Calculated total trip price
- **min_price**: Minimum acceptable price
- **max_price**: Maximum suggested price
- **currency**: Currency code based on country

#### Data Validation
```javascript
expect(data).to.includes.keys([
  'meter',
  'total_price',
  'min_price',
  'max_price',
  'currency'
]);
expect(data.meter).to.eq(1000);
expected(data.currency).to.eq('USD');
```

## Error Handling Test Cases

### Authentication Errors (Code 10003)

#### Missing Authorization Token
**Purpose**: Test authentication requirement enforcement
**Trigger**: Request without Authorization header
**Expected Response**:
```javascript
{
  "result": "fail",
  "error": {
    "code": 10003,
    "msg": "Token required"
  }
}
```

**Validation**:
- Request fails without authentication
- Proper error code returned
- Clear error message provided

### Validation Errors (Code 10001)

#### Missing Required Parameters
**Purpose**: Test parameter validation
**Trigger**: Request without required country parameter
**Expected Response**:
```javascript
{
  "result": "fail",
  "error": {
    "code": 10001,
    "msg": "\"country\" is required"
  }
}
```

**Test Scenario**:
```javascript
const resp = await request.set(auth).get(url).query({});
```

**Validation**:
- Missing country parameter triggers validation error
- Appropriate error code and message
- Request processing stopped at validation

## Authentication Setup

### JWT Token Preparation
```javascript
before('prepare testing data', async () => {
  const { access_token: accessToken } = await AuthUsers.query()
    .select('access_token')
    .findById(userId);
  auth.Authorization = 'Bearer ' + accessToken;
});
```

### Request Headers
```javascript
const auth = {
  userid: userId,
  'Content-Type': 'application/json',
  Authorization: 'Bearer {access_token}'
};
```

## Pricing Logic Analysis

### Distance-Based Pricing
- **Input**: Distance in meters
- **Calculation**: Country-specific pricing algorithms
- **Output**: Min, max, and suggested total prices

### Geographic Pricing
- **Country Parameter**: Determines pricing rules and currency
- **Currency Mapping**: USA → USD currency
- **Regional Adjustments**: Country-specific pricing factors

### Price Range Calculation
- **Minimum Price**: Base fare + minimum distance rate
- **Maximum Price**: Premium pricing ceiling
- **Total Price**: Recommended fair price for distance

## API Endpoint Details

### Endpoint Information
- **Method**: GET
- **Route**: Retrieved via `router.url('getSuggestedPrice')`
- **Authentication**: Required JWT token
- **Parameters**: Query parameters for distance and country

### Query Parameters
- **meter** (required): Distance in meters
- **country** (required): Country code for pricing rules

### Response Format
```javascript
{
  "result": "success|fail",
  "data": {
    "meter": number,
    "total_price": number,
    "min_price": number,
    "max_price": number,
    "currency": "string"
  },
  "error": {
    "code": number,
    "msg": "string"
  }
}
```

## Carpool Pricing Integration

### Service Dependencies
- **Distance Calculation**: Accurate meter-based pricing
- **Currency Service**: Country-to-currency mapping
- **Rate Engine**: Dynamic pricing calculation
- **Geographic Service**: Country validation and rules

### Business Logic
- **Fair Pricing**: Balanced driver compensation and rider affordability
- **Market Rates**: Competitive pricing analysis
- **Dynamic Adjustments**: Time, demand, and location factors

## Test Data Strategy

### Standard Test Cases
- **Distance**: 1000 meters (1 kilometer)
- **Country**: USA for consistent currency testing
- **User**: Authenticated test user (1003)

### Edge Case Considerations
- **Short Distances**: Minimum fare scenarios
- **Long Distances**: Maximum pricing limits
- **Different Countries**: Multiple currency support

## Performance Considerations

### Response Time
- **10-Second Timeout**: Accounts for pricing calculation complexity
- **External Services**: Potential third-party rate lookups
- **Database Queries**: Pricing rule retrieval

### Calculation Efficiency
- **Real-Time Pricing**: Fast response requirements
- **Cache Strategy**: Pricing rule caching
- **Algorithm Optimization**: Efficient calculation methods

## Integration Points

### Carpool Service Architecture
- **Ride Matching**: Price influences ride matching
- **Payment Processing**: Price feeds into payment system
- **Driver Compensation**: Price affects driver earnings
- **User Experience**: Price transparency for riders

### External Services
- **Mapping Services**: Distance validation
- **Currency Services**: Exchange rate integration
- **Market Data**: Competitive pricing analysis

## Security Considerations

### Authentication Requirements
- **User Authentication**: JWT token validation
- **Request Authorization**: User-specific pricing
- **Rate Limiting**: Prevent pricing abuse

### Data Validation
- **Parameter Sanitization**: Clean input validation
- **Country Validation**: Supported country verification
- **Distance Limits**: Reasonable distance bounds

## Error Code Reference

### Code 10001: Validation Error
- **Missing Parameters**: Required fields not provided
- **Invalid Values**: Parameter format or range errors
- **Country Support**: Unsupported country codes

### Code 10003: Authentication Error
- **Missing Token**: Authorization header required
- **Invalid Token**: Token validation failure
- **Expired Token**: Token refresh required

## Future Test Enhancements

### Extended Coverage
- **Multiple Countries**: Test various country pricing
- **Distance Ranges**: Test short and long distance pricing
- **Currency Validation**: Verify country-currency mapping

### Advanced Scenarios
- **Dynamic Pricing**: Test time-based price variations
- **Surge Pricing**: Test demand-based adjustments
- **Group Pricing**: Test multi-passenger scenarios

### Performance Testing
- **Load Testing**: High-volume pricing requests
- **Response Time**: Pricing calculation speed
- **Concurrent Users**: Multiple simultaneous requests

## Maintenance Notes

### Pricing Algorithm Updates
- **Rate Changes**: Update pricing formulas
- **Currency Updates**: New country support
- **Market Adjustments**: Competitive rate updates

### Test Maintenance
- **Data Currency**: Keep test data relevant
- **Price Validation**: Update expected price ranges
- **Country Support**: Add new country test cases

### Integration Monitoring
- **Service Health**: Monitor pricing service availability
- **Accuracy Validation**: Ensure pricing accuracy
- **Performance Tracking**: Monitor response times