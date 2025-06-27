# UberFareEstimation Model

## 📋 Model Overview
- **Purpose:** Stores Uber fare estimates for ridehail pricing calculations
- **Table/Collection:** uber_fare_est
- **Database Type:** MongoDB (cache)
- **Relationships:** None defined

## 🔧 Schema Definition
- **product_id** | **String** | **Optional** | **Uber product identifier**
- **product_display** | **String** | **Optional** | **Product display name**
- **fare_id** | **String** | **Optional** | **Fare identifier**
- **fare_display** | **String** | **Optional** | **Fare display name**
- **fare_value** | **Number** | **Optional** | **Fare amount**
- **fare_currency** | **String** | **Optional** | **Currency code**
- **pickup_eta** | **Number** | **Optional** | **Pickup ETA in seconds**
- **trip_duration** | **Number** | **Optional** | **Trip duration in seconds**
- **no_cars_available** | **String** | **Optional** | **Availability status**
- **modified_at** | **Date** | **Optional** | **Last modification timestamp**

## 🔑 Key Information
- **Primary Key:** MongoDB ObjectId
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** modified_at: Date.now

## 📝 Usage Examples
```javascript
// Create fare estimation
const fareEst = new UberFareEstimation({
  product_id: 'uber_x',
  fare_value: 15.50,
  fare_currency: 'USD',
  pickup_eta: 300
});
await fareEst.save();

// Find fare estimates
const estimates = await UberFareEstimation.find({ product_id: 'uber_x' });
```

## 🔗 Related Models
- No explicit relationships defined
- Used for ridehail fare calculations

## 📌 Important Notes
- MongoDB document with flexible schema
- Caches Uber API fare estimation responses
- Used for real-time pricing in ridehail services
- Automatically tracks modification timestamps

## 🏷️ Tags
**Keywords:** uber, fare, estimation, ridehail, pricing
**Category:** #model #database #uber #fare #ridehail #mongodb