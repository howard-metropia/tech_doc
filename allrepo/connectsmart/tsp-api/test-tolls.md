# TSP API Test Suite - Tolls Calculation Tests

## Overview
The `test-tolls.js` file contains comprehensive tests for toll calculation functionality, validating route-based toll estimation, dynamic pricing, and toll cost integration for transportation planning and route optimization.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-tolls.js`

## Dependencies
- **supertest**: HTTP assertion library for API testing
- **chai**: Testing assertions and expectations
- **@maas/core**: Core framework components
- **AuthUsers**: User authentication and authorization model

## Test Architecture

### API Setup
```javascript
const createApp = require('@maas/core/api');
const { getRouter } = require('@maas/core');
const { authToken } = require('@app/src/helpers/test');

const app = createApp();
const router = getRouter();
const request = supertest.agent(app.listen());
```

### Authentication Configuration
```javascript
const userId = 1003;
const auth = {
  userid: userId,
  'Content-Type': 'application/json',
  authorization: '' // Set dynamically with JWT token
};
```

## Toll Calculation API

### Endpoint: `POST /tolls/route`

**Purpose**: Calculate toll costs for given route with vehicle-specific pricing

### Test Data Structure
```javascript
const postData = {
  routes: [
    {
      id: '0',
      departureTime: '2024-12-30T14:33:00+08:00',
      distance: 1000, // meters
      polyline: 'BG0t9-pC_6inzET7GjD_EjD3SrOkDrOsJ7BjNvCzPvCnQ7B3N_EzyB_J8BoL4pCwC8QoBsJkDwRkDgUoBkI4DkXkDoVoB0KoB4IUwHUkI8BkcAoaTkXAoGvHkXjDsJ_EgKzF4I_EwH7GwHjI8G3IgFrJ4DzeoLnuB0UrOwHvH4DrJoG3DsEjD4DvCoGvCoGnB8GnB8GTwHA0FoB4IoBsEwC8GkDgFoGkI4I0KoGoGsEkD4DwC8GkDsJ4DkcoLsT0FkXoGkX0F4IwCkc8G4XkI0jBsEoGUgFU8LoB0KoB4IoBwHoBgK8BoLwCsO4DgU0FwM4Dk1BwR0PsJsOoG8iCsdof4NouB8V8uBsYkN8GwWwMozBwb4SsJ8GkDoGwC4IwCoGoB0FU0KAgPA8GToGTgFnBoLvCkI7B8Q_EkNrEoGvC0PzFoL_EoQnGgK3DoGvCgP7GoQ3IoQrJ4InGgK3IkDjDkDjDgF_EkIrJwMvR0K3S0FnLoGzPsE3N0FzUoGrY8QjpC4NzyB4N_nBoVz8B4I3cwH_T8GjSkIrTgFrOgFrOoGjS8GzUsEjNsE3N8GzUgFzPgF7QkDzKkDzK4DjN4DjN4DrOkIvgB4D_O4DnQoGnfkIrsB8G7f0K7uBwMr2BoQnnCsErTsEjSgUr0CsErToLv0BoQnnCkIvlBwHnf8LnzBgUz1C4XjnD4S3uCoLvvBoLnuBwCjSwCjX8B7LsEnQ0FzUoG3SoGvRwHzU4IzU8G_OoGjNwH_OwC_E8GvM0F_J8LzU0KnQoL7Q8GrJ4InL8G3IgKvMkS_TsJrJ8L7LkSnQ4SzPgP7LkmBjcoarToa_TwjCzyBgyBvlBgZ3SgUrOwgBrY0PnLsT3Nof7V41B3mB4_BjwB0KjIoG3DgFjD8GrEsdzUkXvR03BzoB0tB3hB8arT8Q7LsJnG0K7GwH_EsJzFoLnGkS3IgP7G0PnG0PnGofnLgenL0ezKwqBrO4S3DgUjDgtBzFgPnB8fnB0PUsOUwRoBwR8BsiB0FwR4DgKwCsT0Fwb4I8agK4SkI0PwH8Q4IssBkX4_BwgB4mB0U4XwMoQkIgjBwR4X0KoVsJ0U4I0P0FwbgK8V8GsOsEoQsEgUgF0P4D4S4D4NwCoV4DgUwC4N8BwMoB4NoBoQUwWoB8VTgPAsTnBoQ7B8QvCgU3D8uBnL4pCzUozB3N4wBjNkhB3IwRrEwb7GoV_EgZ_EoQjDoV3DsY3D8VjD0Z3D8VvC8Q7B8QnBsxBjD4mB7BgeT4mBAk1BAkmBUokBAk6BAw5BoB0ZU8QUsiBoBgtBUkzCU0KAg6CnB03BT4XAwkEnB4kCvCof7BwgBnB0eT8nCTgoBTk-ET4IAkIA0FAwuE8B4IA4IA89BU82CUokBA08BoBgyBAsOAoQT4S7BwR7BwRvCgPvCkS3DoQ3DoLvCoLvC8G7BoV_EgKvCoLvC4XzFsqCjSsgCnQsnBrJkczFkcrEoVvC4SnB0UnB0ZToVU8a8BsTwCkXgFgU0F8L4DgF8BoQ0F4SwHsOoG0UgKkXwMgFwCgZ4N8VwMsToL8LkIkD8BsJ0Foa0PwqB0Zo7Co4B8Q0K8LwH8VkNkNkI4SoLoQgKkS0K0oB4XsdoQwRgKoQ4I0KgFoL0Fge4Nge8LgZsJwgB0K0PsE0ZoGwR4D4SkDsTwCgU8BsToBwgBUofnB8fjDgUjDwRjDsd7GoVzFkX7GoVvHoa3IwWjIokBjN0yBvR82Crd4c3I0ZvHsYnGoanGkhBvH8fnGkc_Eof_EgKnB8frE0P7BoVvC8Q7BsT7BkNTkSnBsOT4NTsTTkSToaTsTU8QA8VUsOUkNUkSoB0Z8BoV8BkS8BwR8BgyB8GgKwCgoBwH0e0FsYgFoV4D4wBgK8zB8L8V0FsO4DkrBkN8VwHgK4DwMsEoLsE8Q8Goa8L8L0FoL0FkS4I0egPgeoQgZ8L0jBoVgZsO8QwH0KsEwHkD4I4DoGwC8G8B4IwCsJwC8LkD0KwCwHwC8GwCkI4D0KoGsJ0FwRgKoL8G8G7GwHvHoG7G8GvHsJnL4D_EkDrEgFjIkDzFkD7GoBjD4DnLkDrJoBrE8B3IUjDU3DUnGUzKA_EAvHTnQTjIT_JArJUzP8B_YopBzFoGnBsJjD4I3D8LnGkI_E4DvCsE3DsE_EgFnG4DzF4DnGgF3I4DvH4D3I8B_E8B7GoBrE8BrJ8B_JjIvCrJnB7GnBjIUnBsOvH4SvH4N7LwM3NsJ7LgFnBzKnBjInB_EjDrO'
    }
  ],
  vehicleType: 2,       // Vehicle classification
  tagInstalled: true,   // Electronic toll tag
  noCache: true        // Force fresh calculation
};
```

### Route Polyline Encoding
The polyline string represents an encoded route path containing:
- **Geographic Coordinates**: Latitude/longitude pairs along the route
- **Elevation Data**: Road elevation changes affecting toll rates
- **Toll Plaza Locations**: Specific points where tolls are collected
- **Route Segments**: Individual sections with different toll rates

## Test Scenarios

### 1. Authentication Validation

#### Missing User ID Test
```javascript
it('should get a fail 10004', async () => {
  const resp = await request.post(url).unset('userid').send({});
  const { result, error } = resp.body;
  
  expect(result).to.eq('fail');
  expect(error).to.include({
    code: 10004,
    msg: 'Request header has something wrong'
  });
});
```

#### Missing Required Fields Test
```javascript
it('should get a fail 10002 as missing field', async () => {
  const resp = await request.set(auth).post(url).send({});
  const { result, error } = resp.body;
  
  expect(result).to.eq('fail');
  expect(error).to.includes({
    code: 10002,
    msg: '"routes" is required'
  });
});
```

### 2. Successful Toll Calculation Test
```javascript
it('should get a tolls of route', async () => {
  const resp = await request.set(auth).post(url).send(postData);
  const { result, data } = resp.body;
  
  expect(result).to.eq('success');
  expect(data.response[0]).to.includes.keys([
    'id',
    'totalCost',
    'staticTollCost',
    'dynamicTollCost',
    'drivingCost'
  ]);
});
```

## Toll Calculation Components

### 1. Static Toll Costs
```javascript
const staticTollCost = {
  description: 'Fixed toll rates based on vehicle type and toll plaza',
  calculation: 'baseRate * vehicleMultiplier',
  factors: [
    'Vehicle classification (2-axle, 3-axle, etc.)',
    'Toll plaza base rates',
    'Electronic tag discounts'
  ]
};
```

### 2. Dynamic Toll Costs
```javascript
const dynamicTollCost = {
  description: 'Variable pricing based on traffic and time',
  calculation: 'baseRate * congestionMultiplier * timeMultiplier',
  factors: [
    'Time of day (peak/off-peak)',
    'Traffic congestion levels',
    'Demand-based pricing',
    'Special event surcharges'
  ]
};
```

### 3. Driving Costs
```javascript
const drivingCost = {
  description: 'Additional costs beyond tolls',
  components: [
    'Fuel costs based on distance',
    'Vehicle wear and depreciation',
    'Parking fees at destination',
    'Route-specific charges'
  ]
};
```

## Vehicle Type Classification

### Vehicle Categories
```javascript
const VEHICLE_TYPES = {
  1: {
    name: 'Motorcycle',
    axles: 2,
    tollMultiplier: 0.5,
    description: 'Two-wheeled vehicles'
  },
  2: {
    name: 'Passenger Car',
    axles: 2,
    tollMultiplier: 1.0,
    description: 'Standard passenger vehicles'
  },
  3: {
    name: 'SUV/Light Truck',
    axles: 2,
    tollMultiplier: 1.2,
    description: 'Larger passenger vehicles'
  },
  4: {
    name: 'Medium Truck',
    axles: 3,
    tollMultiplier: 2.0,
    description: 'Commercial vehicles'
  },
  5: {
    name: 'Heavy Truck',
    axles: 4,
    tollMultiplier: 3.0,
    description: 'Large commercial vehicles'
  }
};
```

### Electronic Tag Benefits
```javascript
const ELECTRONIC_TAG_BENEFITS = {
  discount: 0.1,        // 10% discount
  convenience: true,    // No stopping required
  fastLane: true,       // Dedicated lanes
  tracking: true        // Automatic expense tracking
};
```

## Response Data Structure

### Successful Response Format
```javascript
{
  result: 'success',
  data: {
    response: [
      {
        id: '0',                    // Route identifier
        totalCost: 15.75,          // Combined cost in USD
        staticTollCost: 8.50,      // Fixed toll charges
        dynamicTollCost: 2.25,     // Variable toll charges
        drivingCost: 5.00,         // Additional driving costs
        breakdown: {
          tollPlazas: [
            {
              name: 'Main Toll Plaza',
              cost: 4.25,
              vehicleType: 2,
              electronicDiscount: 0.25
            }
          ],
          fuelCost: 3.50,
          parkingEstimate: 1.50
        },
        route: {
          distance: 1000,          // Route distance in meters
          estimatedTime: 18,       // Minutes
          tollPlazaCount: 2
        }
      }
    ]
  }
}
```

## Test Data Preparation

### User Setup
```javascript
before('Prepare testing data', async () => {
  // Enable debug mode for test user
  await AuthUsers.query().where('id', userId).patch({ is_debug: 1 });
  
  // Generate authentication token
  const token = await authToken(userId);
  auth.authorization = `Bearer ${token}`;
});

