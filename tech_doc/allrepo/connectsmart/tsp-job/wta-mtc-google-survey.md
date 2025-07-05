# wta-mtc-google-survey.js

## Overview
Job for sending post-experiment Google Form survey invitations to WTA/MTC experiment participants. Generates personalized survey emails with pre-filled Google Forms based on user's most frequent habitual trips and experiment outcomes. Supports different survey types based on user actions taken during the experiment.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/wta-mtc-google-survey.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `ejs` - Template rendering engine for email content
- `moment` / `moment-timezone` - Date/time manipulation
- `@maas/core/mysql` - MySQL database connection (portal)
- `@app/src/services/sendMail` - Email delivery service
- `@maas/core/log` - Logging utility

## Core Functions

### Main Processing Function
Sends personalized Google Form survey invitations to experiment participants based on their experiment completion status and actions taken.

**Process Flow:**
1. Identify target experiment participants
2. Generate personalized Google Form URLs with pre-filled data
3. Render email template with user-specific information
4. Send survey invitation email
5. Record survey invitation in tracking table

## Job Configuration

### Inputs
No input parameters required.

### Survey Configuration
- **Target User**: Currently configured for user ID 10517 (test/demo mode)
- **Template**: `src/static/templates/googleSurveyCreate.ejs`
- **Tracking Table**: `hybrid.wta_mtc_googlesurvey`

## Processing Flow

### 1. Participant Selection
```sql
SELECT * FROM hybrid.auth_user 
WHERE id = '10517'
```
*Note: Current implementation targets specific test user*

### 2. Personalized Survey URL Generation
```javascript
const urlLink = `https://docs.google.com/forms/d/e/1FAIpQLSdwYWxU7HSh2DWtYd0om8Y0Uq5PP9q9a-9MNiZH7N0tNByDIQ/viewform?usp=pp_url&entry.1529062731=10129&entry.257306144=Tucson+Museum+Of+Art,+140+N+Main+Ave,+Tucson,&entry.419524171=485+S+Stone+Ave,+Tucson,+AZ+85701&entry.922944672=11:00am`;
```

### 3. Email Template Rendering
```javascript
const mailData = await ejs.renderFile(
  'src/static/templates/googleSurveyCreate.ejs',
  {
    name: user.first_name,
    urlLink: personalizedSurveyURL
  }
);
```

### 4. Survey Invitation Delivery
```javascript
const subject = `${user.first_name}, do you have a minute to help us out?`;
await sendMail([userEmail], subject, mailData);
```

### 5. Survey Tracking Record
```sql
INSERT INTO hybrid.wta_mtc_googlesurvey (
  user_id, experiment_group, google_question, mail
) VALUES (
  '${user_id}', 'MTC', 'A', '${user_email}'
)
```

## Data Models

### auth_user Table Reference
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

### wta_mtc_googlesurvey Tracking Table
```javascript
{
  id: number,
  user_id: number,
  experiment_group: string, // 'WTA' or 'MTC'
  google_question: string,  // Survey type identifier
  mail: string,             // User email address
  created_on: datetime,
  modified_on: datetime
}
```

### Survey URL Parameters
```javascript
{
  entry_1529062731: user_id,        // Participant identifier
  entry_257306144: origin_address,   // Origin location
  entry_419524171: destination_address, // Destination location
  entry_922944672: departure_time    // Typical departure time
}
```

## Business Logic

### Survey Type Classification
Based on documentation comments, different survey forms are used for different user actions:

**For users who took action:**
- **[A] Time Change**: Time-based behavior modification survey
- **[B] Transit**: Public transit adoption survey  
- **[C] Bike**: Bicycle mode adoption survey
- **[D] Walk**: Walking mode adoption survey

**For users who won but didn't take action:**
- **[E] Time**: Time change with additional "why not" question
- **[F] Transit**: Transit with additional "why not" question
- **[G] Bike**: Bike with additional "why not" question
- **[H] Walk**: Walk with additional "why not" question

### Habitual Trip Data Integration
Pre-fills survey with user's most frequent trip:
- **User ID**: 10129 (example participant)
- **Origin**: Tucson Museum Of Art, 140 N Main Ave, Tucson
- **Destination**: 485 S Stone Ave, Tucson, AZ 85701
- **Departure Time**: 11:00am

### Email Personalization
- **Subject Line**: Personalized with user's first name
- **Content**: Rendered from EJS template with user-specific data
- **Survey Link**: Pre-populated with user's habitual trip information

## Error Handling
- Validates user existence before processing
- Graceful handling of email delivery failures
- Continues processing if individual operations fail
- Comprehensive logging for debugging

## Integration Points
- **User Authentication System**: Retrieves participant data
- **Email Service**: Delivers personalized survey invitations
- **Google Forms**: External survey platform integration
- **Template System**: EJS-based email content generation
- **Survey Tracking**: Database logging for response management

## Performance Considerations
- Single user processing for targeted deployment
- Efficient SQL queries for user data retrieval
- Minimal external API calls
- Template caching through EJS system

## Security Considerations
- Secure email template rendering
- Parameterized SQL queries
- User data privacy in survey URLs
- Controlled access to participant information

## Usage Scenarios
- Post-experiment survey distribution
- Research data collection for behavior modification studies
- User feedback gathering for program improvement
- Academic research survey administration
- Transportation behavior analysis data collection

## Configuration Dependencies
- Email service configuration for delivery
- Google Forms access and URL structure
- EJS template file availability
- Database connection permissions
- Survey tracking table structure

## Monitoring and Logging
- User selection and processing logs
- Email delivery confirmation
- Survey invitation tracking
- Template rendering status
- Database insertion verification

## Data Flow
1. **Source**: Experiment participant database
2. **Processing**: User data retrieval and survey personalization
3. **Template Rendering**: EJS-based email content generation
4. **Delivery**: Personalized email with survey link
5. **Tracking**: Database record of survey invitation
6. **Integration**: Google Forms for response collection

## Survey Form Structure
The job integrates with multiple Google Forms designed for different experimental outcomes:

### Time-based Surveys
- Users who changed departure times
- Users who won time-based incentives but didn't change

### Mode-based Surveys  
- Transit adoption participants
- Bicycle mode adoption participants
- Walking mode adoption participants
- Each with corresponding "no action" variants

### Pre-filled Data Points
- Participant identifier for response matching
- Origin/destination for trip context
- Departure time for behavioral reference
- Demographic and trip pattern context

## Notes
- Currently configured for single-user testing (ID 10517)
- Supports comprehensive post-experiment research data collection
- Integrates with Google Forms for standardized survey delivery
- Maintains detailed tracking for response rate analysis
- Critical component of transportation behavior modification research
- Designed for both WTA and MTC experiment frameworks
- Supports longitudinal study data collection through personalized approaches