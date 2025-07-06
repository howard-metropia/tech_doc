# Static/Constants Documentation: carpool_verify.js

## 📋 File Overview
- **Purpose:** Defines multilingual email templates and messages for carpool verification workflows
- **Usage:** Used by email services for carpool group membership verification and telework trip logging verification
- **Type:** Message templates / Internationalization constants

## 🔧 Main Exports
```javascript
module.exports = {
  carpool: {
    subject: { en: 'Complete your %projectTitle% carpooling...', es: '...', zh: '...', vi: '...' },
    title: { en: 'ONE MORE STEP!', es: '¡Felicidades!', zh: '只需要再一步！', vi: 'Xin chúc mừng!' },
    msg: { en: 'Please tap the button below to verify...', ... }
  },
  telework: { subject: {}, title: {}, msg: {} },
  buttonName: { en: 'Verify Email', es: 'Abre la aplicación', ... },
  verifyMsg: { carpoolSuccess: {}, teleworkSuccess: {}, done: {}, ... },
  rejectMessage: { subject: {}, message: {}, reason: {} }
};
```

## 📝 Constants Reference
| Section | Purpose | Languages | Template Variables |
|---------|---------|-----------|-------------------|
| carpool | Carpool group verification emails | en, es, zh, vi | %projectTitle%, %duoGroupName% |
| telework | Trip logging verification emails | en, es, zh, vi | %projectTitle% |
| buttonName | Email action button text | en, es, zh, vi | None |
| verifyMsg | Post-verification status messages | en, es, zh, vi | %duoGroupName%, %enterpriseName% |
| rejectMessage | Rejection notification emails | en, zh | %projectTitle%, %duoGroupName% |

## 💡 Usage Examples
```javascript
// Import verification templates
const verifyTemplates = require('./static/carpool_verify');

// Send carpool verification email
const emailData = {
  subject: verifyTemplates.carpool.subject[userLang]
    .replace('%projectTitle%', projectName),
  title: verifyTemplates.carpool.title[userLang],
  message: verifyTemplates.carpool.msg[userLang]
    .replace('%duoGroupName%', groupName),
  buttonText: verifyTemplates.buttonName[userLang]
};

// Handle verification success
const successMsg = verifyTemplates.verifyMsg.carpoolSuccess[userLang]
  .replace('%duoGroupName%', groupName);

// Send rejection notification
const rejectEmail = {
  subject: verifyTemplates.rejectMessage.subject[userLang],
  reason: verifyTemplates.rejectMessage.reason[userLang]
    .replace('%duoGroupName%', groupName)
};
```

## ⚠️ Important Notes
- Template variables must be replaced with actual values before sending emails
- Spanish translation uses "Abre la aplicación" (Open the app) instead of "Verify Email"
- Traditional Chinese (zh) is supported for Taiwan market
- Vietnamese (vi) support for diverse user base
- Rejection messages only available in English and Chinese
- Success messages differentiate between carpool and telework contexts

## 🏷️ Tags
**Keywords:** email-templates, verification, internationalization, carpool-groups, telework-logging  
**Category:** #static #constants #email-templates #i18n #verification