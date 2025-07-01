# gluon/contrib/login_methods/motp_auth.py

## Overview

The motp_auth.py module provides mobile One-Time Password (mOTP) authentication integration for Web2py applications. mOTP generates time-based one-time passwords using mobile devices for enhanced security authentication.

## Key Features

- **Mobile OTP generation**: Time-based one-time passwords
- **Multi-factor authentication**: Enhanced security layer
- **Mobile app integration**: Works with mOTP mobile applications
- **Time synchronization**: Clock-based token generation

## Configuration

```python
from gluon.contrib.login_methods.motp_auth import motp_auth

auth.settings.login_methods.append(
    motp_auth(
        secret_length=16,
        window_size=3
    )
)
```

## Security Features

- Time-based token generation
- Configurable time windows
- Replay attack prevention
- Mobile device security