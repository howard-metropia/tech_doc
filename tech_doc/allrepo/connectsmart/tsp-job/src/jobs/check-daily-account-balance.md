# Check Daily Account Balance Job

## Overview
Job that performs daily account balance validation to detect abnormal account states and sends email alerts when issues are found.

## File Location
`/src/jobs/check-daily-account-balance.js`

## Dependencies
- `ejs` - Template engine for email generation
- `config` - Configuration management
- `@maas/core/log` - Logging framework
- `@app/src/helpers/mailer` - Email sending service
- `@app/src/services/check-account` - Account validation service

## Job Configuration

### Inputs
```javascript
inputs: {}
```
No input parameters required.

### Configuration Dependencies
- `config.app.project` - Project identifier
- `config.project.stage` - Environment stage
- `config.dailyAccount.mailActivated` - Email notification toggle
- `config.dailyAccount.receipts` - Email recipient list

## Core Functions

### 1. prepare()
```javascript
const prepare = () => {
  const project = config.app.project;
  const stage = config.project.stage;
  const period = getPeriod();
  const startDate = period[0].format('YYYY-MM-DD');
  return { project, stage, period, startDate };
};
```
**Purpose**: Initializes job parameters and determines analysis period

### 2. job() - Main Function
```javascript
const job = async () => {
  const { project, stage, period, startDate } = prepare();
  const abnormalRecords = await process(period, stage);
  
  if (!abnormalRecords || abnormalRecords.length <= 0) {
    logger.info('no abnormal records found after daily account checking');
    return;
  }
  
  await notify(startDate, project, stage, abnormalRecords);
};
```

### 3. notify()
```javascript
const notify = async (startDate, project, stage, abnormalRecords) => {
  const mailData = await ejs.renderFile(
    'src/static/templates/balanceAccountAlert.ejs',
    { date: startDate, project, stage, data: abnormalRecords }
  );
  const subject = formatSubject(project, stage);
  // Send email if mailActivated is enabled
};
```

## Account Validation Process

### 1. Period Determination
- **Service**: `getPeriod()` from check-account service
- **Purpose**: Determines date range for balance checking
- **Format**: Returns moment.js date objects

### 2. Balance Processing
- **Service**: `process(period, stage)` from check-account service
- **Purpose**: Analyzes account balances for abnormalities
- **Returns**: Array of abnormal account records

### 3. Abnormality Detection
- Identifies accounts with balance discrepancies
- Flags accounts with suspicious transaction patterns
- Detects potential data integrity issues

## Email Notification System

### Template Rendering
```javascript
const mailData = await ejs.renderFile(
  'src/static/templates/balanceAccountAlert.ejs',
  { date: startDate, project, stage, data: abnormalRecords }
);
```

### Email Configuration
- **Toggle**: `config.dailyAccount.mailActivated` controls email sending
- **Recipients**: `config.dailyAccount.receipts` (comma-separated list)
- **Subject**: Generated using `formatSubject(project, stage)`

### Email Data Structure
- **Date**: Analysis date
- **Project**: Project identifier
- **Stage**: Environment stage
- **Data**: Array of abnormal account records

## Error Handling and Logging

### Success Scenario
```javascript
logger.info('no abnormal records found after daily account checking');
```

### Abnormal Records Found
```javascript
logger.warn(`abnormal records found: ${abnormalRecords.length}`);
const msg = {
  tag: 'daily-account-checking',
  content: subject,
  data: abnormalRecords
};
logger.error(msg);
```

### Email Failure Handling
```javascript
try {
  await sendMail(receivers, subject, mailData);
} catch (e) {
  logger.error(e.message);
}
```

## Service Integration

### Check Account Service
- **getPeriod()**: Determines analysis timeframe
- **process()**: Performs balance validation
- **formatSubject()**: Generates email subject

## Configuration Management

### Mail Activation
```javascript
const mailActivated = config.dailyAccount.mailActivated;
if (mailActivated === 'false') {
  return; // Skip email sending
}
```

### Recipient Parsing
```javascript
let receivers = config.dailyAccount.receipts;
if (receivers) {
  receivers = receivers.split(',');
}
```

## Logging Strategy
- **Tag**: `[daily-account-checking]` for easy log filtering
- **Levels**: Info for normal operation, warn/error for issues
- **Context**: Includes project, stage, and date information
- **Structured**: Uses object format for abnormal record logging

## Usage Context
- **Financial Monitoring**: Ensures account balance integrity
- **Data Quality**: Detects balance calculation errors
- **Compliance**: Monitors financial data accuracy
- **Operations**: Daily health check for account system

## Alert Scenarios
- Account balances that don't match transaction history
- Negative balances in restricted accounts
- Large unexplained balance changes
- System calculation errors

## Related Components
- Account balance calculation system
- Transaction processing pipeline
- Email notification infrastructure
- Financial data validation services

## Schedule Context
Designed to run daily to provide continuous monitoring of account balance integrity and early detection of financial data issues.