# Gluon Contrib PaymenTech Module

## Overview
PaymenTech payment processing integration for web2py applications. Provides a simple API for processing credit card transactions through the PaymenTech (Chase Paymentech) payment gateway service.

## Module Information
- **Module**: `gluon.contrib.paymentech`
- **Author**: Alan Etkin (based on work by Adnan Smajlovic)
- **License**: BSD
- **Dependencies**: `xml.dom.minidom`, `urllib2`, `httplib`
- **Status**: Legacy payment processor

## Key Features
- **Credit Card Processing**: Charge, authorize, and capture transactions
- **XML API Integration**: Direct XML communication with PaymenTech gateway
- **Development Mode**: Separate testing environment support
- **Web2py Integration**: Designed for web2py payment workflows
- **Transaction Management**: Complete transaction lifecycle support

## Main Class

### PaymenTech
Primary class for PaymenTech payment processing operations.

**Constructor:**
```python
def __init__(self, user, password, industry, message, bin_code, 
             merchant, terminal, development=False, target=None, 
             host=None, api_url=None)
```

**Required Parameters:**
- `user`: PaymenTech username
- `password`: PaymenTech password  
- `industry`: Industry code
- `message`: Message type
- `bin_code`: Bank Identification Number
- `merchant`: Merchant ID
- `terminal`: Terminal ID

**Optional Parameters:**
- `development`: Use test environment (default: False)
- `target`: Target endpoint
- `host`: Host server
- `api_url`: API URL endpoint

## Payment Operations

### charge()
Process a credit card charge transaction.

**Parameters:**
- `account`: Credit card number
- `exp`: Expiration date (MMYYYY format)
- `amount`: Amount in cents (string, e.g., "215" for $2.15)
- `cvv2`: Card verification value
- Additional transaction details

**Example:**
```python
pos_data = {
    'user': 'merchant_user',
    'password': 'merchant_pass',
    'industry': 'ECOMMERCE',
    'message': 'AC',
    'bin_code': '000000',
    'merchant': '123456789012',
    'terminal': '001',
    'development': True
}

payment = PaymenTech(**pos_data)

charge_data = {
    'account': '4000000000000002',
    'exp': '122025',
    'amount': '1500',  # $15.00
    'cvv2': '123'
}

result = payment.charge(**charge_data)
```

## Format Requirements

### Credit Card Expiration
```python
# Format: MMYYYY
exp = '122025'  # December 2025
exp = '012024'  # January 2024
```

### Amount Format
```python
# Amount in cents as string
amount = '215'   # $2.15
amount = '1000'  # $10.00
amount = '5'     # $0.05
```

### Credit Card Number
```python
# Test card numbers for development
test_cards = {
    'visa': '4000000000000002',
    'mastercard': '5555555555554444',
    'amex': '378282246310005',
    'discover': '6011111111111117'
}
```

## Configuration

### Development Environment
```python
# Development configuration
config = {
    'user': 'test_user',
    'password': 'test_password',
    'industry': 'ECOMMERCE',
    'message': 'AC',
    'bin_code': '000000',
    'merchant': 'TEST_MERCHANT',
    'terminal': '001',
    'development': True,  # Use test environment
}

payment_processor = PaymenTech(**config)
```

### Production Environment
```python
# Production configuration
config = {
    'user': 'prod_user',
    'password': 'prod_password',
    'industry': 'RETAIL',
    'message': 'AC',
    'bin_code': '123456',
    'merchant': 'PROD_MERCHANT_ID',
    'terminal': '001',
    'development': False,  # Use production environment
    'host': 'production.paymentech.com',
    'api_url': '/api/gateway'
}
```

## Web2py Integration

### Model Configuration
```python
# In models/0_private.py
PAYMENTECH_USER = "your_username"
PAYMENTECH_PASSWORD = "your_password"
PAYMENTECH_INDUSTRY = "ECOMMERCE"
PAYMENTECH_MESSAGE = "AC"
PAYMENTECH_BIN_CODE = "000000"
PAYMENTECH_MERCHANT = "your_merchant_id"
PAYMENTECH_TERMINAL = "001"
DEVELOPMENT = True  # Set to False for production

# In models/db.py
db.define_table('payments',
    Field('order_id', 'string'),
    Field('amount', 'decimal(10,2)'),
    Field('card_last_four', 'string'),
    Field('transaction_id', 'string'),
    Field('status', 'string'),
    Field('created_on', 'datetime', default=request.now),
    Field('response_data', 'text')  # Store full response
)
```

