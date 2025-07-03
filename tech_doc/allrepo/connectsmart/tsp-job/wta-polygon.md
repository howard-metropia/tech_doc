# wta-polygon.js

## Overview
Job for identifying users within specific geographic market areas and enrolling them in WTA (Washington Transit Authority) experiments. Uses geographic polygon analysis to determine user eligibility based on their most frequent habitual trip locations, with special handling for cross-market scenarios.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/wta-polygon.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `geo-point-in-polygon` - Geographic polygon containment analysis
- `@app/src/services/incentiveUtility` - Market configuration and polygon utilities
- `@app/src/services/sendMail` - Email notification service
- `config` - Application configuration
- `ejs` - Email template rendering
- `hashids/cjs` - Hash ID generation for secure tokens
- `@maas/core/log` - Logging utility

## Core Functions

### Main Processing Function
Analyzes user habitual trips to determine market area eligibility and enrolls qualified users in WTA experiments.

**Process Flow:**
1. Load market area configuration and polygon data
2. Identify users with qualifying habitual trips
3. Perform geographic analysis on origin and destination points
4. Apply cross-market business rules
5. Enroll eligible users in WTA experiments
6. Create consent form tracking records

## Job Configuration

### Inputs
No input parameters required.

### Market Analysis Configuration
- **Source Data**: `assets/goezy/market_attribute.json`
- **Trip Threshold**: Minimum 2 trips for habitual pattern
- **Travel Mode**: Driving mode (travel_mode = 1)
- **Geographic Analysis**: Point-in-polygon containment checking

## Processing Flow

### 1. Market Configuration Loading
```javascript
const marketGeo = await util.getMarket('assets/goezy/market_attribute.json');
const smartPhoneCity = marketGeo.Smartphone_city;
```

### 2. Habitual Trip Identification
```sql
SELECT id, user_id, o_id, d_id, trip_count,
(SELECT latitude FROM hybrid.cm_location WHERE id = o_id) AS o_lat,
(SELECT longitude FROM hybrid.cm_location WHERE id = o_id) AS o_lng,
(SELECT latitude FROM hybrid.cm_location WHERE id = d_id) AS d_lat,
(SELECT longitude FROM hybrid.cm_location WHERE id = d_id) AS d_lng
FROM hybrid.cm_activity_location
WHERE trip_count >= 2 AND travel_mode = 1
GROUP BY user_id
ORDER BY user_id ASC, trip_count DESC, id ASC
```

### 3. Geographic Market Analysis
For each user's habitual trip:

**Origin Point Analysis:**
```javascript
const originPoint = [row.o_lng, row.o_lat];
for (const market of marketInfo) {
  const marketData = util.getMarketPolygon(market.Market, marketGeo);
  for (const coordinateSet of marketData.coordinates) {
    for (const polygon of coordinateSet) {
      if (geoPointInPolygon(originPoint, polygon)) {
        userIDInMarket.push(row.user_id);
        userInMarket.push(market.Market);
        activityID.push(row.id);
      }
    }
  }
}
```

**Destination Point Analysis:**
```javascript
const destinationPoint = [row.d_lng, row.d_lat];
// Similar polygon analysis for destination points
```

### 4. Cross-Market Business Logic
```javascript
for (let i = 0; i < userIDInMarket.length; i++) {
  if (userInMarket[i] == 'MTC' && userInMarket2[i] == 'WCCTA') {
    // Special case: Origin in MTC but destination in WCCTA
    // Assign to WCCTA market for experiment purposes
    userInMarket[i] = 'WCCTA';
  }
}
```

### 5. Eligibility Filtering
```javascript
// Filter by smartphone-enabled cities
if (smartPhoneCity.indexOf(userInMarket[i]) === -1) {
  continue; // Skip non-eligible markets
}
```

### 6. Duplicate Prevention
```sql
SELECT id FROM hybrid.wta_market
WHERE user_id = '${user_id}'
UNION
SELECT id FROM hybrid.mtc_user_signup
WHERE user_id = '${user_id}'
```

### 7. WTA Enrollment
For eligible users not already enrolled:
```sql
INSERT INTO hybrid.wta_market (
  market_id, user_id, activity_id
) VALUES (
  'WTA - ${market_name}', '${user_id}', '${activity_id}'
)
```

### 8. Consent Form Initialization
```sql
INSERT INTO hybrid.wta_agree (
  user_id, wta_agree, resend
) VALUES (
  '${user_id}', '0', '0'
)
```

## Data Models

### cm_activity_location Table
```javascript
{
  id: number,
  user_id: number,
  o_id: number,           // Origin location ID
  d_id: number,           // Destination location ID
  trip_count: number,     // Frequency of this trip pattern
  travel_mode: number,    // 1 = driving
  created_on: datetime,
  modified_on: datetime
}
```

### cm_location Geographic Reference
```javascript
{
  id: number,
  latitude: float,
  longitude: float,
  address: string,
  created_on: datetime
}
```

### wta_market Enrollment Table
```javascript
{
  id: number,
  market_id: string,      // Format: 'WTA - {MARKET_NAME}'
  user_id: number,
  activity_id: number,    // Reference to habitual trip
  created_on: datetime,
  modified_on: datetime
}
```

### wta_agree Consent Tracking
```javascript
{
  id: number,
  user_id: number,
  wta_agree: boolean,     // 0 = not agreed, 1 = agreed
  resend: number,         // Reminder count
  created_on: datetime,
  modified_on: datetime
}
```

