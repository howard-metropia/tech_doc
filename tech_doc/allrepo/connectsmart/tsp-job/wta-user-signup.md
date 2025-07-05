# wta-user-signup.js

## Overview
Job for processing WTA (Washington Transit Authority) user signup data from Google Sheets and creating consent agreement records in the database. Matches phone numbers from external signup sources with existing authenticated users and automatically grants consent for experiment participation.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/wta-user-signup.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `@app/src/services/googleSheet.js` - Google Sheets data retrieval service
- `@maas/core/log` - Logging utility

## Core Functions

### Main Processing Function
Synchronizes WTA user signups from Google Sheets with internal user consent tracking system.

**Process Flow:**
1. Retrieve signup data from specified Google Sheet
2. Clean and normalize phone number data
3. Match phone numbers to existing authenticated users
4. Create consent agreement records for matched users
5. Skip users already in consent tracking system

## Job Configuration

### Inputs
No input parameters required.

### Google Sheets Configuration
- **Document ID**: `1XqM0duZgSHewAbsb6KykFVg6iIsl4iZlBiSgztRIi4w`
- **Sheet ID**: `0` (first sheet/tab)
- **Data Format**: Phone numbers in column index [2]

## Processing Flow

### 1. Google Sheets Data Retrieval
```javascript
const docID = '1XqM0duZgSHewAbsb6KykFVg6iIsl4iZlBiSgztRIi4w';
const sheetID = '0';
const resp = await getData(docID, sheetID);
```

### 2. Phone Number Processing
For each row in the spreadsheet:
```javascript
const rawPhoneNumber = resp[attr][2];
const cleanedPhoneNumber = rawPhoneNumber
  .replace(/\-{1}/, '')  // Remove first hyphen
  .replace(/\-{1}/, ''); // Remove second hyphen
```

### 3. User Matching Query
```sql
SELECT Table1.* FROM (
  SELECT * FROM hybrid.auth_user
  WHERE phone_number LIKE '%${cleanedPhoneNumber}%'
) AS Table1 WHERE NOT EXISTS (
  SELECT user_id FROM hybrid.wta_agree 
  WHERE user_id = Table1.id
)
```

### 4. Consent Agreement Creation
For matched users not already in consent system:
```sql
INSERT INTO hybrid.wta_agree (
  user_id, wta_agree, resend
) VALUES (
  "${user_id}", "1", "3"
)
```

## Data Models

### Google Sheets Data Structure
```javascript
{
  [rowIndex]: [
    column0_data,
    column1_data,
    phone_number,    // Index [2] - target data
    column3_data,
    // ... additional columns
  ]
}
```

### auth_user Reference Table
```javascript
{
  id: number,
  first_name: string,
  last_name: string,
  email: string,
  phone_number: string,
  created_on: datetime,
  modified_on: datetime
}
```

### wta_agree Consent Table
```javascript
{
  id: number,
  user_id: number,
  wta_agree: boolean,     // 1 = automatically agreed
  resend: number,         // 3 = max resends reached
  created_on: datetime,
  modified_on: datetime
}
```

## Business Logic

### Phone Number Normalization
```javascript
// Clean phone number format
const phoneNumberCleaning = (rawNumber) => {
  return rawNumber
    .replace(/\-{1}/, '')  // Remove first hyphen
    .replace(/\-{1}/, ''); // Remove second hyphen
};

// Example transformations
'555-123-4567' → '5551234567'
'(555) 123-4567' → '(555) 1234567'  // Preserves parentheses
```

### User Matching Strategy
- **Flexible Matching**: Uses LIKE operator with wildcards for partial matches
- **Format Tolerance**: Accommodates various phone number formats in database
- **Duplicate Prevention**: NOT EXISTS clause prevents duplicate consent records

### Automatic Consent Logic
Users from Google Sheets signup are automatically granted:
```javascript
const autoConsentSettings = {
  wta_agree: "1",  // Automatically agreed (bypasses consent form)
  resend: "3"      // Maximum resends reached (no further reminders)
};
```

### Duplicate Prevention Strategy
```sql
-- Only process users not already in consent system
WHERE NOT EXISTS (
  SELECT user_id FROM hybrid.wta_agree 
  WHERE user_id = auth_user.id
)
```

## Error Handling
- **Missing User Matches**: Continues processing if phone number not found
- **Database Errors**: Handles insertion failures gracefully
- **Invalid Phone Numbers**: Skips malformed phone number entries
- **Google Sheets Access**: Manages API connectivity issues

## Integration Points
- **Google Sheets API**: External signup data source
- **User Authentication System**: Matches against existing user database
- **WTA Consent System**: Creates consent agreement records
- **Experiment Management**: Enables participation in WTA studies

