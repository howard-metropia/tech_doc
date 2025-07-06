# Portal Language File - Vietnamese

## Overview
Vietnamese language localization file for the ConnectSmart Portal application, providing comprehensive translations for Vietnamese-speaking users across all mobility platform features including carpooling, transit, wallet, and notification systems.

## File Details
- **Location**: `/applications/portal/languages/vi.py`
- **Type**: Python Language Dictionary
- **Language Code**: `vi`
- **Language Name**: Vietnamese
- **Total Entries**: 327 translation entries

## Language Structure

### System-Required Entries
Framework and system messages (lines 3-121) that remain untranslated per requirements:
- Language metadata and web2py framework messages
- Database operation responses
- Cache and administration interface
- Error logs and system debugging

### Application-Specific Translations

#### Authentication & User Management
```python
'Duplicate Email': 'Một người dùng khác đã sử dụng email này, và vui lòng thử sử dụng một email khác để đăng ký tài khoản.'
'Email verification': 'Xác thực Email'
'User not found': 'Không tìm thấy người dùng'
'Wrong password': 'Sai mật khẩu'
```

#### Carpooling & Trip Management
```python
'Oh no! Your driver %(first_name)s has cancelled the carpooling trip.': 'Ôi không! Tài xế của bạn %(first_name)s đã hủy chuyến đi chung xe.'
'You have a new match!': 'Bạn có kết quả phù hợp mới!'
'Your trip with %(first_name)s is complete. Total %(chip_in)s Coins have been added to your Wallet!': 'Your trip with %(first_name)s is complete. Total %(chip_in)s Coins have been added to your Wallet!'
```

#### Financial & Wallet Features
```python
'Coins balance not enough for escrow, there\'re %(short)s short.': 'Số dư tiền xu không đủ để ký quỹ, còn thiếu %(short)s.'
'Stripe charge failed': 'Tính phí Stipe không thành công'
'Coin product not found': 'Không tìm thấy sản phẩm tiền xu'
```

#### Trip States & Driver Communication
```python
'Driver Has Arrived': 'Tài xế đã đến'
'Driver Is Approaching': 'Tài xế đang đến gần'
'En Route': 'Đang trên đường'
'Arriving Now': 'Đang đến ngay bây giờ'
```

#### Group & Enterprise Features
```python
'Congratulations! You\'ve officially joined the %(group_name)s carpooling group!': 'Xin chúc mừng! Bạn đã chính thức tham gia nhóm đi chung xe %(group_name)s!'
'The group %(group_name)s has been disbanded.': 'Nhóm %(group_name)s đã bị giải tán.'
'No same group': 'Người được mời không có trong nhóm của bạn.'
```

## Key Features

### 1. Vietnamese Cultural Adaptation
- **Respectful Language**: Uses polite forms appropriate for service communications
- **Transportation Terms**: "đi chung xe" for carpooling, "tài xế" for driver
- **Currency**: Maintains USD/TWD with Vietnamese context
- **Time Expressions**: Localized time and date formats

### 2. Transportation Terminology
```python
'driver': 'tài xế'
'Driver': 'Tài xế'
'rider': 'người đi xe'
'Passenger': 'người đi xe'
'Carpooling': 'Đi chung xe'
'Trip': 'Chuyến đi'
```

### 3. Formal Communication Style
Maintains professional tone throughout:
```python
'Use the button below to verify your email address': 'Sử dụng nút bên dưới để xác minh địa chỉ email của bạn'
'Please reply to it soon': 'Hãy trả lời sớm'
'Thank you for using': 'Cảm ơn bạn đã sử dụng'
```

### 4. Error Messages & System Feedback
```python
'Invalid parameters': 'Thông số không hợp lệ'
'This email has already been used.': 'Email này đã được sử dụng.'
'Phone number already use': 'Số điện thoại đã sử dụng'
'City not in our support': 'Thành phố không ở trọng phạm vi hỗ trợ của chúng tôi'
```

