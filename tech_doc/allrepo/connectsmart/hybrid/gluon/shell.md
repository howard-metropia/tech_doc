# Shell Module

## Overview
The shell module provides interactive command-line interface capabilities for web2py applications. It enables running applications in shell mode, executing controllers and functions directly, running tests, and providing interactive Python sessions with web2py context. This module is essential for development, debugging, and administrative tasks.

## Core Functions

### env()
Creates a web2py execution environment for a specified application.

```python
def env(a, import_models=False, c=None, f=None, 
        dir="", extra_request={})
```

**Parameters:**
- `a`: Application name
- `import_models`: Execute model files
- `c`: Controller name
- `f`: Function name  
- `dir`: Custom application directory
- `extra_request`: Additional request attributes

**Returns**: Dictionary containing web2py environment

**Example:**
```python
# Basic environment
_env = env('myapp')

# With models loaded
_env = env('myapp', import_models=True)

# Specific controller/function
_env = env('myapp', c='default', f='index')
```

### run()
Main function for running web2py in various modes.

```python
def run(appname, plain=False, import_models=False, 
        startfile=None, bpython=False, python_code=None,
        cron_job=False, scheduler_job=False,
        force_migrate=False, fake_migrate=False)
```

**Modes:**
1. **Interactive Shell**: No additional parameters
2. **Script Execution**: `startfile` parameter
3. **Code Execution**: `python_code` parameter
4. **Function Call**: `appname` includes function

**Examples:**
```bash
# Interactive shell
python web2py.py -S myapp

# Run script
python web2py.py -S myapp -R script.py

# Execute code
python web2py.py -S myapp -C "print(db.tables)"

# Call function
python web2py.py -S myapp/default/index
```

### test()
Run doctests on controllers or applications.

```python
def test(testpath, import_models=True, verbose=False)
```

**Test Targets:**
- `myapp`: All controllers in application
- `myapp/controller`: Specific controller
- `myapp/controller/function`: Specific function
- File path: Individual file

**Example:**
```bash
# Test entire application
python web2py.py -T myapp

# Test specific controller
python web2py.py -T myapp/default

# Verbose output
python web2py.py -T myapp -v
```

## Shell Environments

### Environment Components
Every shell environment contains:

```python
environment = {
    # Core objects
    'request': Request(),
    'response': Response(),
    'session': Session(),
    
    # Database (if models imported)
    'db': database_connection,
    
    # Web2py helpers
    'T': translator,
    'cache': cache_object,
    'auth': authentication,
    
    # HTML helpers
    'A': A, 'DIV': DIV, 'SPAN': SPAN,
    # ... all HTML helpers
    
    # Application globals
    '__name__': '__main__'
}
```

### Request Object Configuration
```python
request.application = 'myapp'
request.controller = 'default'
request.function = 'index'
request.folder = '/path/to/applications/myapp'
request.is_shell = True
request.is_scheduler = False
```

## Interactive Sessions

### IPython Integration
Automatic IPython detection and usage:

```python
# Tries IPython variants
try:
    import IPython
    if IPython.__version__ > '1.0.0':
        IPython.start_ipython(user_ns=_env)
    # ... version-specific handling
except ImportError:
    # Fallback to standard Python shell
    code.interact(local=_env)
```

### BPython Support
```bash
# Use BPython if available
python web2py.py -S myapp --bpython
```

### History and Completion
Automatic setup when available:

```python
def enable_autocomplete_and_history(adir, env):
    import readline
    import rlcompleter
    
    readline.parse_and_bind("tab: complete")
    history_file = os.path.join(adir, ".pythonhistory")
    readline.read_history_file(history_file)
    readline.set_completer(rlcompleter.Completer(env).complete)
```

## Application Path Parsing

### parse_path_info()
Parse web2py-style paths into components.

```python
def parse_path_info(path_info, av=False)
```

**Format**: `application/controller/function`

**Examples:**
```python
# Basic parsing
a, c, f = parse_path_info('myapp/default/index')
# Returns: ('myapp', 'default', 'index')

# With args and vars
a, c, f, args, vars = parse_path_info(
    'myapp/default/show/123?format=json', av=True
)
# Returns: ('myapp', 'default', 'show', ['123'], {'format': 'json'})
```

## Script Execution

### Code Execution Modes

#### Python File Execution
```python
# Execute .py file
execfile(startfile, _env)

# Execute .pyc file  
exec(read_pyc(startfile), _env)
```

#### Direct Code Execution
```python
# Execute code string
exec(python_code, _env)
```

#### Function Calling
```python
# Call specific function
if f:
    exec("print(%s())" % f, _env)
```

### Error Handling
```python
try:
    execute_user_code()
    if import_models:
        BaseAdapter.close_all_instances('commit')
except SystemExit:
    if import_models:
        BaseAdapter.close_all_instances('rollback')
    raise
except Exception:
    if import_models:
        BaseAdapter.close_all_instances('rollback')
    print(traceback.format_exc())
```

