# Portal Language File - English (US)

## Overview
Main English (US) language localization file for the ConnectSmart Portal application, providing comprehensive translations for the entire portal interface including carpooling, transit, wallet, notifications, and system messages.

## File Details
- **Location**: `/applications/portal/languages/en.py`
- **Type**: Python Language Dictionary
- **Language Code**: `en-us`
- **Language Name**: English (US)
- **Total Entries**: 228 translation entries

## Language Structure

### System-Required Entries
Language metadata and web2py framework required translations that should not be translated:
- Language identification (`!langcode!`, `!langname!`)
- Framework messages and error handling
- Database operation messages
- Cache and administration interface

### Application-Specific Translations

#### Authentication & User Management
```python
'Duplicate Email': 'Another user has already used this email, and please try to use a different email to register an account.'
'Email verification': 'Email verification'
'Enter the activation code %(code)s to verify your email': 'Enter the activation code %(code)s to verify your email'
'User not found': 'User not found'
'Wrong password': 'Wrong password'
```

#### Carpooling & Trip Management
```python
'Oh no! Your carpooler %(first_name)s has cancelled the carpooling trip.': 'Oh no! Your carpooler %(first_name)s has cancelled the carpooling trip.'
'You have a new match!': 'You have a new match!'
'Your trip with %(first_name)s is complete. Total %(chip_in)s Coins have been added to your Wallet!': 'Your trip with %(first_name)s is complete. Total %(chip_in)s Coins have been added to your Wallet!'
```

#### Financial & Wallet Features
```python
'Coins balance not enough for escrow, there\'re %(short)s short.': 'Coins balance not enough for escrow, there\'re %(short)s short.'
'Auto Refill paused': 'Auto Refill paused'
'$%(amount)s Coins have been deposited in your Wallet.': '$%(amount)s Coins have been deposited in your Wallet.'
```

#### Trip States & Notifications
```python
'Driver Has Arrived': 'Your Driver Has Arrived'
'Your Driver is Approaching': 'Your Driver is Approaching'
'Get Ready to Carpool!': 'Get Ready to Carpool!'
'Trip Completed': 'Trip Completed'
```

#### Error Handling
```python
'Trip verification failed': 'Trip verification failed'
'Invalid url': 'Invalid url'
'Group not exists': 'Group not exists'
'Verification passed': 'Verification passed'
```

## Key Features

### 1. Multi-Context Translations
- **Web2py Framework**: System-level messages
- **Portal Application**: User-facing interface
- **Mobile Notifications**: Push notification content
- **Email Templates**: Email verification and notifications

### 2. Dynamic Content Support
Parameterized strings supporting variable substitution:
```python
'%(first_name)s should arrive in 5 minutes in a %(vehicle_color)s %(vehicle_type)s. (License #%(vehicle_plate)s)'
'Because we could not confirm that you were onboard, no Chip-In was paid. To learn more, please visit our Help Desk.'
```

### 3. Currency & Financial Localization
- Currency symbols: USD, TWD
- Financial transaction messages
- Wallet and payment notifications

### 4. Transportation Modes
- Carpooling terminology
- Driver/passenger role descriptions
- Vehicle information display
- Trip status updates

## Integration Points

### Portal Controllers
Used by all portal controllers for:
- Error message display
- Success notifications
- Form validation messages
- User interaction feedback

### Notification System
Provides text for:
- Push notifications
- Email content
- SMS messages
- In-app alerts

### Mobile Applications
Referenced by mobile apps for:
- Consistent messaging
- Localized content
- Error handling
- User guidance

## Best Practices

### Translation Guidelines
1. Maintain consistent terminology across features
2. Use natural, conversational language
3. Include context for dynamic variables
4. Consider mobile screen constraints

### Parameter Handling
```python
# Correct usage with named parameters
'Enter code %(code)s to verify your phone with %(project)s'

# Supporting multiple variables
'%(first_name)s will arrive within %(eta)s minutes in a %(vehicle_color)s %(vehicle_type)s'
```

### Error Message Standards
- Clear, actionable error descriptions
- User-friendly language
- Guidance for resolution
- Consistent tone and style

## Dependencies
- **Python**: Dictionary-based language file
- **web2py Framework**: T() translation function
- **Portal Controllers**: Language key references
- **Notification Systems**: Message templating

## Usage Example
```python
# In controller
T('You have a new match!')

# With parameters
T('Enter code %(code)s to verify your phone with %(project)s', 
  dict(code='123456', project='ConnectSmart'))

# Error handling
T('Coins balance not enough for escrow, there\'re %(short)s short.', 
  dict(short='5'))
```

This English language file serves as the primary localization source for the ConnectSmart portal, providing comprehensive coverage for all user-facing text and system messages across the mobility platform.