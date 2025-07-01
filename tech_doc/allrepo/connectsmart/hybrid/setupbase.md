# Setup Base - Web2py Build Utilities

## Overview
`setupbase.py` provides essential build utilities and Python setup helpers for the Web2py framework installation. This module manages Git submodules, ensures clean repository state, and provides setuptools commands for automated Web2py deployment and maintenance.

## Key Features
- **Git Submodule Management**: Automated initialization and synchronization of PyDAL and YATL submodules
- **Repository State Validation**: Ensures clean submodule state before build operations
- **Custom Setuptools Commands**: Extends setuptools with Web2py-specific build commands
- **Cross-Platform Compatibility**: Handles Windows Unicode path issues and frozen executable detection

## Core Components

### Constants
```python
SUBMODULES = ['pydal', 'yatl']
SUBMODULE_SYNC_PATHS = [('gluon/dal', 'gluon/yatl')]
```
- **SUBMODULES**: Core Web2py framework dependencies (PyDAL ORM, YATL templating)
- **SUBMODULE_SYNC_PATHS**: Directory mapping for submodule synchronization

### Repository Management Functions

#### `is_repo(d)`
Detects if directory is a Git repository.
- **Parameters**: `d` (str) - Directory path to check
- **Returns**: Boolean indicating Git repository presence
- **Implementation**: Checks for `.git` directory existence

#### `check_submodule_status(root=None)`
Comprehensive submodule status validation with three-state return:
- **'clean'**: All submodules up-to-date and properly synchronized
- **'missing'**: Required submodules absent from filesystem
- **'unclean'**: Submodules contain unstaged changes or conflicts

**Special Handling**:
- Frozen executables (py2exe) return 'clean' automatically
- Non-Git directories assumed clean
- Windows Python 2.x Unicode path encoding

**Git Status Parsing**:
```python
for line in status.splitlines():
    if line.startswith('-'):  # Missing submodule
        return 'missing'
    elif line.startswith('+'):  # Uncommitted changes
        return 'unclean'
```

#### `update_submodules(repo_dir)`
Automated submodule initialization and recursive updates.
- **Implementation**: Executes `git submodule init` followed by `git submodule update --recursive`
- **Error Handling**: Uses `subprocess.check_call()` for immediate failure detection

#### `require_clean_submodules(repo_dir, argv)`
Pre-build validation ensuring repository integrity.
- **Bypass Conditions**: Help commands, clean operations, explicit submodule commands
- **Automatic Fixes**: First-time missing submodules auto-initialized
- **Build Prevention**: Exits with error code 1 for unclean states

**Error Messaging**:
```python
print('\n'.join([
    "Cannot build / install web2py with unclean submodules",
    "Please update submodules with",
    "    python setup.py submodule",
    "or",
    "    git submodule update",
    "or commit any submodule changes you have made."
]))
```

### Custom Setuptools Commands

#### `UpdateSubmodules(Command)`
Setuptools-integrated submodule management command.
- **Command Name**: `submodule`
- **Description**: "Update git submodules"
- **Implementation**: Spawns Git commands via `self.spawn()`
- **Validation**: Post-update status verification

**Execution Flow**:
1. Initialize submodules (`git submodule init`)
2. Recursive update (`git submodule update --recursive`)
3. Status verification
4. Exit on failure

#### `require_submodules(command)`
Decorator factory for command submodule validation.
- **Purpose**: Ensures commands only run with clean submodules
- **Implementation**: Creates dynamic command class wrapper
- **Usage**: Decorates setup.py build commands

**Decorator Pattern**:
```python
class DecoratedCommand(command):
    def run(self):
        if not check_submodule_status(repo_root) == 'clean':
            print("submodules missing! Run `setup.py submodule` and try again")
            sys.exit(1)
        command.run(self)
```

## Dependencies
- **Core**: `os`, `subprocess`, `sys`
- **Setuptools**: `Command` class (fallback to `distutils.cmd`)
- **Git**: Repository management via subprocess calls

## Usage Patterns

### Standard Setup Integration
```python
from setupbase import (
    UpdateSubmodules,
    require_clean_submodules
)

# Pre-build validation
require_clean_submodules(here, sys.argv)

# Custom command registration
setup(
    cmdclass={'submodule': UpdateSubmodules}
)
```

### Command Decoration
```python
@require_submodules
class CustomBuildCommand(Command):
    def run(self):
        # Build logic here
        pass
```

## Error Handling
- **Subprocess Failures**: Git command errors propagated to setuptools
- **Missing Submodules**: Automatic initialization on first run
- **Unclean State**: Build prevention with clear remediation steps
- **Windows Compatibility**: Unicode path encoding for subprocess calls

## Platform Considerations
- **Windows Python 2.x**: Filesystem encoding conversion for subprocess
- **Frozen Executables**: Bypassed validation for py2exe/similar
- **Shell Commands**: Platform-appropriate shell execution

## Integration Points
- **setup.py**: Main entry point for Web2py installation
- **Git Workflow**: Submodule synchronization with upstream repositories
- **Build Pipeline**: Pre-build validation and automated fixes
- **Development Workflow**: Developer-friendly error messages and remediation

## Security Considerations
- **Command Injection**: Uses `shell=True` but with controlled input
- **Path Traversal**: Directory operations use `os.path.join()` safely
- **Subprocess Safety**: Git commands executed in controlled repository context

## Performance Notes
- **Lazy Evaluation**: Status checks only when needed
- **Subprocess Overhead**: Git operations may be slow on large repositories
- **Recursive Updates**: Deep submodule trees increase update time

This utility module provides the foundation for reliable Web2py framework installation and maintenance, ensuring consistent submodule state across development and production environments.