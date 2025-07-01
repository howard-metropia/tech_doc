# Gluon Contrib Shell Module

## Overview
Interactive shell utilities for web2py applications. Provides enhanced shell functionality for debugging, testing, and administrative tasks with full access to the web2py environment.

## Module Information
- **Module**: `gluon.contrib.shell`
- **Purpose**: Interactive shell enhancements
- **Use Case**: Development, debugging, administration
- **Environment**: Full web2py context access

## Key Features
- **Web2py Context**: Full application environment access
- **Interactive Debugging**: Live debugging capabilities
- **Database Access**: Direct DAL interaction
- **Code Execution**: Dynamic code execution
- **History Support**: Command history and completion

## Basic Usage

### Interactive Shell
```python
# Start enhanced web2py shell
python web2py.py -S myapp -M -R applications/myapp/private/shell_script.py

# In shell script
from gluon.contrib.shell import ShellUtilities

shell = ShellUtilities(globals())
shell.start_interactive()
```

### Database Operations
```python
# Direct database queries
users = db(db.users.active == True).select()
print(f"Active users: {len(users)}")

# Interactive data exploration
for user in users:
    print(f"User: {user.name}, Email: {user.email}")
```

### Administrative Tasks
```python
def admin_shell():
    """Administrative shell for maintenance tasks"""
    
    # Database maintenance
    def cleanup_old_sessions():
        old_sessions = db(db.web2py_session.modified_datetime < 
                         datetime.datetime.now() - datetime.timedelta(days=30))
        count = old_sessions.count()
        old_sessions.delete()
        db.commit()
        print(f"Deleted {count} old sessions")
    
    # User management
    def create_admin_user(email, password):
        user_id = db.auth_user.insert(
            email=email,
            password=CRYPT()(password)[0],
            first_name='Admin',
            last_name='User'
        )
        db.auth_membership.insert(user_id=user_id, group_id=1)  # Admin group
        db.commit()
        print(f"Created admin user: {email}")
    
    # Make functions available in shell
    return locals()

# Load admin functions
admin_funcs = admin_shell()
globals().update(admin_funcs)
```

This module enhances the web2py shell experience for development and administrative tasks.