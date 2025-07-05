# Notification Message Templates

## Overview
**File**: `src/static/notification-msg.js`  
**Type**: Localized Message Template Module  
**Purpose**: Provides internationalized notification message templates for TSP job system notifications

## Core Functionality

### Internationalized Messaging
This module manages localized notification message templates that support multiple languages for user-facing notifications in the TSP (Transportation Service Provider) system.

### Template Structure
The module organizes notification content into title and body sections with multi-language support for consistent user communication across different locales.

## Module Dependencies

### Notification Type Integration
```javascript
const NOTIFICATION_TYPE = require('@app/src/static/defines').notificationType;
```

**Purpose**: Links notification message templates with standardized notification type constants from the system definitions

## Message Template Organization

### Structure Overview
```javascript
module.exports = {
  title: {
    [NOTIFICATION_TYPE.NOTIFICATION_KEY]: {
      en: 'English Title',
      es: 'Spanish Title',
      vi: 'Vietnamese Title',
      zh: 'Chinese Title',
    },
  },
  body: {
    [NOTIFICATION_TYPE.NOTIFICATION_KEY]: {
      en: 'English Message Body',
      es: 'Spanish Message Body',
      vi: 'Vietnamese Message Body',
      zh: 'Chinese Message Body',
    },
  },
};
```

### Supported Languages
- **en**: English (primary language)
- **es**: Spanish
- **vi**: Vietnamese
- **zh**: Chinese (Traditional)

## Current Implementation

### DUO End Zombie Trip Notification
```javascript
title: {
  [NOTIFICATION_TYPE.DUO_END_ZOMBIE_TRIP]: {
    en: 'Trip has been ended',
    es: ' ',
    vi: ' ',
    zh: ' ',
  },
},
body: {
  [NOTIFICATION_TYPE.DUO_END_ZOMBIE_TRIP]: {
    en: 'Attention %name%! Your carpool has ended. For any further support, please reach out to us through Help Desk. Safe travels!',
    es: ' ',
    vi: ' ',
    zh: ' ',
  },
},
```

**Notification Type**: `DUO_END_ZOMBIE_TRIP` (value: 62)
**Purpose**: Notifies users when their carpool trip has been automatically terminated by the system

### Message Features
- **Personalization**: Uses `%name%` placeholder for dynamic user name insertion
- **Call to Action**: Directs users to Help Desk for support
- **Friendly Tone**: Includes "Safe travels!" for positive user experience

## Template Variable System

### Variable Substitution
```javascript
// Example of variable usage in message body
'Attention %name%! Your carpool has ended.'
```

**Supported Variables**:
- `%name%`: User's display name or first name
- Additional variables can be added as needed

### Variable Processing
```javascript
const processNotificationMessage = (template, variables) => {
  let message = template;
  Object.keys(variables).forEach(key => {
    const placeholder = `%${key}%`;
    message = message.replace(new RegExp(placeholder, 'g'), variables[key]);
  });
  return message;
};

// Usage example
const message = processNotificationMessage(
  notificationMsg.body[NOTIFICATION_TYPE.DUO_END_ZOMBIE_TRIP].en,
  { name: 'John' }
);
// Result: "Attention John! Your carpool has ended..."
```

## Integration Patterns

### Notification Service Integration
```javascript
const notificationMsg = require('@app/src/static/notification-msg');
const { notificationType } = require('@app/src/static/defines');

class NotificationService {
  async sendNotification(userId, type, variables = {}, locale = 'en') {
    const title = notificationMsg.title[type]?.[locale] || 
                  notificationMsg.title[type]?.en || 
                  'Notification';
    
    const body = notificationMsg.body[type]?.[locale] || 
                 notificationMsg.body[type]?.en || 
                 'You have a new notification';
    
    const processedBody = this.processVariables(body, variables);
    
    await this.sendPushNotification(userId, {
      title,
      body: processedBody,
      type,
    });
  }
  
  processVariables(template, variables) {
    let message = template;
    Object.keys(variables).forEach(key => {
      message = message.replace(
        new RegExp(`%${key}%`, 'g'), 
        variables[key]
      );
    });
    return message;
  }
}
```

