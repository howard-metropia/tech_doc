# AuthorizeNet.py

🔍 **Quick Summary (TL;DR)**
- Comprehensive Authorize.Net payment gateway integration providing secure credit card processing with AIM API support for Web2py applications
- Core functionality: payment processing | credit card transactions | Authorize.Net API | AIM integration | secure payments | transaction management
- Primary use cases: E-commerce transactions, subscription billing, credit card validation, payment gateway integration
- Quick compatibility: Python 2.7+/3.x, Authorize.Net merchant account, Web2py framework, HTTPS connectivity

❓ **Common Questions Quick Index**
- Q: What payment types are supported? A: [Technical Specifications](#technical-specifications) - Credit cards via AIM API
- Q: How to process a basic payment? A: [Usage Methods](#usage-methods) - Use process() function with card details
- Q: Is this secure for production? A: [Important Notes](#important-notes) - Yes, uses HTTPS and test/production modes
- Q: What transaction types are available? A: [Detailed Code Analysis](#detailed-code-analysis) - AUTH_CAPTURE, AUTH_ONLY, CREDIT, etc.
- Q: How to handle test transactions? A: [Output Examples](#output-examples) - Use testmode=True parameter
- Q: What if a payment is declined? A: [Output Examples](#output-examples) - Check isDeclined() method
- Q: How to set billing information? A: [Usage Methods](#usage-methods) - Use setParameter() for customer data
- Q: How to troubleshoot failures? A: [Important Notes](#important-notes) - Check API credentials and network connectivity

📋 **Functionality Overview**
- **Non-technical explanation:** Like a digital cash register that securely processes credit card payments - imagine a store checkout system that talks to the bank to approve or decline purchases, handles different card types, and keeps transaction records. This module provides all the technical plumbing to make online payments work safely.
- **Technical explanation:** Full-featured Authorize.Net AIM (Advanced Integration Method) API wrapper that handles credit card processing, transaction management, and secure communication with payment gateways.
- Business value: Enables secure e-commerce functionality, reduces PCI compliance burden, provides reliable payment processing for revenue generation
- Context: Core payment processing component for Web2py applications requiring credit card transaction capabilities

🔧 **Technical Specifications**
- File: AuthorizeNet.py, /gluon/contrib/, Python, Payment gateway integration, ~8KB, High complexity
- Dependencies: urllib (HTTP requests), operator (namedtuple functionality), gluon._compat (Web2py compatibility)
- Compatibility: Python 2.7+/3.x, Authorize.Net merchant account, PCI DSS compliance environment
- Configuration: API login ID, transaction key, test/production mode selection
- System requirements: HTTPS connectivity, valid Authorize.Net merchant account, SSL/TLS support
- Security: HTTPS communication, encrypted data transmission, test environment isolation

📝 **Detailed Code Analysis**
```python
class AIM:
    def __init__(self, login, transkey, testmode=False):
        # Initialize with merchant credentials
        self.parameters = {
            'x_login': login,
            'x_tran_key': transkey,
            'x_version': '3.1',
            'x_method': 'CC',
            'x_type': 'AUTH_CAPTURE'  # Default transaction type
        }
        
    def process(self):
        # Select appropriate endpoint
        if self.testmode:
            url = 'https://test.authorize.net/gateway/transact.dll'
        else:
            url = 'https://secure.authorize.net/gateway/transact.dll'
        
        # Send request and parse response
        encoded_args = urlencode(self.parameters)
        response = urlopen(url, encoded_args).read()
        self.results = response.split(self.delimiter)
```

**Transaction Processing Flow:**
```python
def setTransaction(self, creditcard, expiration, total, cvv=None, tax=None, invoice=None):
    # Validate required parameters
    if not creditcard or not expiration or not total:
        raise AIM.AIMError('Missing required transaction parameters')
    
    # Set transaction parameters
    self.setParameter('x_card_num', creditcard)
    self.setParameter('x_exp_date', expiration)
    self.setParameter('x_amount', total)
    
    # Optional security and billing parameters
    if cvv:
        self.setParameter('x_card_code', cvv)
```

**Response Handling:**
```python
def process(self):
    # Parse delimited response into named tuple
    Results = namedtuple('Results', 'ResultResponse ResponseSubcode ResponseCode ...')
    self.response = Results(*self.results[0:40])
    
    # Determine transaction status
    if self.getResultResponseFull() == 'Approved':
        self.success = True
    elif self.getResultResponseFull() == 'Declined':
        self.declined = True
    else:
        raise AIM.AIMError(self.response.ResponseText)
```

**Design Patterns:** Gateway pattern, Builder pattern for parameters, Exception handling for API errors
**Performance:** Single HTTP request per transaction, ~200-500ms response time typical
**Security:** HTTPS encryption, sensitive data not logged, test mode isolation

🚀 **Usage Methods**
```python
# Basic payment processing
from gluon.contrib.AuthorizeNet import AIM, process

# Using the simplified process function
success = process(
    creditcard='4111111111111111',  # Test card
    expiration='1225',
    total='29.99',
    cvv='123',
    login='your_login',
    transkey='your_key',
    testmode=True
)

# Using the AIM class directly
payment = AIM('your_login', 'your_transkey', testmode=True)
payment.setTransaction('4111111111111111', '1225', '29.99', cvv='123')
payment.setParameter('x_first_name', 'John')
payment.setParameter('x_last_name', 'Doe')
payment.setParameter('x_email', 'john@example.com')

try:
    payment.process()
    if payment.isApproved():
        print(f"Payment approved! Transaction ID: {payment.response.TransactionID}")
    elif payment.isDeclined():
        print("Payment declined by bank")
    else:
        print("Payment error occurred")
except AIM.AIMError as e:
    print(f"Payment processing error: {e}")
```

**Transaction Types:**
```python
# Different transaction types
payment.setTransactionType('AUTH_CAPTURE')  # Authorize and capture
payment.setTransactionType('AUTH_ONLY')     # Authorize only
payment.setTransactionType('CREDIT')        # Refund
payment.setTransactionType('VOID')          # Void transaction
```

**Advanced Configuration:**
```python
# Full billing and shipping information
payment.setParameter('x_address', '123 Main St')
payment.setParameter('x_city', 'Anytown')
payment.setParameter('x_state', 'CA')
payment.setParameter('x_zip', '12345')
payment.setParameter('x_invoice_num', 'INV-001')
payment.setParameter('x_description', 'Product purchase')
```

📊 **Output Examples**
**Successful Transaction:**
```python
>>> payment.process()
>>> payment.isApproved()
True
>>> print(payment.response.TransactionID)
'2345678901'
>>> print(payment.response.AuthCode)
'ABC123'
>>> print(payment.response.AVSResponse)
'Y'  # Address verification passed
```

**Transaction Response Details:**
```python
>>> payment.response.ResponseCode
'1'  # Approved
>>> payment.response.ResponseText
'This transaction has been approved.'
>>> payment.response.Amount
'29.99'
>>> payment.response.PaymentMethod
'CC'
```

**Declined Transaction:**
```python
>>> payment.process()
>>> payment.isDeclined()
True
>>> print(payment.response.ResponseText)
'This transaction has been declined.'
>>> print(payment.response.ResponseCode)
'2'
```

**Error Scenarios:**
```python
>>> payment.process()
AIM.AIMError: A valid amount is required.

>>> payment.isError()
True
>>> print(payment.response.ResponseText)
'Missing or invalid payment information.'
```

**Test Card Numbers:**
```python
# Authorize.Net test cards
VISA_TEST = '4111111111111111'
MASTERCARD_TEST = '5555555555554444'
AMEX_TEST = '370000000000002'
DISCOVER_TEST = '6011000000000012'
```

⚠️ **Important Notes**
- **PCI Compliance:** Never store credit card numbers or CVV codes in logs or databases
- **Test vs Production:** Always use testmode=True during development, never test with real card numbers in production
- **API Credentials:** Protect login and transaction key credentials, use environment variables
- **Network Security:** Requires HTTPS for production, validate SSL certificates
- **Transaction Limits:** Respect Authorize.Net daily/monthly transaction limits
- **Error Handling:** Always implement proper error handling for network timeouts and API errors

**Common Troubleshooting:**
- Invalid credentials → Verify login ID and transaction key in Authorize.Net account
- Network timeout → Check internet connectivity and Authorize.Net service status
- Invalid card → Verify card number format and test card usage in test mode
- Amount errors → Ensure amount format is decimal with 2 places (e.g., '10.00')
- AVS mismatch → Verify billing address matches card on file

🔗 **Related File Links**
- Authorize.Net API documentation for AIM integration
- PCI DSS compliance guidelines for payment processing
- Web2py payment controller implementations
- SSL certificate configuration for secure transactions
- Payment logging and audit trail implementations
- Error handling and retry logic for payment failures

📈 **Use Cases**
- **E-commerce Checkout:** Process customer purchases with credit card payments
- **Subscription Billing:** Recurring payment processing for subscription services
- **Invoice Payment:** Allow customers to pay invoices online
- **Donation Processing:** Accept charitable donations through website
- **Event Registration:** Process payments for event tickets and registrations
- **Service Payments:** Accept payments for professional services

🛠️ **Improvement Suggestions**
- **Retry Logic:** Implement automatic retry for transient network failures
- **Tokenization:** Add support for Authorize.Net customer payment profiles
- **Webhook Integration:** Implement webhook handling for payment notifications
- **Analytics Integration:** Add payment metrics and reporting capabilities
- **Multi-Currency:** Extend support for international currencies
- **Mobile Optimization:** Add mobile-specific payment optimizations
- **Fraud Detection:** Integrate with Authorize.Net fraud detection services

🏷️ **Document Tags**
- Keywords: payment processing, Authorize.Net, AIM API, credit card, e-commerce, secure transactions, payment gateway, PCI compliance, financial transactions, Web2py payments
- Technical tags: #payment-gateway #authorizenet #credit-card-processing #ecommerce #secure-payments #web2py-contrib
- Target roles: Payment developers (expert), E-commerce developers (advanced), Financial systems engineers (expert)
- Difficulty level: ⭐⭐⭐⭐ - Requires understanding of payment processing, security, and financial regulations
- Maintenance level: Medium - Requires updates for API changes and security patches
- Business criticality: Critical - Direct impact on revenue and customer transactions
- Related topics: Payment processing, PCI compliance, financial integrations, e-commerce security, transaction management