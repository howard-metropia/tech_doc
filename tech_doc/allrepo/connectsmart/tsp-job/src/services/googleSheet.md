# Google Sheets Service

## Overview

The Google Sheets service provides a streamlined interface for accessing Google Spreadsheet data using service account authentication. This service enables automated data extraction from Google Sheets for integration with TSP job processing workflows, supporting various data import and synchronization scenarios.

## Service Information

- **Service Name**: Google Sheets Data Extraction Service
- **File Path**: `/src/services/googleSheet.js`
- **Type**: Data Integration Service
- **Dependencies**: google-spreadsheet NPM package, Service Account Credentials

## Core Functions

### getData(docID, sheetID, credentialsPath)

Extracts raw data from a specified Google Spreadsheet using service account authentication and returns it in a processable format.

**Purpose**: Retrieve spreadsheet data for automated processing
**Parameters**: 
- `docID` (string): Google Spreadsheet document identifier
- `sheetID` (string): Specific sheet/tab identifier within the document
- `credentialsPath` (string): Path to service account credentials JSON file (default: '../../docs/credentials.json')
**Returns**: Array of arrays containing raw row data

**Authentication Flow**:
1. Loads service account credentials from specified JSON file
2. Authenticates with Google Sheets API using service account
3. Loads document metadata and information
4. Accesses specific sheet by ID
5. Retrieves all rows from the target sheet

**Data Processing**:
```javascript
const result = [];
const doc = new GoogleSpreadsheet(docID);
const creds = require(credentialsPath);
await doc.useServiceAccountAuth(creds);
await doc.loadInfo();
const sheet = doc.sheetsById[sheetID];
const rows = await sheet.getRows();
for (row of rows) {
  result.push(row._rawData);
}
return result;
```

**Return Format**:
The function returns an array where each element represents a spreadsheet row as an array of cell values:
```javascript
[
  ["Header1", "Header2", "Header3"],
  ["Value1", "Value2", "Value3"],
  ["Value4", "Value5", "Value6"]
]
```

## Technical Architecture

### Authentication System

**Service Account Authentication**:
- Uses Google Service Account for server-to-server authentication
- Eliminates need for user consent flow
- Supports automated, unattended data access
- Requires JSON credentials file with private key

**Credentials Structure**:
The service expects a JSON credentials file containing:
- **type**: "service_account"
- **project_id**: Google Cloud Project identifier
- **private_key_id**: Key identifier for the service account
- **private_key**: RSA private key for authentication
- **client_email**: Service account email address
- **client_id**: Unique client identifier
- **auth_uri**: OAuth 2.0 authorization endpoint
- **token_uri**: OAuth 2.0 token endpoint

### Google Sheets API Integration

**API Access Pattern**:
1. **Document Loading**: Retrieves spreadsheet metadata
2. **Sheet Selection**: Accesses specific sheet by internal ID
3. **Data Extraction**: Fetches all rows with values
4. **Raw Data Access**: Uses `_rawData` property for unprocessed values

**Sheet Identification**:
- Uses `sheetID` parameter to identify specific tabs within spreadsheet
- Different from sheet index (position-based)
- Provides stable reference even if sheet order changes
- Can be found in Google Sheets URL or via API inspection

### Data Access Patterns

**Row-based Processing**:
```javascript
const rows = await sheet.getRows();
for (row of rows) {
  result.push(row._rawData);
}
```

**Raw Data Extraction**:
- Accesses `_rawData` property for unformatted cell values
- Preserves original data types and formatting
- Includes empty cells as undefined/null values
- Maintains column order and structure

## Security Considerations

### Service Account Security

**Credential Management**:
- Store credentials file outside web-accessible directories
- Use environment variables for sensitive file paths
- Implement file permission restrictions (600 or 400)
- Regular credential rotation following security policies

**Access Control**:
- Grant minimal necessary permissions to service account
- Use Google Workspace domain restrictions where applicable
- Monitor service account usage through audit logs
- Implement IP-based access restrictions if needed

**Best Practices**:
```javascript
// Secure credential loading with error handling
let creds;
try {
  creds = require(credentialsPath);
  if (!creds.private_key || !creds.client_email) {
    throw new Error('Invalid service account credentials');
  }
} catch (error) {
  logger.error('Failed to load service account credentials');
  throw error;
}
```

### Data Privacy

**Information Protection**:
- Ensure spreadsheets don't contain sensitive personal data
- Implement data retention policies for extracted information
- Consider data encryption for temporary storage
- Audit data access and usage patterns

## Error Handling Strategy

### Common Error Scenarios

**Authentication Failures**:
- Invalid or expired service account credentials
- Insufficient permissions for target spreadsheet
- Network connectivity issues
- API quota limitations

**Data Access Errors**:
- Spreadsheet not found or access denied
- Invalid sheet ID or deleted sheet
- Empty spreadsheet or sheet
- API rate limiting

**Robust Error Handling Pattern**:
```javascript
async function getDataWithErrorHandling(docID, sheetID, credentialsPath) {
  try {
    const result = await getData(docID, sheetID, credentialsPath);
    return result;
  } catch (error) {
    if (error.message.includes('Unable to parse')) {
      throw new Error('Invalid spreadsheet format or structure');
    } else if (error.message.includes('Insufficient Permission')) {
      throw new Error('Service account lacks access to spreadsheet');
    } else if (error.message.includes('not found')) {
      throw new Error('Spreadsheet or sheet not found');
    } else {
      logger.error(`Google Sheets API error: ${error.message}`);
      throw error;
    }
  }
}
```

