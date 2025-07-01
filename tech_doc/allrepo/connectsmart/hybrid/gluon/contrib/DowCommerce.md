# DowCommerce.py

🔍 **Quick Summary (TL;DR)**
- DowCommerce payment gateway integration providing secure credit card processing with comprehensive billing and shipping information support for Web2py applications
- Core functionality: payment processing | DowCommerce API | credit card transactions | billing management | shipping info | transaction validation
- Primary use cases: E-commerce payments, online transactions, subscription billing, secure payment processing
- Quick compatibility: Python 2.7+/3.x, DowCommerce merchant account, Web2py framework, HTTPS connectivity

❓ **Common Questions Quick Index**
- Q: How does this differ from Authorize.Net? A: [Functionality Overview](#functionality-overview) - Different gateway with DowCommerce-specific API
- Q: What transaction types are supported? A: [Detailed Code Analysis](#detailed-code-analysis) - Sale, auth, credit transactions
- Q: How to handle demo mode? A: [Usage Methods](#usage-methods) - Set demomode=True with test credentials
- Q: What billing info can be captured? A: [Technical Specifications](#technical-specifications) - Full billing and shipping details
- Q: How to process a basic payment? A: [Usage Methods](#usage-methods) - Use setTransaction() and process() methods
- Q: What response codes indicate success? A: [Output Examples](#output-examples) - Response code '1' means approved
- Q: How to handle declined payments? A: [Output Examples](#output-examples) - Check isDeclined() method
- Q: Is this secure for production? A: [Important Notes](#important-notes) - Yes, uses HTTPS with proper credentials

📋 **Functionality Overview**
- **Non-technical explanation:** Like a digital payment terminal that connects to DowCommerce's payment processing network - imagine a point-of-sale system that can process credit cards, capture customer information, and handle different types of transactions (charges, refunds, authorizations) while keeping everything secure and compliant.
- **Technical explanation:** Comprehensive DowCommerce payment gateway integration providing secure credit card processing with support for detailed billing/shipping information, multiple transaction types, and comprehensive error handling.
- Business value: Enables secure payment processing for e-commerce, reduces PCI compliance burden, provides reliable transaction handling for revenue generation
- Context: Payment gateway alternative for Web2py applications requiring DowCommerce-specific integration instead of other payment processors

🔧 **Technical Specifications**
- File: DowCommerce.py, /gluon/contrib/, Python, Payment gateway integration, ~6KB, High complexity
- Dependencies: urllib (HTTP requests), operator (utility functions), gluon._compat (Web2py compatibility)
- Compatibility: Python 2.7+/3.x, DowCommerce merchant account, PCI DSS compliance environment
- Configuration: Username/password credentials, demo mode support, proxy configuration
- System requirements: HTTPS connectivity, valid DowCommerce merchant account, SSL/TLS support
- Security: HTTPS communication, encrypted credential transmission, test environment isolation

📝 **Detailed Code Analysis**
```python
class DowCommerce:
    def __init__(self, username=None, password=None, demomode=False):
        if not demomode:
            if not username or not password:
                raise DowCommerce.DowCommerceError('Missing credentials')
        else:
            # Demo mode with default test credentials
            username = 'demo'
            password = 'password'
        
        self.url = 'https://secure.dowcommerce.net/api/transact.php'
        self.parameters = {
            'username': username,
            'password': password
        }
```

**Transaction Processing:**
```python
def setTransaction(self, creditcard, expiration, total, cvv=None, 
                  orderid=None, orderdescription=None, ipaddress=None,
                  # Billing information
                  firstname=None, lastname=None, company=None,
                  address1=None, address2=None, city=None, state=None,
                  zipcode=None, country=None, phone=None, fax=None,
                  emailaddress=None, website=None,
                  # Shipping information  
                  shipping_firstname=None, shipping_lastname=None,
                  shipping_company=None, shipping_address1=None, ...):
    
    # Validate required parameters
    if not creditcard or not expiration or not total:
        raise DowCommerce.DowCommerceError('Missing required parameters')
    
    # Set core transaction data
    self.setParameter('ccnumber', creditcard)
    self.setParameter('ccexp', expiration)
    self.setParameter('amount', total)
```

**Response Processing:**
```python
def process(self):
    encoded_args = urlencode(self.parameters)
    results = str(urlopen(self.url, encoded_args).read()).split('&')
    
    # Parse key=value response format
    for result in results:
        (key, val) = result.split('=')
        self.results[key] = val
    
    # Determine transaction status
    if self.results['response'] == '1':    # Approved
        self.success = True
        self.error = False
        self.declined = False
    elif self.results['response'] == '2':  # Declined
        self.declined = True
        self.success = False
        self.error = False
    elif self.results['response'] == '3':  # Error
        self.error = True
        raise DowCommerce.DowCommerceError(self.results)
```

**Transaction Types:**
```python
def setTransactionType(self, transtype=None):
    types = ['sale', 'auth', 'credit']
    if transtype.lower() not in types:
        raise DowCommerce.DowCommerceError(f'Invalid transaction type: {transtype}')
    self.setParameter('type', transtype.lower())
```

**Design Patterns:** Gateway pattern, Builder pattern for transaction setup, Exception handling for API errors
**Performance:** Single HTTP request per transaction, synchronous processing
**Security:** HTTPS encryption, credential protection, parameter validation

🚀 **Usage Methods**
```python
# Basic payment processing
from gluon.contrib.DowCommerce import DowCommerce

# Demo mode for testing
payment = DowCommerce(demomode=True)
payment.setTransaction(
    creditcard='4111111111111111',  # Test Visa card
    expiration='1010',              # MMYY format
    total='25.99',
    cvv='999'
)

try:
    payment.process()
    if payment.isApproved():
        print("Payment approved!")
        print(f"Transaction details: {payment.getFullResponse()}")
    elif payment.isDeclined():
        print("Payment was declined")
    else:
        print("Payment error occurred")
except DowCommerce.DowCommerceError as e:
    print(f"Error: {e}")

# Production mode with real credentials
payment = DowCommerce(
    username='your_username',
    password='your_password'
)

# Comprehensive transaction with billing info
payment.setTransaction(
    creditcard='4111111111111111',
    expiration='1225',
    total='149.99',
    cvv='123',
    orderid='ORD-001',
    orderdescription='Product Purchase',
    ipaddress='192.168.1.100',
    # Billing information
    firstname='John',
    lastname='Doe',
    company='Acme Corp',
    address1='123 Main Street',
    address2='Suite 100',
    city='Anytown',
    state='CA',
    zipcode='90210',
    country='US',
    phone='555-123-4567',
    emailaddress='john@example.com',
    # Shipping information (if different)
    shipping_firstname='Jane',
    shipping_lastname='Doe',
    shipping_address1='456 Oak Avenue',
    shipping_city='Somewhere',
    shipping_state='NY',
    shipping_zipcode='10001'
)

# Different transaction types
payment.setTransactionType('sale')    # Immediate charge
payment.setTransactionType('auth')    # Authorization only
payment.setTransactionType('credit')  # Refund transaction
```

**Error Handling:**
```python
try:
    payment.process()
    if payment.isApproved():
        # Success handling
        transaction_id = payment.results.get('transactionid')
        auth_code = payment.results.get('authcode')
        save_transaction(transaction_id, auth_code)
    elif payment.isDeclined():
        # Decline handling
        reason = payment.getResponseText()
        log_declined_payment(reason)
    elif payment.isError():
        # Error handling
        error_msg = payment.getResponseText()
        log_payment_error(error_msg)
except DowCommerce.DowCommerceError as e:
    # API or validation error
    log_exception(str(e))
```

📊 **Output Examples**
**Successful Transaction:**
```python
>>> payment.process()
>>> payment.isApproved()
True
>>> payment.getFullResponse()
{
    'response': '1',
    'responsetext': 'SUCCESS',
    'authcode': 'ABC123',
    'transactionid': '2345678901',
    'avsresponse': 'Y',
    'cvvresponse': 'M',
    'orderid': 'ORD-001',
    'type': 'sale',
    'response_code': '100'
}
>>> payment.getResultResponseShort()
'Approved'
```

**Declined Transaction:**
```python
>>> payment.process()
>>> payment.isDeclined()
True
>>> payment.getResponseText()
'DECLINE'
>>> payment.getFullResponse()
{
    'response': '2',
    'responsetext': 'DECLINE',
    'authcode': '',
    'transactionid': '',
    'avsresponse': 'N',
    'cvvresponse': 'N'
}
```

**Error Response:**
```python
>>> payment.process()
DowCommerce.DowCommerceError: {'response': '3', 'responsetext': 'Invalid credit card number'}

>>> payment.isError()
True
>>> payment.getResponseText()
'Invalid credit card number'
```

**Test Card Numbers:**
```python
# DowCommerce test cards (from API documentation)
VISA_TEST = '4111111111111111'
MASTERCARD_TEST = '5431111111111111'
DISCOVER_TEST = '6011601160116611'
AMEX_TEST = '341111111111111'

# Test expiration: 10/10 (MMYY format)
# Test CVV: 999
# Minimum amount: > $1.00 (amounts < $1.00 will be declined)
```

⚠️ **Important Notes**
- **API Credentials:** Protect username/password credentials, use environment variables for production
- **Test Environment:** Always use demomode=True during development and testing
- **Transaction Limits:** Respect DowCommerce daily/monthly transaction limits and policies
- **Amount Validation:** DowCommerce may decline transactions under $1.00 in test mode
- **Response Parsing:** Always check transaction status before processing as successful
- **Error Handling:** Implement comprehensive error handling for network and API failures

**Common Troubleshooting:**
- Invalid credentials → Verify username/password in DowCommerce merchant account
- Network timeout → Check internet connectivity and DowCommerce service status
- Invalid card number → Verify card format and use proper test cards in demo mode
- Amount declined → Ensure amount is greater than $1.00 for test transactions
- Response parsing error → Check response format and handle missing fields

🔗 **Related File Links**
- DowCommerce API documentation and integration guides
- PCI DSS compliance guidelines for payment processing
- Web2py payment controller implementations
- SSL certificate configuration for secure transactions
- Payment logging and audit trail requirements
- Error handling and retry logic for payment processing

📈 **Use Cases**
- **E-commerce Platforms:** Process customer purchases with comprehensive billing capture
- **Subscription Services:** Handle recurring billing and payment updates
- **Digital Services:** Accept payments for online services and downloads
- **B2B Transactions:** Process business-to-business payments with detailed information
- **Invoice Processing:** Allow customers to pay invoices online
- **Event Registration:** Handle event ticket and registration payments

🛠️ **Improvement Suggestions**
- **Retry Logic:** Implement automatic retry for transient network failures
- **Response Caching:** Cache successful authorization codes for capture later
- **Webhook Support:** Add webhook handling for payment notifications if supported
- **Multi-Currency:** Extend support for international currencies and localization
- **Fraud Detection:** Integrate with fraud detection services for enhanced security
- **Analytics Integration:** Add payment metrics and reporting capabilities
- **Token Support:** Implement tokenization for stored payment methods if available

🏷️ **Document Tags**
- Keywords: DowCommerce payment gateway, credit card processing, e-commerce payments, billing information, shipping details, transaction processing, secure payments, Web2py integration
- Technical tags: #payment-gateway #dowcommerce #credit-card-processing #ecommerce #secure-payments #web2py-contrib
- Target roles: Payment developers (advanced), E-commerce developers (intermediate), Financial systems engineers (advanced)
- Difficulty level: ⭐⭐⭐⭐ - Requires understanding of payment processing, security, and API integration
- Maintenance level: Medium - Requires updates for API changes and security requirements
- Business criticality: Critical - Direct impact on payment processing and revenue
- Related topics: Payment processing, e-commerce integration, financial transactions, PCI compliance, secure communications