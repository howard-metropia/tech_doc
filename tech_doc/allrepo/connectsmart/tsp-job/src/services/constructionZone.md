# Construction Zone Service

## Overview

The Construction Zone service generates AI-powered multilingual notifications for construction events using OpenAI's GPT-3.5 API. It provides context-aware messaging based on construction impact categories and user preferences.

## Service Information

- **Service Name**: Construction Zone
- **File Path**: `/src/services/constructionZone.js`
- **Type**: AI-Powered Notification Service
- **Dependencies**: OpenAI API, Moment.js, Axios

## Configuration

### OpenAI Integration
- **Model**: GPT-3.5-turbo
- **API Configuration**: Loaded from config.vendor.openai
- **Retry Delay**: 10 seconds for failed requests
- **Character Limit**: Defined in construction alert settings

### Supported Languages
- **English**: "Construction Alert"
- **Spanish**: "Alerta de construcción"
- **Vietnamese**: "Cảnh báo xây dựng"
- **Traditional Chinese**: "施工通知"

## Functions

### getAIMessage(message, language)

Generates AI-powered construction alert messages using OpenAI API.

**Purpose**: Creates localized, context-aware construction notifications
**Parameters**:
- `message` (string): Prompt containing construction event details
- `language` (string): User's preferred language code

**Returns**: Object containing title, body, and language

**API Integration**:
- Uses GPT-3.5-turbo model
- System role: "operator" for consistent messaging
- Handles API failures gracefully with fallback content

**Example**:
```javascript
const message = "Construction on Main St, lanes blocked...";
const result = await getAIMessage(message, "en-US");
// Returns: { title: "Construction Alert", body: "AI-generated message", language: "English" }
```

### formMessage(event, nowTime, language)

Creates structured prompts for AI message generation based on construction categories.

**Purpose**: Formats event data into comprehensive prompts for AI processing
**Parameters**:
- `event` (object): Construction event data including category, location, dates, lanes
- `nowTime` (string): Current timestamp for context
- `language` (string): Target language for message generation

**Returns**: Formatted prompt string for AI processing

**Construction Categories**:
- **Category 5**: Friendly reminder tone
- **Category 3-4**: Important reminder with impact advice
- **Category 1**: Urgent attention with alternative route suggestions

**Message Guidelines**:
- Character limit enforcement
- No emojis or newlines
- Include start/end dates
- Mention lane status
- Category-appropriate tone

### getDayDifference(date, nowTime)

Calculates day difference between construction start and current time.

**Purpose**: Provides temporal context for notification urgency
**Parameters**:
- `date` (string): Construction start date
- `nowTime` (string): Current timestamp

**Returns**: Number of days until construction begins

**Example**:
```javascript
const days = getDayDifference("2023-12-25", "2023-12-20");
// Returns: 5 (days until construction starts)
```

## Construction Categories

### Category 5 - Minor Impact
- **Tone**: Friendly reminder
- **Approach**: Gentle notification
- **Example**: "Hello! A friendly reminder about upcoming construction..."

### Category 3-4 - Moderate Impact
- **Tone**: Important reminder
- **Approach**: Advice on impact mitigation
- **Example**: "Important reminder: Construction may affect your route..."

### Category 1 - Major Impact
- **Tone**: Urgent attention
- **Approach**: Alternative route suggestions
- **Example**: "Immediate attention needed: Plan alternative routes..."

## Message Structure

### Required Elements
- Construction start date (formatted as "MMMM Do YYYY")
- Construction end date (formatted as "MMMM Do YYYY")
- Lane status information
- Event location details
- Time until event begins

### Content Guidelines
- Concise messaging under character limits
- No emoji or newline characters
- Clear, natural language
- Category-appropriate urgency level
- Actionable advice when applicable

## Integration Points

### Used By
- Notification scheduling systems
- Push notification services
- SMS/RCS messaging services
- Email notification systems

### External Dependencies
- **OpenAI API**: Message generation
- **Moment.js**: Date formatting and calculations
- **Axios**: HTTP requests with retry logic
- **@maas/core/log**: Error logging
- **Config**: OpenAI credentials and settings

## Error Handling

### API Failures
- Graceful fallback to original event information
- Comprehensive error logging
- Retry mechanism with delays
- Response validation

### Language Processing
- Default to English for unsupported languages
- Language code normalization (- to _)
- Fallback title generation

### Data Validation
- Event category validation
- Date format verification
- Message length enforcement
- Character limit compliance

## Technical Details

### AI Prompt Engineering
- System role definition for consistent output
- Context-rich prompts with temporal information
- Category-specific instruction sets
- Language-specific generation requests

### Date Handling
- Timezone-aware processing
- Human-readable date formatting
- Precise day difference calculations
- Moment.js integration for reliability

### Language Support
- Multi-language title mapping
- Dynamic language detection
- Localized message generation
- Cultural tone adaptation

## Performance Considerations

- **API Latency**: 10-second retry delays
- **Character Limits**: Enforced message constraints
- **Async Processing**: Non-blocking API calls
- **Error Recovery**: Fallback content available

## Security Considerations

- **API Key Management**: Loaded from secure configuration
- **Request Validation**: Input sanitization
- **Rate Limiting**: Handled by retry logic
- **Error Information**: Sensitive data filtered from logs

## Usage Guidelines

1. **Event Categories**: Use appropriate category for impact level
2. **Language Codes**: Provide standard language identifiers
3. **Time Context**: Include accurate current time for relevance
4. **Event Data**: Ensure complete location and lane information
5. **Error Handling**: Always check for API failures

## Dependencies

- **OpenAI API**: GPT-3.5-turbo model access
- **Moment.js**: Date manipulation and formatting
- **Axios**: HTTP client with retry capabilities
- **@maas/core/log**: Centralized logging
- **Config**: Application configuration management