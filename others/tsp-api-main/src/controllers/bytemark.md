# Bytemark Integration Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller processes incoming email notifications from AWS SES that are related to the Bytemark ticketing service. It specifically handles password reset and account confirmation emails by parsing their content and triggering the corresponding actions.

**Keywords:** bytemark | email-processing | ses-webhook | password-reset | account-confirmation | aws-ses | mail-parser | ticketing | transit-payment | s3-integration

**Primary use cases:** 
- Automating Bytemark password resets triggered by user requests.
- Automating Bytemark account email confirmations.
- Integrating AWS Simple Email Service (SES) with the Bytemark third-party service.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, Axios for HTTP requests.

## ❓ Common Questions Quick Index
- **Q: What triggers this endpoint?** → It's triggered by an AWS SES notification when an email is received.
- **Q: What specific emails does this controller handle?** → Only Bytemark password reset and account confirmation emails.
- **Q: How does it get the email content?** → It fetches the raw email from an S3 bucket (`smart-aws-logs`).
- **Q: How does the password reset work?** → [Password Reset Flow](#password-reset-flow)
- **Q: What is the purpose of `knex('bytemark_tokens').update`?** → [Password Reset Flow](#password-reset-flow)
- **Q: How does account confirmation work?** → [Account Confirmation Flow](#account-confirmation-flow)
- **Q: Why does this endpoint exist?** → To automate user lifecycle events for a third-party service (Bytemark) that communicates via email.
- **Q: What happens if the email is not from Bytemark?** → The controller does nothing and returns a success response.

## 📋 Functionality Overview

**Non-technical explanation:** 
Imagine you have a special mailbox (AWS SES) that only accepts mail from your public transit ticketing partner, Bytemark. This controller is like a robotic assistant monitoring that mailbox. When a "Forgot Password" letter arrives, the robot opens it, finds the special reset link, generates a new temporary password, saves a copy of it, and then uses the link along with the new password to complete the reset on your behalf. Similarly, if an "Confirm Your Account" letter arrives, the robot clicks the confirmation link for you. It ignores any other mail.

**Technical explanation:** 
This Koa.js controller provides a single `POST /api/v1/bytemark/mail` webhook endpoint designed to be triggered by AWS SES notifications. When invoked, it receives an S3 object key, fetches the corresponding raw email content from an S3 bucket, and parses it using a mail-parsing service. It identifies Bytemark-specific emails, extracts action URLs (for password reset or account confirmation) from the HTML body, and performs the necessary actions: either calling the Bytemark service to complete a password reset with a newly generated password or making a GET request to a confirmation URL.

**Business value explanation:**
This controller provides crucial automation for integrating with the Bytemark ticketing system, a third-party vendor. By programmatically handling user-initiated password resets and account confirmations, it creates a seamless user experience without manual intervention. This reduces administrative overhead and support tickets related to Bytemark account management, ensuring users can self-serve for common account issues.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/bytemark.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Webhook Controller
- **File Size:** ~1.5 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - Involves multiple service integrations: S3, mail parsing, database, and external API calls)

**Dependencies (Criticality Level):**
- `knex`: SQL query builder for database interaction (**Critical** for password reset).
- `@koa/router`: HTTP routing framework (**Critical**).
- `koa-body`: Request body parsing middleware (**Critical**).
- `axios`: HTTP client for making requests to external Bytemark URLs (**Critical**).
- `@app/src/services/s3`: Wrapper for fetching objects from AWS S3 (**Critical**).
- `@app/src/services/mail`: Service to parse raw email content (**Critical**).
- `@app/src/services/bytemark`: Service encapsulating the Bytemark API logic (**Critical**).
- `config`: Manages configuration, specifically Bytemark URLs (**High**).

**Configuration (`config.vendor.bytemark`):**
- `url.account`: A base URL string that is expected to be present in the Bytemark emails. Used to identify the correct links.

## 📝 Detailed Code Analysis

### Main Route Definition

**`POST /api/v1/bytemark/mail` Endpoint Signature:**
```javascript
router.post('ses_mail', '/api/v1/bytemark/mail', koaBody(), async (ctx) => { ... })
```
- **Webhook Trigger:** This endpoint is intended to be called by an automated process, likely an AWS Lambda function triggered by an S3 put event from AWS SES.
- **Request Body:** It expects a JSON body with a `key` field, e.g., `{ "key": "path/to/email/in/s3" }`.

### Execution Flow Analysis

1.  **Request Ingress**: Receives a POST request, and `koaBody()` parses the body to extract the S3 object `key`.
2.  **Fetch Email from S3**: It calls `getObject()` to download the raw email content from the `smart-aws-logs` S3 bucket using the provided `key`.
3.  **Parse Email**: The raw content is passed to `parseMail()`, which converts it into a structured object containing `from`, `to`, and an HTML document object (`html`).
4.  **Source Verification**: It checks if `mail.from` includes the string 'bytemark'. If not, the function effectively terminates, and a success response is sent.
5.  **Action URL Extraction**: It parses the `mail.html` content, searching for an anchor tag (`<a>`) whose `href` attribute contains the Bytemark account URL from the config.
6.  **Conditional Logic (Password Reset vs. Confirmation)**:
    - **Password Reset Flow**: If the extracted `url` contains the substring `'reset'`:
        a. It extracts the password reset `token` from the end of the URL.
        b. It generates a new random `password` (12 characters).
        c. It updates a `bytemark_tokens` table in the `portal` database, setting the `password` field for the user identified by the email's `to` address (`mail.to`). This seems to be for internal record-keeping.
        d. It calls `bytemark.resetPassword(token, password)`, which makes the actual API call to Bytemark to finalize the password change.
    - **Account Confirmation Flow**: If the extracted `url` contains the substring `'confirm'`:
        a. It makes a simple `axios.get()` request to the confirmation URL to activate the account.
7.  **Response**: In all cases (including if the email was not from Bytemark), it returns a generic `success()` response with an HTTP 200 status. This is typical for webhooks, acknowledging receipt without returning detailed results.

## 🚀 Usage Methods

This endpoint is not designed for direct manual use. It is part of an automated workflow.

**Workflow Setup (AWS):**
1.  **AWS SES**: Configure SES to receive emails for a specific domain.
2.  **SES Rule**: Create a rule in SES that, upon receiving an email, saves the full raw email to the `smart-aws-logs` S3 bucket.
3.  **S3 Trigger**: Configure an S3 "put event" trigger on that bucket.
4.  **Lambda Function**: The S3 trigger invokes a simple Lambda function.
5.  **Lambda Logic**: The Lambda function's sole purpose is to make a POST request to this `/api/v1/bytemark/mail` endpoint, putting the S3 object key in the request body.

**Example Lambda Payload (to this endpoint):**
```json
{
  "key": "emails/0123456789abcdef0123456789abcdef"
}
```

## 📊 Output Examples

### Successful Response
Regardless of the email's content or the actions taken, a successful invocation that does not throw an unhandled error will result in an HTTP 200 OK with this body:

```json
{
  "result": "success",
  "data": null
}
```

### Error Scenarios
This endpoint does not have explicit error handling. If any of the `await`-ed functions fail (e.g., `getObject` fails to find the S3 key, `axios.get` returns a 500 error, or `knex` fails to connect to the database), the Koa application's global error handler would be invoked, likely resulting in an HTTP 500 Internal Server Error response.

## ⚠️ Important Notes

### Security Considerations
- **Webhook Security**: The endpoint is implicitly public. It should ideally be secured to only accept requests from the trusted AWS Lambda function. This could be done via a secret key/token in the header or by restricting the source IP address at the firewall/load balancer level.
- **S3 Bucket Permissions**: The IAM role executing this code needs `s3:GetObject` permissions on the `smart-aws-logs` bucket.
- **Database Credentials**: The `knex` connection relies on properly secured database credentials.

### Idempotency
The endpoint is **not** idempotent. If the same SES notification is processed twice:
- For a password reset, it would generate a *new* password, update the database again, and attempt the reset again. The second attempt on the Bytemark side would likely fail as the token would have already been used.
- For an account confirmation, it would simply hit the confirmation URL a second time, which is likely harmless.

### Error Handling Strategy
The current implementation lacks robust error handling. A failure in any step of the process will cause the entire request to fail with a generic server error. For a production system, it would be beneficial to wrap the logic in a `try...catch` block to log specific errors and still return a 200 OK status to the webhook caller, preventing unnecessary retries.

## 🔗 Related File Links
- **S3 Service:** `allrepo/connectsmart/tsp-api/src/services/s3.js`
- **Mail Parsing Service:** `allrepo/connectsmart/tsp-api/src/services/mail.js`
- **Bytemark Service:** `allrepo/connectsmart/tsp-api/src/services/bytemark.js`
- **Database Connection:** `@maas/core/mysql` (points to the core MySQL setup)
- **Configuration:** `config` files, specifically looking for the `vendor.bytemark` section.

---
*This documentation was generated to provide a comprehensive overview of the `bytemark.js` controller and its role in the Bytemark integration workflow.* 