## Performance Considerations

### API Efficiency

**Request Optimization**:
- Single API call retrieves all sheet data
- Batch processing for multiple sheets
- Implement caching for frequently accessed data
- Monitor API quota usage and implement throttling

**Data Processing**:
- Stream processing for large datasets
- Memory-efficient row iteration
- Lazy loading for unused data
- Implement data pagination if needed

### Caching Strategies

**Local Caching**:
```javascript
const cache = new Map();
const cacheKey = `${docID}-${sheetID}`;

async function getCachedData(docID, sheetID, credentialsPath, ttl = 300000) {
  const cached = cache.get(cacheKey);
  if (cached && (Date.now() - cached.timestamp) < ttl) {
    return cached.data;
  }
  
  const data = await getData(docID, sheetID, credentialsPath);
  cache.set(cacheKey, { data, timestamp: Date.now() });
  return data;
}
```

## Integration Patterns

### TSP Job Integration

**Data Import Workflows**:
- Configuration data loading from Google Sheets
- User data imports and updates
- Report generation source data
- Reference data synchronization

**Common Use Cases**:
1. **Configuration Management**: Load application settings from sheets
2. **Data Migration**: Import legacy data from spreadsheets
3. **Report Processing**: Extract data for analytics and reporting
4. **Content Management**: Manage dynamic content through sheets

### Data Processing Pipeline

**Typical Processing Flow**:
```javascript
async function processSpreadsheetData(docID, sheetID) {
  // Extract raw data
  const rawData = await getData(docID, sheetID);
  
  // Process header row
  const [headers, ...dataRows] = rawData;
  
  // Convert to objects
  const processedData = dataRows.map(row => {
    const obj = {};
    headers.forEach((header, index) => {
      obj[header] = row[index];
    });
    return obj;
  });
  
  // Additional processing
  return processedData.filter(item => item.status === 'active');
}
```

## Usage Examples

### Basic Data Extraction

```javascript
const { getData } = require('./googleSheet');

// Extract data with default credentials path
const data = await getData(
  '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms',
  '0',
  '../../docs/credentials.json'
);

console.log(`Extracted ${data.length} rows`);
```

### Advanced Processing

```javascript
async function processConfigurationSheet() {
  try {
    const rawData = await getData(docID, sheetID);
    
    // Skip header row and process configuration
    const [headers, ...configRows] = rawData;
    const config = {};
    
    configRows.forEach(row => {
      const [key, value, type] = row;
      if (key && value) {
        config[key] = type === 'number' ? parseFloat(value) : value;
      }
    });
    
    return config;
  } catch (error) {
    logger.error(`Configuration processing failed: ${error.message}`);
    throw error;
  }
}
```

### Error Handling Implementation

```javascript
async function safeGetData(docID, sheetID, credentialsPath) {
  const maxRetries = 3;
  let attempt = 0;
  
  while (attempt < maxRetries) {
    try {
      return await getData(docID, sheetID, credentialsPath);
    } catch (error) {
      attempt++;
      
      if (attempt >= maxRetries) {
        logger.error(`Failed to retrieve data after ${maxRetries} attempts`);
        throw error;
      }
      
      // Exponential backoff
      const delay = Math.pow(2, attempt) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

## Limitations and Considerations

### Current Limitations

**Function Simplicity**:
- Single function with limited configuration options
- No built-in error handling or retry logic
- Basic data extraction without processing capabilities
- No support for writing data back to sheets

**API Constraints**:
- Google Sheets API quota limitations
- Rate limiting for high-frequency access
- Maximum sheet size limitations
- Network dependency for all operations

### Future Enhancements

**Enhanced Functionality**:
- Data writing and updating capabilities
- Advanced filtering and query options
- Batch processing for multiple sheets
- Caching and offline support

**Error Handling Improvements**:
- Automatic retry mechanisms with exponential backoff
- Comprehensive error categorization and handling
- Logging and monitoring integration
- Graceful degradation strategies

**Performance Optimizations**:
- Streaming for large datasets
- Partial data loading and pagination
- Connection pooling and reuse
- Memory usage optimization

## Dependencies

- **google-spreadsheet**: Primary library for Google Sheets API integration
  - Version: Latest stable version supporting service account authentication
  - Provides comprehensive API for spreadsheet operations
  - Handles authentication, data retrieval, and formatting

**Service Account Requirements**:
- Google Cloud Project with Sheets API enabled
- Service account with appropriate permissions
- JSON credentials file with private key
- Spreadsheet sharing permissions for service account email

## Best Practices

### Implementation Guidelines

1. **Credential Security**: Store credentials securely and rotate regularly
2. **Error Handling**: Implement comprehensive error handling and retry logic
3. **Caching**: Use caching for frequently accessed data to reduce API calls
4. **Monitoring**: Track API usage and performance metrics
5. **Documentation**: Maintain clear documentation of spreadsheet schemas and usage

### Performance Optimization

1. **Batch Operations**: Process multiple sheets in single API session
2. **Data Validation**: Validate data structure before processing
3. **Memory Management**: Handle large datasets efficiently
4. **API Quota Management**: Monitor and manage API quota usage
5. **Connection Reuse**: Reuse authenticated connections when possible