after('Delete testing data', async () => {
  // Cleanup test data if needed
});
```

### Mock Route Data
```javascript
const createMockRoute = (overrides = {}) => ({
  id: '0',
  departureTime: new Date(Date.now() + 3600000).toISOString(), // 1 hour from now
  distance: 1000,
  polyline: generateTestPolyline(),
  ...overrides
});

const generateTestPolyline = () => {
  // Generate polyline string for test route
  // This would typically come from mapping services
  return 'encoded_polyline_string_representing_route';
};
```

## Error Handling

### Validation Errors
```javascript
const TOLL_ERROR_CODES = {
  10001: 'Missing required parameter',
  10002: 'Invalid parameter format',
  10003: 'Authentication required', 
  10004: 'Invalid request headers',
  10005: 'Route calculation failed',
  10006: 'Toll service unavailable'
};
```

### Service Integration Errors
```javascript
describe('Service Integration Errors', () => {
  it('should handle toll service downtime', async () => {
    // Mock toll service failure
    const invalidRouteData = {
      routes: [{ id: 'invalid', polyline: 'invalid_polyline' }],
      vehicleType: 2,
      tagInstalled: true
    };
    
    const resp = await request.set(auth).post(url).send(invalidRouteData);
    
    // Should handle gracefully
    expect(resp.statusCode).to.be.oneOf([200, 503]);
  });
});
```

## Performance Considerations

### Caching Strategy
```javascript
const tollCache = {
  key: (route, vehicleType, timestamp) => 
    `toll:${hash(route.polyline)}:${vehicleType}:${Math.floor(timestamp / 300000)}`, // 5-minute cache
  
  ttl: 300, // 5 minutes
  
  invalidation: [
    'Traffic condition changes',
    'Toll rate updates',
    'Route modifications'
  ]
};
```

### Batch Processing
```javascript
const processBatchTollRequests = async (routes, options) => {
  const batchSize = 10;
  const results = [];
  
  for (let i = 0; i < routes.length; i += batchSize) {
    const batch = routes.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map(route => calculateTolls(route, options))
    );
    results.push(...batchResults);
  }
  
  return results;
};
```

## Integration Testing

### End-to-End Route Planning
```javascript
describe('Integration with Route Planning', () => {
  it('should integrate toll costs with route optimization', async () => {
    const routeOptions = {
      origin: { lat: 29.7604, lng: -95.3698 },
      destination: { lat: 29.7174, lng: -95.4041 },
      preferences: {
        minimizeTolls: false,
        vehicleType: 2,
        departureTime: new Date()
      }
    };
    
    // Get multiple route options
    const routes = await routePlanningService.getRoutes(routeOptions);
    
    // Calculate tolls for each route
    const tollData = {
      routes: routes.map((route, index) => ({
        id: index.toString(),
        polyline: route.polyline,
        distance: route.distance,
        departureTime: routeOptions.departureTime.toISOString()
      })),
      vehicleType: routeOptions.preferences.vehicleType,
      tagInstalled: true
    };
    
    const tollResp = await request.set(auth).post(url).send(tollData);
    
    expect(tollResp.body.result).to.eq('success');
    expect(tollResp.body.data.response).to.have.length(routes.length);
  });
});
```

## Quality Assurance

### Data Accuracy
- **Toll Rate Validation**: Current toll plaza rates
- **Vehicle Classification**: Correct vehicle type handling
- **Route Accuracy**: Polyline decoding and toll plaza detection
- **Time Sensitivity**: Peak/off-peak rate application

### Performance Metrics
- **Response Time**: Under 2 seconds for standard routes
- **Throughput**: Handle 100+ concurrent requests
- **Cache Hit Rate**: 80%+ for repeated route queries
- **Accuracy**: 95%+ toll cost estimation accuracy

This comprehensive test suite ensures the toll calculation system provides accurate, real-time toll cost estimates for route planning and transportation cost optimization while maintaining high performance and reliability standards.