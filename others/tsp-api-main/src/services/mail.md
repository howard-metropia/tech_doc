# TSP API Mail Service Documentation

## 🔍 Quick Summary (TL;DR)
The Mail service provides email parsing functionality to extract structured data from raw email content, including recipients, sender, subject, and parsed HTML content using mailparser and node-html-parser libraries.

**Keywords:** email-parsing | mail-parser | html-extraction | email-processing | mime-parsing | email-headers | html-parsing | email-content

**Primary use cases:** Processing incoming emails, extracting email metadata, parsing HTML email content, handling email-based integrations and notifications

**Compatibility:** Node.js >= 16.0.0, supports standard email formats (MIME, RFC 822)

## ❓ Common Questions Quick Index
- **Q: What email formats are supported?** → Standard MIME/RFC 822 email formats with HTML content
- **Q: Can it parse attachments?** → No, current implementation only extracts to/from/subject/HTML
- **Q: Does it handle plain text emails?** → Focus is on HTML content, plain text may need additional handling
- **Q: Is it for sending or receiving?** → Parsing only - for processing received email content
- **Q: What's returned from parsing?** → Object with to, from, subject fields and parsed HTML DOM
- **Q: Can it parse email headers?** → Only basic headers (to/from/subject) are extracted

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as an **email reader and organizer**. When the system receives an email in raw format (like opening an email file in notepad), this service reads it and extracts the important parts - who sent it, who it's for, what the subject is, and the actual message content in a format the app can understand.

**Technical explanation:** 
A lightweight email parsing service that processes raw email content using mailparser to extract MIME structure and metadata, then parses the HTML body using node-html-parser to create a DOM structure. Returns structured data with sender, recipient, subject, and parsed HTML content for further processing.

**Business value explanation:**
Enables email-based integrations, automated email processing workflows, and email-to-action features. Supports customer service automation, notification processing, and email-based data collection. Essential for systems that need to interact with email communications programmatically.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/mail.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with email parsing libraries
- **Type:** Email Parsing Service
- **File Size:** ~0.4 KB
- **Complexity Score:** ⭐ (Low - Simple parsing wrapper)

**Dependencies:**
- `mailparser`: MIME email parsing library (**Critical**)
- `node-html-parser`: Fast HTML parser with DOM interface (**High**)

## 📝 Detailed Code Analysis

### parseMail Function

**Purpose:** Parses raw email content into structured data

**Parameters:**
- `content`: String/Buffer - Raw email content in MIME format

**Returns:** Object containing:
- `to`: String - Recipient email address(es)
- `from`: String - Sender email address
- `subject`: String - Email subject line
- `html`: HTMLElement - Parsed HTML DOM tree

**Implementation:**
```javascript
async function parseMail(content) {
  const mail = await simpleParser(content);
  const html = await htmlParser(mail.html);
  return {
    to: mail.to.text,
    from: mail.from.text,
    subject: mail.subject,
    html,
  };
}
```

**Processing Steps:**
1. **MIME Parsing:** Uses simpleParser to decode email structure
2. **Metadata Extraction:** Extracts to/from/subject from headers
3. **HTML Parsing:** Converts HTML body to DOM structure
4. **Data Assembly:** Returns structured object with all components

## 🚀 Usage Methods

### Basic Email Parsing
```javascript
const mailService = require('@app/src/services/mail');

async function processIncomingEmail(rawEmailContent) {
  try {
    const parsedEmail = await mailService.parseMail(rawEmailContent);
    
    console.log('Email received:');
    console.log('From:', parsedEmail.from);
    console.log('To:', parsedEmail.to);
    console.log('Subject:', parsedEmail.subject);
    
    // Access HTML content
    const bodyText = parsedEmail.html.innerText;
    console.log('Body text:', bodyText);
    
    return parsedEmail;
  } catch (error) {
    console.error('Failed to parse email:', error);
    throw error;
  }
}
```

