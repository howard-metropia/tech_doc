# Token Notification Service

## Overview

The Token Notification service manages notifications for token distribution and expiration events, sending multilingual notifications to users when they receive tokens or when tokens are about to expire.

## Service Information

- **Service Name**: Token Notification
- **File Path**: `/src/services/tokenNotification.js`
- **Type**: Notification Management Service
- **Dependencies**: MySQL, Moment.js, Notification Service

## Functions

### tokenGetNotification()

Sends notifications to users when new tokens are distributed to their accounts.

**Purpose**: Notifies users about newly issued tokens from agencies
**Parameters**: None (processes pending token distributions)
**Returns**: Array of notification results

**Process Flow**:
1. Queries active token transactions awaiting notification
2. Groups tokens by user and token ID to calculate balances
3. Sends multilingual notifications based on user language preference
4. Updates notification status to prevent duplicate notifications

**Token Query Conditions**:
- Activity type = 1 (token distribution)
- Issued date < current time
- Expiry date > current time
- Notification status = 0 (not yet notified)

**Example**:
```javascript
const results = await tokenGetNotification();
// Processes all pending token notifications
// Sends messages like: "You've Got New Tokens!"
```

### tokenExpireNotification()

Sends notifications to users when their tokens are approaching expiration.

**Purpose**: Warns users about tokens expiring within 14 days
**Parameters**: None (processes tokens nearing expiration)
**Returns**: Array of notification results

**Process Flow**:
1. Identifies tokens expiring within 14 days
2. Filters users with positive balances and no prior expiration notice
3. Sends expiration warnings with localized dates
4. Updates expiration notification status

**Expiration Criteria**:
- Days until expiration <= 14
- Days until expiration > 0
- Token balance > 0
- No previous expiration notification sent

## Language Support

### Supported Languages
- **English (en-us)**: Default language
- **Traditional Chinese (zh-tw)**: Full support
- **Spanish (es)**: Full support
- **Vietnamese (vi)**: Full support

### Language Processing
- Normalizes language codes (underscore to dash)
- Defaults to English for unsupported languages
- Uses user's device language preference

## Notification Types

### Token Received (ID: 68)
- **English**: "You've Got New Tokens!"
- **Chinese**: "獲得新的代幣"
- **Spanish**: "¡Tiene fichas nuevas!"
- **Vietnamese**: "Bạn có Token mới!"

### Token Expiration (ID: 67)
- **English**: "Expiration Notice"
- **Chinese**: "代幣到期"
- **Spanish**: "Aviso de expiración"
- **Vietnamese**: "Thông báo hết hạn"

## Message Templates

### Token Distribution Messages
```javascript
// English
"Congratulations! {agencyName} has given you {balance} tokens to spend on transit tickets! Visit your wallet to use them now."

// Chinese
"恭喜您！{agencyName} 剛剛發放了 {balance} 代幣到你的錢包，這些代幣可用於購買車票！快點進錢包查看一下吧！"
```

### Token Expiration Messages
```javascript
// English
"You have {total} Tokens from {agencyName}, which will expire on {expireDate}, we encourage you to use them to get the most out of your membership."
```

## Database Operations

### Token Transaction Table
- **Joins**: auth_user for language preferences
- **Grouping**: By token ID and user ID for balance calculation
- **Status Updates**: dist_notify_status and expire_notify_status

### Data Processing
- **Balance Calculation**: Sum of token transaction amounts
- **Date Filtering**: Time-based queries for active and expiring tokens
- **Duplicate Prevention**: Status flags prevent repeated notifications

## Integration Points

### Used By
- Scheduled notification jobs
- Token distribution systems
- Agency token management
- User wallet services

### External Dependencies
- **MySQL Portal**: Token and user data
- **Moment.js**: Date manipulation and formatting
- **Send Notification Service**: Message delivery
- **Common Service**: User locale date formatting

## Notification Metadata

### Token Received Metadata
```javascript
{
  agency_id: agencyId,
}
```

### Token Expiration Metadata
```javascript
{
  agency_id: agencyId,
  agency_name: agencyName,
  expire_date: localizedExpireDate
}
```

## Error Handling

### Query Failures
- Logs database errors
- Continues processing remaining notifications
- Graceful handling of missing data

### Language Processing
- Defaults to English for invalid language codes
- Handles missing language preferences
- Validates language format

## Performance Optimization

### Batch Processing
- Groups tokens by user to minimize notifications
- Uses Set for efficient duplicate tracking
- Batch status updates reduce database calls

### Query Efficiency
- Joins minimize database round trips
- Indexed queries on dates and status
- Efficient grouping and aggregation

## Security Considerations

- **User Privacy**: Token balances handled securely
- **Agency Information**: Proper agency name display
- **Status Tracking**: Prevents notification spam
- **Data Validation**: Validates token amounts and dates

## Usage Guidelines

1. **Scheduling**: Run as regular background job
2. **Monitoring**: Check notification delivery success rates
3. **Language Support**: Ensure translations are current
4. **Date Formatting**: Verify locale-specific date formats
5. **Testing**: Test with various language preferences

## Dependencies

- **@maas/core/mysql**: Database connection management
- **@maas/core/log**: Centralized logging
- **Moment.js**: Date manipulation and timezone handling
- **Send Notification Service**: Message delivery system
- **Common Service**: User locale utilities