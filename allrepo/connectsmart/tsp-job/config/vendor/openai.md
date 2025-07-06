# OpenAI Configuration Documentation

## Quick Summary

This configuration module provides the essential credentials and endpoint settings for integrating OpenAI's API services into the TSP Job system. It manages API key authentication and endpoint configuration for accessing OpenAI's GPT models, enabling AI-powered features such as natural language processing, trip analysis, and intelligent automation within the transportation service provider platform.

## Technical Analysis

### Code Structure

```javascript
module.exports = {
  apiKey: process.env.OPENAI_API_KEY || '[REDACTED]',
  apiUrl: process.env.OPENAI_URL || 'https://api.openai.com/v1/chat/completions',
};
```

### Configuration Properties

1. **apiKey**: Authentication token for OpenAI API access
   - Sources from `OPENAI_API_KEY` environment variable
   - Falls back to hardcoded default key (security consideration)
   - Used for Bearer token authentication in API requests

2. **apiUrl**: OpenAI API endpoint URL
   - Sources from `OPENAI_URL` environment variable
   - Defaults to chat completions endpoint
   - Supports API version v1 chat interface

### Environment Variable Integration

The module prioritizes environment variables over default values, following the twelve-factor app methodology:
- `OPENAI_API_KEY`: Production API key should be set via environment
- `OPENAI_URL`: Allows endpoint customization for different environments

## Usage/Integration

### Loading Configuration

```javascript
const openaiConfig = require('./config/vendor/openai');

// Access configuration values
const apiKey = openaiConfig.apiKey;
const apiUrl = openaiConfig.apiUrl;
```

### API Request Implementation

```javascript
const axios = require('axios');
const openaiConfig = require('./config/vendor/openai');

async function generateCompletion(prompt) {
  const response = await axios.post(openaiConfig.apiUrl, {
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.7
  }, {
    headers: {
      'Authorization': `Bearer ${openaiConfig.apiKey}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.data.choices[0].message.content;
}
```

### Integration Points

1. **AI Log Helper** (`helpers/ai-log.js`): Uses this configuration for logging AI interactions
2. **Trip Analysis**: Processes natural language trip descriptions
3. **User Query Processing**: Handles intelligent query responses
4. **Automated Content Generation**: Creates dynamic notifications and alerts

## Dependencies

### Internal Dependencies
- Used by AI-related helpers and services
- Referenced in job processors requiring AI capabilities
- Integrated with logging and monitoring systems

### External Dependencies
- **OpenAI API**: Requires active API subscription
- **axios/fetch**: HTTP client for API requests
- **Environment Configuration**: Relies on proper environment setup

### Security Considerations

1. **API Key Management**:
   - Production keys should never be hardcoded
   - Use environment variables or secure key management systems
   - Rotate keys regularly according to security policies

2. **Rate Limiting**:
   - OpenAI enforces rate limits per API key
   - Implement retry logic with exponential backoff
   - Monitor usage to avoid quota exhaustion

3. **Error Handling**:
   ```javascript
   try {
     const response = await makeOpenAIRequest();
   } catch (error) {
     if (error.response?.status === 429) {
       // Handle rate limiting
     } else if (error.response?.status === 401) {
       // Handle authentication errors
     }
   }
   ```

## Code Examples

### Basic Configuration Usage

```javascript
// Load configuration
const { apiKey, apiUrl } = require('./config/vendor/openai');

// Validate configuration
if (!apiKey || apiKey.startsWith('sk-')) {
  console.warn('OpenAI API key may be invalid or missing');
}
```

### Advanced Integration Pattern

```javascript
class OpenAIService {
  constructor() {
    this.config = require('./config/vendor/openai');
    this.client = this.initializeClient();
  }

  initializeClient() {
    return {
      apiKey: this.config.apiKey,
      apiUrl: this.config.apiUrl,
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json'
      }
    };
  }

  async analyzeTrip(tripData) {
    const prompt = `Analyze this trip data and provide insights: ${JSON.stringify(tripData)}`;
    
    const response = await fetch(this.config.apiUrl, {
      method: 'POST',
      headers: this.client.headers,
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 150
      })
    });

    return response.json();
  }
}
```

### Environment-Specific Configuration

```javascript
// Development environment setup
if (process.env.NODE_ENV === 'development') {
  process.env.OPENAI_API_KEY = process.env.DEV_OPENAI_KEY;
  process.env.OPENAI_URL = 'https://api.openai.com/v1/chat/completions';
}

// Production environment validation
if (process.env.NODE_ENV === 'production' && !process.env.OPENAI_API_KEY) {
  throw new Error('OPENAI_API_KEY must be set in production');
}
```

### Error Handling and Retry Logic

```javascript
const openaiConfig = require('./config/vendor/openai');

async function makeOpenAIRequestWithRetry(requestData, maxRetries = 3) {
  let lastError;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch(openaiConfig.apiUrl, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${openaiConfig.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });

      if (!response.ok) {
        throw new Error(`OpenAI API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      lastError = error;
      
      // Exponential backoff
      const delay = Math.pow(2, attempt) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError;
}
```

## Best Practices

1. **Environment Variable Management**:
   - Always use environment variables in production
   - Document required environment variables
   - Validate configuration on application startup

2. **Security**:
   - Never commit API keys to version control
   - Use secret management tools in production
   - Implement API key rotation procedures

3. **Error Handling**:
   - Implement comprehensive error handling
   - Log API errors for monitoring
   - Provide fallback mechanisms for API failures

4. **Performance**:
   - Cache API responses when appropriate
   - Implement request batching for efficiency
   - Monitor API usage and costs

This configuration module serves as the foundation for all OpenAI integrations within the TSP Job system, enabling intelligent features while maintaining security and flexibility across different deployment environments.