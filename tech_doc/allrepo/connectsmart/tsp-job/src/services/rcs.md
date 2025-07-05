# RCS Service

## Overview

The RCS (Rich Communication Services) service handles Rich Business Messaging (RBM) for Google to send enhanced notifications with rich content, images, and interactive elements to users' mobile devices.

## Service Information

- **Service Name**: RCS
- **File Path**: `/src/services/rcs.js`
- **Type**: Communication Service
- **Dependencies**: Google RCS Business Messaging API, Google Maps Static API

## Configuration

### API Setup
- **Private Key**: Uses Google Cloud service account credentials
- **Agent ID**: `houston_connectsmart_0mioumo5_agent`
- **Service Account**: `gbc-metropia-7yktmzu-0ae4699589cf.json`

### External APIs
- **Google RCS Business Messaging**: For rich message delivery
- **Google Maps Static API**: For generating map images
- **API Key**: `AIzaSyAG8WRGnb__gThAv9Dln5O59HkEvcO_7EU`

## Functions

### sendRCSMessage(payload)

Sends rich card messages via Google RCS Business Messaging.

**Purpose**: Delivers enhanced notifications with text, images, and geographic information
**Parameters**:
- `payload.phone_number` (string): Recipient's phone number in international format
- `payload.title` (string): Message title/header text
- `payload.body` (string): Message description/body content
- `payload.polygon` (array): Optional polygon coordinates for map visualization
- `payload.user_id` (string): User identifier for logging

**Returns**: Promise (async function)

**Rich Card Features**:
- Message text and description
- Dynamic map image generation
- Tall card height for enhanced visibility
- Interactive rich content support

**Example**:
```javascript
const payload = {
  phone_number: "+1234567890",
  title: "Traffic Alert",
  body: "Construction detected on your route",
  polygon: [[lat1, lng1], [lat2, lng2], ...],
  user_id: "user123"
};
await sendRCSMessage(payload);
```

### addImpactedAreaOnGoogleMap(data)

Generates Google Maps Static API URLs with polygon overlays.

**Purpose**: Creates map images showing impacted areas with visual overlays
**Parameters**:
- `data.polygon` (array): Array of coordinate pairs [longitude, latitude]

**Returns**: Google Maps Static API URL string

**Map Configuration**:
- **Center**: Houston, TX coordinates (29.756304374689236, -95.36267221950618)
- **Zoom Level**: 12
- **Image Size**: 600x300 pixels
- **Polygon Style**: Red color with transparency and weight

**Polygon Styling**:
- Border Color: `0xff000077` (red with transparency)
- Fill Color: `0xFF000033` (red with lower transparency)
- Border Weight: 5 pixels
- Path Color: `ff0000ff` (solid red)

**Example**:
```javascript
const data = {
  polygon: [[-95.123, 29.456], [-95.234, 29.567], [-95.345, 29.678]]
};
const mapUrl = addImpactedAreaOnGoogleMap(data);
// Returns: Full Google Maps Static API URL with polygon overlay
```

## Integration Points

### Used By
- Notification services for traffic alerts
- Construction zone notifications
- Emergency alert systems
- Transit disruption notifications

### External Dependencies
- **Google RCS Business Messaging API**: Message delivery
- **Google Maps Static API**: Map image generation
- **@google/rcsbusinessmessaging**: RBM SDK
- **@maas/core/log**: Logging infrastructure

## Message Flow

1. **Payload Processing**: Validates and extracts message data
2. **Map Generation**: Creates map URL if polygon data exists
3. **Rich Card Assembly**: Combines text, description, and image
4. **RCS Delivery**: Sends via Google RBM API
5. **Response Handling**: Logs success/failure status

## Error Handling

### API Errors
- Catches RBM API communication failures
- Logs user-specific error information
- Graceful degradation for map generation failures

### Validation
- Validates phone number format
- Handles missing polygon data gracefully
- Validates message content before sending

### Logging
- Success confirmations with response status
- Detailed error logging with user context
- API response tracking for debugging

## Technical Details

### RCS Business Messaging
- Uses official Google RBM SDK
- Supports rich card format with images
- Handles asynchronous message delivery
- Provides delivery status callbacks

### Map Integration
- Dynamic polygon rendering on maps
- Houston-centric default positioning
- Customizable styling and colors
- Optimized image size for mobile devices

### Phone Number Handling
- Supports international format with country codes
- MSISDN format compatibility
- Validation through RBM API

## Security Considerations

- **Service Account**: Secure credential management
- **API Keys**: Hardcoded but environment-specific
- **Phone Privacy**: No storage of phone numbers
- **Message Content**: No sensitive data logging

## Performance Optimization

- **Async Processing**: Non-blocking message delivery
- **Image Caching**: Static map URLs enable browser caching
- **Error Isolation**: Failures don't affect other services
- **Minimal Dependencies**: Lightweight Google SDK usage

## Usage Guidelines

1. **Message Content**: Keep titles concise, descriptions informative
2. **Polygon Data**: Provide coordinates in [longitude, latitude] format
3. **Phone Numbers**: Use international format with country code
4. **Error Monitoring**: Check logs for delivery failures
5. **Map Overlays**: Ensure polygon coordinates are within reasonable bounds

## Dependencies

- **@google/rcsbusinessmessaging**: Google RBM SDK
- **@maas/core/log**: Centralized logging
- **Google Cloud Service Account**: Authentication
- **Google Maps Static API**: Map image generation