# Gluon Contrib Google Wallet Module

## Overview
Google Wallet (formerly Google Checkout) integration module for web2py applications. Provides functionality to generate Google Wallet "Buy Now" buttons with product information for e-commerce transactions.

## Module Information
- **Module**: `gluon.contrib.google_wallet`
- **Purpose**: Google Wallet payment integration
- **Dependencies**: `gluon.html.XML`
- **Status**: Legacy (Google Checkout discontinued)

## Key Features
- **Buy Button Generation**: Creates HTML forms for Google Wallet checkout
- **Multi-product Support**: Handles multiple products in single transaction
- **Customizable Products**: Flexible product configuration with pricing
- **HTML Integration**: Returns web2py XML object for safe template rendering

## Main Function

### button()
Generates HTML form for Google Wallet "Buy Now" button with product details.

**Signature:**
```python
def button(merchant_id="123456789012345", 
           products=[dict(name="shoes", quantity=1, price=23.5, 
                         currency='USD', description="running shoes black")])
```

**Parameters:**
- `merchant_id`: Google Wallet merchant ID (string)
- `products`: List of product dictionaries

**Returns:**
- `XML` object containing HTML form for Google Wallet checkout

## Product Configuration

### Product Dictionary Structure
Each product must contain the following keys:
- `name`: Product name (string)
- `description`: Product description (string)  
- `quantity`: Product quantity (integer)
- `price`: Product price (float)
- `currency`: Currency code (string, e.g., 'USD')

### Example Product
```python
product = {
    'name': 'running shoes',
    'description': 'Nike Air Max running shoes',
    'quantity': 2,
    'price': 129.99,
    'currency': 'USD'
}
```

## Generated HTML Structure

### Form Elements
The function generates an HTML form with:
- **Action URL**: Points to Google Checkout API
- **Method**: POST submission
- **Target**: Opens in current window (_top)
- **Hidden Fields**: Product details as form inputs
- **Submit Button**: Google Wallet buy button image

### Form Template
```html
<form action="https://checkout.google.com/api/checkout/v2/checkoutForm/Merchant/{merchant_id}" 
      id="BB_BuyButtonForm" method="post" name="BB_BuyButtonForm" target="_top">
  <!-- Product fields -->
  <input name="item_1_name" type="hidden" value="product_name"/>
  <input name="item_1_description" type="hidden" value="product_description"/>
  <input name="item_1_quantity" type="hidden" value="1"/>
  <input name="item_1_price" type="hidden" value="23.5"/>
  <input name="item_1_currency" type="hidden" value="USD"/>
  
  <!-- Encoding -->
  <input name="_charset_" type="hidden" value="utf-8"/>
  
  <!-- Submit button -->
  <input alt="" src="https://checkout.google.com/buttons/buy.gif?merchant_id={merchant_id}&w=117&h=48&style=white&variant=text&loc=en_US" 
         type="image"/>
</form>
```

### Field Naming Convention
Product fields follow the pattern: `item_{index}_{property}`
- `item_1_name`: First product name
- `item_1_price`: First product price
- `item_2_name`: Second product name (if applicable)

## Usage Examples

### Single Product
```python
from gluon.contrib.google_wallet import button

# Single product checkout
buy_button = button(
    merchant_id="123456789012345",
    products=[{
        'name': 'T-Shirt',
        'description': 'Cotton T-Shirt Size L',
        'quantity': 1,
        'price': 19.99,
        'currency': 'USD'
    }]
)

# In view template
{{=buy_button}}
```

### Multiple Products
```python
# Multiple products in one transaction
products = [
    {
        'name': 'Laptop',
        'description': 'Dell Inspiron 15 Laptop',
        'quantity': 1,
        'price': 799.99,
        'currency': 'USD'
    },
    {
        'name': 'Mouse',
        'description': 'Wireless optical mouse',
        'quantity': 1,
        'price': 29.99,
        'currency': 'USD'
    }
]

buy_button = button(
    merchant_id="your_merchant_id",
    products=products
)
```

