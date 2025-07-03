# mtc-user-signup.js

## Overview
Job for synchronizing MTC (Metropolitan Transportation Commission) user signup data from Google Sheets to the database. Processes phone numbers from spreadsheet and creates user records for experiment participation.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/mtc-user-signup.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `@app/src/services/googleSheet.js` - Google Sheets integration service
- `@maas/core/log` - Logging utility

## Core Functions

### Main Processing Function
Reads Google Sheets data and synchronizes with MTC user signup table.

**Process Flow:**
1. Fetch data from specified Google Sheet
2. Clean and normalize phone numbers
3. Match phone numbers to existing users
4. Insert new MTC signup records

## Job Configuration

### Inputs
No input parameters required.

### Google Sheets Configuration
- **Document ID**: `16sgMYC9TSkX58jKogshE99W_UZYvjOGACgss0Q-wvr4`
- **Sheet ID**: `0` (first sheet)
- **Data Source**: Phone numbers in column format

## Processing Flow

### 1. Data Retrieval
```javascript
const resp = await getData(docID, sheetID);
```

### 2. Phone Number Processing
For each entry in the spreadsheet:
- Extract phone number from column index [1]
- Remove hyphens and formatting characters
- Normalize to clean numeric format

### 3. User Matching
```sql
SELECT * FROM hybrid.auth_user 
WHERE phone_number LIKE '%${cleanedPhoneNumber}%'
AND NOT EXISTS (
  SELECT user_id FROM hybrid.mtc_user_signup 
  WHERE user_id = auth_user.id
)
```

### 4. Record Insertion
For matched users not already in MTC signup:
```sql
INSERT INTO hybrid.mtc_user_signup (
  user_id, first_name, last_name, e_mail, phone_number
) VALUES (...)
```

## Data Models

### Google Sheets Structure
```javascript
{
  [rowIndex]: [
    column0_value,
    phone_number, // Index [1] - target data
    column2_value,
    ...
  ]
}
```

### mtc_user_signup Table
```javascript
{
  user_id: number,
  first_name: string,
  last_name: string,
  e_mail: string,
  phone_number: string
}
```

### auth_user Reference Table
```javascript
{
  id: number,
  first_name: string,
  last_name: string,
  email: string,
  phone_number: string
}
```

## Business Logic

### Phone Number Normalization
```javascript
const cleanedNumber = phoneNumber
  .replace(/\-{1}/, '')  // Remove first hyphen
  .replace(/\-{1}/, ''); // Remove second hyphen
```

### Duplicate Prevention
- Checks for existing records in mtc_user_signup
- Uses NOT EXISTS clause to prevent duplicates
- Ensures data integrity across processing runs

### User Matching Strategy
- Uses LIKE operator with wildcards for flexible matching
- Accommodates variations in phone number formatting
- Matches against existing authenticated users only

## Error Handling
- Graceful handling of missing user matches
- Continues processing if individual records fail
- Logs successful insertions for audit trail

## Integration Points
- Google Sheets API for data retrieval
- User authentication system (auth_user table)
- MTC experiment framework
- Database transaction management

## Performance Considerations
- Processes records sequentially to maintain data integrity
- Uses efficient SQL queries with EXISTS clauses
- Minimizes database calls through targeted queries

## Security Considerations
- Read-only access to Google Sheets
- Phone number data handling with proper sanitization
- Database insertion with parameterized queries

## Usage Scenarios
- Daily synchronization of new experiment participants
- Manual execution after signup campaigns
- Data migration from external signup forms
- Participant list management for research studies

## Configuration Dependencies
- Google Sheets API credentials and access
- Specific document and sheet ID configuration
- Database connection permissions
- Service account authentication for sheets access

## Monitoring and Logging
- Logs cleaned phone numbers for verification
- SQL query logging for debugging
- Successful insertion confirmation
- Processing completion status

## Data Flow
1. **Source**: Google Sheets with participant data
2. **Processing**: Phone number cleaning and user matching
3. **Validation**: Duplicate checking and user existence
4. **Storage**: MTC user signup table insertion
5. **Logging**: Audit trail for successful operations

## Notes
- Designed for MTC-specific experiment user management
- Supports manual participant enrollment processes
- Integrates with broader MTC research infrastructure
- Maintains data consistency across multiple processing runs
- Simple but effective approach to external data synchronization