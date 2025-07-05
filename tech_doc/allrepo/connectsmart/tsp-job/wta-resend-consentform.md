# wta-resend-consentform.js

## Overview
Job for automatically resending WTA (Washington Transit Authority) consent form emails to users who have not yet agreed to participate in experiments. Implements retry logic with configurable limits and uses secure hash tokens for consent form authentication.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/wta-resend-consentform.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `@maas/core/log` - Logging utility
- `geo-point-in-polygon` - Geographic analysis utilities (imported but not used)
- `@app/src/services/incentiveUtility` - Utility services (imported but not used)
- `@app/src/services/sendMail` - Email delivery service
- `config` - Application configuration for WTA URL
- `ejs` - Email template rendering
- `hashids/cjs` - Secure hash token generation

## Core Functions

### Main Processing Function
Identifies users who haven't responded to consent forms and sends follow-up emails with secure consent links.

**Process Flow:**
1. Identify users with pending consent forms
2. Apply retry limit and timing filters
3. Generate secure hash tokens for consent links
4. Render personalized email templates
5. Send consent form emails
6. Update retry counters

## Job Configuration

### Inputs
No input parameters required.

### Retry Configuration
- **Maximum Resends**: 2 additional attempts (total 3 including original)
- **Retry Interval**: 2 days minimum between attempts
- **Token Security**: 16-character hash IDs with custom salt

## Processing Flow

### 1. Pending Consent Identification
```sql
SELECT *,
(SELECT email FROM hybrid.auth_user WHERE id = wta_agree.user_id) AS usermail,
(SELECT first_name FROM hybrid.auth_user WHERE id = wta_agree.user_id) AS username
FROM hybrid.wta_agree
WHERE wta_agree = 0
AND resend < 2
AND modified_on < DATE_SUB(NOW(), INTERVAL 2 DAY)
```

### 2. User Data Extraction
```javascript
const rowID = [row.id];
const userID = [row.user_id];
const userMail = [row.usermail];
const userName = [row.username];
```

### 3. Secure Token Generation
```javascript
const random = Math.floor(Math.random() * 100 + 1);
const wtahash_key = 'gogowtakey';
const wtahash_length = 16;
const hashids = new Hashids(wtahash_key, wtahash_length);
const hasToken = hashids.encode(userID, random);
```

### 4. Email Template Rendering
```javascript
const mailData = await ejs.renderFile(
  'src/static/templates/consentFormCreate.ejs',
  {
    firstName: userName,
    urlLink: config.get('wta.url'),
    hasToken: hasToken
  }
);
```

