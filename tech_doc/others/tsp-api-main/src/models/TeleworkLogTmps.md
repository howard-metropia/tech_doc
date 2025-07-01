# TeleworkLogTmps Model

## 📋 Model Overview
- **Purpose:** Stores temporary telework log data for processing and analysis
- **Table/Collection:** telework_log_tmp
- **Database Type:** MongoDB (cache)
- **Relationships:** None defined

## 🔧 Schema Definition
- **id** | **Number** | **Optional** | **Log entry identifier**
- **origin_name** | **String** | **Optional** | **Origin location name**
- **origin_address** | **String** | **Optional** | **Origin location address**
- **started_on** | **Date** | **Optional** | **Telework session start time**
- **[dynamic fields]** | **Mixed** | **Optional** | **Flexible schema allows additional fields**

## 🔑 Key Information
- **Primary Key:** MongoDB ObjectId
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Create telework log entry
const logEntry = new TeleworkLogTmps({
  id: 12345,
  origin_name: 'Home Office',
  origin_address: '123 Main St',
  started_on: new Date()
});
await logEntry.save();

// Find logs by date range
const recentLogs = await TeleworkLogTmps.find({
  started_on: { $gte: new Date('2023-01-01') }
});
```

## 🔗 Related Models
- No explicit relationships defined
- Part of telework tracking system

## 📌 Important Notes
- Uses flexible schema (strict: false) for dynamic data structure
- Temporary storage for processing telework data
- Exported as part of an object { TeleworkLogTmps }
- Cache database for temporary data storage

## 🏷️ Tags
**Keywords:** telework, log, temporary, remote, work
**Category:** #model #database #telework #temporary #cache #mongodb