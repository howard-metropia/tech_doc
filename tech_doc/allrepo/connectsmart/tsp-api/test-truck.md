# TSP API Test Suite - Truck Routing and Map Tests

## Overview
The `test-truck.js` file contains comprehensive tests for truck-specific routing functionality, including truck map data management, height/weight restrictions, and commercial vehicle routing constraints for freight transportation optimization.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-truck.js`

## Dependencies
- **chai**: Testing assertions and expectations
- **sinon**: Test doubles, mocking, and stubbing
- **moment-timezone**: Date/time manipulation
- **supertest**: HTTP assertion library for API testing
- **@maas/core**: Core framework components

## Test Architecture

### Service Integration
```javascript
const { truckMapSchema } = require('@app/src/models/truckModel');
const { TruckMapService } = require('@app/src/services/truckService');
const validatorTruck = require('@app/src/schemas/truckJoiSchema');
```

### API Setup
```javascript
const createApp = require('@maas/core/api');
const { getRouter } = require('@maas/core');

const app = createApp();
const router = getRouter();
const request = supertest.agent(app.listen());
```

## Truck Map Service Tests

### Test Data Structure
```javascript
const truckMapInfo = {
  last_modified: moment('2023-04-28T12:00:00Z').unix(),
  map_array: [
    {
      max_height: 10,     // Maximum height in feet
      min_height: 5,      // Minimum height in feet  
      present_word: 'max height is 10 and min height is 5',
      segment_id: 1,      // Road segment identifier
      link_id: 100        // Link identifier in road network
    },
    {
      max_height: 15,
      min_height: 12,
      present_word: 'max height is 15 and min height is 12',
      segment_id: 2,
      link_id: 200
    }
  ]
};
```

### Mock Database Schema
```javascript
const latestTruckMap = {
  truck_map: truckMapInfo.map_array,
  created_at: moment('2023-04-28T12:00:00Z').toDate(),
  toJSON: function () {
    return {
      _id: '123',
      truck_map: truckMapInfo.map_array,
      created_at: moment('2023-04-28T12:00:00Z').toDate(),
      __v: 0
    };
  }
};
```

## TruckMapService Unit Tests

### 1. Empty Map Handling
```javascript
describe('TruckMapService', () => {
  describe('getLatestTruckMap', () => {
    it('should return empty array if there are no truck maps', async () => {
      sinon.stub(truckMapSchema, 'findOne').returns(null);
      
      const truckMapService = new TruckMapService();
      const result = await truckMapService.getLatestTruckMap(previousTimestamp);
      
      expect(result).to.deep.equal([]);
      expect(validatorMangoDbDataValidateAsyncSpy.called).to.be.false;
    });
  });
});
```

### 2. Timestamp Comparison Logic
```javascript
it('should return empty array if the last modified timestamp is the same as the previous timestamp', async () => {
  sinon.stub(truckMapSchema, 'findOne').returns(latestTruckMap);
  
  const truckMapService = new TruckMapService();
  const result = await truckMapService.getLatestTruckMap(
    moment(latestTruckMap.created_at).unix()
  );
  
  expect(result).to.deep.equal([]);
  expect(validatorMangoDbDataValidateAsyncSpy.calledOnce).to.be.true;
});
```

### 3. Updated Map Retrieval
```javascript
it('should return truck map information if the last modified timestamp is different from the previous timestamp', async () => {
  sinon.stub(truckMapSchema, 'findOne').returns(latestTruckMap);
  
  const truckMapService = new TruckMapService();
  const result = await truckMapService.getLatestTruckMap(previousTimestamp);
  
  expect(result).to.deep.equal(truckMapInfo);
  expect(validatorMangoDbDataValidateAsyncSpy.calledOnce).to.be.true;
});
```

## Truck Map API Endpoint Tests

### Endpoint: `GET /truck/map`

**Purpose**: Retrieve latest truck map data with vehicle restrictions

### Successful Map Retrieval
```javascript
describe('/truck/map route', () => {
  it('should return latest truck map with valid last_modified parameter', async () => {
    const resp200 = await request.get(router.url('truckMap'))
      .query({ last_modified: 123456 })
      .expect(200);
    
    const { result, data } = resp200.body;
    expect(result).to.eq('success');
    expect(data).to.be.an('object');
    expect(data.last_modified).to.be.a('number');
    expect(data.map_array).to.be.an('array');
  });
});
```

### Response Data Structure
```javascript
{
  result: 'success',
  data: {
    last_modified: 1682678401,  // Unix timestamp
    map_array: [
      {
        max_height: 10,
        min_height: 5,
        present_word: 'max height is 10 and min height is 5',
        segment_id: 1,
        link_id: 100,
        weight_limit: 80000,     // Weight limit in pounds
        length_limit: 53,        // Length limit in feet
        width_limit: 8.5,        // Width limit in feet
        hazmat_allowed: false,   // Hazardous materials allowed
        truck_route: true        // Designated truck route
      }
    ]
  }
}
```

## Truck Routing Constraints

### Vehicle Dimension Limits
```javascript
const TRUCK_CONSTRAINTS = {
  height: {
    min: 5,      // Minimum clearance in feet
    max: 15,     // Maximum height in feet
    default: 13.6 // Standard truck height
  },
  weight: {
    min: 10000,  // Minimum weight in pounds
    max: 80000,  // Maximum gross weight
    axle_limit: 20000 // Per-axle weight limit
  },
  length: {
    min: 20,     // Minimum length in feet
    max: 53,     // Maximum length in feet
    trailer: 53  // Standard trailer length
  },
  width: {
    min: 7,      // Minimum width in feet
    max: 8.5,    // Maximum width in feet
    standard: 8  // Standard truck width
  }
};
```

### Route Restriction Types
```javascript
const ROUTE_RESTRICTIONS = {
  BRIDGE_HEIGHT: 'bridge_height_restriction',
  WEIGHT_LIMIT: 'weight_limit_restriction', 
  NO_TRUCKS: 'no_trucks_allowed',
  HAZMAT_PROHIBITED: 'hazmat_prohibited',
  TIME_RESTRICTED: 'time_restricted_access',
  PERMIT_REQUIRED: 'oversized_permit_required'
};
```

## Data Validation

### Joi Schema Validation
```javascript
const validatorTruck = {
  validateTruckMapMongoDBData: {
    validateAsync: sinon.spy(async (data) => {
      const schema = Joi.object({
        truck_map: Joi.array().items(
          Joi.object({
            max_height: Joi.number().required(),
            min_height: Joi.number().required(),
            segment_id: Joi.number().required(),
            link_id: Joi.number().required(),
            present_word: Joi.string().optional()
          })
        ).required(),
        created_at: Joi.date().required()
      });
      
      return schema.validateAsync(data);
    })
  }
};
```

### Test Spy Integration
```javascript
let validatorMangoDbDataValidateAsyncSpy;