### Email Content Extraction
```javascript
async function extractEmailData(emailContent) {
  const mailService = require('@app/src/services/mail');
  
  try {
    const parsed = await mailService.parseMail(emailContent);
    
    // Extract specific elements from HTML
    const links = parsed.html.querySelectorAll('a');
    const images = parsed.html.querySelectorAll('img');
    const tables = parsed.html.querySelectorAll('table');
    
    return {
      metadata: {
        from: parsed.from,
        to: parsed.to,
        subject: parsed.subject
      },
      content: {
        plainText: parsed.html.innerText,
        linkCount: links.length,
        links: links.map(a => ({
          text: a.innerText,
          href: a.getAttribute('href')
        })),
        imageCount: images.length,
        images: images.map(img => img.getAttribute('src')),
        hasTable: tables.length > 0
      }
    };
  } catch (error) {
    console.error('Email extraction failed:', error);
    throw error;
  }
}
```

### Email-Based Command Processing
```javascript
class EmailCommandProcessor {
  constructor() {
    this.mailService = require('@app/src/services/mail');
    this.commands = new Map();
    
    // Register command handlers
    this.registerCommand('SUBSCRIBE', this.handleSubscribe);
    this.registerCommand('UNSUBSCRIBE', this.handleUnsubscribe);
    this.registerCommand('HELP', this.handleHelp);
    this.registerCommand('STATUS', this.handleStatus);
  }

  registerCommand(keyword, handler) {
    this.commands.set(keyword.toUpperCase(), handler);
  }

  async processEmail(rawEmail) {
    try {
      const parsed = await this.mailService.parseMail(rawEmail);
      
      // Extract command from subject or body
      const command = this.extractCommand(parsed);
      
      if (!command) {
        return {
          processed: false,
          reason: 'No valid command found',
          email: parsed
        };
      }

      const handler = this.commands.get(command.toUpperCase());
      
      if (!handler) {
        return {
          processed: false,
          reason: `Unknown command: ${command}`,
          email: parsed
        };
      }

      const result = await handler.call(this, parsed);
      
      return {
        processed: true,
        command,
        result,
        email: parsed
      };
    } catch (error) {
      console.error('Email command processing failed:', error);
      return {
        processed: false,
        error: error.message
      };
    }
  }

  extractCommand(parsedEmail) {
    // Check subject for command
    const subjectMatch = parsedEmail.subject.match(/^(SUBSCRIBE|UNSUBSCRIBE|HELP|STATUS)/i);
    if (subjectMatch) {
      return subjectMatch[1];
    }

    // Check first line of body
    const bodyText = parsedEmail.html.innerText.trim();
    const firstLine = bodyText.split('\n')[0];
    const bodyMatch = firstLine.match(/^(SUBSCRIBE|UNSUBSCRIBE|HELP|STATUS)/i);
    
    return bodyMatch ? bodyMatch[1] : null;
  }

  async handleSubscribe(parsedEmail) {
    const email = this.extractEmailAddress(parsedEmail.from);
    console.log(`Processing SUBSCRIBE for ${email}`);
    
    // Add subscription logic here
    return {
      action: 'subscribe',
      email,
      status: 'success'
    };
  }

  async handleUnsubscribe(parsedEmail) {
    const email = this.extractEmailAddress(parsedEmail.from);
    console.log(`Processing UNSUBSCRIBE for ${email}`);
    
    // Add unsubscribe logic here
    return {
      action: 'unsubscribe',
      email,
      status: 'success'
    };
  }

  async handleHelp(parsedEmail) {
    return {
      action: 'help',
      availableCommands: Array.from(this.commands.keys()),
      message: 'Send email with command in subject line'
    };
  }

  async handleStatus(parsedEmail) {
    const email = this.extractEmailAddress(parsedEmail.from);
    
    // Check subscription status
    return {
      action: 'status',
      email,
      subscribed: true, // Would check actual status
      lastActivity: new Date().toISOString()
    };
  }

  extractEmailAddress(fromField) {
    // Extract email from "Name <email@domain.com>" format
    const match = fromField.match(/<([^>]+)>/);
    return match ? match[1] : fromField;
  }
}
```

