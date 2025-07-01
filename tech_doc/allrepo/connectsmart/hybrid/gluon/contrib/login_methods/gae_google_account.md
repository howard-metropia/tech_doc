# gluon/contrib/login_methods/gae_google_account.py

## Overview

The gae_google_account.py module provides Google App Engine (GAE) specific Google account authentication for Web2py applications running on GAE. This module leverages GAE's built-in Google authentication services.

## Key Features

- **GAE integration**: Optimized for Google App Engine environment
- **Google account authentication**: Direct Google account login
- **Seamless integration**: Built-in GAE authentication APIs
- **Automatic user management**: Handles user creation and updates

## Usage

```python
from gluon.contrib.login_methods.gae_google_account import gae_google_auth

# Only works on Google App Engine
auth.settings.login_methods.append(gae_google_auth())
```

## GAE Requirements

- Application must run on Google App Engine
- Google authentication must be enabled
- Proper GAE configuration required