### Controller Implementation
```python
def process_payment():
    """Process credit card payment"""
    form = FORM(
        INPUT(_name='card_number', _placeholder='Card Number'),
        INPUT(_name='exp_month', _placeholder='MM'),
        INPUT(_name='exp_year', _placeholder='YYYY'),
        INPUT(_name='cvv', _placeholder='CVV'),
        INPUT(_name='amount', _placeholder='Amount'),
        INPUT(_type='submit', _value='Process Payment')
    )
    
    if form.process().accepted:
        # Initialize PaymenTech
        payment_processor = PaymenTech(
            user=PAYMENTECH_USER,
            password=PAYMENTECH_PASSWORD,
            industry=PAYMENTECH_INDUSTRY,
            message=PAYMENTECH_MESSAGE,
            bin_code=PAYMENTECH_BIN_CODE,
            merchant=PAYMENTECH_MERCHANT,
            terminal=PAYMENTECH_TERMINAL,
            development=DEVELOPMENT
        )
        
        # Format expiration date
        exp_date = '%02d%s' % (int(request.vars.exp_month), 
                              request.vars.exp_year)
        
        # Convert amount to cents
        amount_cents = str(int(float(request.vars.amount) * 100))
        
        # Process payment
        try:
            result = payment_processor.charge(
                account=request.vars.card_number,
                exp=exp_date,
                amount=amount_cents,
                cvv2=request.vars.cvv
            )
            
            # Store transaction record
            payment_id = db.payments.insert(
                order_id=session.order_id,
                amount=request.vars.amount,
                card_last_four=request.vars.card_number[-4:],
                transaction_id=result.get('transaction_id'),
                status=result.get('status'),
                response_data=str(result)
            )
            
            if result.get('approved'):
                session.flash = 'Payment processed successfully'
                redirect(URL('payment_success', args=[payment_id]))
            else:
                form.errors.card_number = 'Payment declined: %s' % result.get('message')
        
        except Exception as e:
            form.errors.card_number = 'Payment processing error: %s' % str(e)
    
    return dict(form=form)
```

### Security Implementation
```python
def secure_payment_process():
    """Secure payment processing with validation"""
    
    # Validate card number using Luhn algorithm
    def validate_card_number(card_number):
        def luhn_checksum(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10
        return luhn_checksum(card_number) == 0
    
    # Validate expiration date
    def validate_expiration(month, year):
        from datetime import datetime
        current = datetime.now()
        exp_date = datetime(int(year), int(month), 1)
        return exp_date > current
    
    # Process with validation
    if validate_card_number(request.vars.card_number):
        if validate_expiration(request.vars.exp_month, request.vars.exp_year):
            # Process payment
            pass
        else:
            response.flash = 'Card has expired'
    else:
        response.flash = 'Invalid card number'
```

## Error Handling

### Response Processing
```python
def parse_payment_response(response):
    """Parse PaymenTech XML response"""
    try:
        from xml.dom.minidom import parseString
        dom = parseString(response)
        
        # Extract response fields
        result = {}
        result['approved'] = dom.getElementsByTagName('approved')[0].firstChild.nodeValue
        result['transaction_id'] = dom.getElementsByTagName('txRefNum')[0].firstChild.nodeValue
        result['auth_code'] = dom.getElementsByTagName('authCode')[0].firstChild.nodeValue
        result['message'] = dom.getElementsByTagName('respText')[0].firstChild.nodeValue
        
        return result
    except Exception as e:
        return {'error': 'Failed to parse response: %s' % str(e)}
```

### Transaction Logging
```python
def log_transaction(payment_data, response, success=True):
    """Log payment transaction for audit trail"""
    db.payment_logs.insert(
        card_last_four=payment_data['account'][-4:],
        amount=payment_data['amount'],
        transaction_id=response.get('transaction_id'),
        success=success,
        response_code=response.get('response_code'),
        message=response.get('message'),
        timestamp=request.now,
        ip_address=request.env.remote_addr,
        user_agent=request.env.http_user_agent
    )
```

## Testing

### Test Implementation
```python
def test_payment_processing():
    """Test PaymenTech integration"""
    
    # Test configuration
    test_config = {
        'user': 'test_user',
        'password': 'test_password',
        'industry': 'ECOMMERCE',
        'message': 'AC',
        'bin_code': '000000',
        'merchant': 'TEST_MERCHANT',
        'terminal': '001',
        'development': True
    }
    
    # Test payment data
    test_payment = {
        'account': '4000000000000002',  # Test Visa
        'exp': '122025',
        'amount': '100',  # $1.00
        'cvv2': '123'
    }
    
    try:
        processor = PaymenTech(**test_config)
        result = processor.charge(**test_payment)
        
        print("Test Payment Result:")
        print("Approved:", result.get('approved'))
        print("Transaction ID:", result.get('transaction_id'))
        print("Message:", result.get('message'))
        
        return result.get('approved') == 'true'
    
    except Exception as e:
        print("Test failed:", str(e))
        return False
```

## Industry Codes

### Common Industry Types
- `ECOMMERCE`: E-commerce transactions
- `RETAIL`: Retail point-of-sale
- `RESTAURANT`: Restaurant transactions
- `HOTEL`: Hotel and lodging
- `AUTO_RENTAL`: Car rental
- `DIRECT_MARKETING`: Direct marketing

## Message Types

### Transaction Types
- `AC`: Authorization and Capture
- `A`: Authorization only
- `C`: Capture only
- `V`: Void transaction
- `R`: Refund transaction

## Limitations

### Legacy Status
- PaymenTech has been acquired and integrated into other systems
- Limited support for modern payment features
- XML-based API is outdated compared to REST APIs

### Security Considerations
- No built-in PCI compliance features
- Manual SSL/TLS handling required
- Limited tokenization support

## Migration Recommendations

Consider migrating to modern payment processors:
- Stripe
- PayPal
- Square
- Authorize.Net

These provide better security, more features, and active support.

This module provides basic PaymenTech integration capabilities but should be considered for modernization in current applications due to the legacy nature of the PaymenTech platform.