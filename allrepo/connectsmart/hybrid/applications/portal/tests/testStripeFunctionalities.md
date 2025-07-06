# testStripeFunctionalities.py

🔍 **Quick Summary (TL;DR)**
- Comprehensive unit test suite for Stripe payment gateway integration, validating card management operations including retrieval, addition, deletion, and default card settings
- Core functionality: unittest | Stripe API | payment processing | card management | integration testing | financial transactions
- Primary use cases: Testing payment card operations, validating Stripe integration, ensuring payment system reliability
- Quick compatibility: Python unittest, Stripe Python SDK, Web2py framework, requires valid Stripe API credentials

❓ **Common Questions Quick Index**
- Q: What Stripe operations are tested? A: [Functionality Overview](#functionality-overview) - Card retrieval, addition, deletion, default setting
- Q: What user ID is used for testing? A: [Technical Specifications](#technical-specifications) - User ID 1007 for all operations
- Q: How to run these tests safely? A: [Important Notes](#important-notes) - Use Stripe test environment with test tokens
- Q: What test cards are used? A: [Detailed Code Analysis](#detailed-code-analysis) - tok_visa token with 4242 last four digits
- Q: How to troubleshoot API failures? A: [Important Notes](#important-notes) - Check API keys and test environment setup
- Q: What's the test execution flow? A: [Usage Methods](#usage-methods) - setUp gets customer, tests run operations, cleanup
- Q: What if payment methods exist? A: [Output Examples](#output-examples) - Tests clean up existing 4242 cards first
- Q: How are assertions structured? A: [Detailed Code Analysis](#detailed-code-analysis) - Validates counts, IDs, and state changes

📋 **Functionality Overview**
- **Non-technical explanation:** Like testing a digital wallet's credit card management features - imagine ensuring a mobile payment app can properly add cards, remove cards, and set a default payment method. This test suite validates all these operations work correctly with the payment processor.
- **Technical explanation:** Comprehensive integration test suite that validates Stripe payment gateway functionality including customer retrieval, payment method management, and card operations within the Web2py application framework.
- Business value: Ensures payment system reliability, prevents transaction failures, and validates critical financial operations
- Context: Part of the wallet controller testing within the portal application, essential for e-commerce and payment functionality

🔧 **Technical Specifications**
- File: testStripeFunctionalities.py, /applications/portal/tests/, Python, Test file, ~3KB, High complexity
- Dependencies: unittest (Python standard), stripe (Stripe Python SDK), wallet.py controller, gluon.globals
- Compatibility: Python 2.7+/3.x, Stripe API v2+, Web2py framework, requires active Stripe account
- Configuration: Uses configuration.get('stripe.api_key'), hardcoded user_id = 1007, test tokens
- System requirements: Stripe API access, wallet controller module, valid API credentials
- Security: Uses Stripe test environment, test tokens only, no real financial transactions

📝 **Detailed Code Analysis**
```python
class TestStripeFunctionalities(unittest.TestCase):
    def setUp(self):
        # Get customer ID for test user 1007
        self.customer_id = _get_customer_id(user_id)
    
    def testGetCardSetting(self):
        # Validate customer exists and has payment methods
        customer_id = self.customer_id
        self.assertIsNotNone(customer_id)
        customer = _get_customer(customer_id)
        payments = _get_payments(customer.id)
        cards = _get_cards(customer, payments)
        
        # Assert all components are valid
        self.assertIsNotNone(cards)
        self.assertGreater(len(cards), 0)
```

**Card Management Flow:**
```python
def testAddAndDeleteNewCard(self):
    # 1. Clean existing test cards
    for payment in payments:
        if payment.card.last4 == '4242':
            customer = _delete_card(customer_id, payment.id)
    
    # 2. Add new test card
    token_id = 'tok_visa'  # Stripe test token
    customer = _create_new_card(customer_id, token_id)
    
    # 3. Validate card count increased
    payments_count2 = len(_get_payments(customer_id))
    self.assertEqual(payments_count2, payments_count1 + 1)
    
    # 4. Clean up - remove test card
    customer = _delete_card(customer_id, payment.id)
```

**Default Card Management:**
```python
def testSetDefaultCard(self):
    # Add test card and set as default
    customer = _create_new_card(customer_id, 'tok_visa')
    customer = _set_default_card(customer_id, payment.id)
    self.assertEqual(customer.default_source, default_payment)
```

**Design Patterns:** Integration testing with setup/teardown, state validation, cleanup operations
**Error Handling:** Stripe API exceptions bubble up, assertion failures for validation
**Resource Management:** Automatic cleanup of test cards to prevent pollution

🚀 **Usage Methods**
```python
# Basic execution (requires Stripe test environment)
python testStripeFunctionalities.py

# Run specific test methods
python -m unittest testStripeFunctionalities.TestStripeFunctionalities.testGetCardSetting

# Run with verbose output for detailed Stripe operations
python -m unittest -v testStripeFunctionalities.TestStripeFunctionalities

# Integration with test suite
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestStripeFunctionalities))
unittest.TextTestRunner(verbosity=2).run(suite)
```

**Environment Configuration:**
```python
# Required configuration in Web2py
configuration = {
    'stripe.api_key': 'sk_test_...',  # Stripe test secret key
    'stripe.publishable_key': 'pk_test_...',  # Stripe test publishable key
}

# Test environment setup
import stripe
stripe.api_key = configuration.get('stripe.api_key')
```

**Test Data Requirements:**
- User ID 1007 must exist in system
- Customer must have valid Stripe customer ID
- Test tokens: 'tok_visa' for Visa test card (4242 4242 4242 4242)

📊 **Output Examples**
**Successful Test Execution:**
```
testGetCardSetting (testStripeFunctionalities.TestStripeFunctionalities) ... ok
testAddAndDeleteNewCard (testStripeFunctionalities.TestStripeFunctionalities) ... ok
testSetDefaultCard (testStripeFunctionalities.TestStripeFunctionalities) ... ok

----------------------------------------------------------------------
Ran 3 tests in 4.567s

OK
```

**Card Addition Flow:**
```python
# Before addition: 2 existing payment methods
# After addition: 3 payment methods (count + 1)
# After deletion: 2 payment methods (back to original)

# Test card details:
# Token: tok_visa
# Last 4 digits: 4242
# Brand: Visa
# Test card: 4242 4242 4242 4242
```

**Stripe API Response Example:**
```python
# Customer object
{
  'id': 'cus_test123',
  'default_source': 'card_test456',
  'sources': {...}
}

# Payment method object
{
  'id': 'pm_test789',
  'card': {
    'last4': '4242',
    'brand': 'visa'
  }
}
```

**Test Failure Scenarios:**
```
FAIL: testGetCardSetting - Customer ID is None
FAIL: testAddAndDeleteNewCard - Card count mismatch after addition
FAIL: testSetDefaultCard - Default source not updated correctly
```

⚠️ **Important Notes**
- **Test Environment Only:** Must use Stripe test API keys, never production keys in testing
- **Financial Safety:** All operations use test tokens, no real money transactions
- **API Rate Limits:** Stripe has rate limits, tests may fail if executed too frequently
- **Customer Dependency:** Requires user 1007 to have valid Stripe customer record
- **Cleanup Responsibility:** Tests clean up test cards but may leave data if assertions fail
- **API Key Security:** Store API keys securely, never commit to version control

**Common Troubleshooting:**
- Invalid API key → Verify test API key configuration and Stripe account access
- Customer not found → Ensure user 1007 exists and has associated Stripe customer
- Card already exists → Test cleanup may have failed, manually remove test cards
- Rate limit exceeded → Wait before re-running tests or implement rate limiting
- Network timeout → Check internet connection and Stripe API status

🔗 **Related File Links**
- `applications/portal/controllers/wallet.py` - Contains tested Stripe integration functions
- Stripe API documentation for payment methods and customers
- Web2py configuration files for API key management
- Other payment-related test files for comprehensive coverage
- Stripe webhook handling code for real-time payment updates
- Error handling documentation for Stripe API exceptions

📈 **Use Cases**
- **Payment Integration Testing:** Validate Stripe integration before deployment
- **Regression Testing:** Ensure payment features work after code changes
- **API Compatibility:** Test Stripe API version compatibility and updates
- **Error Handling Validation:** Verify proper handling of payment failures
- **Security Testing:** Validate secure handling of payment information
- **Performance Testing:** Measure payment operation response times

🛠️ **Improvement Suggestions**
- **Mock Integration:** Use Stripe test fixtures to reduce API dependency and improve speed
- **Parameterized Testing:** Test multiple user scenarios and card types dynamically
- **Error Case Testing:** Add tests for invalid tokens, failed payments, and API errors
- **Performance Monitoring:** Add timing assertions for payment operation performance
- **Security Validation:** Test PCI compliance and secure data handling
- **Webhook Testing:** Add tests for Stripe webhook event handling
- **Cleanup Automation:** Implement automatic cleanup of all test data regardless of test outcome

🏷️ **Document Tags**
- Keywords: unittest, Stripe integration, payment testing, card management, financial transactions, API testing, e-commerce, payment gateway, test tokens, integration testing
- Technical tags: #unittest #stripe-api #payment-testing #integration-test #financial-api #card-management
- Target roles: Backend developers (advanced), Payment engineers (expert), QA engineers (intermediate)
- Difficulty level: ⭐⭐⭐⭐ - Requires understanding of payment systems, Stripe API, and financial testing
- Maintenance level: High - Requires updates with Stripe API changes and security requirements
- Business criticality: Critical - Payment system failures directly impact revenue and user experience
- Related topics: Payment processing, Stripe API, financial integrations, PCI compliance, e-commerce testing