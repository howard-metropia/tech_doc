# Enterprise Carpool Module - ConnectSmart Portal

🔍 **Quick Summary (TL;DR)**
- Enterprise employee verification system with JWT token generation, email verification workflows, and database integration for carpool access
- enterprise-carpool | jwt-verification | email-verification | employee-database | carpool-access | token-generation
- Used for validating enterprise employees for carpool services, sending verification emails, and managing enterprise user onboarding
- Compatible with Web2py framework, JWT authentication, SMTP email services, requires database access and email service configuration

❓ **Common Questions Quick Index**
- Q: How do I verify enterprise employees for carpool access? → See [Usage Methods](#usage-methods)
- Q: What's in the JWT verification token? → See [Detailed Code Analysis](#detailed-code-analysis)
- Q: How do verification emails work? → See [Usage Methods](#usage-methods)
- Q: How do I check if an employee is already verified? → See [Output Examples](#output-examples)
- Q: What database tables are involved? → See [Technical Specifications](#technical-specifications)
- Q: How do I customize verification email templates? → See [Related File Links](#related-file-links)
- Q: What happens if email sending fails? → See [Important Notes](#important-notes)
- Q: How long are verification tokens valid? → See [Technical Specifications](#technical-specifications)

📋 **Functionality Overview**
- **Non-technical explanation:** Like a secure employee badge system for carpool services - it creates special verification codes, sends them via email to company employees, and tracks who has permission to use corporate carpool features. Similar to how office key cards verify employees for building access, or how concert tickets validate entry to events.
- **Technical explanation:** JWT-based enterprise employee verification system with email workflow automation, database persistence, and template-driven communication for carpool service authorization.
- **Business value:** Ensures only authorized corporate employees access enterprise carpool features, provides audit trail for compliance, and automates onboarding workflows to reduce manual verification overhead.
- **System context:** Integrates with enterprise authentication, email delivery services, and carpool management features within the ConnectSmart portal application.

🔧 **Technical Specifications**
- **File info:** `enterprise_carpool.py`, 82 lines, Python enterprise verification module, medium complexity
- **Dependencies:**
  - `gluon.current` (Web2py): Framework context for database, auth, configuration access
  - `datetime` (built-in): Timestamp generation for token creation and database records
  - `calendar.timegm` (built-in): UTC timestamp conversion for JWT payload
  - `jwt_helper.JWTHelper` (internal): JWT token generation and validation
- **Database integration:** `enterprise` table for verification tracking, user association, domain extraction
- **Configuration parameters:**
  - `domain.url`: Base domain for verification link generation
  - `project.name`: Application name for email subject lines
  - `project.logo`: Logo image URL for email templates
  - `mail.url`: Email service endpoint for message delivery
- **Token specification:** JWT with standard claims (iat, exp, iss) plus user verification data
- **Security:** Email parameter validation, domain extraction, secure token generation with expiration

📝 **Detailed Code Analysis**
```python
def generate_verification_token(user_id, email, verify_type):
    """Generate JWT token for enterprise email verification"""
    # Create UTC timestamp for token issuance and expiration
    now = timegm(datetime.utcnow().utctimetuple())
    exp = now + JWTHelper().expiration_range  # Add configured expiration period
    
    payload = {
        'iat': now,                    # Issued at timestamp
        'exp': exp,                    # Expiration timestamp  
        'iss': 'Metropia Auth',        # Token issuer identification
        'user': {
            'id': user_id,             # User identifier
            'email': email,            # Employee email address
            'verify_type': verify_type # Verification context (carpool/trip_log)
        },
        'hmac_key': ''                 # Placeholder for HMAC validation
    }
    return current.auth.jwt_handler.generate_token(payload)

def send_verification_mail(response, user_id, email, verify_type):
    """Send enterprise verification email with JWT token link"""
    # Handle Unicode email encoding for compatibility
    # Generate unique verification token
    # Extract company domain from email address
    # Database upsert operation for verification tracking
    # Template rendering with localized content
    # Email delivery via configured mail service

def check_verification(db, user_id, email):
    """Verify if enterprise employee has completed verification"""
    # Query enterprise table for user/email combination
    # Check employee_status field for approval (1 = verified)
    # Return boolean verification status

def sendmail(to, subject, html):
    """Send email via configured mail service API"""
    # JSON payload construction with recipient, subject, HTML content
    # HTTP POST to mail service endpoint with proper headers
```

🚀 **Usage Methods**
```python
from applications.portal.modules.enterprise_carpool import *

# Complete enterprise verification workflow
def enterprise_onboarding_flow(user_id, email, verify_type="carpool"):
    # Generate and send verification email
    token = send_verification_mail(response, user_id, email, verify_type)
    
    # Token contains verification link like:
    # https://portal.com/api/v1/verify_carpool_email.html?verify_token=eyJ0eXAi...
    
    return token

# Check employee verification status
def is_employee_verified(user_id, email):
    db = current.db
    return check_verification(db, user_id, email)

# Manual token generation for API integration
def create_verification_token(user_id, email, purpose="carpooling"):
    token = generate_verification_token(user_id, email, purpose)
    return token

# Email verification for different services
def verify_for_trip_logging(user_id, email):
    send_verification_mail(response, user_id, email, "trip_log")

# Custom email sending
def send_custom_notification(recipients, subject, message):
    sendmail(recipients, subject, message)

# Database verification check with error handling
def safe_verification_check(user_id, email):
    try:
        db = current.db
        is_verified = check_verification(db, user_id, email)
        return {'verified': is_verified, 'error': None}
    except Exception as e:
        return {'verified': False, 'error': str(e)}
```

📊 **Output Examples**
```python
# Successful verification token generation
>>> generate_verification_token("user123", "john@company.com", "carpool")
'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MTk3NjA4MDA...'

# Verification email sending
>>> send_verification_mail(response, "user123", "john@company.com", "carpool")
'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'  # Returns verification token

# Database verification check
>>> check_verification(db, "user123", "john@company.com")  
True  # Employee is verified and active

>>> check_verification(db, "user456", "invalid@email.com")
False  # No verification record or inactive status

# Enterprise table record after verification
Database record:
{
    'user_id': 'user123',
    'enterprise_email': 'john@company.com', 
    'email_verify_token': 'eyJ0eXAi...',
    'enterprise_domain': 'company.com',
    'employee_status': 1,  # 1 = verified, 0 = pending
    'created_on': '2024-06-30 10:30:00',
    'updated_on': '2024-06-30 10:30:00'
}

# Generated verification email content
Subject: "ConnectSmart carpooling verification"
Body: HTML template with:
- Title: "Congratulations!"
- Message: "Use the button below to verify your email address..."
- Button: "Open the App" → links to verification URL
- Logo: Company branding image

# Email service API call
POST /mail-service/send
{
    "to": ["john@company.com"],
    "subject": "ConnectSmart carpooling verification", 
    "html": "<html>...</html>"
}
```

⚠️ **Important Notes**
- **Unicode handling:** Email addresses converted from Unicode to string for compatibility with email systems
- **Database upsert pattern:** Uses `update_or_insert` to handle both new registrations and re-verification requests
- **Domain extraction:** Automatically extracts company domain from email for enterprise association
- **Token expiration:** JWT tokens have configurable expiration - ensure timely user verification
- **Email delivery dependency:** Relies on external mail service - implement fallback for service outages
- **Verification types:** "carpool" vs "trip_log" may trigger different email templates and permissions
- **Employee status codes:** Status 1 indicates verified employee, other values may indicate pending/rejected states
- **Template localization:** Email content supports internationalization through Web2py T() function

🔗 **Related File Links**
- **Email template:** `carpool_verify_mail.html` - HTML template for verification emails
- **JWT implementation:** `jwt_helper.py` - JWT token generation and validation logic
- **Enterprise API:** `enterpirse_helper.py` - Enterprise employee verification service integration
- **Database schema:** Enterprise table definition in Web2py database models
- **Mail service:** External email delivery service configuration and endpoints
- **Configuration files:** Web2py application settings for domain, project, and mail configuration
- **Authentication system:** Web2py auth integration for user session management

📈 **Use Cases**
- **New employee onboarding:** Verify corporate email addresses for carpool service access authorization
- **Service access control:** Gate premium carpool features behind enterprise employee verification
- **Compliance auditing:** Track verification history for corporate mobility program compliance
- **Multi-service verification:** Support both carpool and trip logging verification workflows
- **Re-verification workflows:** Handle employee status changes and re-verification requests
- **Email campaign automation:** Batch verification emails for enterprise rollouts
- **Integration testing:** Verify enterprise integration endpoints during development and deployment

🛠️ **Improvement Suggestions**
- **Token refresh mechanism:** Add token refresh capability to extend verification without re-sending emails
- **Email template customization:** Support enterprise-specific email branding and messaging
- **Verification analytics:** Add tracking for email open rates, click-through rates, and verification completion
- **Bulk verification:** Implement batch processing for large enterprise employee verification campaigns
- **Error handling enhancement:** Add specific error codes and retry mechanisms for failed email delivery
- **Security hardening:** Add rate limiting for verification email sending to prevent abuse
- **Database optimization:** Add indexes on frequently queried enterprise table columns
- **Notification system:** Add webhook notifications for completed verifications

🏷️ **Document Tags**
- **Keywords:** enterprise-verification, jwt-tokens, email-verification, carpool-access, employee-onboarding, database-integration, template-rendering, mail-service, authentication-workflow, verification-tokens
- **Technical tags:** `#enterprise` `#jwt` `#email-verification` `#carpool` `#authentication` `#web2py` `#database` `#templates` `#onboarding`
- **Target roles:** Backend developers (intermediate), enterprise integrators, email system administrators, authentication specialists  
- **Difficulty level:** ⭐⭐⭐ (advanced) - Requires JWT understanding, database design, email service integration, and template systems
- **Maintenance level:** Medium - email template updates, JWT configuration changes, database schema evolution
- **Business criticality:** High - essential for enterprise customer onboarding and carpool access control
- **Related topics:** JWT authentication, email automation, enterprise SSO, carpool management, employee verification, template systems