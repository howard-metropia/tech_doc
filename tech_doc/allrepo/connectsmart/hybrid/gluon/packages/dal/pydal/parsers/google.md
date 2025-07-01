# PyDAL Google Cloud SQL Parser

## Overview
Specialized parser for Google Cloud SQL and BigQuery, supporting Google's SQL dialect and cloud-specific features.

## Key Features

### Google SQL Support
```python
class GoogleParser(BaseParser):
    """
    Google Cloud SQL parser
    
    Features:
    - BigQuery SQL dialect
    - Standard SQL compliance
    - Cloud functions
    - Analytics operations
    """
```

### BigQuery Features
- **Array Functions**: ARRAY operations parsing
- **Struct Types**: Nested data structure parsing
- **Analytics Functions**: Window function parsing
- **Geography Functions**: Spatial operation parsing

### Cloud Integration
- **Standard SQL**: ANSI SQL compliance
- **Legacy SQL**: BigQuery legacy syntax
- **Cloud Functions**: UDF parsing
- **Data Types**: Cloud-specific type parsing

This parser handles Google's cloud database SQL dialects and advanced analytics features.