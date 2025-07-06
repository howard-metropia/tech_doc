# Mailer Helper

## Overview
**File**: `src/helpers/mailer.js`  
**Type**: Email Utility  
**Purpose**: Sends emails via SMTP using Nodemailer with support for single and batch sending

## Core Function

### Email Sending
```javascript
module.exports = async (emailList, subject, html, allAtOnce = false) => {
  // Configure SMTP transport
  // Send emails individually or as batch
  // Log success messages
}
```

## Configuration

### SMTP Setup
```javascript
const { host, port, user, pass, from } = config.get('mail.smtp');
const smtpTransport = nodemailer.createTransporter({
  host,
  port,
  auth: { user, pass },
});
```

### Required Config
- **host**: SMTP server hostname
- **port**: SMTP server port
- **user**: Authentication username  
- **pass**: Authentication password
- **from**: Default sender address

## Sending Modes

### Individual Sending (Default)
```javascript
await Promise.all(
  emailList.map(async (email) => {
    const mailOptions = {
      from,
      to: email,
      subject,
      html,
    };
    await smtpTransport.sendMail(mailOptions);
  })
);
```

### Batch Sending
```javascript
if (allAtOnce) {
  const mailOptions = {
    from,
    to: emailList,  // Array of recipients
    subject,
    html,
  };
  await smtpTransport.sendMail(mailOptions);
}
```

## Parameters

### Required Parameters
- **emailList**: Array of email addresses
- **subject**: Email subject line
- **html**: Email content (HTML format)

### Optional Parameters
- **allAtOnce**: Boolean flag for batch vs individual sending

## Usage Examples

### Individual Emails
```javascript
const mailer = require('./mailer');

await mailer(
  ['user1@example.com', 'user2@example.com'],
  'Welcome to MaaS Platform',
  '<h1>Welcome!</h1><p>Thank you for joining.</p>'
);
```

### Batch Email
```javascript
await mailer(
  ['user1@example.com', 'user2@example.com'],
  'System Announcement',
  '<h1>Maintenance Notice</h1><p>Scheduled maintenance tonight.</p>',
  true  // allAtOnce = true
);
```

### Dynamic Content
```javascript
const generateHtml = (userName) => `
  <h1>Hello ${userName}</h1>
  <p>Your account has been activated.</p>
`;

await mailer(
  ['user@example.com'],
  'Account Activated',
  generateHtml('John Doe')
);
```

## Error Handling

### Input Validation
```javascript
if (!Array.isArray(emailList)) {
  throw new Error('emailList must be array');
}
```

### SMTP Errors
- **Connection Errors**: Network or server issues
- **Authentication Errors**: Invalid credentials
- **Send Errors**: Individual email failures

## Logging

### Success Logging
```javascript
// Individual sends
logger.info(`Send mail to:${email} subject:${subject} Success!`);

// Batch sends  
logger.info(`Send mail to:${emailList} subject:${subject} Success!`);
```

### Log Information
- **Recipients**: Email addresses or array
- **Subject**: Email subject for tracking
- **Status**: Success confirmation

## Dependencies

### External Libraries
- **nodemailer**: SMTP email sending
- **config**: Configuration management
- **@maas/core/log**: Logging functionality

### Configuration Requirements
```javascript
mail: {
  smtp: {
    host: 'smtp.example.com',
    port: 587,
    user: 'username',
    pass: 'password',
    from: 'noreply@example.com'
  }
}
```

## Performance Considerations

### Individual vs Batch
- **Individual**: Better for personalization, slower
- **Batch**: Faster for identical content, less personalized
- **Parallel**: Individual sends use Promise.all for concurrency

### Rate Limiting
- **SMTP Limits**: Consider server rate limits
- **Throttling**: May need throttling for large lists
- **Retry Logic**: Not implemented, relies on nodemailer

## Email Content

### HTML Support
- **Rich Content**: Full HTML email support
- **Styling**: Inline CSS recommended
- **Images**: External image URLs supported

### Best Practices
- **Responsive**: Mobile-friendly HTML
- **Fallback**: Consider plain text versions
- **Testing**: Test across email clients

## Integration Points

### Common Use Cases
- **User Notifications**: Account updates, alerts
- **System Notifications**: Maintenance, outages
- **Marketing**: Newsletters, announcements
- **Transactional**: Receipts, confirmations

### Template Integration
```javascript
const emailTemplate = require('./email-templates');

const html = emailTemplate.render('welcome', {
  userName: 'John',
  activationLink: 'https://...'
});

await mailer(['user@example.com'], 'Welcome', html);
```

## Security Considerations

### Credential Management
- **Environment Variables**: Store SMTP credentials securely
- **Encryption**: Use TLS/SSL for SMTP connections
- **Access Control**: Limit access to mailer configuration

### Content Security
- **Input Sanitization**: Validate email addresses
- **HTML Safety**: Sanitize HTML content if user-generated
- **Spam Prevention**: Follow email best practices

## Monitoring

### Email Delivery
- **Success Rates**: Track successful sends
- **Bounce Rates**: Monitor bounced emails
- **Performance**: Track send times and throughput

### Error Tracking
- **SMTP Errors**: Connection and authentication issues
- **Invalid Addresses**: Track failed recipients
- **Rate Limiting**: Monitor for rate limit hits

## Configuration Examples

### Production SMTP
```javascript
mail: {
  smtp: {
    host: 'smtp.mailgun.org',
    port: 587,
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
    from: 'noreply@metropia.com'
  }
}
```

### Development SMTP
```javascript
mail: {
  smtp: {
    host: 'localhost',
    port: 1025,  // MailHog or similar
    user: '',
    pass: '',
    from: 'dev@example.com'
  }
}
```

## Testing

### Unit Tests
```javascript
// Mock nodemailer
jest.mock('nodemailer');

const mockSendMail = jest.fn().mockResolvedValue();
nodemailer.createTransport.mockReturnValue({
  sendMail: mockSendMail
});
```

### Integration Tests
- **SMTP Connection**: Test actual SMTP connectivity
- **Email Delivery**: Verify emails reach destinations
- **Error Scenarios**: Test invalid addresses, connection failures

## Limitations

### Current Implementation
- **No Templates**: Basic HTML content only
- **No Attachments**: File attachment not supported
- **No Retry Logic**: Failed sends not retried
- **No Unsubscribe**: No built-in unsubscribe handling

### Enhancement Opportunities
- **Template Engine**: Add email template support
- **Attachment Support**: File attachment capability
- **Retry Mechanism**: Automatic retry for failed sends
- **Analytics**: Open/click tracking integration