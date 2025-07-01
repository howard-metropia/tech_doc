# test-region-code.js

## Overview
Test suite for the region code helper function in the TSP API. Tests geographic coordinate-to-region mapping for the Greater Houston Area, including ZIP code, city, and county identification.

## File Location
`/test/test-region-code.js`

## Dependencies
- **chai**: BDD/TDD assertion library
- **sinon**: Test spies, stubs, and mocks
- **Helper**: get-region-code helper function
- **Models**: ZipcodeGeometry
- **Logging**: @maas/core/log

## Helper Under Test
```javascript
const getRegionCode = require('@app/src/helpers/get-region-code');
```

## Test Data

### Greater Houston Area Coordinates
```javascript
const testCoordinates = {
  // Downtown Houston (77002)
  downtown: { lat: 29.7604, lon: -95.3698 },
  
  // Sugar Land City Center (77479)
  sugarland: { lat: 29.6197, lon: -95.6349 },
  
  // The Woodlands City Center (77380)
  woodlands: { lat: 30.1658, lon: -95.4613 },
  
  // Invalid coordinates for error handling
  invalid: { lat: 0, lon: 0 }
};
```

### Expected Region Mappings
- **Houston**: Harris County, ZIP codes 770xx
- **Sugar Land**: Fort Bend County, ZIP codes 774xx
- **The Woodlands**: Montgomery County, ZIP codes 773xx

## Test Cases

### 1. Downtown Houston Region Detection
**Coordinates**: `{ lat: 29.7604, lon: -95.3698 }`

**Expected Response**:
```javascript
{
  zipcode_tag: number,        // ZIP code (77002 area)
  city_tag: 'Houston',
  county_tag: 'Harris County'
}
```

**Validation**:
- ZIP code is numeric
- City correctly identified as Houston
- County correctly identified as Harris County

### 2. Sugar Land Region Detection
**Coordinates**: `{ lat: 29.6197, lon: -95.6349 }`

**Expected Response**:
```javascript
{
  zipcode_tag: number,           // ZIP code (77479 area)
  city_tag: 'Sugar Land',
  county_tag: 'Fort Bend County'
}
```

**Validation**:
- ZIP code is numeric
- City correctly identified as Sugar Land
- County correctly identified as Fort Bend County

### 3. The Woodlands Region Detection
**Coordinates**: `{ lat: 30.1658, lon: -95.4613 }`

**Expected Response**:
```javascript
{
  zipcode_tag: number,              // ZIP code (77380 area)
  city_tag: 'The Woodlands',
  county_tag: 'Montgomery County'
}
```

**Validation**:
- ZIP code is numeric
- City correctly identified as The Woodlands
- County correctly identified as Montgomery County

### 4. Invalid Coordinates Handling
**Coordinates**: `{ lat: 0, lon: 0 }`

**Expected Response**:
```javascript
{
  zipcode_tag: null,
  city_tag: null,
  county_tag: null
}
```

**Purpose**:
- Tests graceful handling of coordinates outside service area
- Ensures no system errors for invalid locations
- Returns null values for unknown regions

### 5. Database Error Handling
**Scenario**: Database connection failure

**Test Setup**:
```javascript
const error = new Error('Database connection error');
const ZipcodeGeometry = require('@app/src/models/regionCode/ZipcodeGeometry');
const findStub = sinon.stub(ZipcodeGeometry, 'find').throws(error);
```

**Expected Response**:
```javascript
{
  zipcode_tag: null,            // ZIP lookup failed
  city_tag: 'Houston',          // Fallback city
  county_tag: 'Harris County'   // Fallback county
}
```

**Error Logging**:
```javascript
expect(loggerErrorStub.calledWith(`getZipCode failed: ${error}`)).to.be.true;
```

## Geographic Coverage

### Houston Metropolitan Area
- **Harris County**: Primary urban core (Houston)
- **Fort Bend County**: Southwest suburbs (Sugar Land)
- **Montgomery County**: North suburbs (The Woodlands)

### ZIP Code System
- **77xxx**: Houston area ZIP code range
- **Geographic Boundaries**: Polygon-based coordinate-to-ZIP mapping
- **Precision**: Address-level geographic accuracy

## Database Integration

### ZipcodeGeometry Model
```javascript
const ZipcodeGeometry = require('@app/src/models/regionCode/ZipcodeGeometry');
```

**Query Process**:
1. **Coordinate Input**: Latitude/longitude coordinates
2. **Polygon Intersection**: Find ZIP code polygon containing coordinates
3. **Region Lookup**: Map ZIP code to city and county
4. **Response Formation**: Return structured region data

### Error Handling
- **Database Failures**: Graceful degradation with partial data
- **Invalid Coordinates**: Return null values
- **Logging**: Error tracking for debugging

## Testing Strategy

### Realistic Test Data
- **Real Coordinates**: Actual Houston area locations
- **Known Mappings**: Expected city/county results
- **Edge Cases**: Invalid coordinates, error conditions

### Stubbing Approach
```javascript
beforeEach(() => {
  loggerErrorStub = sinon.stub(logger, 'error');
});

afterEach(() => {
  loggerErrorStub.restore();
});
```

### Error Simulation
```javascript
const findStub = sinon.stub(ZipcodeGeometry, 'find').throws(error);
// Test error handling
findStub.restore();
```

## Response Structure

### Successful Response
```javascript
{
  zipcode_tag: 77002,              // Numeric ZIP code
  city_tag: 'Houston',             // City name
  county_tag: 'Harris County'      // County name with "County"
}
```

### Error Response
```javascript
{
  zipcode_tag: null,               // Failed ZIP lookup
  city_tag: null,                  // Unknown city
  county_tag: null                 // Unknown county
}
```

### Partial Success Response
```javascript
{
  zipcode_tag: null,               // ZIP lookup failed
  city_tag: 'Houston',             // Fallback city available
  county_tag: 'Harris County'     // Fallback county available
}
```

## Business Logic

### Geographic Services
- **Address Validation**: Verify coordinates within service area
- **Regional Identification**: Map coordinates to administrative regions
- **Service Area Coverage**: Houston metropolitan area focus

### Transportation Integration
- **Route Planning**: Regional data for route optimization
- **Service Zones**: Transportation service area definitions
- **Local Regulations**: City/county-specific transportation rules

## Error Resilience

### Graceful Degradation
- **Partial Data**: Return available region information
- **Fallback Values**: Default to known good values when possible
- **No Failures**: System continues operation despite errors

### Logging Strategy
- **Error Tracking**: Log all database failures
- **Debug Information**: Include error details for troubleshooting
- **Service Monitoring**: Track region lookup success rates

## Integration Points

### Geographic Systems
- **Coordinate Processing**: Latitude/longitude handling
- **Polygon Operations**: Point-in-polygon geographic calculations
- **Administrative Boundaries**: ZIP code, city, county boundaries

### Transportation Services
- **Route Planning**: Regional context for routing decisions
- **Service Areas**: Transportation provider coverage zones
- **Regulatory Compliance**: Local transportation regulations

## Performance Considerations

### Database Queries
- **Spatial Queries**: Efficient coordinate-to-region lookups
- **Indexed Searches**: Geographic index optimization
- **Response Time**: Fast region identification for real-time use

### Caching Opportunities
- **Coordinate Caching**: Cache region results for repeated coordinates
- **Regional Data**: Cache city/county mappings
- **Error Caching**: Temporary cache for error conditions

This test suite ensures the region code helper accurately maps coordinates to administrative regions in the Houston metropolitan area, handles errors gracefully, and provides reliable geographic data for the TSP API's location-based services.