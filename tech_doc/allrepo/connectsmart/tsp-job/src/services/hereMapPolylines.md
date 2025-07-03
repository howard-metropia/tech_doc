# HERE Map Polylines Service

## Overview

The HERE Map Polylines service provides advanced polyline encoding and decoding capabilities using HERE's Flexible Polyline Algorithm. This service supports efficient storage and transmission of geographic coordinate sequences with customizable precision levels and third-dimension support for elevation, altitude, and custom data channels.

## Service Information

- **Service Name**: HERE Flexible Polyline Algorithm Service
- **File Path**: `/src/services/hereMapPolylines.js`
- **Type**: Geographic Data Processing Service
- **License**: MIT License (Copyright HERE Europe B.V.)
- **Dependencies**: Native JavaScript (BigInt support for precision)

## Core Functions

### decode(encoded)

Decodes HERE flexible polyline strings into coordinate arrays with support for third-dimensional data.

**Purpose**: Convert compressed polyline strings to coordinate arrays
**Parameters**: 
- `encoded` (string): HERE flexible polyline encoded string
**Returns**: Object containing decoded polyline data and metadata

**Decoding Process**:
1. **Header Extraction**: Parses format version and encoding parameters
2. **Value Decoding**: Converts encoded characters to unsigned integer values
3. **Delta Decoding**: Applies delta compression reversal for coordinates
4. **Precision Scaling**: Applies precision factors to restore original coordinates
5. **Third Dimension Processing**: Handles elevation/altitude/custom data if present

**Return Structure**:
```javascript
{
  precision: 5,           // Coordinate precision (decimal places)
  thirdDim: 2,           // Third dimension type (ALTITUDE)
  thirdDimPrecision: 0,  // Third dimension precision
  polyline: [
    [lat1, lng1, alt1],  // Coordinate with third dimension
    [lat2, lng2, alt2],  // Additional coordinates
    // ... more coordinates
  ]
}
```

**Third Dimension Support**:
- **ABSENT** (0): No third dimension
- **LEVEL** (1): Level/floor information
- **ALTITUDE** (2): Altitude above sea level
- **ELEVATION** (3): Elevation above ground
- **CUSTOM1** (6): Custom data channel 1
- **CUSTOM2** (7): Custom data channel 2

### encode(options)

Encodes coordinate arrays into HERE flexible polyline format with configurable precision and third-dimension support.

**Purpose**: Compress coordinate sequences for efficient storage/transmission
**Parameters**: 
- `options` (object): Encoding configuration object
  - `precision` (number): Coordinate precision (default: 5)
  - `thirdDim` (number): Third dimension type (default: ABSENT)
  - `thirdDimPrecision` (number): Third dimension precision (default: 0)
  - `polyline` (array): Array of coordinate arrays to encode
**Returns**: Encoded polyline string

**Encoding Process**:
1. **Parameter Validation**: Validates precision and dimension parameters
2. **Header Generation**: Creates encoded header with format version and parameters
3. **Delta Compression**: Applies delta encoding to reduce coordinate differences
4. **Precision Scaling**: Scales coordinates based on specified precision
5. **Character Encoding**: Converts values to HERE's base-64 character set

**Usage Example**:
```javascript
const encoded = encode({
  precision: 5,
  thirdDim: ALTITUDE,
  thirdDimPrecision: 0,
  polyline: [
    [52.5, 13.4, 100],  // Berlin with altitude
    [52.6, 13.5, 105],  // Next point
    [52.7, 13.6, 110]   // Final point
  ]
});
```

### Supporting Functions

#### decodeUnsignedValues(encoded)

Converts encoded character sequence to array of unsigned integer values.

**Purpose**: Low-level decoding of variable-length integer encoding
**Parameters**: 
- `encoded` (string): Encoded character string
**Returns**: Array of BigInt/Number values

