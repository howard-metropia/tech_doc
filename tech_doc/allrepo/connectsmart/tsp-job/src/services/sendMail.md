# Send Mail Service

## Overview

The Send Mail Service is a lightweight email utility that provides a simple HTTP API interface for sending emails through a configured mail service endpoint. It acts as a centralized wrapper for email delivery functionality across the TSP Job application.

## Service Information

- **Service Name**: Send Mail Service
- **File Path**: `/src/services/sendMail.js`
- **Type**: Email Delivery Utility
- **Dependencies**: Axios HTTP Client, Application Configuration

## Core Function

### sendMail(to, subject, html)

The main and only exported function that sends email via HTTP POST request to configured mail service.

**Purpose**: Sends HTML email through configured mail service endpoint
**Parameters**:
- `to` (string): Recipient email address
- `subject` (string): Email subject line  
- `html` (string): HTML email content
**Returns**: Promise (async function)

**Implementation**:
```javascript
module.exports = async (to, subject, html) => {
  await axios({
    method: 'POST',
    url: config.get('mail.url'),
    data: {
      to,
      subject,
      html,
    },
  });
};
```

**Usage Example**:
```javascript
const sendMail = require('@app/src/services/sendMail');

await sendMail(
  'user@example.com',
  'Weekly Transportation Report',
  '<html><body><h1>Your Report</h1></body></html>'
);
```

## Configuration Requirements

### Mail Service Configuration
The service requires configuration of the mail service URL in the application config:

**Configuration Path**: `mail.url`
**Example Configuration**:
```javascript
{
  mail: {
    url: 'https://mail-service.example.com/api/send'
  }
}
```

### Environment-Specific URLs
Different environments typically use different mail service endpoints:
- **Development**: Local or development mail service
- **Staging**: Staging mail service with limited sending
- **Production**: Production mail service with full delivery

## HTTP Request Details

### Request Method
- **Method**: POST
- **Content-Type**: application/json (default for Axios)
- **Timeout**: Uses Axios default timeout settings

### Request Payload
```javascript
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "html": "<html>Email Content</html>"
}
```

### Expected Response
The function expects the mail service to return a successful HTTP status code (2xx). Any error responses will cause the Promise to reject.

## Error Handling

### HTTP Errors
- **Network Errors**: Connection failures to mail service
- **HTTP Status Errors**: 4xx/5xx responses from mail service
- **Timeout Errors**: Request timeout based on Axios configuration

### Error Propagation
The service does not catch or transform errors - all exceptions are propagated to the calling code:

```javascript
try {
  await sendMail(to, subject, html);
  console.log('Email sent successfully');
} catch (error) {
  console.error('Email sending failed:', error.message);
  // Handle specific error types
  if (error.response) {
    console.error('HTTP Status:', error.response.status);
    console.error('Error Data:', error.response.data);
  }
}
```

## Integration Points

### Used By
- **Report Mail Service**: Sending bi-weekly user reports
- **Notification Services**: Alert and update emails
- **Job Schedulers**: Automated email notifications
- **Admin Functions**: Manual email triggers

### Mail Service Requirements
The configured mail service endpoint must:
1. Accept POST requests with JSON payload
2. Support the expected data structure (to, subject, html)
3. Return appropriate HTTP status codes
4. Handle HTML email content properly

## Security Considerations

### Input Validation
The service performs no input validation, relying on:
- Calling code to validate email addresses
- Mail service to sanitize HTML content
- Configuration management for secure URLs

### Authentication
- **No Built-in Auth**: Service does not handle authentication
- **Service-Level Auth**: Authentication handled by configured mail service
- **Network Security**: Relies on HTTPS for secure transmission

### Content Security
- **HTML Content**: No sanitization of HTML input
- **Email Headers**: Basic email headers only
- **Attachment Support**: Not supported by this simple interface

## Performance Considerations

### Synchronous Operation
- **Blocking**: Function waits for HTTP response
- **No Queuing**: Direct HTTP call without queuing
- **No Retry Logic**: Single attempt per call

### Scalability Limitations
- **No Rate Limiting**: Does not implement sending rate limits
- **No Batch Support**: One email per function call
- **No Connection Pooling**: Uses default Axios connection handling

### Recommended Improvements
For high-volume email sending, consider:
1. **Queue Integration**: Add message queue for async processing
2. **Retry Logic**: Implement exponential backoff for failures
3. **Rate Limiting**: Prevent overwhelming mail service
4. **Batch Processing**: Support multiple recipients per call

## Usage Patterns