### Controller Integration
```python
def product_page():
    product_id = request.args(0)
    product = db.products[product_id]
    
    # Generate Google Wallet button
    wallet_button = button(
        merchant_id=current.app_config.google_merchant_id,
        products=[{
            'name': product.name,
            'description': product.description,
            'quantity': 1,
            'price': float(product.price),
            'currency': 'USD'
        }]
    )
    
    return dict(product=product, wallet_button=wallet_button)
```

### Dynamic Product Configuration
```python
def shopping_cart():
    cart_items = session.cart or []
    products = []
    
    for item in cart_items:
        products.append({
            'name': item['name'],
            'description': item['description'],
            'quantity': item['quantity'],
            'price': float(item['price']),
            'currency': 'USD'
        })
    
    if products:
        checkout_button = button(
            merchant_id=current.app.config.google_merchant_id,
            products=products
        )
        return dict(checkout_button=checkout_button)
    else:
        return dict(checkout_button=None)
```

## Configuration Requirements

### Merchant Account Setup
1. **Google Merchant Account**: Required for processing payments
2. **Merchant ID**: Unique identifier from Google
3. **API Configuration**: Checkout API access
4. **SSL Certificate**: Required for secure transactions

### Application Configuration
```python
# In app configuration
GOOGLE_MERCHANT_ID = "123456789012345"

# Usage in controller
from gluon.contrib.google_wallet import button

def checkout():
    wallet_button = button(
        merchant_id=current.app_config.GOOGLE_MERCHANT_ID,
        products=get_cart_products()
    )
    return dict(button=wallet_button)
```

## Security Considerations

### Input Validation
```python
def validate_product(product):
    required_fields = ['name', 'description', 'quantity', 'price', 'currency']
    for field in required_fields:
        if field not in product:
            raise ValueError("Missing required field: %s" % field)
    
    if not isinstance(product['price'], (int, float)) or product['price'] <= 0:
        raise ValueError("Invalid price")
    
    if not isinstance(product['quantity'], int) or product['quantity'] <= 0:
        raise ValueError("Invalid quantity")
```

### HTML Escaping
The module uses `XML()` which assumes content is safe. Ensure product data is properly escaped:

```python
import cgi

def safe_button(merchant_id, products):
    # Escape product data
    safe_products = []
    for product in products:
        safe_product = {}
        for key, value in product.items():
            safe_product[key] = cgi.escape(str(value))
        safe_products.append(safe_product)
    
    return button(merchant_id, safe_products)
```

## Limitations

### Legacy Status
- **Google Checkout Discontinued**: Service no longer available
- **Historical Reference**: Code maintained for reference only
- **Migration Required**: Use modern payment processors

### Technical Limitations
- **No Error Handling**: No validation of merchant ID or products
- **Fixed Currency**: Limited multi-currency support
- **Static Templates**: No customization of button appearance
- **No Callbacks**: No server-side payment confirmation

## Migration Alternatives

### Modern Payment Processors
```python
# Stripe integration example
from gluon.contrib.stripe import StripePayment

def modern_checkout():
    stripe_payment = StripePayment(api_key="sk_test_...")
    checkout_session = stripe_payment.create_checkout_session(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': product['name']},
                'unit_amount': int(product['price'] * 100),
            },
            'quantity': product['quantity'],
        }],
        mode='payment',
        success_url=URL('payment_success'),
        cancel_url=URL('payment_cancel'),
    )
    return dict(checkout_url=checkout_session.url)
```

### PayPal Integration
```python
# PayPal button alternative
def paypal_button(products):
    # Generate PayPal checkout button
    # Implementation would use PayPal API
    pass
```

This module represents a historical payment integration that is no longer functional but provides insight into e-commerce integration patterns and HTML form generation for payment processing.