**Algorithm Details**:
- Uses variable-length encoding (similar to Protocol Buffers varint)
- Each character encodes 5 bits of data plus continuation bit
- Supports both BigInt and Number for large value handling
- Processes characters using HERE's custom base-64 table

#### decodeHeader(version, encodedHeader)

Extracts encoding parameters from polyline header information.

**Purpose**: Parse polyline metadata and configuration
**Parameters**: 
- `version` (BigInt/Number): Format version identifier
- `encodedHeader` (BigInt/Number): Encoded header containing parameters
**Returns**: Object with precision and dimension configuration

**Header Structure**:
```javascript
{
  precision: number,           // Lat/lng precision (0-15)
  thirdDim: number,           // Third dimension type (0-7)
  thirdDimPrecision: number   // Third dimension precision (0-15)
}
```

#### toSigned(val)

Converts unsigned encoded values back to signed integers using zigzag encoding.

**Purpose**: Restore signed coordinate deltas from unsigned encoding
**Parameters**: 
- `val` (BigInt/Number): Unsigned encoded value
**Returns**: Signed integer value

**Zigzag Decoding**:
- Reverses zigzag encoding: `(val >> 1) ^ (-(val & 1))`
- Efficiently handles both positive and negative coordinate deltas
- Maintains precision for large coordinate values

## Technical Architecture

### Encoding Tables

**Character Encoding Table**:
```javascript
const ENCODING_TABLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
```

**Decoding Table** (ASCII offset mapping):
```javascript
const DECODING_TABLE = [
  62, -1, -1, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1,
  -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
  21, 22, 23, 24, 25, -1, -1, -1, -1, 63, -1, 26, 27, 28, 29, 30, 31, 32, 33,
  34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
];
```

### Precision and Scaling

**Coordinate Scaling**:
- **Latitude/Longitude**: `10^precision` multiplier
- **Third Dimension**: `10^thirdDimPrecision` multiplier
- **Default Precision**: 5 decimal places (meter-level accuracy)

**Precision Guidelines**:
- **Precision 0**: ~111 km accuracy
- **Precision 1**: ~11 km accuracy
- **Precision 2**: ~1.1 km accuracy
- **Precision 3**: ~110 m accuracy
- **Precision 4**: ~11 m accuracy
- **Precision 5**: ~1.1 m accuracy (default)
- **Precision 6**: ~0.11 m accuracy

### Third Dimension Types

**Supported Dimensions**:
```javascript
const ABSENT = 0;     // No third dimension
const LEVEL = 1;      // Building level/floor
const ALTITUDE = 2;   // Altitude above sea level
const ELEVATION = 3;  // Elevation above ground
const CUSTOM1 = 6;    // Custom data channel 1
const CUSTOM2 = 7;    // Custom data channel 2
```

**Reserved Values**: 4 and 5 are reserved for future use

### BigInt Support

**Compatibility Layer**:
```javascript
const Num = typeof BigInt !== 'undefined' ? BigInt : Number;
```

**Features**:
- Automatic BigInt detection and fallback
- Supports large coordinate values and high precision
- Maintains compatibility with older JavaScript environments
- Handles coordinate deltas exceeding 32-bit integer limits

## Algorithm Details

### Delta Compression

**Coordinate Delta Calculation**:
```javascript
// Encoding: Store differences between consecutive points
const deltaLat = currentLat - previousLat;
const deltaLng = currentLng - previousLng;

// Decoding: Accumulate deltas to restore coordinates
lastLat += deltaLat;
lastLng += deltaLng;
```

**Benefits**:
- Significantly reduces encoded string length
- More efficient for routes with nearby consecutive points
- Maintains full precision while reducing storage requirements

### Variable-Length Integer Encoding

**Encoding Process**:
1. Convert signed values to unsigned using zigzag encoding
2. Split values into 5-bit chunks
3. Set continuation bit (0x20) for all chunks except the last
4. Map to character using encoding table

**Decoding Process**:
1. Extract 5-bit values from characters
2. Check continuation bit to determine value boundaries
3. Reconstruct full integers from chunks
4. Convert back to signed values using zigzag decoding