### Notification Email Parser
```javascript
class NotificationEmailParser {
  constructor() {
    this.mailService = require('@app/src/services/mail');
  }

  async parseTransactionEmail(emailContent) {
    try {
      const parsed = await this.mailService.parseMail(emailContent);
      
      // Extract transaction details from common email formats
      const transactionData = {
        type: this.detectTransactionType(parsed.subject),
        amount: this.extractAmount(parsed.html),
        date: this.extractDate(parsed.html),
        merchant: this.extractMerchant(parsed.html),
        reference: this.extractReference(parsed.html)
      };

      return {
        email: {
          from: parsed.from,
          subject: parsed.subject,
          receivedAt: new Date().toISOString()
        },
        transaction: transactionData
      };
    } catch (error) {
      console.error('Transaction email parsing failed:', error);
      throw error;
    }
  }

  detectTransactionType(subject) {
    if (subject.toLowerCase().includes('payment')) return 'payment';
    if (subject.toLowerCase().includes('refund')) return 'refund';
    if (subject.toLowerCase().includes('invoice')) return 'invoice';
    if (subject.toLowerCase().includes('receipt')) return 'receipt';
    return 'unknown';
  }

  extractAmount(htmlElement) {
    // Look for currency patterns
    const text = htmlElement.innerText;
    const amountMatch = text.match(/\$([0-9,]+\.?\d{0,2})/);
    
    if (amountMatch) {
      return parseFloat(amountMatch[1].replace(',', ''));
    }
    
    return null;
  }

  extractDate(htmlElement) {
    // Look for date patterns
    const text = htmlElement.innerText;
    const datePatterns = [
      /(\d{1,2}\/\d{1,2}\/\d{4})/,
      /(\d{4}-\d{2}-\d{2})/,
      /(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}/i
    ];

    for (const pattern of datePatterns) {
      const match = text.match(pattern);
      if (match) {
        return new Date(match[1]).toISOString();
      }
    }

    return null;
  }

  extractMerchant(htmlElement) {
    // Look for merchant/vendor information
    const merchantElement = htmlElement.querySelector('.merchant') ||
                           htmlElement.querySelector('[class*="vendor"]') ||
                           htmlElement.querySelector('[class*="company"]');
    
    if (merchantElement) {
      return merchantElement.innerText.trim();
    }

    // Fallback to looking for patterns
    const text = htmlElement.innerText;
    const merchantMatch = text.match(/(?:from|merchant|vendor|company):\s*([^\n]+)/i);
    
    return merchantMatch ? merchantMatch[1].trim() : null;
  }

  extractReference(htmlElement) {
    // Look for reference/order numbers
    const text = htmlElement.innerText;
    const refPatterns = [
      /(?:order|reference|transaction|confirmation)\s*#?\s*([A-Z0-9-]+)/i,
      /(?:ID|Number):\s*([A-Z0-9-]+)/i
    ];

    for (const pattern of refPatterns) {
      const match = text.match(pattern);
      if (match) {
        return match[1];
      }
    }

    return null;
  }
}
```