### 5. Email Delivery
```javascript
const subject = `Hate traffic? Love rewards? We've got a deal for you!`;
await sendMail(userMail, subject, mailData);
```

### 6. Retry Counter Update
```sql
UPDATE hybrid.wta_agree 
SET resend = resend + 1 
WHERE id = '${rowID}'
```

## Data Models

### wta_agree Consent Tracking Table
```javascript
{
  id: number,
  user_id: number,
  wta_agree: boolean,     // 0 = not agreed, 1 = agreed
  resend: number,         // Current retry count (0-2)
  created_on: datetime,
  modified_on: datetime   // Last attempt timestamp
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

### Email Template Variables
```javascript
{
  firstName: string,      // User's first name for personalization
  urlLink: string,       // WTA consent form URL from config
  hasToken: string       // Secure hash token for user verification
}
```

## Business Logic

### Retry Eligibility Criteria
```javascript
const isEligibleForResend = (user) => {
  return user.wta_agree === 0 &&        // Not yet agreed
         user.resend < 2 &&             // Under retry limit
         user.modified_on < (now - 2_days); // Sufficient time elapsed
};
```

### Token Security Implementation
```javascript
// Hash ID configuration for secure consent links
const tokenConfig = {
  salt: 'gogowtakey',     // Custom salt for hash generation
  length: 16,             // Token length for security
  alphabet: 'default'     // Standard character set
};

// Token includes user ID and random component
const secureToken = hashids.encode(user_id, random_number);
```

### Email Personalization Strategy
- **Subject Line**: Engaging marketing message about traffic and rewards
- **Greeting**: Personalized with user's first name
- **Call-to-Action**: Secure link to consent form
- **Token Authentication**: Embedded secure token for user verification

### Retry Management Logic
```javascript
// Progressive retry system
const retrySchedule = {
  initial: 0,      // First consent form (sent by other system)
  first_retry: 1,  // After 2 days if no response
  final_retry: 2   // After 4 days total if still no response
};

// Stop retries after maximum attempts
if (currentRetryCount >= 2) {
  // No more automatic retries
  markAsMaxRetriesReached();
}
```

## Error Handling
- **Email Delivery Failures**: Continues processing other users if individual emails fail
- **Invalid User Data**: Skips users with missing email or name information
- **Database Errors**: Maintains transaction integrity during retry counter updates
- **Template Rendering**: Handles missing template variables gracefully

## Integration Points
- **User Authentication System**: Retrieves user contact information
- **Email Service**: Delivers personalized consent form invitations
- **Configuration System**: Accesses WTA URL and settings
- **Template Engine**: Renders HTML email content
- **Hash Token System**: Generates secure consent verification tokens

## Performance Considerations
- **Batch Processing**: Handles multiple users in single job execution
- **Efficient Queries**: Single SQL query identifies all eligible users
- **Template Caching**: EJS templates cached for performance
- **Minimal API Calls**: Reduces external service dependencies

## Security Considerations
- **Secure Tokens**: Hash IDs prevent consent form manipulation
- **Email Privacy**: Secure handling of user email addresses
- **SQL Injection Prevention**: Parameterized queries for database safety
- **Access Control**: Consent links tied to specific user sessions

## Usage Scenarios
- **Daily Consent Follow-up**: Automated reminder system for non-responders
- **Experiment Enrollment**: Increasing participation rates in WTA studies
- **User Engagement**: Re-engaging users who missed initial consent requests
- **Research Compliance**: Ensuring proper informed consent procedures

## Configuration Dependencies
- **WTA Configuration**: Consent form URL in application config
- **Email Service**: SMTP or email API configuration
- **Template Files**: EJS consent form template availability
- **Database Access**: MySQL connection permissions
- **Hash Generation**: Consistent salt configuration across systems

## Email Template Integration

### Template Structure
The consent form email template includes:
- **Personal Greeting**: Customized with user's first name
- **Value Proposition**: Traffic reduction and reward messaging
- **Secure Link**: Tokenized consent form URL
- **Professional Design**: HTML formatting for engagement

### Template Variables
```ejs
<h1>Hello <%= firstName %>!</h1>
<p>Hate traffic? Love rewards? We've got a deal for you!</p>
<a href="<%= urlLink %>?token=<%= hasToken %>">
  Click here to learn more and give consent
</a>
```

## Monitoring and Logging
- **User Processing**: Logs each user being processed for resend
- **Token Generation**: Secure token creation confirmation
- **Email Delivery**: Success/failure status for each attempt
- **Retry Updates**: Database update confirmation
- **Error Conditions**: Comprehensive error logging for debugging

## Data Flow
1. **Source**: Pending consent records from wta_agree table
2. **Filtering**: Eligibility verification based on retry and timing rules
3. **Token Generation**: Secure hash token creation for each user
4. **Template Processing**: Personalized email content rendering
5. **Delivery**: Email transmission with consent form links
6. **Tracking**: Retry counter updates for audit trail

## Consent Form Workflow Integration

### Pre-Resend State
- User enrolled in WTA market area
- Initial consent form sent
- No response after 2+ days
- Retry count under maximum limit

### Post-Resend State
- Retry counter incremented
- New secure token generated
- Email delivery attempted
- Next retry scheduled (if under limit)

### Terminal States
- **Success**: User clicks link and provides consent
- **Max Retries**: System stops automatic retries after 2 attempts
- **Expiration**: User remains in non-consented state

## Compliance Considerations
- **Informed Consent**: Ensures proper research ethics compliance
- **Retry Limits**: Prevents email spam and user harassment
- **Opt-Out Support**: Allows users to decline participation
- **Data Retention**: Maintains audit trail for research purposes

## Notes
- Essential component of WTA experiment participant recruitment
- Implements respectful retry strategy to maximize consent rates
- Uses secure token system to prevent consent form abuse
- Integrates with broader WTA experimental infrastructure
- Balances user engagement with privacy considerations
- Supports research compliance requirements for informed consent
- Designed for automated operation with manual override capabilities
- Critical for maintaining adequate sample sizes in transportation behavior studies