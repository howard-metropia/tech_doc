# testStripeFunctionalities.py - Stripe Payment Integration Testing Documentation

## File Overview
**Path:** `/applications/portal/tests/testStripeFunctionalities.py`
**Purpose:** Comprehensive unit tests for Stripe payment integration functionality, testing customer management, card operations, and payment method handling in the portal application.

## Functionality Overview
This module contains extensive unit tests for Stripe payment processing functionality imported from the wallet controller. It tests customer creation, card management, payment method operations, and default card settings using both live Stripe API integration and test data.

## Key Components

### Test Class

#### `TestStripeFunctionalities(unittest.TestCase)`
Main test class that inherits from unittest.TestCase to provide testing infrastructure for Stripe payment functionality.

**Class Variables:**
- **`user_id`**: Set to 1007 (hardcoded test user for payment operations)

**Methods:**

##### `init(self)`
- **Purpose:** Initializes instance variables for storing Stripe customer data
- **Variables:**
  - `self.cucstomer_id`: Stores customer ID (note: appears to have typo, should be customer_id)
- **Note:** Uses non-standard `init` instead of `__init__`

##### `setUp(self)`
- **Purpose:** Sets up test fixtures before each test method execution
- **Operations:**
  - Retrieves customer ID for the test user using `_get_customer_id(user_id)`
  - Stores customer ID for use in test methods
- **Customer Management:** Establishes connection to existing Stripe customer

##### `testGetCardSetting(self)`
- **Purpose:** Tests the complete card retrieval and settings workflow
- **Test Flow:**
  1. Validates customer_id is not None and has content
  2. Retrieves customer object using `_get_customer(customer_id)`
  3. Validates customer object and customer.id
  4. Gets payment methods using `_get_payments(customer.id)`
  5. Validates payments list exists and has content
  6. Retrieves cards using `_get_cards(customer, payments)`
  7. Validates cards list exists and has content

##### `testAddAndDeleteNewCard(self)`
- **Purpose:** Tests the complete card addition and deletion workflow
- **Test Flow:**
  1. Sets up Stripe API key from configuration
  2. Gets current customer and payment methods
  3. Deletes existing test cards (ending in '4242')
  4. Counts initial payment methods
  5. Adds new card using test token 'tok_visa'
  6. Validates payment count increased by 1
  7. Deletes the newly added test card
  8. Validates payment count decreased by 1

##### `testSetDefaultCard(self)`
- **Purpose:** Tests setting a payment method as the default card
- **Test Flow:**
  1. Sets up Stripe API key and gets customer data
  2. Deletes existing test cards (ending in '4242')
  3. Adds new test card using 'tok_visa' token
  4. Sets the new card as default using `_set_default_card()`
  5. Validates that customer.default_source matches the set card

## Dependencies

### External Libraries
- **`unittest`**: Python's built-in testing framework
- **`stripe`**: Stripe Python SDK for payment processing
- **`datetime`**: For timestamp operations (imported but used in commented code)

### Internal Modules
- **`gluon.globals.Request`**: web2py request context
- **Wallet Controller Functions**: Imported via exec from wallet.py
  - `_get_customer_id()`: Retrieve customer ID for user
  - `_get_customer()`: Get Stripe customer object
  - `_get_payments()`: Get customer payment methods
  - `_get_cards()`: Extract card information from payments
  - `_create_new_card()`: Add new payment method
  - `_delete_card()`: Remove payment method
  - `_set_default_card()`: Set default payment method

### Configuration Dependencies
- **`configuration`**: Configuration object for Stripe API key access
- **Stripe API Key**: Retrieved via `configuration.get('stripe.api_key')`

## Stripe Integration Testing

### Test Environment Setup
```python
import stripe
stripe.api_key = configuration.get('stripe.api_key')
```

### Test Payment Methods
- **Test Token**: 'tok_visa' (Stripe test token for Visa cards)
- **Test Card Identifier**: Cards ending in '4242' (common Stripe test card)
- **Customer ID**: Retrieved dynamically for test user 1007

## Test Data Management

### Test User Configuration
- **User ID**: 1007 (hardcoded test user)
- **Customer Lookup**: Uses existing Stripe customer for this user
- **Test Cards**: Uses Stripe test tokens and identifies by last4 digits

### Card Management Testing
```python
# Pattern for test card cleanup
for payment in payments:
    if payment.card.last4 == '4242':
        customer = _delete_card(customer_id, payment.id)
```

## Business Logic Testing

### Customer Management Workflow
1. **Customer Retrieval**: Get customer ID from user ID
2. **Customer Validation**: Ensure customer exists in Stripe
3. **Payment Method Access**: Retrieve all payment methods
4. **Card Information**: Extract card details from payments

