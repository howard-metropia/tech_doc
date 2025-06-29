# Calendar Events Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates calendar event creation and updates for trip planning
- **Validation Library:** Joi
- **Related Controller:** calendar-events.js

### 🔧 Schema Structure
```javascript
// Position object for destinations
position: {
  name: string (optional),
  address: string (optional),
  latitude: number (required),
  longitude: number (required)
}

// Create multiple events
create: {
  events: array of event objects (required)
}

// Update single event
update: {
  uuid: string (required),
  title: string (optional),
  arrival_time: string (optional),
  destination: position (optional),
  reminder_time: number (optional, positive),
  platform: string (optional, 'iOS' or 'Android'),
  is_removed: boolean (optional)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| events | array | Yes | array of event objects | Multiple events for batch creation |
| uuid | string | Yes | - | Unique event identifier |
| title | string | Yes/No | allow empty string | Event title |
| arrival_time | string | Yes/No | - | Target arrival time |
| destination | object | Yes/No | position schema | Event location |
| reminder_time | number | Yes/No | positive number | Minutes before event |
| platform | string | Yes/No | 'iOS', 'Android' | Device platform |
| is_removed | boolean | Yes/No | - | Deletion flag |

### 💡 Usage Example
```javascript
// Create events request
{
  "events": [
    {
      "uuid": "event-123",
      "title": "Doctor Appointment",
      "arrival_time": "2024-01-15T10:00:00Z",
      "destination": {
        "name": "Medical Center",
        "address": "123 Health St",
        "latitude": 40.7128,
        "longitude": -74.0060
      },
      "reminder_time": 30,
      "platform": "iOS",
      "is_removed": false
    }
  ]
}

// Update event request
{
  "uuid": "event-123",
  "title": "Updated Appointment",
  "reminder_time": 15,
  "platform": "Android"
}

// Invalid request - missing required field
{
  "events": [
    {
      "title": "Test", // Error: uuid required
      "arrival_time": "invalid-date"
    }
  ]
}
```

### ⚠️ Important Validations
- Create operation requires array of complete event objects
- All event objects in create must have uuid, title, arrival_time, destination, reminder_time, platform, and is_removed
- Update operation only requires uuid, all other fields are optional
- Reminder time must be positive number
- Platform must be exactly 'iOS' or 'Android' for updates
- Title can be empty string but not null

### 🏷️ Tags
**Keywords:** calendar, events, appointments, reminders, scheduling
**Category:** #schema #validation #joi #calendar-events