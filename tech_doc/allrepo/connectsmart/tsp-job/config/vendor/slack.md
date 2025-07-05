# TSP Job Service - Slack Configuration

## Overview

The `config/vendor/slack.js` file manages Slack integration configuration for the TSP Job service's notification and alerting system. This configuration enables automated notifications, operational alerts, and team communication through dedicated Slack channels for different types of system events.

## File Information

- **File Path**: `/config/vendor/slack.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: Slack bot and webhook configuration for notifications
- **Dependencies**: Environment variables for Slack bot token and channel IDs

## Configuration Structure

```javascript
module.exports = {
  token: process.env.SLACK_BOT_TOKEN,
  channelId: process.env.SLACK_CHANNEL_ID,
  vendorFailedChannelId: process.env.SLACK_CHANNEL_ID_VENDOR_SERVICE_FAILED,
  vendorIncorrectChannelId: process.env.SLACK_CHANNEL_ID_VENDOR_INCORRECT_DATA,
};
```

## Configuration Components

### Bot Authentication
```javascript
token: process.env.SLACK_BOT_TOKEN
```

**Purpose**: Slack bot token for API authentication
- **Format**: `xoxb-` prefixed OAuth token
- **Permissions**: Required scopes for channel posting and user interaction
- **Security**: Environment-based token management

### Primary Channel Configuration
```javascript
channelId: process.env.SLACK_CHANNEL_ID
```

**Purpose**: Default channel for general system notifications
- **Use Cases**: System status updates, job completion notifications
- **Format**: Channel ID (e.g., `C1234567890`) or channel name (e.g., `#general`)
- **Audience**: Development and operations teams

### Vendor Service Failure Channel
```javascript
vendorFailedChannelId: process.env.SLACK_CHANNEL_ID_VENDOR_SERVICE_FAILED
```

**Purpose**: Dedicated channel for vendor service failure alerts
- **Use Cases**: API failures, service timeouts, authentication errors
- **Urgency**: High-priority alerts requiring immediate attention
- **Escalation**: Direct notification to on-call engineers

### Vendor Data Quality Channel
```javascript
vendorIncorrectChannelId: process.env.SLACK_CHANNEL_ID_VENDOR_INCORRECT_DATA
```

**Purpose**: Specialized channel for vendor data quality issues
- **Use Cases**: Inconsistent data, validation failures, data anomalies
- **Monitoring**: Data quality team notifications
- **Analysis**: Pattern detection for recurring data issues

## Slack Integration Implementation

### Slack Client Setup
```javascript
const { WebClient } = require('@slack/web-api');
const config = require('../config/vendor/slack');

const slack = new WebClient(config.token, {
  retryConfig: {
    retries: 3,
    factor: 2
  },
  timeout: 10000
});

class SlackNotificationService {
  static async sendMessage(channel, text, options = {}) {
    try {
      const result = await slack.chat.postMessage({
        channel: channel || config.channelId,
        text: text,
        ...options
      });
      
      return {
        success: true,
        timestamp: result.ts,
        channel: result.channel
      };
    } catch (error) {
      console.error('Slack message error:', error);
      throw error;
    }
  }
  
  static async sendRichMessage(channel, blocks, options = {}) {
    try {
      const result = await slack.chat.postMessage({
        channel: channel || config.channelId,
        blocks: blocks,
        text: options.fallbackText || 'System Notification',
        ...options
      });
      
      return {
        success: true,
        timestamp: result.ts,
        channel: result.channel
      };
    } catch (error) {
      console.error('Slack rich message error:', error);
      throw error;
    }
  }
  
  static async sendAlert(title, message, severity = 'info', additionalData = {}) {
    const color = this.getSeverityColor(severity);
    const channel = this.getChannelBySeverity(severity);
    
    const blocks = [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: title
        }
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: message
        }
      }
    ];
    
    if (Object.keys(additionalData).length > 0) {
      blocks.push({
        type: 'section',
        fields: Object.entries(additionalData).map(([key, value]) => ({
          type: 'mrkdwn',
          text: `*${key}:*\n${value}`
        }))
      });
    }
    
    blocks.push({
      type: 'context',
      elements: [
        {
          type: 'mrkdwn',
          text: `Severity: ${severity.toUpperCase()} | ${new Date().toISOString()}`
        }
      ]
    });
    
    return await this.sendRichMessage(channel, blocks, {
      attachments: [{
        color: color,
        fallback: `${title}: ${message}`
      }]
    });
  }
  
  static getSeverityColor(severity) {
    const colors = {
      'critical': '#FF0000',
      'error': '#FF6B6B',
      'warning': '#FFB347',
      'info': '#4A90E2',
      'success': '#5CB85C'
    };
    return colors[severity] || colors.info;
  }
  
  static getChannelBySeverity(severity) {
    if (['critical', 'error'].includes(severity)) {
      return config.vendorFailedChannelId;
    }
    return config.channelId;
  }
}
```

