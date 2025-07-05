# Weather Service

## Overview

The Weather service generates AI-powered weather alert notifications using OpenAI's GPT-3.5 API, creating localized and contextual weather warnings for mobile app users with precise formatting and multilingual support.

## Service Information

- **Service Name**: Weather
- **File Path**: `/src/services/weather.js`
- **Type**: AI-Powered Weather Notification Service
- **Dependencies**: OpenAI API, Moment.js, Axios

## Configuration

### OpenAI Integration
- **Model**: GPT-3.5-turbo
- **System Role**: "trip adviser" for travel-focused messaging
- **API Configuration**: Loaded from config.vendor.openai
- **Character Limit**: Defined in weather configuration

### Timezone Settings
- **Primary Timezone**: US/Central for weather event times
- **Local Time Format**: Human-readable format for users
- **Date Display**: "MMMM Do YYYY" and "YYYY-MM-DD h A" formats

## Functions

### getAIMessage(eventInfos, language, currentDatetime)

Generates AI-powered weather alert messages with structured formatting.

**Purpose**: Creates localized weather notifications with precise formatting rules
**Parameters**:
- `eventInfos` (array): Weather event objects with details
- `language` (string): User's preferred language code
- `currentDatetime` (string): Current timestamp for context

**Returns**: Object with title, body, prompt, and original message

**Message Structure**:
- **Title**: Event type (e.g., "Hurricane Warning!")
- **Separator**: "__" between title and body
- **Body**: Detailed message under character limit
- **Format**: No emojis, no line breaks, location-specific

**Single Event Format**:
```javascript
// Input
const eventInfos = [{
  event: "Hurricane Warning",
  instruction: "Seek shelter immediately",
  loc_name: ["Houston", "Harris County"],
  start: "2023-12-25T10:00:00Z"
}];

// Output
{
  title: "Hurricane Warning!",
  body: "Seek shelter immediately. Hurricane affecting Houston, Harris County starting December 25th at 4 AM.",
  prompt: "...", // Full AI prompt
  origin_message: "Hurricane Warning!__Seek shelter immediately..."
}
```

## Message Generation Rules

### Content Requirements
- **Character Limit**: Enforced based on weather configuration
- **Location Mention**: Must include event location names
- **Time Specification**: Human-readable start time with timezone
- **Instruction Integration**: One sentence from official instructions
- **Tone Adjustment**: Based on event timing (upcoming/ongoing/started)

### Format Restrictions
- **No Emojis**: Strict emoji prohibition
- **No Line breaks**: Single line message body
- **Separator**: "__" between title and body
- **Language**: Localized based on user preference

### Multiple Events Handling
- Processes multiple weather events in single notification
- Combines event information into comprehensive alert
- Maintains individual event details and timing

## Event Data Structure

### Required Fields
- **event** (string): Weather event type
- **instruction** (string): Official weather service instructions
- **loc_name** (array): Array of affected location names
- **start** (string): Event start time in ISO format

### Location Processing
- Joins multiple location names with newlines in prompt
- Displays all affected areas in notification
- Prioritizes primary location names

### Time Processing
- Converts UTC times to US/Central timezone
- Formats for human readability
- Adjusts messaging tone based on temporal context

## Language Support

### Supported Languages
- Uses DEFINES.language mapping for localization
- Defaults to English for unsupported languages
- Handles language code variations (- to _ conversion)

### Localization Features
- AI-generated content in target language
- Culturally appropriate messaging tone
- Timezone-aware date formatting

## Integration Points

### Used By
- Weather alert notification systems
- Push notification services
- Emergency alert systems
- Travel advisory services

### External Dependencies
- **OpenAI API**: AI message generation
- **Moment.js**: Date/time manipulation and timezone conversion
- **Axios**: HTTP requests for API communication
- **Config**: OpenAI credentials and weather settings

## Error Handling

### API Failures
- Comprehensive error logging with request/response details
- Exception propagation for upstream handling
- Request metadata preservation
- Structured error responses

### Data Validation
- Event information validation
- Language code normalization
- Timezone conversion error handling
- Character limit enforcement

### Logging
- Detailed prompt and response logging
- API call tracking
- Error context preservation
- Performance monitoring

## Technical Details

### AI Prompt Engineering
- Role-based system prompts for consistency
- Context-rich prompts with current time
- Detailed formatting instructions
- Event-specific content guidelines

### Response Processing
- Separator-based title/body extraction
- Newline character removal
- Original message preservation
- Structured response formatting

### Timezone Management
- US/Central default for weather events
- Moment.js timezone conversion
- Human-readable time formatting
- Daylight saving time handling

## Performance Considerations

- **API Latency**: Dependent on OpenAI response times
- **Character Limits**: Enforced for optimal mobile display
- **Batch Processing**: Single API call for multiple events
- **Error Recovery**: Graceful degradation on API failures

## Security Considerations

- **API Key Management**: Secure configuration loading
- **Input Validation**: Event data sanitization
- **Error Information**: Filtered sensitive data in logs
- **Rate Limiting**: Managed through OpenAI API limits

## Usage Guidelines

1. **Event Data**: Provide complete event information including instructions
2. **Language Codes**: Use standard language identifiers
3. **Timing**: Include accurate current datetime for context
4. **Character Limits**: Monitor message length constraints
5. **Error Handling**: Implement fallback for API failures

## Dependencies

- **OpenAI API**: GPT-3.5-turbo model for message generation
- **Moment.js**: Date manipulation and timezone conversion
- **Axios**: HTTP client for API communication
- **Config**: Application configuration management
- **@maas/core/log**: Centralized logging system