### Simple Email Sending
```javascript
const sendMail = require('@app/src/services/sendMail');

// Basic usage
await sendMail(
  'user@example.com',
  'Notification',
  '<p>Your action was completed.</p>'
);
```

### Error Handling Pattern
```javascript
const sendMail = require('@app/src/services/sendMail');

try {
  await sendMail(to, subject, html);
  logger.info(`Email sent successfully to ${to}`);
} catch (error) {
  logger.error(`Failed to send email to ${to}:`, error.message);
  // Implement fallback or retry logic
}
```

### Bulk Email Pattern
```javascript
const sendMail = require('@app/src/services/sendMail');

const recipients = ['user1@example.com', 'user2@example.com'];
const results = [];

for (const recipient of recipients) {
  try {
    await sendMail(recipient, subject, html);
    results.push({ email: recipient, status: 'sent' });
  } catch (error) {
    results.push({ email: recipient, status: 'failed', error: error.message });
  }
}
```

## Configuration Examples

### Development Configuration
```javascript
module.exports = {
  mail: {
    url: 'http://localhost:3001/api/mail/send'
  }
};
```

### Production Configuration
```javascript
module.exports = {
  mail: {
    url: 'https://mail-api.production.com/v1/send'
  }
};
```

### Environment Variable Configuration
```javascript
module.exports = {
  mail: {
    url: process.env.MAIL_SERVICE_URL || 'http://localhost:3001/api/mail/send'
  }
};
```

## Mail Service Interface Contract

### Expected Request Format
The mail service must accept requests in this format:
```json
{
  "to": "string (required)",
  "subject": "string (required)", 
  "html": "string (required)"
}
```

### Expected Response Format
- **Success**: HTTP 200-299 status code
- **Client Error**: HTTP 400-499 for invalid requests
- **Server Error**: HTTP 500-599 for service issues

### Optional Response Body
```json
{
  "messageId": "unique-message-identifier",
  "status": "sent|queued|failed"
}
```

## Testing Considerations

### Unit Testing
```javascript
const axios = require('axios');
const sendMail = require('@app/src/services/sendMail');

jest.mock('axios');

test('sends email with correct parameters', async () => {
  axios.mockResolvedValue({ status: 200 });
  
  await sendMail('test@example.com', 'Test Subject', '<p>Test</p>');
  
  expect(axios).toHaveBeenCalledWith({
    method: 'POST',
    url: expect.any(String),
    data: {
      to: 'test@example.com',
      subject: 'Test Subject',
      html: '<p>Test</p>'
    }
  });
});
```

### Integration Testing
- **Mail Service Availability**: Verify configured endpoint responds
- **Request Format**: Confirm mail service accepts expected payload
- **Error Handling**: Test various failure scenarios
- **Configuration**: Verify config values are loaded correctly

## Monitoring & Observability

### Logging Recommendations
Since the service doesn't include built-in logging, implement logging in calling code:

```javascript
const { logger } = require('@maas/core/log');
const sendMail = require('@app/src/services/sendMail');

const sendEmailWithLogging = async (to, subject, html) => {
  logger.info(`Sending email to ${to} with subject: ${subject}`);
  
  try {
    await sendMail(to, subject, html);
    logger.info(`Email sent successfully to ${to}`);
  } catch (error) {
    logger.error(`Email sending failed for ${to}:`, error.message);
    throw error;
  }
};
```

### Metrics Tracking
Consider tracking:
- **Send Attempts**: Total emails attempted
- **Success Rate**: Percentage of successful sends
- **Error Types**: Categorization of failure reasons
- **Response Times**: Performance of mail service

## Limitations & Considerations

### Current Limitations
1. **No Authentication**: Service doesn't handle auth headers
2. **No Attachments**: Only supports HTML content
3. **No Templates**: No built-in template processing
4. **No Validation**: No input validation or sanitization
5. **No Queuing**: Synchronous operation only

### Migration Considerations
When upgrading or replacing this service:
1. **Interface Compatibility**: Maintain the simple function signature
2. **Error Handling**: Preserve error propagation behavior
3. **Configuration**: Keep configuration structure consistent
4. **Dependencies**: Minimize impact on existing code

### Alternative Implementations
For enhanced functionality, consider:
1. **Direct SES Integration**: Use AWS SES SDK directly
2. **Nodemailer**: Full-featured email library
3. **Queue-Based**: Async email processing with Bull/Agenda
4. **Template Service**: Integration with template engines

## Dependencies

- **axios**: HTTP client for making requests to mail service
- **config**: Application configuration management for mail service URL