### Vendor Monitoring Integration
```javascript
class VendorMonitoringSlack {
  static async notifyVendorFailure(vendorName, service, error, metadata = {}) {
    const message = `🚨 *Vendor Service Failure*\n\n` +
      `*Vendor:* ${vendorName}\n` +
      `*Service:* ${service}\n` +
      `*Error:* ${error.message || error}\n` +
      `*Time:* ${new Date().toISOString()}`;
    
    const additionalData = {
      'Error Code': error.code || 'Unknown',
      'Request ID': metadata.requestId || 'N/A',
      'Retry Count': metadata.retryCount || 0,
      'Endpoint': metadata.endpoint || 'Unknown'
    };
    
    return await SlackNotificationService.sendAlert(
      `${vendorName} Service Failure`,
      message,
      'critical',
      additionalData
    );
  }
  
  static async notifyDataQualityIssue(vendorName, dataType, issue, sample = null) {
    const blocks = [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: `⚠️ Data Quality Issue - ${vendorName}`
        }
      },
      {
        type: 'section',
        fields: [
          {
            type: 'mrkdwn',
            text: `*Vendor:*\n${vendorName}`
          },
          {
            type: 'mrkdwn',
            text: `*Data Type:*\n${dataType}`
          },
          {
            type: 'mrkdwn',
            text: `*Issue:*\n${issue}`
          },
          {
            type: 'mrkdwn',
            text: `*Detected:*\n${new Date().toISOString()}`
          }
        ]
      }
    ];
    
    if (sample) {
      blocks.push({
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Sample Data:*\n\`\`\`${JSON.stringify(sample, null, 2)}\`\`\``
        }
      });
    }
    
    return await SlackNotificationService.sendRichMessage(
      config.vendorIncorrectChannelId,
      blocks
    );
  }
  
  static async notifyServiceRecovery(vendorName, service, downtime) {
    const message = `✅ *Service Recovered*\n\n` +
      `*Vendor:* ${vendorName}\n` +
      `*Service:* ${service}\n` +
      `*Downtime:* ${this.formatDuration(downtime)}\n` +
      `*Recovered:* ${new Date().toISOString()}`;
    
    return await SlackNotificationService.sendAlert(
      `${vendorName} Service Recovered`,
      message,
      'success'
    );
  }
  
  static formatDuration(milliseconds) {
    const seconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) {
      return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${seconds % 60}s`;
    } else {
      return `${seconds}s`;
    }
  }
}
```

### System Monitoring Integration
```javascript
class SystemMonitoringSlack {
  static async notifyJobCompletion(jobType, jobId, duration, success, results = {}) {
    const emoji = success ? '✅' : '❌';
    const status = success ? 'Completed' : 'Failed';
    
    const message = `${emoji} *Job ${status}*\n\n` +
      `*Type:* ${jobType}\n` +
      `*Job ID:* ${jobId}\n` +
      `*Duration:* ${this.formatDuration(duration)}\n` +
      `*Completed:* ${new Date().toISOString()}`;
    
    const additionalData = success ? {
      'Records Processed': results.recordsProcessed || 0,
      'Output Size': results.outputSize || 'N/A',
      'Success Rate': results.successRate ? `${results.successRate}%` : 'N/A'
    } : {
      'Error': results.error || 'Unknown error',
      'Failed At': results.failedAt || 'Unknown',
      'Retry Count': results.retryCount || 0
    };
    
    return await SlackNotificationService.sendAlert(
      `Job ${status}: ${jobType}`,
      message,
      success ? 'success' : 'error',
      additionalData
    );
  }
  
  static async notifySystemHealth(healthData) {
    const overallHealth = this.calculateOverallHealth(healthData);
    const emoji = this.getHealthEmoji(overallHealth);
    
    const blocks = [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: `${emoji} System Health Report`
        }
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Overall Status:* ${overallHealth.toUpperCase()}`
        }
      }
    ];
    
    // Add service status fields
    const serviceFields = Object.entries(healthData.services).map(([service, data]) => ({
      type: 'mrkdwn',
      text: `*${service}:*\n${data.status} (${data.latency}ms)`
    }));
    
    blocks.push({
      type: 'section',
      fields: serviceFields
    });
    
    return await SlackNotificationService.sendRichMessage(
      config.channelId,
      blocks
    );
  }
  
  static calculateOverallHealth(healthData) {
    const services = Object.values(healthData.services);
    const healthyCount = services.filter(s => s.status === 'healthy').length;
    const healthPercentage = (healthyCount / services.length) * 100;
    
    if (healthPercentage === 100) return 'healthy';
    if (healthPercentage >= 80) return 'degraded';
    return 'unhealthy';
  }
  
  static getHealthEmoji(health) {
    const emojis = {
      'healthy': '🟢',
      'degraded': '🟡',
      'unhealthy': '🔴'
    };
    return emojis[health] || '⚪';
  }
  
  static formatDuration(milliseconds) {
    return VendorMonitoringSlack.formatDuration(milliseconds);
  }
}
```

## Interactive Features

### Slack Commands
```javascript
class SlackCommandHandler {
  static async handleSystemStatus(command) {
    try {
      const healthData = await this.getSystemHealth();
      await SystemMonitoringSlack.notifySystemHealth(healthData);
      
      return {
        response_type: 'in_channel',
        text: 'System health report sent to channel'
      };
    } catch (error) {
      return {
        response_type: 'ephemeral',
        text: 'Failed to get system status'
      };
    }
  }
  