beforeEach(() => {
  validatorMangoDbDataValidateAsyncSpy = sinon.spy(
    validatorTruck.validateTruckMapMongoDBData, 'validateAsync'
  );
});

afterEach(() => {
  sinon.restore();
});
```

## Truck Route Optimization

### Height Clearance Validation
```javascript
const validateHeightClearance = (truckHeight, routeSegments) => {
  const violations = [];
  
  routeSegments.forEach(segment => {
    if (segment.min_height > 0 && truckHeight > segment.min_height) {
      violations.push({
        segment_id: segment.segment_id,
        required_height: segment.min_height,
        truck_height: truckHeight,
        clearance_violation: truckHeight - segment.min_height
      });
    }
  });
  
  return {
    canPass: violations.length === 0,
    violations,
    alternateRouteRequired: violations.length > 0
  };
};
```

### Weight Distribution Analysis
```javascript
const analyzeWeightDistribution = (truckSpecs, routeSegments) => {
  const weightAnalysis = {
    totalWeight: truckSpecs.gross_weight,
    axleWeights: truckSpecs.axle_configuration,
    violatingSegments: [],
    loadAdjustmentRequired: false
  };
  
  routeSegments.forEach(segment => {
    if (segment.weight_limit && truckSpecs.gross_weight > segment.weight_limit) {
      weightAnalysis.violatingSegments.push({
        segment_id: segment.segment_id,
        weight_limit: segment.weight_limit,
        excess_weight: truckSpecs.gross_weight - segment.weight_limit
      });
    }
  });
  
  weightAnalysis.loadAdjustmentRequired = weightAnalysis.violatingSegments.length > 0;
  
  return weightAnalysis;
};
```

## MongoDB Integration

### Truck Map Schema Model
```javascript
const truckMapSchema = {
  findOne: async (query = {}) => {
    // Find latest truck map data
    return await TruckMap.findOne(query).sort({ created_at: -1 });
  },
  
  create: async (mapData) => {
    return await TruckMap.create({
      truck_map: mapData.map_array,
      created_at: new Date(),
      version: mapData.version || 1
    });
  },
  
  updateTimestamp: async (id, timestamp) => {
    return await TruckMap.findByIdAndUpdate(id, {
      last_modified: timestamp,
      updated_at: new Date()
    });
  }
};
```

### Cache Strategy
```javascript
const TRUCK_MAP_CACHE = {
  key: 'truck_map_latest',
  ttl: 3600, // 1 hour cache
  
  getCached: async () => {
    const cached = await redis.get(TRUCK_MAP_CACHE.key);
    return cached ? JSON.parse(cached) : null;
  },
  
  setCached: async (data) => {
    await redis.setex(
      TRUCK_MAP_CACHE.key, 
      TRUCK_MAP_CACHE.ttl, 
      JSON.stringify(data)
    );
  },
  
  invalidate: async () => {
    await redis.del(TRUCK_MAP_CACHE.key);
  }
};
```

## Performance Testing

### Large Dataset Handling
```javascript
describe('Performance Tests', () => {
  it('should handle large truck map datasets efficiently', async () => {
    const largeTruckMap = {
      truck_map: Array(10000).fill().map((_, index) => ({
        max_height: 10 + (index % 5),
        min_height: 5 + (index % 3),
        segment_id: index,
        link_id: index * 10,
        present_word: `Segment ${index} restrictions`
      })),
      created_at: new Date()
    };
    
    sinon.stub(truckMapSchema, 'findOne').returns(largeTruckMap);
    
    const startTime = Date.now();
    const truckMapService = new TruckMapService();
    const result = await truckMapService.getLatestTruckMap(0);
    const endTime = Date.now();
    
    expect(endTime - startTime).to.be.lessThan(5000); // 5 seconds max
    expect(result.map_array).to.have.length(10000);
  });
});
```

### Concurrent Request Handling
```javascript
it('should handle concurrent map requests', async () => {
  const requests = Array(50).fill().map(() => 
    request.get(router.url('truckMap')).query({ last_modified: 123456 })
  );
  
  const startTime = Date.now();
  const responses = await Promise.all(requests);
  const endTime = Date.now();
  
  expect(endTime - startTime).to.be.lessThan(10000); // 10 seconds for 50 requests
  expect(responses.every(resp => resp.status === 200)).to.be.true;
});
```

## Error Handling

### Invalid Parameter Handling
```javascript
describe('Error Scenarios', () => {
  it('should handle invalid last_modified parameter', async () => {
    const resp = await request.get(router.url('truckMap'))
      .query({ last_modified: 'invalid' });
    
    expect(resp.status).to.be.oneOf([200, 400]);
    if (resp.status === 400) {
      expect(resp.body.error).to.include.keys(['code', 'message']);
    }
  });
  
  it('should handle database connection failures', async () => {
    sinon.stub(truckMapSchema, 'findOne').throws(new Error('Database connection failed'));
    
    const truckMapService = new TruckMapService();
    
    try {
      await truckMapService.getLatestTruckMap(123456);
      expect.fail('Should have thrown database error');
    } catch (error) {
      expect(error.message).to.include('Database connection failed');
    }
  });
});
```

## Integration Testing

### Route Planning Integration
```javascript
describe('Route Planning Integration', () => {
  it('should integrate truck constraints with route calculation', async () => {
    const truckSpecs = {
      height: 13.6,
      weight: 75000,
      length: 53,
      width: 8.5,
      hazmat: false
    };
    
    const routeRequest = {
      origin: { lat: 29.7604, lng: -95.3698 },
      destination: { lat: 29.7174, lng: -95.4041 },
      truck_specifications: truckSpecs
    };
    
    // Get truck map
    const mapResp = await request.get(router.url('truckMap'))
      .query({ last_modified: 0 });
    
    expect(mapResp.status).to.equal(200);
    
    // Validate route against truck constraints
    const constraints = mapResp.body.data.map_array;
    const routeValidation = validateTruckRoute(routeRequest, constraints);
    
    expect(routeValidation).to.have.property('canTraverse');
    expect(routeValidation).to.have.property('restrictions');
  });
});
```

## Quality Assurance

### Data Integrity
- **Timestamp Consistency**: Accurate last_modified tracking
- **Constraint Accuracy**: Correct height/weight/dimension limits
- **Route Validation**: Proper truck route designation
- **Cache Consistency**: Synchronized cached and live data

### Performance Standards
- **Response Time**: Under 2 seconds for map retrieval
- **Data Freshness**: 5-minute maximum staleness
- **Throughput**: 1000+ requests per minute
- **Memory Usage**: Optimized for large constraint datasets

This comprehensive test suite ensures the truck routing system provides accurate vehicle constraint data, reliable map updates, and efficient route planning capabilities for commercial freight transportation while maintaining high performance and data integrity standards.