## Language Characteristics

### 1. Directional & Spatial Terms
Vietnamese language structure for location and movement:
```python
'Your Driver is Approaching': 'Tài xế đang đến gần'
'En Route': 'Đang trên đường'
'Your destination arrives soon': 'Bạn sẽ đến điểm đến sớm'
```

### 2. Time & Sequence Expressions
Natural Vietnamese temporal expressions:
```python
'%(first_name)s will arrive within 5 minutes': '%(first_name)s sẽ đến trong vòng 5 phút'
'Driver Has Departed': 'Tài xế đã khởi hành'
'Trip Completed': 'Trip Completed' # Some terms maintained in English
```

### 3. Courtesy & Politeness Markers
Vietnamese emphasis on respectful communication:
```python
'Please meet %(first_name)s at the pickup location': 'Vui lòng gặp %(first_name)s tại địa điểm đón'
'Thank you for using %(project_name)s carpooling!': 'Cảm ơn bạn đã sử dụng dịch vụ đi chung xe %(project_name)s!'
```

## Technical Implementation

### 1. Character Encoding
- **UTF-8 Support**: Handles Vietnamese diacritical marks
- **Tone Marks**: Proper rendering of Vietnamese tones
- **Special Characters**: Support for Vietnamese character set

### 2. Mixed Language Content
Strategic use of English terms where appropriate:
```python
'Auto Refill paused': 'Auto Refill paused' # Technical term maintained
'Trip Completed': 'Trip Completed' # App interface consistency
'$%(amount)s Coins have been deposited': '$%(amount)s Coins have been deposited' # Financial terms
```

### 3. Parameter Integration
Seamless variable substitution in Vietnamese sentence structure:
```python
'%(first_name)s has arrived. Please meet your driver at the pickup location.': '%(first_name)s đã đến. Vui lòng gặp tài xế của bạn tại địa điểm đón.'
```

## Integration Points

### Mobile Application Support
- Push notification localization
- In-app messaging
- Error handling
- Success confirmations

### Web Portal Interface
- Form validation messages
- Navigation elements
- User feedback
- System notifications

### Communication Systems
- Email templates
- SMS notifications
- Customer support messages
- Verification processes

## Translation Quality Standards

### 1. Contextual Accuracy
Maintains meaning while adapting to Vietnamese communication patterns:
```python
'Trip verification failed': 'Xác minh chuyến đi không thành công'
'Because we could not confirm that you were onboard': 'Vì chúng tôi không thể xác nhận rằng bạn đã tham gia nhóm đi chung xe này, tiền đóng góp của bạn đã được hoàn trả lại'
```

### 2. User Experience Focus
Clear, actionable language for user interactions:
```python
'Open the App': 'Mở ứng dụng'
'Verify Email': 'Xác nhận Email'
'Request to Join': 'Yêu cầu tham gia'
```

## Dependencies
- **Python**: Dictionary-based language file with UTF-8 encoding
- **web2py Framework**: T() translation function compatibility
- **Portal Controllers**: Vietnamese language key mapping
- **Notification Systems**: Unicode message delivery support

## Usage Example
```python
# Basic translation
T('You have a new match!') # Returns: "Bạn có kết quả phù hợp mới!"

# With parameters
T('Oh no! Your driver %(first_name)s has cancelled the carpooling trip.', 
  dict(first_name='Minh')) 
# Returns: "Ôi không! Tài xế của bạn Minh đã hủy chuyến đi chung xe."

# Financial notifications
T('Coins balance not enough for escrow, there\'re %(short)s short.', 
  dict(short='5'))
# Returns: "Số dư tiền xu không đủ để ký quỹ, còn thiếu 5."
```

This Vietnamese language file provides culturally appropriate and linguistically accurate localization for Vietnamese-speaking users of the ConnectSmart mobility platform, ensuring clear communication across all system features while maintaining technical precision.