## Development Utilities

### Application Creation
```python
if not os.path.exists(adir):
    confirm = raw_input(
        "application %s does not exist, create (y/N)?" % a
    )
    if confirm.lower() in ('y', 'yes'):
        os.mkdir(adir)
        fileutils.create_app(adir)
```

### Migration Control
```python
# Force migrations
if force_migrate:
    from gluon.dal import DAL
    orig_init = DAL.__init__
    
    def custom_init(*args, **kwargs):
        kwargs['migrate_enabled'] = True
        kwargs['migrate'] = True
        kwargs['fake_migrate'] = fake_migrate
        orig_init(*args, **kwargs)
    
    DAL.__init__ = custom_init
```

## Testing Framework

### Doctest Integration
```python
def doctest_object(name, obj):
    """Run doctests on object and nested methods"""
    
    if type(obj) in (types.FunctionType, type, ClassType):
        # Reload environment before each test
        globs = env(a, c=c, f=f, import_models=import_models)
        execfile(testfile, globs)
        
        doctest.run_docstring_examples(
            obj, globs=globs,
            name="%s: %s" % (os.path.basename(testfile), name),
            verbose=verbose
        )
```

### Test Discovery
```python
# Test file patterns
if c:
    # Specific controller
    files = [os.path.join(cdir, c + '.py')]
else:
    # All controllers
    files = glob.glob(os.path.join(cdir, '*.py'))
```

## Advanced Features

### exec_environment()
Low-level environment builder for custom setups.

```python
def exec_environment(pyfile="", request=None, 
                    response=None, session=None):
    # Build minimal environment
    env = build_environment(request, response, session, 
                           store_current=False)
    if pyfile:
        execfile(pyfile, env)
    return Storage(env)
```

### Credential Bypass
```python
def check_credentials(request, other_application="admin"):
    return True  # Allow admin access in shell

fileutils.check_credentials = check_credentials
```

## Command Line Integration

### Common Patterns
```bash
# Interactive shell with models
python web2py.py -S myapp -M

# Run script with imports
python web2py.py -S myapp -M -R scripts/populate.py

# Execute one-liner
python web2py.py -S myapp -M -C "print(len(db().select()))"

# Run tests with verbose output
python web2py.py -T myapp -v

# Force database migration
python web2py.py -S myapp -M --force-migrate
```

### Shell Scripts
```python
#!/usr/bin/env python
# shell_script.py
import sys
sys.path.append('/path/to/web2py')

from gluon.shell import env

# Get environment
_env = env('myapp', import_models=True)

# Access database
db = _env['db']
print("Tables:", db.tables)

# Use models
records = db(db.mytable).select()
print("Records:", len(records))
```

## Configuration Examples

### Development Workflow
```python
# development_shell.py
def setup_dev_environment():
    _env = env('myapp', import_models=True)
    
    # Add development helpers
    _env['reload_models'] = lambda: env('myapp', import_models=True)
    _env['clear_cache'] = lambda: cache.clear()
    _env['reset_db'] = lambda: db.executesql('DELETE FROM auth_user;')
    
    return _env

# Interactive session
if __name__ == '__main__':
    import code
    code.interact(local=setup_dev_environment())
```

### Batch Processing
```python
# batch_process.py
from gluon.shell import env

def process_users():
    _env = env('myapp', import_models=True)
    db = _env['db']
    
    for user in db(db.auth_user).select():
        # Process each user
        update_user_profile(user)
        
    db.commit()

if __name__ == '__main__':
    process_users()
```

## Error Handling

### Common Issues

1. **Module Import Errors**
```python
try:
    _env = env('myapp', import_models=True)
except Exception as e:
    print("Model import failed:", e)
    _env = env('myapp', import_models=False)
```

2. **Application Not Found**
```python
def safe_env(app_name):
    app_dir = os.path.join('applications', app_name)
    if not os.path.exists(app_dir):
        raise ValueError("Application %s not found" % app_name)
    return env(app_name)
```

3. **Database Connection Issues**
```python
def env_with_fallback(app_name):
    try:
        return env(app_name, import_models=True)
    except Exception:
        # Fallback without database
        return env(app_name, import_models=False)
```

## Best Practices

### Shell Development
1. Always use `import_models=True` for database access
2. Handle exceptions in batch scripts
3. Use transaction management for data modifications
4. Test scripts before running on production data

### Testing
1. Write comprehensive doctests
2. Use verbose mode for debugging
3. Test both success and failure cases
4. Mock external dependencies

### Performance
1. Avoid loading models when not needed
2. Use specific controller/function targeting
3. Close database connections properly
4. Profile long-running scripts

## See Also
- Web2py book shell chapter
- Python doctest documentation
- IPython configuration guide
- Web2py testing best practices