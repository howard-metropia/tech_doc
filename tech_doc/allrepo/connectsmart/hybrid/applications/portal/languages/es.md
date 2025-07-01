# Portal Language File - Spanish

## Overview
Spanish language localization file for the ConnectSmart Portal application, providing comprehensive translations for Spanish-speaking users across all mobility platform features including carpooling, transit, wallet, and notification systems.

## File Details
- **Location**: `/applications/portal/languages/es.py`
- **Type**: Python Language Dictionary
- **Language Code**: `es`
- **Language Name**: Inglés (EE.UU) [Spanish label for English (US)]
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
'Duplicate Email': 'Otro usuario ya ha utilizado este correo electrónico, por favor intente utilizar un correo electrónico diferente para registrar una cuenta.'
'Email verification': 'Verificación de Correo electrónico'
'User not found': 'Usuario no encontrado'
'Wrong password': 'Contraseña incorrecta'
```

#### Carpooling & Trip Management
```python
'Oh no! Your driver %(first_name)s has cancelled the carpooling trip.': '¡Ay no! su conductor %(first_name)s ha cancelado el carpooling/ viaje compartido'
'You have a new match!': '¡Tiene un nuevo emparejamiento!'
'Your trip with %(first_name)s is complete. Total %(chip_in)s Coins have been added to your Wallet!': '¡Su viaje con %(first_name)s fue completado. %(chip_in)s en monedas han sido agregadas a su billetera!'
```

#### Financial & Wallet Features
```python
'Coins balance not enough for escrow, there\'re %(short)s short.': 'Saldo de monedas no es suficiente para el depósito, está %(short)s corto'
'Stripe charge failed': 'Cargo de Stripe ha fallado'
'Coin product not found': 'Producto de moneda no encontrado'
```

#### Trip States & Driver Communication
```python
'Driver Has Arrived': 'El conductor/La conductora ha llegado'
'Driver Is Approaching': 'El conductor/La conductora se está acercando'
'En Route': 'En ruta/ camino'
'Arriving Now': 'Llegando ahora'
```

#### Group & Enterprise Features
```python
'Congratulations! You\'ve officially joined the %(group_name)s carpooling group!': '¡Felicitaciones! ¡Usted se unió oficialmente a %(group_name)s grupo de carpooling/ viaje compartido!'
'The group %(group_name)s has been disbanded.': 'El grupo %(group_name)s ha sido disuelto.'
'No same group': 'No el mismo grupo'
```

## Key Features

### 1. Cultural Localization
- **Polite Forms**: Uses formal "usted" addressing
- **Regional Terminology**: Carpooling = "carpooling/viaje compartido"
- **Currency**: Maintains USD/TWD with Spanish context
- **Time Expressions**: Localized time and date formats

### 2. Gender-Inclusive Language
```python
'Driver': 'Conductor' # Male/neutral form
'El conductor/La conductora ha llegado' # Gender-inclusive arrival message
'Passenger': 'Pasajero' # Standard passenger term
```

### 3. Transportation Terminology
- **Carpooling**: "carpooling/viaje compartido"
- **Driver**: "conductor/conductora"
- **Passenger/Rider**: "pasajero"
- **Trip**: "viaje"
- **Route**: "ruta"

### 4. Error Messages & Validation
```python
'Invalid parameters': 'parámetros inválidos'
'This email has already been used.': 'Este correo electrónico ya ha sido usado'
'Phone number already use': 'Número de teléfono ya está en uso'
```

## Regional Adaptations

### Mexican Spanish Influences
- "carpooling" term retained alongside "viaje compartido"
- Currency terminology maintained in English (USD)
- Technical terms often kept in English with Spanish explanation

### Formal vs. Informal Address
Consistent use of formal "usted" addressing throughout:
```python
'Use the button below to verify your email address': 'Use el botón abajo para verificar su correo electrónico'
'Please reply to it soon': 'Por favor responda pronto'
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

### Email & SMS Templates
- Verification messages
- Trip notifications
- Payment confirmations
- Account alerts

## Translation Quality Features

### 1. Contextual Accuracy
Messages maintain context-appropriate translations:
```python
'Trip verification failed': 'La verificación del viaje falló'
'Because we could not confirm that you were onboard': 'Su aporte para el viaje fue devuelto porque no pudimos confirmar que se unió a este carpool'
```

### 2. Technical Term Handling
- Preserves technical accuracy
- Maintains user-friendly language
- Includes explanatory context where needed

### 3. Action-Oriented Language
Clear, actionable instructions:
```python
'Open the App': 'Abre la aplicación'
'Verify Email': 'Verifique Correo Electrónico'
'Request to Join': 'Solicitud para unirse'
```

## Dependencies
- **Python**: Dictionary-based language file
- **web2py Framework**: T() translation function compatibility
- **Portal Controllers**: Spanish language key mapping
- **Notification Systems**: Localized message delivery

## Usage Example
```python
# Basic translation
T('You have a new match!') # Returns: "¡Tiene un nuevo emparejamiento!"

# With parameters
T('Oh no! Your driver %(first_name)s has cancelled the carpooling trip.', 
  dict(first_name='María')) 
# Returns: "¡Ay no! su conductor María ha cancelado el carpooling/ viaje compartido"

# Financial notifications
T('Coins balance not enough for escrow, there\'re %(short)s short.', 
  dict(short='5'))
# Returns: "Saldo de monedas no es suficiente para el depósito, está 5 corto"
```

This Spanish language file provides comprehensive localization for Spanish-speaking users of the ConnectSmart mobility platform, maintaining cultural appropriateness while preserving technical accuracy across all system functions.