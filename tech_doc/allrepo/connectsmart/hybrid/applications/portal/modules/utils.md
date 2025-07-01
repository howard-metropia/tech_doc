# Utils Module Documentation

## Overview
The Utils Module provides essential utility functions for the ConnectSmart Hybrid Portal application. It includes credit card brand identification and CDN URL generation functionality with Web2py integration.

## File Location
**Source**: `/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/applications/portal/modules/utils.py`

## Dependencies
- `gluon.current`: Web2py current context for configuration access

## Functions

### `card_brand_mapping(card_type)`

#### Purpose
Maps numeric card type identifiers to human-readable credit card brand names.

#### Parameters
- `card_type` (int): Numeric card type identifier

#### Returns
String representing the card brand name

#### Card Type Mapping
```python
{
    -1: "Unknown",      # Unidentified or invalid card
    1: "VISA",          # Visa cards
    2: "MasterCard",    # MasterCard cards
    3: "JCB",           # JCB cards
    4: "Union Pay",     # UnionPay cards
    5: "AMEX"           # American Express cards
}
```

#### Usage Examples
```python
# Identify card brands
brand = card_brand_mapping(1)    # Returns "VISA"
brand = card_brand_mapping(2)    # Returns "MasterCard"
brand = card_brand_mapping(3)    # Returns "JCB"
brand = card_brand_mapping(-1)   # Returns "Unknown"
brand = card_brand_mapping(99)   # Returns None (unmapped)
```

#### Integration with Payment Processing
```python
def process_payment_card(card_info):
    card_type = card_info.get('type', -1)
    brand_name = card_brand_mapping(card_type)
    
    payment_data = {
        'card_number': card_info['number'],
        'card_brand': brand_name,
        'expiry_date': card_info['expiry'],
        'cvv': card_info['cvv']
    }
    
    # Log payment attempt
    logger.info(f"Processing {brand_name} payment")
    
    return payment_data
```

### `cdn_url(file_path)`

#### Purpose
Generates complete CDN URLs from relative file paths using application configuration.

#### Parameters
- `file_path` (str): Relative file path or None

#### Returns
- **Valid Path**: Complete CDN URL string
- **None/Empty Path**: None (no URL generated)

#### Configuration Integration
```python
configuration = current.globalenv['configuration']
cdn_base_url = configuration.get('app.cdn_url')
```

#### URL Generation Logic
```python
if file_path:
    return str(cdn_base_url) + str(file_path)
else:
    return None  # Implicit return for falsy values
```

#### Usage Examples
```python
# Generate CDN URLs
avatar_url = cdn_url('/images/avatars/user_123.jpg')
# Returns: "https://cdn.example.com/images/avatars/user_123.jpg"

document_url = cdn_url('/documents/contract.pdf')
# Returns: "https://cdn.example.com/documents/contract.pdf"

# Handle empty paths
empty_url = cdn_url(None)     # Returns None
empty_url = cdn_url('')       # Returns None
```

## Configuration Requirements

### CDN Configuration
```python
# Web2py configuration file
app = {
    'cdn_url': 'https://cdn.example.com',
    # Alternative configurations
    'cdn_url': 'https://d1234567.cloudfront.net',
    'cdn_url': 'https://assets.mydomain.com'
}
```

### Environment-Specific CDN URLs
```python
# Development
app.cdn_url = 'http://localhost:8000/static'

# Staging  
app.cdn_url = 'https://staging-cdn.example.com'

# Production
app.cdn_url = 'https://cdn.example.com'
```

## Integration Patterns

### User Profile Images
```python
def get_user_profile(user_id):
    user = db.auth_user(user_id)
    
    profile = {
        'id': user.id,
        'name': f"{user.first_name} {user.last_name}",
        'avatar': cdn_url(user.avatar),           # CDN URL
        'background': cdn_url(user.background_image)
    }
    
    return profile
```

### Vehicle Photos
```python
def get_vehicle_details(vehicle_id):
    vehicle = db.vehicles(vehicle_id)
    
    return {
        'id': vehicle.id,
        'make': vehicle.make,
        'model': vehicle.model,
        'photos': {
            'front': cdn_url(vehicle.photo_front),
            'side': cdn_url(vehicle.photo_side),
            'interior': cdn_url(vehicle.photo_interior)
        }
    }
```

### Payment Card Display
```python
def get_user_payment_methods(user_id):
    cards = db(db.payment_cards.user_id == user_id).select()
    
    payment_methods = []
    for card in cards:
        payment_methods.append({
            'id': card.id,
            'brand': card_brand_mapping(card.card_type),
            'last_four': card.last_four_digits,
            'expiry': card.expiry_date,
            'is_default': card.is_default
        })
    
    return payment_methods
```

### Document Management
```python
def get_user_documents(user_id):
    documents = db(db.user_documents.user_id == user_id).select()
    
    doc_list = []
    for doc in documents:
        doc_list.append({
            'id': doc.id,
            'title': doc.title,
            'type': doc.document_type,
            'url': cdn_url(doc.file_path),
            'uploaded_at': doc.created_at
        })
    
    return doc_list
```

## API Response Formatting

