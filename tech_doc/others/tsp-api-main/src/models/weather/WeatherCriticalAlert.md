# WeatherCriticalAlert Model

## 📋 Model Overview
- **Purpose:** Manages critical weather alerts that impact transportation services
- **Table/Collection:** weather_critical_alert
- **Database Type:** MongoDB (cache)
- **Relationships:** None defined

## 🔧 Schema Definition
- **alert_id** | **String** | **Optional** | **Unique alert identifier**
- **start_at** | **Date** | **Optional** | **Alert start time**
- **end_at** | **Date** | **Optional** | **Alert end time**
- **impacted_area** | **Array** | **Optional** | **List of impacted geographic areas**
- **geometry** | **Object** | **Optional** | **Geographic boundary data**
- **properties** | **Object** | **Optional** | **Additional alert properties**

## 🔑 Key Information
- **Primary Key:** MongoDB ObjectId
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Create critical weather alert
const alert = new WeatherCriticalAlert({
  alert_id: 'ALERT_123',
  start_at: new Date(),
  end_at: new Date(Date.now() + 24*60*60*1000),
  impacted_area: ['GRID_1', 'GRID_2'],
  properties: { severity: 'high', type: 'storm' }
});
await alert.save();

// Find active alerts
const activeAlerts = await WeatherCriticalAlert.find({
  start_at: { $lte: new Date() },
  end_at: { $gte: new Date() }
});
```

## 🔗 Related Models
- WeatherGrids - Related through impacted_area
- Part of weather monitoring and alert system

## 📌 Important Notes
- Critical alerts for transportation impact assessment
- Flexible geometry and properties for various alert types
- Cache database for real-time alert processing
- Used for service disruption notifications

## 🏷️ Tags
**Keywords:** weather, critical, alert, impact, transportation
**Category:** #model #database #weather #alert #critical #mongodb