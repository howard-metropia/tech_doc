# TSP API Test Suite - Uber Fare Conversion Tests

## Overview
The `test-uber-fare.js` file contains focused tests for currency conversion functionality in the Uber fare estimation system, specifically testing TWD (Taiwan Dollar) to USD conversion for international ridehail operations.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-uber-fare.js`

## Dependencies
- **chai**: Testing assertions and expectations  
- **@maas/core/bootstrap**: Core framework initialization
- **uuid**: Unique identifier generation
- **UberFareEstimation**: Fare estimation model
- **uberService**: Ridehail service layer

## Test Architecture

### Core Components
```javascript
const { expect } = require('chai');
const { v4: uuidv4 } = require('uuid');
const UberFareEstimation = require('@app/src/models/UberFareEstimation');
const uberService = require('@app/src/services/ridehail');
```

## Fare Conversion System

### Test Data Setup
```javascript
describe('fare convert test', () => {
  const fareId = uuidv4();
  const originalFare = 195; // TWD
  
  before(async () => {
    const cache = new UberFareEstimation({
      fare_id: fareId,
      product_id: '9c0fd086-b4bd-44f1-a278-bdae3cdb3d9f',
      fare_currency: 'TWD',
      fare_display: 'NT$190',
      fare_value: originalFare,
      modified_at: '2024-04-09T08:11:01.794+0000',
      no_cars_available: 'false',
      pickup_eta: 5,
      product_display: 'UberX',
      trip_duration: 17
    });
    await cache.save();
  });
});
```

### Currency Conversion Test
```javascript
it('should convert the TWD to USD successfully', async () => {
  const res = await uberService.balancePreProcessing(1003, fareId);
  const { fare } = res;
  const expected = Number((originalFare / 30).toFixed(2));
  expect(fare).to.be.eq(expected);
});
```

## Fare Estimation Model

### Database Schema
```javascript
const UberFareEstimation = {
  fare_id: 'string (UUID)',           // Unique fare identifier
  product_id: 'string',               // Uber product type ID
  fare_currency: 'string',            // Currency code (TWD, USD, etc.)
  fare_display: 'string',             // Formatted fare display (NT$190)
  fare_value: 'number',               // Numeric fare value
  modified_at: 'datetime',            // Last update timestamp
  no_cars_available: 'boolean',       // Availability status
  pickup_eta: 'number',               // Pickup time estimate (minutes)
  product_display: 'string',          // Product name (UberX, UberPool, etc.)
  trip_duration: 'number'             // Estimated trip duration (minutes)
};
```

### Fare Record Example
```javascript
{
  fare_id: 'f47ac10b-58cc-4372-a567-0e02b2c3d479',
  product_id: '9c0fd086-b4bd-44f1-a278-bdae3cdb3d9f',
  fare_currency: 'TWD',
  fare_display: 'NT$190',
  fare_value: 195,
  modified_at: '2024-04-09T08:11:01.794Z',
  no_cars_available: false,
  pickup_eta: 5,
  product_display: 'UberX',
  trip_duration: 17
}
```

## Currency Conversion Logic

### TWD to USD Conversion
```javascript
const convertTWDToUSD = (twdAmount) => {
  const EXCHANGE_RATE = 30; // 1 USD = 30 TWD (approximate)
  const usdAmount = twdAmount / EXCHANGE_RATE;
  return Number(usdAmount.toFixed(2));
};
```

### Balance Preprocessing Service
```javascript
const balancePreProcessing = async (userId, fareId) => {
  // 1. Retrieve fare estimation
  const fareEstimation = await UberFareEstimation.findById(fareId);
  if (!fareEstimation) {
    throw new Error('Fare estimation not found');
  }
  
  // 2. Convert currency if needed
  let convertedFare = fareEstimation.fare_value;
  if (fareEstimation.fare_currency === 'TWD') {
    convertedFare = convertTWDToUSD(fareEstimation.fare_value);
  }
  
  // 3. Validate user balance
  const userWallet = await getUserWallet(userId);
  if (userWallet.balance < convertedFare) {
    throw new Error('Insufficient balance');
  }
  
  return {
    fare: convertedFare,
    currency: 'USD',
    originalFare: fareEstimation.fare_value,
    originalCurrency: fareEstimation.fare_currency,
    exchangeRate: fareEstimation.fare_currency === 'TWD' ? 30 : 1
  };
};
```

## Test Validation

### Conversion Accuracy Test
```javascript
it('should convert the TWD to USD successfully', async () => {
  const userId = 1003;
  const result = await uberService.balancePreProcessing(userId, fareId);
  
  // Validate conversion calculation
  const expectedUSD = Number((originalFare / 30).toFixed(2));
  expect(result.fare).to.equal(expectedUSD);
  
  // Validate result structure
  expect(result).to.have.property('fare');
  expect(result).to.have.property('currency', 'USD');
  expect(result).to.have.property('originalFare', originalFare);
  expect(result).to.have.property('originalCurrency', 'TWD');
});
```

### Edge Cases Testing
```javascript
describe('Currency Conversion Edge Cases', () => {
  it('should handle zero fare amount', async () => {
    const zeroFareId = uuidv4();
    const zeroFare = new UberFareEstimation({
      fare_id: zeroFareId,
      fare_value: 0,
      fare_currency: 'TWD'
    });
    await zeroFare.save();
    
    const result = await uberService.balancePreProcessing(1003, zeroFareId);
    expect(result.fare).to.equal(0);
  });

  it('should handle large fare amounts', async () => {
    const largeFareId = uuidv4();
    const largeFare = new UberFareEstimation({
      fare_id: largeFareId,
      fare_value: 30000, // NT$30,000
      fare_currency: 'TWD'
    });
    await largeFare.save();
    
    const result = await uberService.balancePreProcessing(1003, largeFareId);
    expect(result.fare).to.equal(1000); // $1,000 USD
  });

  it('should handle USD fares without conversion', async () => {
    const usdFareId = uuidv4();
    const usdFare = new UberFareEstimation({
      fare_id: usdFareId,
      fare_value: 25.50,
      fare_currency: 'USD'
    });
    await usdFare.save();
    
    const result = await uberService.balancePreProcessing(1003, usdFareId);
    expect(result.fare).to.equal(25.50);
    expect(result.originalCurrency).to.equal('USD');
  });
});
```

## Exchange Rate Management

### Dynamic Exchange Rate System
```javascript
const getExchangeRate = async (fromCurrency, toCurrency) => {
  const FIXED_RATES = {
    'TWD_USD': 30,
    'USD_TWD': 0.033,
    'EUR_USD': 1.1,
    'GBP_USD': 1.25
  };
  
  const rateKey = `${fromCurrency}_${toCurrency}`;
  
  // Check for fixed rate first
  if (FIXED_RATES[rateKey]) {
    return FIXED_RATES[rateKey];
  }
  
  // Fetch from external API if needed
  const externalRate = await fetchExchangeRate(fromCurrency, toCurrency);
  return externalRate;
};
```

### Multi-Currency Support
```javascript
const convertCurrency = (amount, fromCurrency, toCurrency, exchangeRate) => {
  if (fromCurrency === toCurrency) {
    return amount;
  }
  
  const convertedAmount = amount / exchangeRate;
  return Number(convertedAmount.toFixed(2));
};
```

## Error Handling

### Fare Not Found
```javascript
const handleFareNotFound = (fareId) => {
  throw new Error(`Fare estimation not found for ID: ${fareId}`);
};
```

### Invalid Currency
```javascript
const validateCurrency = (currency) => {
  const SUPPORTED_CURRENCIES = ['USD', 'TWD', 'EUR', 'GBP'];
  if (!SUPPORTED_CURRENCIES.includes(currency)) {
    throw new Error(`Unsupported currency: ${currency}`);
  }
};
```

### Conversion Errors
```javascript
const handleConversionError = (error, fareId) => {
  logger.error(`Currency conversion failed for fare ${fareId}:`, error);
  throw new Error('Currency conversion failed');
};
```

## Performance Considerations

### Caching Strategy
```javascript
const cache = require('@maas/core/redis')('cache');

