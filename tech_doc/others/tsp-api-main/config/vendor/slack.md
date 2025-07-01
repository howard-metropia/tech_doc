# Slack Integration Configuration

### 📋 Configuration Overview
- **Purpose:** Configures Slack bot integration for automated notifications and alerts
- **Module Type:** Service credentials and channel configuration
- **Environment:** All environments (dev/staging/prod)

### 🔧 Configuration Values
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `parkingDataAccuracyWarningUrl` | String | No | Slack webhook URL for parking data accuracy warnings | `process.env.SLACK_ALARM_PARKING_NOTIFY` |
| `token` | String | Yes | Slack bot token for API authentication | `process.env.SLACK_BOT_TOKEN` |
| `channelId` | String | No | Default Slack channel ID for general notifications | `'C0500872XUY'` |
| `vendorFailedChannelId` | String | No | Channel ID for vendor service failure alerts | `'C042ZB2HMEG'` |
| `vendorIncorrectChannelId` | String | No | Channel ID for vendor data accuracy issues | `'C0406DX0AGL'` |

### 📝 Usage Example
```javascript
// How to import and use this configuration
const slackConfig = require('./config/vendor/slack');

// Send notification to default channel
const response = await axios.post('https://slack.com/api/chat.postMessage', {
  channel: slackConfig.channelId,
  text: 'System notification message'
}, {
  headers: {
    'Authorization': `Bearer ${slackConfig.token}`
  }
});

// Send vendor failure alert to specific channel
await notifyChannel(slackConfig.vendorFailedChannelId, 'Vendor service is down');
```

### ⚠️ Security Notes
- **Sensitive Data:** `SLACK_BOT_TOKEN` contains authentication credentials and must be protected
- **Environment Management:** All tokens should be stored in environment variables
- **Access Control:** Bot token should have minimal required permissions (channels:write, chat:write)
- **Channel Security:** Verify channel IDs are correct to prevent information leakage

### 🏷️ Tags
**Keywords:** slack, notifications, alerts, bot-integration, monitoring, webhooks  
**Category:** #config #vendor #credentials #slack #notifications

---
Note: Ensure Slack bot has appropriate permissions and channel access configured properly.