### Header Encoding

**Header Structure** (single encoded value):
```
Bits 0-3:   Precision (0-15)
Bits 4-6:   Third dimension type (0-7)
Bits 7-10:  Third dimension precision (0-15)
Bits 11+:   Reserved for future use
```

**Header Validation**:
- Precision values must be between 0 and 15
- Third dimension precision must be between 0 and 15
- Third dimension type must be valid (0, 1, 2, 3, 6, or 7)
- Values 4 and 5 are explicitly rejected

## Error Handling

### Validation Errors

**Parameter Validation**:
```javascript
if (precision < 0 || precision > 15) {
  throw new Error('precision out of range. Should be between 0 and 15');
}
if (thirdDim < 0 || thirdDim > 7 || thirdDim === 4 || thirdDim === 5) {
  throw new Error('thirdDim should be between 0, 1, 2, 3, 6 or 7');
}
```

**Decoding Errors**:
- **Invalid encoding**: Premature ending or malformed data
- **Invalid format version**: Unsupported version number
- **Character errors**: Invalid characters in encoded string

### Robust Error Handling

```javascript
function safeEncode(options) {
  try {
    return encode(options);
  } catch (error) {
    if (error.message.includes('out of range')) {
      throw new Error('Invalid precision or dimension parameters');
    } else if (error.message.includes('thirdDim')) {
      throw new Error('Invalid third dimension type');
    } else {
      throw new Error(`Encoding failed: ${error.message}`);
    }
  }
}
```

## Performance Characteristics

### Encoding Efficiency

**String Length Comparison**:
- Raw coordinate storage: ~15-20 characters per point
- HERE flexible polyline: ~2-6 characters per point
- Compression ratio: 3-10x reduction typical

**Processing Performance**:
- Linear time complexity O(n) for n coordinates
- Memory efficient streaming processing
- Minimal object allocation during processing

### Memory Usage

**Optimization Strategies**:
- In-place processing where possible
- Minimal intermediate array creation
- Efficient string concatenation
- BigInt usage only when necessary

## Integration Patterns

### HERE Maps Integration

**Route API Integration**:
```javascript
// Decode route polyline from HERE API response
const routeData = decode(hereApiResponse.routes[0].polyline);
const coordinates = routeData.polyline;

// Process coordinates for mapping display
coordinates.forEach(([lat, lng, alt]) => {
  // Add to map visualization
  addRoutePoint(lat, lng, alt);
});
```

### Data Storage Optimization

**Database Storage**:
```javascript
// Store compressed polyline instead of coordinate arrays
const compressedRoute = encode({
  precision: 5,
  polyline: routeCoordinates
});

// Store single string instead of array of coordinates
await saveRoute({ id: routeId, polyline: compressedRoute });
```

### API Response Optimization

**Bandwidth Reduction**:
```javascript
// Encode route data for API response
const response = {
  routeId: route.id,
  polyline: encode({
    precision: 5,
    thirdDim: ALTITUDE,
    polyline: route.coordinates
  }),
  metadata: {
    distance: route.distance,
    duration: route.duration
  }
};
```

## Usage Examples

### Basic Encoding and Decoding

```javascript
const { encode, decode, ALTITUDE } = require('./hereMapPolylines');

// Sample route coordinates
const route = [
  [52.5200, 13.4050],     // Berlin
  [52.5170, 13.3888],     // Brandenburg Gate
  [52.5067, 13.4437]      // Alexanderplatz
];

// Encode route
const encoded = encode({
  precision: 5,
  polyline: route
});
console.log('Encoded:', encoded);

// Decode route
const decoded = decode(encoded);
console.log('Decoded coordinates:', decoded.polyline);
console.log('Precision:', decoded.precision);
```

### Advanced Usage with Third Dimension

