# InstantCarpoolings Model

## 📋 Model Overview
- **Purpose:** Manages instant carpool matching and trip coordination between drivers and riders
- **Table/Collection:** instant_carpoolings
- **Database Type:** MongoDB (cache)
- **Relationships:** None defined

## 🔧 Schema Definition
- **driver** | **Object** | **Optional** | **Driver user information and trip details**
- **riders** | **Array** | **Optional** | **Array of rider user information**
- **origin** | **Object** | **Optional** | **Trip origin location details**
- **destination** | **Object** | **Optional** | **Trip destination location**
- **finalDestination** | **Object** | **Optional** | **Final destination location**
- **travelTime** | **Number** | **Optional** | **Travel time in seconds**
- **etaOnStart** | **Number** | **Optional** | **ETA timestamp at trip start**
- **etaOnEnd** | **Number** | **Optional** | **ETA timestamp at trip end**
- **createdAt** | **Date** | **Auto** | **Record creation timestamp**
- **updatedAt** | **Date** | **Auto** | **Record update timestamp**

### User Schema (driver/riders)
- **userId** | **Number** | **Optional** | **User identifier**
- **tripId** | **Number** | **Optional** | **Trip identifier**
- **status** | **String** | **Optional** | **Trip status**
- **rating** | **String** | **Optional** | **User rating**
- **feedback** | **String** | **Optional** | **Trip feedback**
- **distance** | **Number** | **Optional** | **Distance traveled**
- **endType** | **String** | **Optional** | **Trip end type**
- **startAt** | **Date** | **Optional** | **Trip start time**
- **endAt** | **Date** | **Optional** | **Trip end time**
- **verifyResult** | **Boolean** | **Optional** | **Trip verification status**
- **isTimePassed** | **Boolean** | **Optional** | **Time validity flag**
- **trajectoryScore** | **Number** | **Optional** | **Trip trajectory score**

### Position Schema (origin/destination/finalDestination)
- **name** | **String** | **Optional** | **Location name**
- **address** | **String** | **Optional** | **Location address**
- **access_latitude** | **Number** | **Optional** | **Access point latitude**
- **access_longitude** | **Number** | **Optional** | **Access point longitude**
- **latitude** | **Number** | **Optional** | **Location latitude**
- **longitude** | **Number** | **Optional** | **Location longitude**

## 🔑 Key Information
- **Primary Key:** MongoDB ObjectId
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** Automatic timestamps

## 📝 Usage Examples
```javascript
// Create instant carpool
const carpool = new InstantCarpoolings({
  driver: {
    userId: 123,
    status: 'active'
  },
  riders: [{
    userId: 456,
    status: 'matched'
  }],
  origin: {
    name: 'Downtown',
    latitude: 29.7604,
    longitude: -95.3698
  },
  travelTime: 1800
});
await carpool.save();

// Find active carpools
const activePools = await InstantCarpoolings.find({ 'driver.status': 'active' });
```

## 🔗 Related Models
- No explicit relationships defined
- References user data through userId fields

## 📌 Important Notes
- Complex nested schema for comprehensive carpool data
- Supports multiple riders per driver
- Tracks verification and scoring for trip quality
- Includes detailed location and timing information
- Automatic timestamp management

## 🏷️ Tags
**Keywords:** carpool, instant, matching, driver, rider, trip
**Category:** #model #database #carpool #trip #matching #mongodb