## Performance Considerations
- **Sequential Processing**: Processes one record at a time for data integrity
- **Efficient Queries**: Uses EXISTS clauses for duplicate checking
- **Minimal API Calls**: Single Google Sheets API call per execution
- **Database Optimization**: Indexed phone number searches

## Security Considerations
- **Data Privacy**: Secure handling of phone number information
- **SQL Injection Prevention**: Parameterized queries (needs improvement)
- **API Access Control**: Google Sheets service account authentication
- **User Consent**: Automatic consent granted for external signups

## Google Sheets Integration

### Data Source Configuration
```javascript
const googleSheetsConfig = {
  documentId: '1XqM0duZgSHewAbsb6KykFVg6iIsl4iZlBiSgztRIi4w',
  sheetId: '0',          // First sheet tab
  dataColumn: 2,         // Phone numbers in column C (0-indexed)
  hasHeaders: true       // Assumes first row contains headers
};
```

### Expected Sheet Format
| Column A | Column B | Column C (Phone) | Column D |
|----------|----------|------------------|----------|
| Name     | Email    | 555-123-4567     | Other    |
| John     | john@ex  | 555-987-6543     | Data     |

### API Service Integration
```javascript
// Utilizes custom Google Sheets service
const { getData } = require('@app/src/services/googleSheet.js');

// Service handles authentication and data parsing
const sheetData = await getData(documentId, sheetId);
```

## Usage Scenarios
- **External Signup Integration**: Processing users who signed up through web forms
- **Manual Enrollment**: Adding users who registered through other channels
- **Bulk User Import**: Migrating signup lists from external systems
- **Campaign Integration**: Processing participants from marketing campaigns

## Configuration Dependencies
- **Google Sheets API**: Service account credentials and permissions
- **Database Access**: MySQL connection with insert permissions
- **Document Access**: Read permissions for specified Google Sheet
- **Phone Number Indexing**: Database indexes for efficient phone searches

## Data Processing Workflow

### Input Phase
1. Connect to Google Sheets API
2. Retrieve data from specified document and sheet
3. Parse row-based data structure
4. Extract phone numbers from designated column

### Matching Phase
1. Clean and normalize phone number format
2. Search auth_user table for matching phone numbers
3. Apply duplicate prevention filtering
4. Identify users eligible for consent creation

### Output Phase
1. Create wta_agree records for matched users
2. Set automatic consent flags
3. Log successful processing
4. Continue with remaining entries

## Monitoring and Logging
- **Google Sheets Access**: API connection and data retrieval status
- **Phone Number Processing**: Cleaning and normalization results
- **User Matching**: Successful and failed phone number matches
- **Consent Creation**: Database insertion confirmation
- **Processing Summary**: Total records processed and success rate

## Data Flow
1. **Source**: Google Sheets with external signup data
2. **Extraction**: Phone number data retrieval and cleaning
3. **Matching**: User identification in authentication system
4. **Validation**: Duplicate prevention and eligibility checking
5. **Creation**: Consent agreement record insertion
6. **Logging**: Processing status and audit trail

## Consent Management Integration

### Automatic Consent Workflow
Users processed through this job receive automatic consent:
- **Bypass Consent Form**: No email consent form required
- **Immediate Participation**: Ready for experiment enrollment
- **No Reminders**: Maximum resend count prevents further emails

### Integration with WTA Pipeline
1. **Signup Processing**: This job creates consent records
2. **Market Analysis**: wta-polygon.js identifies geographic eligibility
3. **Experiment Enrollment**: Users enter WTA experimental framework
4. **Survey Distribution**: Micro-surveys and post-experiment questionnaires

## Quality Assurance

### Data Validation
- **Phone Number Format**: Handles various formatting conventions
- **User Existence**: Verifies users exist in authentication system
- **Duplicate Prevention**: Ensures single consent record per user

### Processing Integrity
- **Transaction Safety**: Database operations maintain consistency
- **Error Recovery**: Continues processing despite individual failures
- **Audit Trail**: Comprehensive logging for verification

## Notes
- **External Integration**: Bridges gap between external signups and internal systems
- **Automatic Consent**: Streamlines user onboarding for research participation
- **Flexible Matching**: Accommodates various phone number formats
- **WTA Specific**: Designed for Washington Transit Authority research studies
- **Scalable Processing**: Handles variable-sized signup lists
- **Privacy Compliant**: Maintains secure handling of personal information
- **Research Focused**: Supports transportation behavior modification studies
- **Integration Ready**: Works with broader WTA experimental infrastructure