```javascript
// Route with altitude data
const routeWithAltitude = [
  [52.5200, 13.4050, 34],   // Berlin, 34m elevation
  [52.5170, 13.3888, 35],   // Brandenburg Gate, 35m
  [52.5067, 13.4437, 37]    // Alexanderplatz, 37m
];

// Encode with altitude
const encodedWithAlt = encode({
  precision: 5,
  thirdDim: ALTITUDE,
  thirdDimPrecision: 0,
  polyline: routeWithAltitude
});

// Decode and verify
const decodedWithAlt = decode(encodedWithAlt);
console.log('Route with altitude:', decodedWithAlt.polyline);
console.log('Third dimension type:', decodedWithAlt.thirdDim);
```

### Error Handling Implementation

```javascript
function processPolyline(encodedData) {
  try {
    const decoded = decode(encodedData);
    return decoded.polyline;
  } catch (error) {
    if (error.message.includes('Invalid format version')) {
      throw new Error('Unsupported polyline format version');
    } else if (error.message.includes('Invalid encoding')) {
      throw new Error('Corrupted polyline data');
    } else {
      throw new Error(`Polyline processing failed: ${error.message}`);
    }
  }
}
```

## Testing and Validation

### Round-trip Testing

```javascript
function validateRoundTrip(originalCoordinates) {
  const encoded = encode({
    precision: 5,
    polyline: originalCoordinates
  });
  
  const decoded = decode(encoded);
  
  // Verify coordinates match within precision tolerance
  const tolerance = Math.pow(10, -5); // 5 decimal places
  originalCoordinates.forEach(([lat, lng], index) => {
    const [decodedLat, decodedLng] = decoded.polyline[index];
    
    if (Math.abs(lat - decodedLat) > tolerance || 
        Math.abs(lng - decodedLng) > tolerance) {
      throw new Error(`Round-trip validation failed at index ${index}`);
    }
  });
  
  return true;
}
```

### Performance Testing

```javascript
function benchmarkEncoding(coordinates, iterations = 1000) {
  const start = performance.now();
  
  for (let i = 0; i < iterations; i++) {
    encode({ precision: 5, polyline: coordinates });
  }
  
  const end = performance.now();
  const avgTime = (end - start) / iterations;
  
  console.log(`Average encoding time: ${avgTime.toFixed(3)}ms`);
  return avgTime;
}
```

## Limitations and Considerations

### Current Limitations

**Format Constraints**:
- Fixed format version (version 1)
- Limited third dimension types
- Maximum precision of 15 decimal places
- No built-in compression for sparse data

**JavaScript Limitations**:
- BigInt requirement for high precision in newer environments
- Number precision limits in older JavaScript environments
- No native streaming support for very large polylines

### Future Enhancements

**Potential Improvements**:
- Format version evolution support
- Additional third dimension types
- Streaming processing for large datasets
- Custom compression algorithms for specific use cases

**Performance Optimizations**:
- WebAssembly implementation for performance-critical applications
- SIMD optimizations where available
- Memory pool allocation for frequent encoding/decoding

## Dependencies

- **Native JavaScript**: ES2015+ features (arrow functions, const/let)
- **BigInt Support**: Optional, falls back to Number for older environments
- **No External Dependencies**: Self-contained implementation
- **MIT License**: Compatible with open-source and commercial use

## Best Practices

### Implementation Guidelines

1. **Precision Selection**: Choose appropriate precision for use case (5 is typically sufficient)
2. **Error Handling**: Always wrap encode/decode operations in try-catch blocks
3. **Memory Management**: Process large polylines in chunks when possible
4. **Validation**: Validate input coordinates before encoding
5. **Caching**: Cache encoded polylines for frequently accessed routes

### Performance Optimization

1. **Batch Processing**: Process multiple polylines in single operations
2. **Precision Optimization**: Use minimum required precision to reduce string length
3. **Memory Reuse**: Reuse coordinate arrays when possible
4. **String Handling**: Use efficient string concatenation methods
5. **BigInt Usage**: Only use BigInt when necessary for very large coordinates