  static async handleVendorStatus(vendorName) {
    try {
      const vendorHealth = await this.getVendorHealth(vendorName);
      
      return {
        response_type: 'in_channel',
        blocks: [
          {
            type: 'section',
            text: {
              type: 'mrkdwn',
              text: `*${vendorName} Status:* ${vendorHealth.status}\n` +
                    `*Latency:* ${vendorHealth.latency}ms\n` +
                    `*Last Check:* ${vendorHealth.lastCheck}`
            }
          }
        ]
      };
    } catch (error) {
      return {
        response_type: 'ephemeral',
        text: `Failed to get status for vendor: ${vendorName}`
      };
    }
  }
}
```

### Error Handling and Resilience
```javascript
class ResilientSlackService {
  static async sendWithFallback(primaryMethod, fallbackText, options = {}) {
    try {
      return await primaryMethod();
    } catch (error) {
      console.error('Primary Slack method failed:', error);
      
      try {
        // Fallback to simple text message
        return await SlackNotificationService.sendMessage(
          options.fallbackChannel || config.channelId,
          fallbackText
        );
      } catch (fallbackError) {
        console.error('Slack fallback failed:', fallbackError);
        
        // Log to alternative notification system
        await this.logToAlternativeSystem({
          originalError: error,
          fallbackError: fallbackError,
          message: fallbackText
        });
        
        throw new Error('All Slack notification methods failed');
      }
    }
  }
  
  static async logToAlternativeSystem(errorData) {
    // Implement alternative logging/notification system
    console.error('Slack notification system failure:', errorData);
  }
}
```

This Slack configuration provides comprehensive notification and alerting capabilities for the TSP Job service, enabling real-time communication of system events, vendor issues, and operational status to appropriate team channels with rich formatting and interactive features.