### Card Operations Workflow
1. **Cleanup**: Remove existing test cards
2. **Addition**: Add new card using test token
3. **Validation**: Verify card was added successfully
4. **Deletion**: Remove test card after validation
5. **Count Verification**: Ensure payment counts are correct

### Default Card Management
1. **Setup**: Ensure clean test environment
2. **Card Addition**: Add new test card
3. **Default Setting**: Set new card as default
4. **Validation**: Verify default_source matches set card

## Integration with web2py Framework

### Controller Integration
```python
# Imports wallet controller functions
exec(open("applications/portal/controllers/wallet.py").read(), globals())
```

### Configuration Access
- Uses web2py configuration system for Stripe API key
- Integrates with portal application's payment infrastructure
- Tests real wallet controller functions used in production

## Stripe API Integration

### Live API Testing
- Tests use real Stripe API calls (not mocked)
- Requires valid Stripe test API key in configuration
- Uses Stripe test tokens to avoid real charges
- Validates actual API responses and behaviors

### Payment Method Operations
- **Creation**: Tests adding new payment methods
- **Deletion**: Tests removing payment methods
- **Listing**: Tests retrieving payment methods
- **Default Setting**: Tests changing default payment method

## Error Handling and Validation

### Assertion Testing
```python
# Customer validation
self.assertIsNotNone(customer_id)
self.assertGreater(len(customer_id), 0)

# Payment count validation
self.assertEqual(payments_count2, payments_count1 + 1)
self.assertEqual(payments_count3, payments_count2 - 1)

# Default card validation
self.assertEqual(customer.default_source, default_payment)
```

### Test Robustness
- Validates each step of payment operations
- Ensures proper cleanup of test data
- Tests both positive and state-change scenarios
- Verifies API response integrity

## Performance and Scale Considerations

### Test Execution Characteristics
- **API Calls**: Multiple Stripe API calls per test method
- **Rate Limiting**: Subject to Stripe API rate limits
- **Network Dependency**: Requires internet connectivity
- **Test Data Cleanup**: Performs cleanup operations for each test

### Stripe API Efficiency
- Uses efficient payment method retrieval
- Minimizes API calls through batch operations
- Implements proper test data cleanup
- Validates operations with minimal API overhead

## Security Testing Considerations

### Test Data Security
- Uses Stripe test tokens (not real payment data)
- Tests with designated test user (ID 1007)
- Validates API key configuration access
- Ensures test operations don't affect real customer data

### API Key Management
- Retrieves API key from secure configuration
- Uses test mode operations
- Validates proper authentication with Stripe
- Tests within Stripe's test environment

## Usage Examples

### Running Individual Tests
```python
# Run complete test suite
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestStripeFunctionalities))
unittest.TextTestRunner(verbosity=2).run(suite)

# Run specific test
python -m unittest testStripeFunctionalities.TestStripeFunctionalities.testGetCardSetting
```

### Integration Testing
```python
# Example test flow
customer_id = _get_customer_id(1007)
customer = _get_customer(customer_id)
payments = _get_payments(customer_id)
cards = _get_cards(customer, payments)
```

## Commented Test Code Analysis

### Customer Creation Test (Commented)
```python
# def testAddAccountWithToken(self):
#   # Test customer creation functionality
#   customer = _create_customer(email, full_name)
#   token = 'tok_visa'
#   customer = _create_new_card(customer.id, token)
```
- **Purpose**: Would test customer creation from scratch
- **Status**: Currently commented out (possibly for debugging)
- **Functionality**: Tests complete customer onboarding workflow

## Integration Points

### Portal Application
- Tests core payment functionality used throughout the portal
- Validates wallet controller operations
- Ensures Stripe integration reliability
- Tests real payment workflows used by customers

### Stripe Payment System
- Tests live integration with Stripe API
- Validates payment method management
- Ensures proper customer data handling
- Tests default payment method functionality

### Configuration System
- Tests secure API key retrieval
- Validates configuration management
- Ensures proper environment setup
- Tests integration with web2py configuration

## Error Scenarios and Edge Cases

### Potential Failure Points
- **Stripe API Unavailability**: Network or service issues
- **Configuration Missing**: API key not properly configured
- **Customer Not Found**: Test user doesn't have Stripe customer
- **Rate Limiting**: Too many API calls in test execution
- **Test Data Conflicts**: Existing test cards interfere with tests

### Test Reliability
- Implements cleanup before and after operations
- Uses specific test identifiers (last4 = '4242')
- Validates each operation step
- Provides clear assertion messages

## File Execution
- Executed through unittest framework with custom test suite
- Requires Stripe API key configuration
- Tests live Stripe integration functionality
- Provides detailed test output with verbosity=2
- Supports continuous integration with proper API key setup