### Usage Examples
```javascript
const notificationService = new NotificationService();

// Send zombie trip termination notification
await notificationService.sendNotification(
  userId,
  notificationType.DUO_END_ZOMBIE_TRIP,
  { name: 'Alice' },
  'en'
);

// Send with different locale
await notificationService.sendNotification(
  userId,
  notificationType.DUO_END_ZOMBIE_TRIP,
  { name: 'María' },
  'es'
);
```

## Language Fallback Strategy

### Hierarchical Fallback
```javascript
const getLocalizedMessage = (messageType, section, locale, variables = {}) => {
  const messages = notificationMsg[section][messageType];
  
  if (!messages) {
    return `Unknown ${section}`;
  }
  
  // Try requested locale first
  let template = messages[locale];
  
  // Fallback to English if locale not available
  if (!template || template.trim() === '') {
    template = messages.en;
  }
  
  // Final fallback to default message
  if (!template || template.trim() === '') {
    template = section === 'title' ? 'Notification' : 'You have a notification';
  }
  
  return processNotificationMessage(template, variables);
};
```

### Locale Detection
```javascript
const getUserLocale = (user) => {
  // Priority order for locale detection
  return user.preferredLanguage || 
         user.deviceLanguage || 
         user.regionLanguage || 
         'en';
};
```

## Template Expansion

### Adding New Notification Types
```javascript
// Example: Adding a new notification type
const newNotificationTemplates = {
  title: {
    [NOTIFICATION_TYPE.NEW_CARPOOL_MATCH]: {
      en: 'New Carpool Match Found',
      es: 'Nueva Coincidencia de Viaje Compartido',
      vi: 'Tìm Thấy Đối Tác Chia Sẻ Chuyến Đi Mới',
      zh: '找到新的拼車配對',
    },
  },
  body: {
    [NOTIFICATION_TYPE.NEW_CARPOOL_MATCH]: {
      en: 'Hi %name%! We found a carpool match for your trip to %destination%. Tap to view details.',
      es: 'Hola %name%! Encontramos una coincidencia de viaje compartido para tu viaje a %destination%. Toca para ver detalles.',
      vi: 'Xin chào %name%! Chúng tôi đã tìm thấy một đối tác chia sẻ chuyến đi cho chuyến đi của bạn đến %destination%. Nhấn để xem chi tiết.',
      zh: '你好 %name%! 我們為您前往 %destination% 的行程找到了拼車配對。點擊查看詳情。',
    },
  },
};

// Merge with existing templates
Object.assign(notificationMsg.title, newNotificationTemplates.title);
Object.assign(notificationMsg.body, newNotificationTemplates.body);
```

### Variable Enhancement
```javascript
// Enhanced variable system with formatting
const enhancedVariables = {
  name: 'John',
  destination: 'Downtown',
  time: new Date(),
  distance: 5.2,
};

const formatVariable = (value, type) => {
  switch (type) {
    case 'time':
      return new Date(value).toLocaleTimeString();
    case 'distance':
      return `${value} miles`;
    case 'currency':
      return `$${value.toFixed(2)}`;
    default:
      return value;
  }
};
```

## Quality Assurance

### Template Validation
```javascript
const validateNotificationTemplates = () => {
  const errors = [];
  const requiredLanguages = ['en'];
  
  Object.keys(notificationMsg.title).forEach(notificationType => {
    requiredLanguages.forEach(lang => {
      const title = notificationMsg.title[notificationType]?.[lang];
      const body = notificationMsg.body[notificationType]?.[lang];
      
      if (!title || title.trim() === '') {
        errors.push(`Missing ${lang} title for notification type ${notificationType}`);
      }
      
      if (!body || body.trim() === '') {
        errors.push(`Missing ${lang} body for notification type ${notificationType}`);
      }
    });
  });
  
  return errors;
};
```