### Email Template Analyzer
```javascript
class EmailTemplateAnalyzer {
  constructor() {
    this.mailService = require('@app/src/services/mail');
  }

  async analyzeEmailStructure(emailContent) {
    try {
      const parsed = await this.mailService.parseMail(emailContent);
      
      const analysis = {
        metadata: {
          from: parsed.from,
          to: parsed.to,
          subject: parsed.subject
        },
        structure: this.analyzeHTMLStructure(parsed.html),
        content: this.analyzeContent(parsed.html),
        accessibility: this.checkAccessibility(parsed.html),
        links: this.analyzeLinks(parsed.html)
      };

      return analysis;
    } catch (error) {
      console.error('Email analysis failed:', error);
      throw error;
    }
  }

  analyzeHTMLStructure(htmlElement) {
    return {
      hasHeader: htmlElement.querySelector('header') !== null,
      hasFooter: htmlElement.querySelector('footer') !== null,
      tableCount: htmlElement.querySelectorAll('table').length,
      divCount: htmlElement.querySelectorAll('div').length,
      hasInlineStyles: htmlElement.querySelector('[style]') !== null,
      hasStyleTag: htmlElement.querySelector('style') !== null
    };
  }

  analyzeContent(htmlElement) {
    const images = htmlElement.querySelectorAll('img');
    const videos = htmlElement.querySelectorAll('video');
    const text = htmlElement.innerText;
    
    return {
      wordCount: text.split(/\s+/).length,
      characterCount: text.length,
      imageCount: images.length,
      videoCount: videos.length,
      hasEmojis: /[\u{1F300}-\u{1F9FF}]/u.test(text),
      languages: this.detectLanguages(text)
    };
  }

  checkAccessibility(htmlElement) {
    const images = htmlElement.querySelectorAll('img');
    const links = htmlElement.querySelectorAll('a');
    
    return {
      imagesWithAlt: images.filter(img => img.getAttribute('alt')).length,
      totalImages: images.length,
      linksWithTitle: links.filter(a => a.getAttribute('title')).length,
      totalLinks: links.length,
      hasSemanticHTML: this.checkSemanticHTML(htmlElement)
    };
  }

  analyzeLinks(htmlElement) {
    const links = htmlElement.querySelectorAll('a');
    const linkAnalysis = [];

    links.forEach(link => {
      const href = link.getAttribute('href');
      linkAnalysis.push({
        text: link.innerText,
        href: href,
        isExternal: href && (href.startsWith('http://') || href.startsWith('https://')),
        isEmail: href && href.startsWith('mailto:'),
        isTel: href && href.startsWith('tel:'),
        hasTracking: href && href.includes('utm_')
      });
    });

    return {
      total: links.length,
      external: linkAnalysis.filter(l => l.isExternal).length,
      email: linkAnalysis.filter(l => l.isEmail).length,
      phone: linkAnalysis.filter(l => l.isTel).length,
      tracked: linkAnalysis.filter(l => l.hasTracking).length,
      links: linkAnalysis
    };
  }

  detectLanguages(text) {
    // Simple language detection based on character sets
    const languages = [];
    
    if (/[a-zA-Z]/.test(text)) languages.push('english');
    if (/[\u4e00-\u9fff]/.test(text)) languages.push('chinese');
    if (/[\u0600-\u06ff]/.test(text)) languages.push('arabic');
    if (/[\u0400-\u04ff]/.test(text)) languages.push('cyrillic');
    
    return languages;
  }

  checkSemanticHTML(htmlElement) {
    const semanticTags = ['header', 'footer', 'nav', 'main', 'article', 'section', 'aside'];
    return semanticTags.some(tag => htmlElement.querySelector(tag) !== null);
  }
}
```

### Testing and Validation
```javascript
class MailServiceTester {
  constructor() {
    this.mailService = require('@app/src/services/mail');
  }

  generateTestEmail() {
    return `From: Test Sender <sender@example.com>
To: Test Recipient <recipient@example.com>
Subject: Test Email Subject
Content-Type: text/html; charset=UTF-8

<html>
<head>
  <title>Test Email</title>
</head>
<body>
  <h1>Test Email Content</h1>
  <p>This is a test email with <strong>HTML content</strong>.</p>
  <a href="https://example.com">Click here</a>
  <img src="https://example.com/image.jpg" alt="Test Image">
</body>
</html>`;
  }

  async testBasicParsing() {
    const testEmail = this.generateTestEmail();
    
    try {
      const parsed = await this.mailService.parseMail(testEmail);
      
      const tests = {
        fromParsed: parsed.from === 'Test Sender <sender@example.com>',
        toParsed: parsed.to === 'Test Recipient <recipient@example.com>',
        subjectParsed: parsed.subject === 'Test Email Subject',
        htmlParsed: parsed.html !== null,
        hasH1: parsed.html.querySelector('h1') !== null,
        h1Text: parsed.html.querySelector('h1')?.innerText === 'Test Email Content',
        hasLink: parsed.html.querySelector('a[href="https://example.com"]') !== null
      };

      return {
        passed: Object.values(tests).every(t => t === true),
        tests
      };
    } catch (error) {
      return {
        passed: false,
        error: error.message
      };
    }
  }

  async testEdgeCases() {
    const edgeCases = [
      {
        name: 'Empty HTML',
        email: `From: test@example.com\nTo: user@example.com\nSubject: Empty\n\n<html></html>`
      },
      {
        name: 'No HTML',
        email: `From: test@example.com\nTo: user@example.com\nSubject: Plain\n\nPlain text only`
      },
      {
        name: 'Multiple Recipients',
        email: `From: test@example.com\nTo: user1@example.com, user2@example.com\nSubject: Multi\n\n<p>Test</p>`
      }
    ];

    const results = [];

    for (const testCase of edgeCases) {
      try {
        const parsed = await this.mailService.parseMail(testCase.email);
        results.push({
          name: testCase.name,
          success: true,
          parsed: {
            from: parsed.from,
            to: parsed.to,
            subject: parsed.subject,
            hasHtml: parsed.html !== null
          }
        });
      } catch (error) {
        results.push({
          name: testCase.name,
          success: false,
          error: error.message
        });
      }
    }

    return results;
  }

  async runAllTests() {
    console.log('Running Mail Service Tests...');
    
    const basicTest = await this.testBasicParsing();
    console.log('Basic parsing test:', basicTest.passed ? 'PASSED' : 'FAILED');
    
    const edgeTests = await this.testEdgeCases();
    console.log('Edge case tests:', edgeTests);
    
    return {
      basic: basicTest,
      edgeCases: edgeTests
    };
  }
}
```