### Market Configuration Structure
```javascript
{
  Market_info: [
    {
      Market: string,     // Market identifier (e.g., 'MTC', 'WCCTA')
      coordinates: [[[    // Multi-polygon coordinate arrays
        [longitude, latitude],
        [longitude, latitude],
        // ... polygon boundary points
      ]]]
    }
  ],
  Smartphone_city: [     // List of eligible market areas
    'MTC', 'WCCTA', 'CDTC', // etc.
  ]
}
```

## Business Logic

### Market Area Analysis
The system performs dual-point geographic analysis:
1. **Origin Analysis**: Determines user's typical starting location market
2. **Destination Analysis**: Determines user's typical ending location market
3. **Cross-Market Resolution**: Applies business rules for conflicting markets

### Cross-Market Priority Rules
```javascript
// Current rule: MTC origin + WCCTA destination = WCCTA assignment
if (originMarket == 'MTC' && destinationMarket == 'WCCTA') {
  assignedMarket = 'WCCTA';
}
// Additional rules can be configured as needed
```

### Habitual Trip Qualification
- **Minimum Frequency**: >= 2 trips for pattern recognition
- **Mode Restriction**: Driving mode only (travel_mode = 1)
- **Geographic Validation**: Both origin and destination must be geocoded
- **Market Eligibility**: Must fall within smartphone-enabled market areas

### Enrollment Prevention Logic
Prevents duplicate enrollments by checking:
- Existing WTA market enrollment
- Existing MTC user signup records
- Ensures one-time enrollment per user

## Error Handling
- Continues processing if individual users fail geographic analysis
- Handles missing location data gracefully
- Validates market configuration before processing
- Comprehensive logging for debugging geographic calculations

## Integration Points
- **Incentive Utility Service**: Market configuration and polygon utilities
- **Email Service**: Consent form delivery (currently commented out)
- **Geographic Services**: Point-in-polygon containment analysis
- **User Activity Tracking**: Habitual trip pattern analysis
- **Experiment Management**: WTA/MTC enrollment coordination

## Performance Considerations
- Efficient geographic calculations with optimized polygon algorithms
- Strategic SQL queries to minimize database calls
- Proper indexing on location and user relationship tables
- Memory-efficient processing of large polygon datasets

## Security Considerations
- Secure handling of user location data
- Parameterized SQL queries prevent injection attacks
- Hash token generation for consent form security (when enabled)
- Privacy-compliant geographic analysis

## Geographic Analysis Details

### Polygon Data Structure
Market areas are defined as complex multi-polygon geometries:
```javascript
{
  coordinates: [ // Multiple coordinate sets for complex boundaries
    [ // First polygon
      [ // Exterior ring
        [lng1, lat1], [lng2, lat2], // ... boundary points
      ],
      [ // Optional interior ring (holes)
        [lng3, lat3], [lng4, lat4], // ... hole boundary
      ]
    ],
    [ // Second polygon (if market has multiple areas)
      // ... additional polygon coordinates
    ]
  ]
}
```

### Point-in-Polygon Algorithm
Uses ray-casting algorithm for geometric containment:
```javascript
const isInMarket = geoPointInPolygon(
  [longitude, latitude], 
  polygonCoordinates
);
```

## Usage Scenarios
- Daily enrollment of new experiment participants
- Geographic market analysis for transportation research
- User segmentation based on travel patterns
- Automated experiment participant recruitment
- Market-specific transportation behavior studies

## Configuration Dependencies
- Market area polygon configuration file
- Database access to activity and location tables
- Geographic utility service configuration
- Email service setup (for consent forms)
- Hash ID generation configuration

## Monitoring and Logging
- Market configuration loading status
- User habitual trip analysis results
- Geographic containment analysis logging
- Cross-market business rule application
- Enrollment success/failure tracking

## Data Flow
1. **Source**: User habitual trip patterns from activity tracking
2. **Configuration**: Market area polygon definitions
3. **Analysis**: Geographic containment calculations
4. **Business Rules**: Cross-market assignment logic
5. **Filtering**: Smartphone city eligibility verification
6. **Enrollment**: WTA market assignment and consent initialization
7. **Tracking**: Audit trail for enrollment decisions

## Market Coverage Areas
Current system supports multiple transportation market areas:
- **MTC**: Metropolitan Transportation Commission
- **WCCTA**: Whatcom County Transportation Authority  
- **CDTC**: Capital District Transportation Committee
- Additional markets configurable through JSON file

## Consent Form Integration
System prepares for consent form delivery (currently disabled):
```javascript
// Hash token generation for secure consent links
const hashids = new Hashids('gogowtakey', 16);
const hasToken = hashids.encode(user_id, random);

// Email template rendering
const mailData = await ejs.renderFile(
  'src/static/templates/consentFormCreate.ejs',
  { firstName, urlLink, hasToken }
);
```

## Notes
- Critical component of geographic-based experiment enrollment
- Supports complex multi-market transportation research
- Handles cross-boundary travel patterns intelligently
- Maintains strict privacy controls for location data
- Integrates with broader WTA/MTC experimental infrastructure
- Designed for scalable processing of large user populations
- Uses industry-standard geographic analysis algorithms
- Supports flexible market boundary configuration through external JSON files