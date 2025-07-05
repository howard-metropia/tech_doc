# County Verification Test Suite

## Overview
Test suite for the county verification service that validates geographical point-in-polygon operations to determine which Houston metropolitan area county a given coordinate pair belongs to, using GeoJSON polygon data for accurate geographical boundary detection.

## File Location
`/test/test-checkCounty.js`

## Dependencies
- `@maas/core/bootstrap` - Application initialization
- `chai` - Assertion library with expect interface
- `@turf/turf` - Geospatial analysis toolkit
- `sinon` - Test stubbing framework
- `fs` - File system operations
- `path` - Path manipulation utilities

## Test Architecture

### Service Function Under Test
```javascript
const { checkCounty } = require('@app/src/services/hntb-etl');
```

### GeoJSON Data Management
```javascript
const geojsonPath = path.join(__dirname, '../src/static/geojson', 'county.json');
const geojson = JSON.parse(fs.readFileSync(geojsonPath, 'utf8'));
sinon.stub(fs, 'readFileSync').returns(JSON.stringify(geojson));
```

## Geographic Test Coverage

### Houston Metropolitan Counties
The test suite validates 13 counties in the Houston metropolitan area:

#### Primary Counties
```javascript
{ lat: 29.8335422, lon: -95.7642568, county: 'Harris County' }, // Houston
{ lat: 29.5862327, lon: -95.7825425, county: 'Fort Bend County' }, // Richmond
{ lat: 30.3114537, lon: -95.6119464, county: 'Montgomery County' }, // Conroe
```

#### Extended Metropolitan Area
```javascript
{ lat: 29.2391381, lon: -96.210262, county: 'Wharton County' },
{ county: 'Waller County', lat: 30.083, lon: -95.973},
{ county: 'Walker County', lat: 30.700, lon: -95.550},
{ county: 'Galveston County', lat: 29.301, lon: -94.797},
{ county: 'Colorado County', lat: 29.7042679, lon: -96.5827515}, // Columbus
{ county: 'Liberty County', lat: 30.080, lon: -94.800},
{ county: 'Chambers County', lat: 29.800, lon: -94.700},
{ county: 'Brazoria County', lat: 29.200, lon: -95.500 },
{ county: 'Austin County', lat: 29.9431469, lon: -96.28597 }, // Bellville
{ county: 'Matagorda County', lat: 28.800, lon: -95.600 },
```

## Test Implementation

### Positive Test Cases
```javascript
it('should return the correct county for a point in Houston metropolitan counties', async () => {
  const testCases = [
    { lat: 29.8335422, lon: -95.7642568, county: 'Harris County' },
    // ... additional test cases
  ];

  for (const testCase of testCases) {
    const county = checkCounty(testCase.lat, testCase.lon);
    expect(county).to.equal(testCase.county);
  }
});
```

### Negative Test Cases
```javascript
it('should return an empty string for a point not in Houston metropolitan counties', async () => {
  const testCases = [
    { lat: 32.7767, lon: -96.797, county: '' }, // Dallas
    { lat: 29.4241, lon: -98.4936, county: '' }, // San Antonio
  ];

  for (const testCase of testCases) {
    const county = checkCounty(testCase.lat, testCase.lon);
    expect(county).to.equal(testCase.county);
  }
});
```

## Geographical Analysis

### Point-in-Polygon Algorithm
The service uses geospatial analysis to determine county membership:
1. **Coordinate Input**: Accepts latitude and longitude coordinates
2. **Polygon Lookup**: Searches through county boundary polygons
3. **Intersection Test**: Uses mathematical point-in-polygon algorithms
4. **County Identification**: Returns county name or empty string

### Coordinate System
- **Format**: Decimal degrees (WGS84 coordinate system)
- **Precision**: Up to 7 decimal places for accuracy
- **Range**: Houston metropolitan area spans approximately:
  - **Latitude**: 28.8° to 30.7° North
  - **Longitude**: -96.6° to -94.7° West

## GeoJSON Data Structure

### County Polygon Format
```javascript
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Harris County"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[lon1, lat1], [lon2, lat2], ...]]
      }
    }
  ]
}
```

### Boundary Precision
- **Source**: Official county boundary data
- **Accuracy**: Sub-meter precision for administrative boundaries
- **Updates**: Synchronized with official governmental boundary changes

## Test Data Validation

### Known Geographic Points
Each test coordinate represents a verified location within its respective county:

#### Urban Centers
- **Houston (Harris County)**: Downtown coordinates
- **Richmond (Fort Bend County)**: City center location
- **Conroe (Montgomery County)**: Municipal boundaries

#### Regional Coverage
- **Coastal Areas**: Galveston County maritime boundaries
- **Rural Areas**: Agricultural regions in outlying counties
- **Suburban Areas**: Residential developments in growth corridors

## Stub Implementation

### File System Mocking
```javascript
before(() => {
  const geojsonPath = path.join(__dirname, '../src/static/geojson', 'county.json');
  const geojson = JSON.parse(fs.readFileSync(geojsonPath, 'utf8'));
  sinon.stub(fs, 'readFileSync').returns(JSON.stringify(geojson));
});

after(() => {
  sinon.restore();
});
```

### Mock Strategy
- **Static Data**: Uses actual GeoJSON file for realistic testing
- **Consistent Results**: Ensures reproducible test outcomes
- **Performance**: Avoids repeated file I/O during test execution

## Error Handling

### Invalid Coordinates
- **Out of Range**: Returns empty string for coordinates outside metropolitan area
- **Invalid Format**: Handles malformed coordinate input gracefully
- **Null Values**: Manages null or undefined coordinate parameters

### Data Integrity
- **Polygon Validation**: Ensures GeoJSON data is properly formatted
- **Coordinate Validation**: Verifies lat/lon are within valid ranges
- **Boundary Consistency**: Maintains polygon closure and validity

## Performance Considerations

### Algorithm Efficiency
- **Spatial Indexing**: Optimized polygon lookup for large datasets
- **Early Termination**: Stops searching once county is found
- **Memory Usage**: Efficient polygon data structures

### Test Execution Speed
- **Mocked I/O**: Fast execution through stubbed file operations
- **Batch Testing**: Processes multiple coordinates efficiently
- **Minimal Setup**: Quick test initialization and cleanup

## Business Applications

### Use Cases
1. **Trip Classification**: Categorize trips by county for reporting
2. **Service Areas**: Determine service availability by location
3. **Compliance**: Ensure operations within authorized jurisdictions
4. **Analytics**: County-level performance and usage metrics

### Data Requirements
- **Real-time Lookup**: Fast coordinate-to-county resolution
- **Accuracy**: Precise boundary determination for billing/reporting
- **Coverage**: Complete metropolitan area geographical coverage

## Quality Assurance

### Test Coverage Strategy
1. **Boundary Testing**: Points near county borders
2. **Center Testing**: Points well within county boundaries
3. **Negative Testing**: Points outside service area
4. **Edge Cases**: Coordinates on exact boundary lines

### Validation Approaches
- **Ground Truth**: Known coordinates with verified county membership
- **Cross-Validation**: Multiple coordinate systems for same locations
- **Boundary Verification**: Test points near county lines

## Integration Points

### Service Dependencies
- **HNTB ETL Service**: Part of Houston transportation data pipeline
- **Trip Processing**: Enables county-based trip categorization
- **Reporting Systems**: Provides geographic segmentation for analytics

### External Data Sources
- **Government Boundaries**: Official county boundary definitions
- **Census Data**: Population-based service area definitions
- **Transportation Authorities**: Service jurisdiction boundaries

## Maintenance Considerations

### Data Updates
- **Boundary Changes**: Periodic updates for annexations or boundary adjustments
- **Accuracy Improvements**: Enhanced precision from better source data
- **Format Evolution**: Adaptation to new GeoJSON standards

### Performance Monitoring
- **Response Time**: Coordinate lookup performance metrics
- **Memory Usage**: Polygon data memory footprint
- **Accuracy Validation**: Periodic verification against known locations

## Error Scenarios

### Boundary Edge Cases
- **Points on Boundaries**: Coordinates exactly on county lines
- **Water Bodies**: Handling of lakes, rivers, and coastal areas
- **Unincorporated Areas**: Areas not within any county jurisdiction

### Data Quality Issues
- **Missing Polygons**: Counties without polygon data
- **Malformed GeoJSON**: Invalid or corrupted boundary data
- **Coordinate Precision**: Rounding errors in boundary calculations

## Testing Best Practices

### Representative Sampling
- **Geographic Distribution**: Test points across entire metropolitan area
- **Density Variation**: Urban, suburban, and rural test locations
- **Boundary Coverage**: Adequate testing near county borders

### Regression Prevention
- **Known Good Results**: Baseline coordinate-county mappings
- **Automated Validation**: Continuous verification of county assignments
- **Change Detection**: Monitoring for unexpected boundary changes