### Translation Status Tracking
```javascript
const getTranslationStatus = () => {
  const status = {};
  const languages = ['en', 'es', 'vi', 'zh'];
  
  Object.keys(notificationMsg.title).forEach(notificationType => {
    status[notificationType] = {};
    
    languages.forEach(lang => {
      const hasTitle = notificationMsg.title[notificationType]?.[lang]?.trim() !== '';
      const hasBody = notificationMsg.body[notificationType]?.[lang]?.trim() !== '';
      
      status[notificationType][lang] = {
        title: hasTitle,
        body: hasBody,
        complete: hasTitle && hasBody,
      };
    });
  });
  
  return status;
};
```

## Testing Framework

### Unit Tests
```javascript
describe('Notification Message Templates', () => {
  test('should have English messages for all notification types', () => {
    const notificationTypes = Object.keys(notificationMsg.title);
    
    notificationTypes.forEach(type => {
      expect(notificationMsg.title[type].en).toBeDefined();
      expect(notificationMsg.body[type].en).toBeDefined();
      expect(notificationMsg.title[type].en.trim()).not.toBe('');
      expect(notificationMsg.body[type].en.trim()).not.toBe('');
    });
  });
  
  test('should process variables correctly', () => {
    const template = 'Hello %name%! Your trip to %destination% is ready.';
    const variables = { name: 'John', destination: 'Airport' };
    
    const result = processNotificationMessage(template, variables);
    expect(result).toBe('Hello John! Your trip to Airport is ready.');
  });
});
```

### Integration Tests
```javascript
describe('Notification Service Integration', () => {
  test('should send localized notifications', async () => {
    const notificationService = new NotificationService();
    
    const result = await notificationService.sendNotification(
      'user123',
      NOTIFICATION_TYPE.DUO_END_ZOMBIE_TRIP,
      { name: 'Alice' },
      'en'
    );
    
    expect(result.title).toBe('Trip has been ended');
    expect(result.body).toContain('Attention Alice!');
  });
});
```

## Performance Considerations

### Template Caching
```javascript
const templateCache = new Map();

const getCachedTemplate = (type, section, locale) => {
  const cacheKey = `${type}-${section}-${locale}`;
  
  if (!templateCache.has(cacheKey)) {
    const template = notificationMsg[section][type]?.[locale];
    templateCache.set(cacheKey, template);
  }
  
  return templateCache.get(cacheKey);
};
```

### Batch Processing
```javascript
const sendBatchNotifications = async (notifications) => {
  const processed = notifications.map(notification => ({
    ...notification,
    title: getLocalizedMessage(
      notification.type,
      'title',
      notification.locale,
      notification.variables
    ),
    body: getLocalizedMessage(
      notification.type,
      'body',
      notification.locale,
      notification.variables
    ),
  }));
  
  return await pushNotificationService.sendBatch(processed);
};
```

## Maintenance and Governance

### Translation Workflow
1. **Template Creation**: Define English template with variables
2. **Translation Request**: Submit for professional translation
3. **Review Process**: Native speaker review and approval
4. **Testing**: Validate translations in context
5. **Deployment**: Update production templates

### Content Guidelines
- **Tone**: Friendly but professional
- **Length**: Keep messages concise for mobile display
- **Variables**: Use descriptive variable names
- **Context**: Provide context for translators
- **Cultural Sensitivity**: Consider cultural differences

### Version Control
```javascript
// Track template versions for rollback capability
const templateVersions = {
  version: '1.2.0',
  lastUpdated: '2024-01-15',
  changes: [
    'Added Vietnamese translations',
    'Updated DUO_END_ZOMBIE_TRIP message tone',
  ],
};
```

This notification message template system provides a robust foundation for internationalized user communications in the TSP job system, ensuring consistent and localized messaging across all supported languages and notification types.