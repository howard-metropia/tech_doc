# TSP Job: Truck Map Sync

## Quick Summary

The `truck.js` job synchronizes truck routing restriction data from AWS S3 to MongoDB, managing vertical clearance information for commercial vehicle navigation. This job processes JSON-formatted truck map data containing height restrictions, bridge clearances, and road segment limitations. It's essential for maintaining accurate routing information that prevents commercial vehicles from encountering impassable routes due to height restrictions or other truck-specific limitations.

## Technical Analysis

### Job Structure

The job accepts JSON content as input and delegates processing to a dedicated service:

```javascript
const { TruckMapService } = require('@app/src/services/TruckService');
const truckMapService = new TruckMapService();

module.exports = {
  inputs: {
    truckMapJsonContent: String,
  },
  fn: async function (truckMapJsonContent) {
    await truckMapService.syncTruckMapFromS3ToMongoDb(truckMapJsonContent);
  },
};
```

### Data Format

The input JSON contains truck routing restrictions:

```javascript
{
  "last_modified": 1682585343,
  "truck_map_array": [
    {
      "max_height": 18,        // Maximum clearance in feet
      "min_height": 16,        // Minimum clearance in feet
      "present_word": "Vertical clearance between",
      "segment_id": 412633298, // Road segment identifier
      "link_id": 17804935      // Navigation link ID
    },
    {
      "max_height": 16,
      "min_height": 14,
      "present_word": "Vertical clearance between",
      "segment_id": 408493889,
      "link_id": 17807233
    }
  ]
}
```

### Key Components

1. **Height Restrictions**: Min/max vertical clearances for bridges and overpasses
2. **Segment Mapping**: Links restrictions to specific road segments
3. **Timestamp Tracking**: Maintains data freshness with last_modified timestamp
4. **Batch Processing**: Handles arrays of restrictions efficiently

## Usage/Integration

### Job Invocation

The job is designed to be triggered when new truck map data is available:

```javascript
// Manual execution with truck map data
const truckJob = require('./truck');
const truckMapData = {
  last_modified: Date.now() / 1000,
  truck_map_array: [
    {
      max_height: 15,
      min_height: 13,
      present_word: "Vertical clearance between",
      segment_id: 123456789,
      link_id: 987654321
    }
  ]
};

await truckJob.fn(JSON.stringify(truckMapData));
```

### S3 Integration Pattern

This job typically works with an S3 event-driven architecture:

```javascript
// S3 event trigger configuration
{
  "event": "s3:ObjectCreated:*",
  "bucket": "truck-routing-data",
  "prefix": "clearances/",
  "suffix": ".json",
  "job": "truck",
  "parseContent": true
}
```

### MongoDB Storage Strategy

The service likely implements:
- **Bulk Updates**: Efficient batch processing of restrictions
- **Index Management**: Optimized queries on segment_id and link_id
- **Version Control**: Tracking data versions via last_modified
- **Atomic Updates**: Ensuring data consistency during sync

## Dependencies

### Core Services
- **@app/src/services/TruckService**: Contains sync logic and data validation
- **MongoDB**: Primary storage for truck routing restrictions
- **AWS S3**: Source of truck map data files

### Data Integration
- **Navigation System**: Consumes truck restrictions for route planning
- **Map Services**: Integrates with HERE/Google Maps for visualization
- **Alert System**: Notifies about new restrictions or changes

### Configuration Requirements

Expected service configuration:

```javascript
{
  mongodb: {
    collection: 'truck_restrictions',
    database: 'routing'
  },
  s3: {
    bucket: 'truck-routing-data',
    region: 'us-east-1'
  },
  validation: {
    maxHeightLimit: 30,    // Maximum allowed height in feet
    minHeightLimit: 8      // Minimum valid height
  }
}
```

## Code Examples

### Service Implementation Pattern

