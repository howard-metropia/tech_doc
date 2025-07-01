# CalendarEvents Model Documentation

## 📋 Model Overview
- **Purpose:** Manages user calendar events with destination and reminder functionality
- **Table/Collection:** calendar_events
- **Database Type:** MongoDB
- **Relationships:** References users and location data

## 🔧 Schema Definition

### Main Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| uuid | String | No | Unique event identifier (Android/iOS) |
| userId | String | No | User who owns the event |
| title | String | No | Event title/name |
| arrival_time | Date | No | UTC arrival time (ISO format) |
| destination | Object | No | Event location details |
| reminder_time | Number | No | Reminder timestamp |
| platform | String | No | Platform (Android or iOS) |
| is_removed | Boolean | No | User deletion status |

### Destination Object Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| name | String | No | Location name |
| address | String | No | Full address |
| latitude | Number | No | Latitude coordinate |
| longitude | Number | No | Longitude coordinate |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** Text index on uuid field
- **Unique Constraints:** None
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Create calendar event
const event = new CalendarEvents({
  uuid: 'event_uuid_123',
  userId: 'user_456',
  title: 'Doctor Appointment',
  arrival_time: new Date('2024-06-25T14:00:00Z'),
  destination: {
    name: 'Medical Center',
    address: '123 Health St',
    latitude: 37.7749,
    longitude: -122.4194
  },
  reminder_time: Date.now() + 3600000, // 1 hour reminder
  platform: 'iOS',
  is_removed: false
});
await event.save();

// Get upcoming events for user
const upcomingEvents = await CalendarEvents.find({
  userId: userId,
  arrival_time: { $gte: new Date() },
  is_removed: false
}).sort({ arrival_time: 1 });

// Mark event as removed
await CalendarEvents.updateOne(
  { uuid: eventUuid },
  { is_removed: true }
);
```

## 🔗 Related Models
- **AuthUsers**: Events belong to specific users
- **Notifications**: Reminder system may trigger notifications
- **TripPlanning**: Events can be used for trip planning

## 📌 Important Notes
- Cross-platform support (Android/iOS) with different UUID formats
- UTC time format for consistent scheduling
- Soft delete pattern with is_removed flag
- Geographic destination data for location-based features
- Text search capability on UUID field

## 🏷️ Tags
**Keywords:** calendar, events, reminders, scheduling, cross-platform
**Category:** #model #database #calendar #scheduling