## 📊 Output Examples

### Basic Email Parse Result
```json
{
  "to": "user@example.com",
  "from": "Service Name <noreply@service.com>",
  "subject": "Your Trip Receipt",
  "html": "[HTMLElement object with parsed DOM]"
}
```

### Extracted Email Data
```json
{
  "metadata": {
    "from": "notifications@service.com",
    "to": "user@example.com",
    "subject": "Payment Confirmation"
  },
  "content": {
    "plainText": "Thank you for your payment...",
    "linkCount": 3,
    "links": [
      {
        "text": "View Receipt",
        "href": "https://service.com/receipt/12345"
      }
    ],
    "imageCount": 2,
    "hasTable": true
  }
}
```

### Command Processing Result
```json
{
  "processed": true,
  "command": "SUBSCRIBE",
  "result": {
    "action": "subscribe",
    "email": "user@example.com",
    "status": "success"
  }
}
```

### Email Structure Analysis
```json
{
  "structure": {
    "hasHeader": true,
    "hasFooter": true,
    "tableCount": 2,
    "divCount": 15,
    "hasInlineStyles": true
  },
  "accessibility": {
    "imagesWithAlt": 3,
    "totalImages": 4,
    "linksWithTitle": 2,
    "totalLinks": 5
  }
}
```

## ⚠️ Important Notes

### Current Limitations
- **Minimal Extraction:** Only extracts to/from/subject and HTML
- **No Attachments:** Attachment parsing not implemented
- **Text Preference:** Focuses on HTML, plain text emails may need handling
- **Header Access:** Limited to basic headers, no access to full header data

### Email Format Support
- **MIME Compliant:** Supports standard MIME email format
- **HTML Focus:** Optimized for HTML email content
- **Character Encoding:** Handles standard encodings via mailparser
- **Multipart:** Supports multipart messages via simpleParser

### DOM Parsing Features
- **CSS Selectors:** Full querySelector support on parsed HTML
- **DOM Traversal:** Standard DOM methods available
- **Text Extraction:** innerText property for plain text content
- **Attribute Access:** getAttribute method for element attributes

### Error Handling
- **Parse Failures:** Invalid email format will throw errors
- **Missing Fields:** Undefined behavior if required fields missing
- **HTML Issues:** Malformed HTML handled by parser tolerance
- **Async Errors:** All errors propagate through promise chain

### Performance Considerations
- **Memory Usage:** Large emails consume memory during parsing
- **CPU Usage:** HTML parsing can be CPU intensive
- **Async Operations:** Both parsing steps are asynchronous
- **No Streaming:** Entire email loaded into memory

### Security Considerations
- **Script Execution:** Parsed HTML doesn't execute scripts
- **XSS Prevention:** HTML is parsed, not rendered
- **Input Validation:** Validate email sources before parsing
- **Resource Limits:** Consider size limits for email processing

### Extension Possibilities
- **Attachment Support:** Add attachment extraction
- **Header Access:** Expose full email headers
- **Plain Text:** Add plain text extraction
- **Email Validation:** Add sender verification
- **Template Detection:** Identify email template types

## 🔗 Related File Links

- **Notification Service:** Services that might send parsed emails
- **Email Controllers:** API endpoints for email processing
- **User Models:** Storage for email-based user data
- **Authentication:** Email verification workflows

---
*This service provides essential email parsing capabilities for email-based integrations and automated processing in the TSP platform.*