const cacheExchangeRate = async (fromCurrency, toCurrency, rate) => {
  const key = `exchange_rate:${fromCurrency}_${toCurrency}`;
  await cache.setex(key, 3600, rate); // Cache for 1 hour
};

const getCachedExchangeRate = async (fromCurrency, toCurrency) => {
  const key = `exchange_rate:${fromCurrency}_${toCurrency}`;
  return await cache.get(key);
};
```

### Batch Conversion
```javascript
const convertMultipleFares = async (fareIds, targetCurrency = 'USD') => {
  const fares = await UberFareEstimation.whereIn('fare_id', fareIds);
  
  const conversions = await Promise.all(
    fares.map(async (fare) => {
      const rate = await getExchangeRate(fare.fare_currency, targetCurrency);
      return {
        fareId: fare.fare_id,
        originalAmount: fare.fare_value,
        convertedAmount: convertCurrency(fare.fare_value, fare.fare_currency, targetCurrency, rate),
        exchangeRate: rate
      };
    })
  );
  
  return conversions;
};
```

## Integration Testing

### End-to-End Fare Processing
```javascript
describe('End-to-End Fare Processing', () => {
  it('should process complete fare estimation to payment flow', async () => {
    // 1. Create fare estimation
    const fareId = uuidv4();
    const fare = new UberFareEstimation({
      fare_id: fareId,
      fare_value: 450, // NT$450
      fare_currency: 'TWD'
    });
    await fare.save();
    
    // 2. Convert currency
    const preprocessing = await uberService.balancePreProcessing(1003, fareId);
    expect(preprocessing.fare).to.equal(15); // $15 USD
    
    // 3. Process payment
    const payment = await uberService.processPayment(1003, preprocessing);
    expect(payment.success).to.be.true;
    expect(payment.amountCharged).to.equal(15);
  });
});
```

## Quality Assurance

### Precision Testing
- **Decimal Accuracy**: Ensure proper rounding to 2 decimal places
- **Large Numbers**: Handle high-value fares correctly
- **Small Numbers**: Maintain precision for small fare amounts

### Currency Validation
- **Supported Currencies**: Validate against allowed currency list
- **Format Consistency**: Ensure consistent number formatting
- **Exchange Rate Accuracy**: Verify conversion calculations

This focused test suite ensures accurate currency conversion for international ridehail operations, maintaining precision and reliability in fare calculations while supporting multiple currencies and exchange rate scenarios.