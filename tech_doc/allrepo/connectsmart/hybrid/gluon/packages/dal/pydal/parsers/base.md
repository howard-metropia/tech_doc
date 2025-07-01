# PyDAL Base Parser

## Overview
The base parser provides fundamental SQL parsing capabilities and serves as the foundation for database-specific parsers.

## Key Features

### Core Parsing
```python
class BaseParser:
    """
    Foundation SQL parser for PyDAL
    
    Features:
    - SQL tokenization
    - Syntax tree generation
    - Query validation
    - Error reporting
    """
```

### Parsing Functions
- **Tokenization**: SQL statement tokenization
- **Syntax Analysis**: SQL grammar validation  
- **Tree Generation**: Abstract syntax tree creation
- **Error Handling**: Comprehensive error reporting

### Common Operations
- **Query Type Detection**: SELECT, INSERT, UPDATE, DELETE
- **Table Extraction**: Referenced table identification
- **Column Analysis**: Column usage analysis
- **Join Detection**: Join operation identification

This parser provides the foundation for all database-specific parsing implementations.