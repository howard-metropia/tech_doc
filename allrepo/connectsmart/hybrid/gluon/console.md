# Gluon Console Module Documentation

## Overview
The `console.py` module provides comprehensive command-line interface functionality for the Gluon web framework. It implements argument parsing, configuration management, and command validation using the `argparse` library to handle all web2py startup options and parameters.

## Module Information
- **File**: `allrepo/connectsmart/hybrid/gluon/console.py`
- **Component**: Web2py Framework Console Interface
- **Purpose**: Command-line argument processing and validation
- **Dependencies**: argparse, ast, socket, logging
- **Author**: Paolo Pastori

## Key Components

### Main Function
```python
def console(version):
    """
    Load command line options.
    Trivial -h/--help and --version options are also processed.
    
    Returns a namespace object (in the sense of argparse)
    with all options loaded.
    """
```

### Core Classes

#### HelpFormatter2
Custom argument formatter that hides deprecated and alternative option forms from help display.

**Features:**
- Hides deprecated options from usage help
- Supports both underscore and hyphen option styles
- Maintains backward compatibility

**Hidden Options:**
```python
_omitted_opts = (
    "--add-options", "--errors-to-console", "--no-banner",
    "--log-level", "--no-gui", "--import-models",
    "--force-migrate", "--server-name", "--server-key",
    "--server-cert", "--ca-cert", "--pid-filename",
    "--log-filename", "--min-threads", "--max-threads",
    # ... and more
)
```

#### ExtendAction
Custom argparse action for accumulating values in flat lists.

**Purpose:**
- Handles multiple argument values
- Flattens nested lists
- Extends existing argument lists

### Configuration Groups

#### Global Options
- **-f/--folder**: Web2py installation directory
- **-L/--config**: Python configuration file
- **-a/--password**: Administration password
- **-e/--errors_to_console**: Log errors to console
- **-Q/--quiet**: Disable all output
- **-D/--log_level**: Set logging level

#### Web Server Options
- **-s/--server_name**: Web server name
- **-i/--ip**: Server IP address (IPv4/IPv6)
- **-p/--port**: Server port number
- **-k/--server_key**: SSL private key file
- **-c/--server_cert**: SSL certificate file
- **--interface**: Network interface specification

#### Console Options
- **-S/--shell**: Interactive shell with application environment
- **-B/--bpython**: Use bpython shell
- **-P/--plain**: Use plain Python shell
- **-M/--import_models**: Auto-import model files
- **-R/--run**: Execute Python file in web2py environment
- **-A/--args**: Arguments for executed file

#### Scheduler Options
- **-X/--with_scheduler**: Run schedulers alongside web server
- **-K/--scheduler**: Application scheduler configuration

#### Cron Options
- **-Y/--with_cron**: Run cron service
- **--crontab**: Specify applications for cron processing
- **-C/--cron_run**: Trigger cron run and exit

#### Test Options
- **-T/--run_doctests**: Run application doctests
- **--run_system_tests**: Run web2py test suite
- **--with_coverage**: Collect coverage data

### Validation Functions

#### IP Address Validation
```python
def ip_addr(v):
    if not is_valid_ip_address(v):
        raise argparse.ArgumentTypeError("bad IP address %s" % v)
    return v
```

#### Port Validation
```python
def port(v):
    return not_negative_int(v, err_label="port")
```

#### Interface Validation
```python
def iface(v, sep=","):
    # Validates interface specification
    # Format: IP_ADDR,PORT[,KEY_FILE,CERT_FILE[,CA_CERT_FILE]]
```

### Configuration File Support

#### Configuration Loading
```python
def load_config(config_file, opt_map):
    """
    Load options from config file (a Python script).
    Uses AST parsing for safe evaluation.
    """
```

**Features:**
- Safe AST-based parsing (no code execution)
- PEP 263 encoding support
- Single-line assignment evaluation
- Ordered option preservation

#### Option Mapping
Comprehensive mapping of command-line options to configuration file options:
```python
opt_map = {
    # Global options
    "config": str_or_default,
    "password": str_or_default,
    "log_level": str_or_default,
    # Server options
    "ip": str_or_default,
    "port": str_or_default,
    "server_key": str_or_default,
    # ... complete mapping
}
```

### Deprecated Options Handling

#### Deprecation Mapping
```python
deprecated_opts = {
    "--debug": "--log_level",
    "--nogui": "--no_gui",
    "--ssl_private_key": "--server_key",
    "--ssl_certificate": "--server_cert",
    "--numthreads": "--min_threads",
    # ... full mapping
}
```

#### Warning System
- Automatic detection of deprecated options
- Helpful replacement suggestions
- Backward compatibility maintenance

### Validation Rules

#### Option Consistency Checks
- **-R/--run** requires **-S/--shell**
- **-A/--args** requires **-R/--run**
- **-X/--with_scheduler** requires **-K/--scheduler**
- **--soft_cron** requires **-Y/--with_cron**

#### Conflicting Options Detection
- **-B/--bpython** and **-P/--plain** are mutually exclusive
- **-S/--shell** conflicts with server-related options
- **-C/--cron_run** conflicts with other run modes

### Encoding Support

#### PEP 263 Compliance
```python
def get_pep263_encoding(source):
    """
    Read python source file encoding, according to PEP 263
    """
    REGEX_PEP263 = r"^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)"
```

### Platform-Specific Features

#### Windows Taskbar Support
```python
if options.taskbar and os.name != "nt":
    warn("--taskbar not supported on this platform, skipped")
    options.taskbar = False
```

## Usage Examples

### Basic Web Server
```bash
python web2py.py -i 127.0.0.1 -p 8000 -a password
```

### Interactive Shell
```bash
python web2py.py -S myapp -M
```

### Configuration File
```bash
python web2py.py -L config.py
```

### SSL Server
```bash
python web2py.py -k server.key -c server.crt -i 0.0.0.0 -p 443
```

### Scheduler Service
```bash
python web2py.py -K myapp:group1:group2 -X
```

## Security Considerations

### Password Handling
- Special `<ask>` value prompts for password
- `<recycle>` reuses last password
- Password masked in global settings copy

### File Validation
- Strict validation for certificate files
- Path existence checks
- Encoding detection for config files

## Error Handling

### Validation Errors
- Clear error messages with context
- Suggestion system for deprecated options
- Graceful fallback mechanisms

### Consistency Checks
- Comprehensive option validation
- Conflict detection and reporting
- Required dependency verification

## Integration Points

### Global Settings
- Options copied to `global_settings.cmd_options`
- Password masking for security
- Deep copy for isolation

### Application Context
- Folder detection and validation
- Application directory checking
- Environment setup preparation

## Performance Characteristics

### Parsing Speed
- Single-pass argument processing
- Efficient validation functions
- Minimal overhead for common cases

### Memory Usage
- Option copying and isolation
- Configuration file caching
- Reasonable memory footprint

## Extensibility Features

### Custom Actions
- ExtendAction for list accumulation
- Flexible argument handling
- Type conversion support

### Plugin Architecture
- Modular option groups
- Easy addition of new options
- Backward compatibility preservation

This console module provides the foundation for all web2py command-line operations, offering comprehensive option handling, validation, and configuration management while maintaining excellent backward compatibility and extensibility.