```javascript
// Expected TruckMapService implementation
class TruckMapService {
  async syncTruckMapFromS3ToMongoDb(jsonContent) {
    const data = JSON.parse(jsonContent);
    
    // Validate data structure
    this.validateTruckMapData(data);
    
    // Prepare bulk operations
    const bulkOps = data.truck_map_array.map(restriction => ({
      updateOne: {
        filter: { 
          segment_id: restriction.segment_id,
          link_id: restriction.link_id 
        },
        update: {
          $set: {
            ...restriction,
            last_modified: data.last_modified,
            updated_at: new Date()
          }
        },
        upsert: true
      }
    }));
    
    // Execute bulk update
    const result = await this.collection.bulkWrite(bulkOps);
    
    logger.info('Truck map sync completed', {
      modified: result.modifiedCount,
      upserted: result.upsertedCount,
      timestamp: data.last_modified
    });
    
    return result;
  }
  
  validateTruckMapData(data) {
    if (!data.truck_map_array || !Array.isArray(data.truck_map_array)) {
      throw new Error('Invalid truck map data: missing truck_map_array');
    }
    
    data.truck_map_array.forEach((restriction, index) => {
      if (!restriction.segment_id || !restriction.link_id) {
        throw new Error(`Invalid restriction at index ${index}: missing IDs`);
      }
      
      if (restriction.max_height < restriction.min_height) {
        throw new Error(`Invalid height range at index ${index}`);
      }
    });
  }
}
```

### Enhanced Processing with Validation

```javascript
// Advanced validation and processing
const processTruckRestrictions = async (restrictions) => {
  const processed = [];
  const errors = [];
  
  for (const restriction of restrictions) {
    try {
      // Validate height values
      if (restriction.max_height > 30) {
        throw new Error('Unrealistic max height');
      }
      
      // Convert to metric if needed
      const processed_restriction = {
        ...restriction,
        max_height_meters: restriction.max_height * 0.3048,
        min_height_meters: restriction.min_height * 0.3048,
        restriction_type: 'vertical_clearance'
      };
      
      // Check for existing conflicts
      const existing = await checkConflicts(restriction);
      if (existing) {
        processed_restriction.has_conflict = true;
        processed_restriction.conflict_ids = existing.map(e => e._id);
      }
      
      processed.push(processed_restriction);
    } catch (error) {
      errors.push({ restriction, error: error.message });
    }
  }
  
  return { processed, errors };
};
```

### Integration with Route Planning

```javascript
// Using truck restrictions in route calculation
const calculateTruckRoute = async (origin, destination, vehicleProfile) => {
  // Fetch relevant restrictions
  const restrictions = await TruckRestrictions.find({
    $or: [
      { max_height: { $lt: vehicleProfile.height } },
      { max_weight: { $lt: vehicleProfile.weight } }
    ]
  });
  
  // Extract restricted segments
  const restrictedSegments = restrictions.map(r => r.segment_id);
  
  // Calculate route avoiding restrictions
  const route = await routingService.calculate({
    origin,
    destination,
    avoid: restrictedSegments,
    vehicle_type: 'truck',
    vehicle_height: vehicleProfile.height
  });
  
  return route;
};
```

### Monitoring and Alerting

```javascript
// Monitor sync operations
const monitoredTruckSync = async (jsonContent) => {
  const startTime = Date.now();
  const metrics = {
    restrictions_processed: 0,
    sync_duration: 0,
    errors: []
  };
  
  try {
    const data = JSON.parse(jsonContent);
    metrics.restrictions_processed = data.truck_map_array.length;
    
    await truckMapService.syncTruckMapFromS3ToMongoDb(jsonContent);
    
    metrics.sync_duration = Date.now() - startTime;
    
    // Check for significant changes
    const previousCount = await TruckRestrictions.count();
    if (Math.abs(previousCount - metrics.restrictions_processed) > 100) {
      await alertService.send('Significant truck restriction changes', metrics);
    }
    
    logger.info('Truck sync completed', metrics);
  } catch (error) {
    metrics.errors.push(error.message);
    logger.error('Truck sync failed', metrics);
    throw error;
  }
};
```

### Data Enrichment Example

```javascript
// Enrich truck restrictions with additional context
const enrichTruckData = async (restrictions) => {
  return Promise.all(restrictions.map(async (restriction) => {
    // Get road information
    const roadInfo = await RoadNetwork.findOne({ 
      segment_id: restriction.segment_id 
    });
    
    // Add geographic context
    if (roadInfo) {
      restriction.road_name = roadInfo.name;
      restriction.city = roadInfo.city;
      restriction.state = roadInfo.state;
      restriction.coordinates = roadInfo.geometry;
    }
    
    // Add severity classification
    if (restriction.max_height < 12) {
      restriction.severity = 'critical';
    } else if (restriction.max_height < 14) {
      restriction.severity = 'moderate';
    } else {
      restriction.severity = 'low';
    }
    
    return restriction;
  }));
};
```

This job plays a crucial role in commercial vehicle navigation safety by maintaining up-to-date routing restrictions. It ensures truck drivers receive accurate routing guidance that accounts for physical limitations like bridge heights, preventing accidents and routing failures that could result from attempting to traverse restricted road segments.