### User Profile API
```python
def user_profile_api():
    user_id = request.vars.user_id
    user = db.auth_user(user_id)
    
    response_data = {
        'user_id': user.id,
        'personal_info': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        },
        'media': {
            'avatar': cdn_url(user.avatar),
            'cover_photo': cdn_url(user.cover_photo)
        },
        'vehicle': {
            'type': user.vehicle_type,
            'photos': {
                'front': cdn_url(user.vehicle_picture_front),
                'side': cdn_url(user.vehicle_picture_side)
            }
        }
    }
    
    return response.json(response_data)
```

### Payment Methods API
```python
def payment_methods_api():
    user_id = auth.user.id
    cards = db(db.payment_cards.user_id == user_id).select()
    
    methods = []
    for card in cards:
        methods.append({
            'id': card.id,
            'brand': card_brand_mapping(card.card_type),
            'display_name': f"{card_brand_mapping(card.card_type)} ****{card.last_four}",
            'expiry': card.expiry_date.strftime('%m/%y'),
            'is_default': card.is_default
        })
    
    return response.json({'payment_methods': methods})
```

## Error Handling

### CDN URL Generation
```python
def safe_cdn_url(file_path):
    """Safe CDN URL generation with error handling"""
    try:
        if not file_path:
            return None
            
        # Validate file path format
        if not isinstance(file_path, str):
            logger.warning(f"Invalid file path type: {type(file_path)}")
            return None
            
        # Generate CDN URL
        url = cdn_url(file_path)
        
        # Validate URL format
        if url and not url.startswith(('http://', 'https://')):
            logger.warning(f"Invalid CDN URL generated: {url}")
            return None
            
        return url
        
    except Exception as e:
        logger.error(f"CDN URL generation failed: {e}")
        return None
```

### Card Brand Validation
```python
def validate_card_brand(card_type):
    """Validate and get card brand with error handling"""
    try:
        if not isinstance(card_type, int):
            logger.warning(f"Invalid card type: {card_type}")
            return "Unknown"
            
        brand = card_brand_mapping(card_type)
        
        if brand is None:
            logger.warning(f"Unmapped card type: {card_type}")
            return "Unknown"
            
        return brand
        
    except Exception as e:
        logger.error(f"Card brand validation failed: {e}")
        return "Unknown"
```

## Performance Considerations

### CDN URL Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_cdn_url(file_path):
    """Cached CDN URL generation"""
    return cdn_url(file_path)
```

### Batch URL Generation
```python
def batch_cdn_urls(file_paths):
    """Generate multiple CDN URLs efficiently"""
    cdn_base = current.globalenv['configuration'].get('app.cdn_url')
    
    urls = []
    for path in file_paths:
        if path:
            urls.append(str(cdn_base) + str(path))
        else:
            urls.append(None)
    
    return urls
```

## Security Considerations

### URL Validation
```python
def secure_cdn_url(file_path):
    """Generate CDN URL with security validation"""
    if not file_path:
        return None
        
    # Prevent path traversal
    if '..' in file_path or file_path.startswith('/'):
        logger.warning(f"Potentially malicious file path: {file_path}")
        return None
        
    # Validate file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc']
    if not any(file_path.lower().endswith(ext) for ext in allowed_extensions):
        logger.warning(f"Disallowed file extension: {file_path}")
        return None
        
    return cdn_url(file_path)
```

### Card Type Validation
```python
def secure_card_brand(card_type):
    """Secure card brand identification"""
    # Validate input type
    if not isinstance(card_type, int):
        return "Unknown"
        
    # Validate range
    if card_type < -1 or card_type > 10:
        logger.warning(f"Card type out of expected range: {card_type}")
        return "Unknown"
        
    return card_brand_mapping(card_type) or "Unknown"
```

## Testing Support

### Mock Configuration
```python
def mock_cdn_config(cdn_url_base):
    """Mock CDN configuration for testing"""
    if not hasattr(current, 'globalenv'):
        current.globalenv = {}
    
    current.globalenv['configuration'] = {
        'app.cdn_url': cdn_url_base
    }
```

### Test Utilities
```python
def test_card_brand_mapping():
    """Test card brand mapping functionality"""
    assert card_brand_mapping(1) == "VISA"
    assert card_brand_mapping(2) == "MasterCard"
    assert card_brand_mapping(-1) == "Unknown"
    assert card_brand_mapping(99) is None

def test_cdn_url_generation():
    """Test CDN URL generation"""
    mock_cdn_config('https://test-cdn.com')
    
    assert cdn_url('/test.jpg') == 'https://test-cdn.com/test.jpg'
    assert cdn_url(None) is None
    assert cdn_url('') is None
```

## Future Enhancements

### Extended Card Support
```python
EXTENDED_CARD_MAPPING = {
    -1: "Unknown",
    1: "VISA",
    2: "MasterCard", 
    3: "JCB",
    4: "Union Pay",
    5: "AMEX",
    6: "Discover",
    7: "Diners Club",
    8: "Maestro"
}
```

### Advanced CDN Features
```python
def cdn_url_with_params(file_path, **params):
    """Generate CDN URL with query parameters"""
    base_url = cdn_url(file_path)
    if base_url and params:
        query_string = '&'.join(f"{k}={v}" for k, v in params.items())
        return f"{base_url}?{query_string}"
    return base_url
```

## Related Components
- Payment processing system
- User profile management
- File upload handling
- Media asset management
- Configuration management system