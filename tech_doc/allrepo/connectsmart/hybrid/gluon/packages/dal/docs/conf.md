# PyDAL Documentation Configuration

## Overview
Documentation configuration file for PyDAL, defining documentation generation settings, themes, and build parameters.

## Key Features

### Sphinx Configuration
```python
# Sphinx documentation configuration
project = 'PyDAL'
author = 'PyDAL Development Team'
version = '19.12'
release = '19.12.14'
```

### Documentation Settings
- **Project Information**: Name, version, and metadata
- **Theme Configuration**: Documentation theme and styling
- **Extension Setup**: Sphinx extensions and plugins
- **Build Settings**: Output formats and build options

### Extensions
```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode'
]
```

### Output Configuration
- **HTML Output**: Web documentation generation
- **PDF Output**: LaTeX and PDF generation
- **EPUB Output**: E-book format generation
- **Man Pages**: Unix manual page generation

### API Documentation
- **Autodoc**: Automatic API documentation from docstrings
- **Cross-references**: Inter-module linking
- **Code Examples**: Executable code examples
- **Coverage Reports**: Documentation coverage analysis

### Theme and Styling
- **Theme Selection**: Documentation theme configuration
- **Custom CSS**: Additional styling options
- **Logo and Branding**: Project branding elements
- **Navigation**: Documentation structure and navigation

This configuration enables comprehensive documentation generation for the PyDAL database abstraction layer, providing complete API documentation and user guides.