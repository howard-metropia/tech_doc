# gluon/contrib/login_methods/extended_login_form.py

## Overview

The extended_login_form.py module provides enhanced login form capabilities for Web2py applications. It extends the standard Web2py authentication forms with additional features and customization options.

## Key Features

- **Enhanced form validation**: Advanced input validation rules
- **Custom field types**: Support for additional user data fields
- **Improved user experience**: Better form styling and interaction
- **Extensible design**: Easy customization for specific requirements

## Usage

```python
from gluon.contrib.login_methods.extended_login_form import extended_login_form

# Use extended login form
auth.settings.login_form = extended_login_form()
```

## Customization Options

- Custom validation rules
- Additional form fields
- Enhanced styling support
- JavaScript integration