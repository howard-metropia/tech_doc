# TSP API SharedBike Service Documentation

## 🔍 Quick Summary (TL;DR)
The SharedBike service integrates bike-sharing systems (Bcycle/YouBike) into multi-modal route planning by finding optimal station pairs, calculating walking distances, validating timing conditions, and transforming cycling segments into detailed walk-bike-walk sequences.

**Keywords:** bike-sharing | multi-modal-routing | station-pairing | distance-calculation | route-transformation | gbfs-integration | timing-validation | first-last-mile

**Primary use cases:** Finding nearest bike stations, calculating optimal station pairs, transforming cycle segments into walk-bike-walk routes, validating timing feasibility, integrating with multi-modal trip planning

**Compatibility:** Node.js >= 16.0.0, MongoDB for station data, GBFS (General Bikeshare Feed Specification) integration, complex route transformation logic

## ❓ Common Questions Quick Index
- **Q: What bike systems are supported?** → Bcycle and YouBike with GBFS standard data
- **Q: How are station pairs selected?** → Shortest combined distance (walk + bike + walk)
- **Q: What timing conditions exist?** → Three validation rules: walking speed, original time + 10min, original time × 1.25
- **Q: How are routes transformed?** → Cycle segments become 3-part sequences: walk to station, bike ride, walk from station
- **Q: What distance calculations are used?** → Haversine formula for precise geographic distance
- **Q: How is timing managed?** → Different logic for first-mile vs last-mile segments

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **smart bike-sharing planner** that takes a route where you're supposed to ride a bike and figures out the best way to use shared bikes instead. It finds the nearest bike stations, makes sure the timing works out, and breaks your bike ride into three parts: walk to get a bike, ride the bike, and walk to your final destination.

**Technical explanation:** 
A sophisticated route transformation service that converts abstract cycling segments into practical shared bike usage by finding optimal station pairs, validating timing constraints, and generating detailed multi-segment routes with precise distance calculations and time management for seamless multi-modal trip planning.

**Business value explanation:**
Enables integration with bike-sharing systems, improves last-mile connectivity for public transit, supports sustainable transportation options, enhances user experience with practical routing solutions, and provides partnerships opportunities with bike-sharing operators.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/sharedBike.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with MongoDB/Mongoose
- **Type:** Bike-Sharing Route Transformation Service
- **File Size:** ~18.4 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex geometric calculations and route logic)

**Dependencies:**
- `@app/src/models/GbfsStation`: GBFS station data model (**Critical**)
- MongoDB geospatial queries for station finding (**Critical**)
- Complex route section transformation logic (**High**)

## 📝 Detailed Code Analysis

### Core Distance Calculation

### getDistance Function
**Purpose:** Calculates precise geographic distance using Haversine formula

```javascript
getDistance(pointA, pointB) {
  if (pointA.lat == pointB.lat && pointA.lng == pointB.lng) {
    return 0;
  }
  
  const radiusALat = this.rad(pointA.lat);
  const radiusBLat = this.rad(pointB.lat);
  const a = radiusALat - radiusBLat;
  const b = this.rad(pointA.lng) - this.rad(pointB.lng);
  
  let s = 2 * Math.asin(
    Math.sqrt(
      Math.pow(Math.sin(a / 2), 2) +
      Math.cos(radiusALat) * Math.cos(radiusBLat) * Math.pow(Math.sin(b / 2), 2)
    )
  );
  
  s = s * 6378137.0; // WGS84 Earth radius in meters
  return Math.round(s * 10000) / 10000;
}
```
- Uses WGS84 standard Earth radius for accuracy
- Handles edge case of identical coordinates
- Returns distance in meters with precision

### Route Transformation Pipeline

### parseRoutes Function
**Purpose:** Transforms entire route data by processing first-mile and last-mile cycling segments

```javascript
async parseRoutes(data) {
  const tempJson = [];
  
  for (const index in data.routes) {
    let bikeCondition = 0;
    const route = data.routes[index];
    let tempRoutes = [];
    
    // First mile processing
    if (route.sections[0].type == 'cycle') {
      const origin = route.sections[0].departure.place.location;
      const startNode = route.sections[0].arrival.place.location;
      const firstMileLength = route.sections[0].travelSummary.length;
      const departureTime = route.sections[1].departure.time;
      const duration = route.sections[0].travelSummary.duration;
      
      const firstMileSections = await this.getStationsPair(
        origin, startNode, firstMileLength, departureTime, duration, 'firstNode'
      );
      
      if (firstMileSections.length === 3) {
        firstMileSections.push(JSON.parse(JSON.stringify(route.sections[1])));
        tempRoutes = firstMileSections;
        bikeCondition++;
      }
    }
    
    // Last mile processing (similar logic with complex section handling)
    // ... detailed last mile processing
    
    if (bikeCondition) {
      tempJson.push(tempSections);
    }
  }
  
  return tempJson;
}
```

### Station Finding with Geospatial Queries

### findNearSharedBikeStation Function
**Purpose:** Finds bike stations within radius using MongoDB geospatial indexing

```javascript
async findNearSharedBikeStation(point, maxDistance, addition) {
  const startNear = {
    StationLocation: {
      $near: {
        $geometry: {
          type: 'Point',
          coordinates: [point.lng, point.lat], // GeoJSON format [lng, lat]
        },
        $maxDistance: 500, // meters
      },
    },
  };
  
  const stations = await GbfsStation.find(startNear).exec();
  return stations;
}
```
- Uses MongoDB $near operator for efficient spatial queries
- Fixed 500-meter maximum search radius
- Returns stations sorted by distance

### Optimal Station Pair Selection

### getStationsPair Function
**Purpose:** Finds optimal station pair with comprehensive timing validation

```javascript
async getStationsPair(pointA, pointB, length, departureTime, duration, node) {
  // Timing validation conditions
  const bikeConditionA = Math.round((length / 3) * 3600); // Walking speed calculation
  const bikeConditionB = duration + 600; // Original time + 10 minutes
  const bikeConditionC = Math.round(duration * 1.25); // Original time × 1.25
  const radius = Math.min(400, length / 2);
  
  const stationsA = await this.findNearSharedBikeStation(pointA, radius, {
    availableRentBikes: true,
  });
  const stationsB = await this.findNearSharedBikeStation(pointB, radius, {
    availableReturnBikes: true,
  });
  
  let shortestLength = 0;
  
  // Double loop to find optimal station pair
  stationsA.forEach((a) => {
    const aLength = this.getDistance(
      { lat: pointA.lat, lng: pointA.lng },
      { lat: a.StationLocation.coordinates[1], lng: a.StationLocation.coordinates[0] }
    );
    
    stationsB.forEach((b) => {
      if (a.StationLocation.coordinates[1] == b.StationLocation.coordinates[1] &&
          a.StationLocation.coordinates[0] == b.StationLocation.coordinates[0]) {
        return; // Skip same station
      }
      
      const bLength = this.getDistance(
        { lat: pointB.lat, lng: pointB.lng },
        { lat: b.StationLocation.coordinates[1], lng: b.StationLocation.coordinates[0] }
      );
      
      const bikeLength = this.getDistance(
        { lat: a.StationLocation.coordinates[1], lng: a.StationLocation.coordinates[0] },
        { lat: b.StationLocation.coordinates[1], lng: b.StationLocation.coordinates[0] }
      );
      
      const pathLength = aLength + bLength + bikeLength;
      
      if (shortestLength == 0 || shortestLength > pathLength) {
        shortestLength = pathLength;
        // Store optimal station pair and generate sections
      }
    });
  });
  
  // Validate timing conditions
  const totalDuration = aWalkSection.section.travelSummary.duration +
                       cycleSection.section.travelSummary.duration +
                       bWalkSection.section.travelSummary.duration;
  
  if (totalDuration <= bikeConditionA && 
      (totalDuration <= bikeConditionB || totalDuration <= bikeConditionC)) {
    return [aWalkSection.section, cycleSection.section, bWalkSection.section];
  }
  
  return [];
}
```

### Section Generation

### formatJsonSection Function
**Purpose:** Creates standardized route sections with proper timing

```javascript
formatJsonSection(type, pair, length, departureTime, node, speed) {
  switch (type) {
    case 'pedestrian': speed = 3; break;  // 3 km/h
    case 'cycle': speed = 10; break;      // 10 km/h
    case 'drive': speed = 45; break;      // 45 km/h
  }
  
  const duration = Math.floor(this.distance2sec(length, speed));
  let arrivalTime;
  
  if (node === 'firstNode') {
    arrivalTime = departureTime;
    departureTime = departureTime - duration; // Backward time calculation
  } else if (node === 'lastNode') {
    arrivalTime = departureTime + duration; // Forward time calculation
  }
  
  const section = {
    type,
    actions: [
      { action: 'depart', duration: Math.floor(duration) },
      { action: 'arrive', duration: 0 }
    ],
    travelSummary: {
      duration: Math.floor(duration),
      length: Math.floor(length)
    },
    departure: {
      time: departureTime,
      place: {
        type: pair.a.type,
        location: { lat: pair.a.lat, lng: pair.a.lng }
      }
    },
    arrival: {
      time: arrivalTime,
      place: {
        type: pair.b.type,
        location: { lat: pair.b.lat, lng: pair.b.lng }
      }
    },
    transport: {
      mode: type,
      agency: { name: 'Bcycle', type: '1.0' }
    }
  };
  
  return { section, departureTime, arrivalTime };
}
```

### Timing Validation Logic

**Three Timing Conditions:**
1. **Walking Speed Rule:** `(length / 3) * 3600` - Time if walking entire distance at 3 km/h
2. **Buffer Rule:** `duration + 600` - Original cycling time plus 10-minute buffer
3. **Multiplier Rule:** `duration * 1.25` - Original cycling time multiplied by 1.25

**Validation:** Shared bike route must be faster than walking AND satisfy at least one buffer rule

## 🚀 Usage Methods

### Basic Route Transformation
```javascript
const sharedBikeService = require('@app/src/services/sharedBike');

// Transform routes with cycling segments
const originalRoutes = {
  routes: [
    {
      sections: [
        {
          type: 'cycle',
          departure: { place: { location: { lat: 29.7604, lng: -95.3698 } } },
          arrival: { place: { location: { lat: 29.7500, lng: -95.3600 } } },
          travelSummary: { length: 1200, duration: 720 }
        }
      ],
      transfers: 0,
      generalized_cost: 1000
    }
  ]
};

const transformedRoutes = await sharedBikeService.parseRoutes(originalRoutes);
console.log('Transformed routes:', transformedRoutes.length);
```

### Advanced Station Analysis
```javascript
class BikeShareAnalyzer {
  constructor() {
    this.sharedBikeService = require('@app/src/services/sharedBike');
  }

  async analyzeStationCoverage(origin, destination, maxRadius = 500) {
    try {
      // Find stations near origin and destination
      const originStations = await this.sharedBikeService.findNearSharedBikeStation(
        origin, maxRadius, { availableRentBikes: true }
      );
      
      const destStations = await this.sharedBikeService.findNearSharedBikeStation(
        destination, maxRadius, { availableReturnBikes: true }
      );
      
      // Calculate coverage metrics
      const analysis = {
        origin: {
          coordinates: origin,
          nearbyStations: originStations.length,
          stations: originStations.map(station => ({
            name: station.name,
            distance: this.sharedBikeService.getDistance(
              origin,
              {
                lat: station.StationLocation.coordinates[1],
                lng: station.StationLocation.coordinates[0]
              }
            ),
            availableBikes: station.num_bikes_available || 0
          }))
        },
        destination: {
          coordinates: destination,
          nearbyStations: destStations.length,
          stations: destStations.map(station => ({
            name: station.name,
            distance: this.sharedBikeService.getDistance(
              destination,
              {
                lat: station.StationLocation.coordinates[1],
                lng: station.StationLocation.coordinates[0]
              }
            ),
            availableDocks: station.num_docks_available || 0
          }))
        },
        viability: {
          bothEndsHaveStations: originStations.length > 0 && destStations.length > 0,
          totalPossiblePairs: originStations.length * destStations.length,
          recommendation: this.generateViabilityRecommendation(originStations, destStations)
        }
      };
      
      return analysis;
    } catch (error) {
      console.error('Station coverage analysis failed:', error);
      throw error;
    }
  }

  generateViabilityRecommendation(originStations, destStations) {
    if (originStations.length === 0 && destStations.length === 0) {
      return 'No bike stations available at either origin or destination';
    } else if (originStations.length === 0) {
      return 'No bike stations available near origin - consider walking to nearest station';
    } else if (destStations.length === 0) {
      return 'No bike stations available near destination - consider alternative transport for last mile';
    } else if (originStations.length >= 2 && destStations.length >= 2) {
      return 'Excellent bike share coverage - multiple station options available';
    } else {
      return 'Limited but viable bike share coverage - route feasible with shared bikes';
    }
  }

  async calculateOptimalRoute(origin, destination, constraints = {}) {
    const {
      maxWalkDistance = 400,
      preferredCycleSpeed = 10,
      timeLimit = null
    } = constraints;
    
    try {
      // Simulate getting station pairs (simplified version of getStationsPair)
      const radius = Math.min(maxWalkDistance, 400);
      
      const originStations = await this.sharedBikeService.findNearSharedBikeStation(
        origin, radius, { availableRentBikes: true }
      );
      
      const destStations = await this.sharedBikeService.findNearSharedBikeStation(
        destination, radius, { availableReturnBikes: true }
      );
      
      let optimalRoute = null;
      let shortestTime = Infinity;
      
      // Find optimal station pair
      for (const originStation of originStations) {
        for (const destStation of destStations) {
          const originStationCoords = {
            lat: originStation.StationLocation.coordinates[1],
            lng: originStation.StationLocation.coordinates[0]
          };
          
          const destStationCoords = {
            lat: destStation.StationLocation.coordinates[1],
            lng: destStation.StationLocation.coordinates[0]
          };
          
          // Calculate distances
          const walkToStation = this.sharedBikeService.getDistance(origin, originStationCoords);
          const bikeRide = this.sharedBikeService.getDistance(originStationCoords, destStationCoords);
          const walkFromStation = this.sharedBikeService.getDistance(destStationCoords, destination);
          
          // Calculate times
          const walkToTime = this.sharedBikeService.distance2sec(walkToStation, 3);
          const bikeTime = this.sharedBikeService.distance2sec(bikeRide, preferredCycleSpeed);
          const walkFromTime = this.sharedBikeService.distance2sec(walkFromStation, 3);
          const totalTime = walkToTime + bikeTime + walkFromTime;
          
          // Check time constraint
          if (timeLimit && totalTime > timeLimit) continue;
          
          // Update optimal route if this is better
          if (totalTime < shortestTime) {
            shortestTime = totalTime;
            optimalRoute = {
              totalTime: Math.round(totalTime),
              totalDistance: Math.round(walkToStation + bikeRide + walkFromStation),
              segments: [
                {
                  type: 'walk',
                  from: 'origin',
                  to: originStation.name,
                  distance: Math.round(walkToStation),
                  duration: Math.round(walkToTime)
                },
                {
                  type: 'bike',
                  from: originStation.name,
                  to: destStation.name,
                  distance: Math.round(bikeRide),
                  duration: Math.round(bikeTime)
                },
                {
                  type: 'walk',
                  from: destStation.name,
                  to: 'destination',
                  distance: Math.round(walkFromStation),
                  duration: Math.round(walkFromTime)
                }
              ],
              stationPair: {
                pickup: {
                  name: originStation.name,
                  coordinates: originStationCoords,
                  availableBikes: originStation.num_bikes_available || 0
                },
                dropoff: {
                  name: destStation.name,
                  coordinates: destStationCoords,
                  availableDocks: destStation.num_docks_available || 0
                }
              }
            };
          }
        }
      }
      
      return {
        feasible: optimalRoute !== null,
        route: optimalRoute,
        alternativesAnalyzed: originStations.length * destStations.length
      };
    } catch (error) {
      console.error('Optimal route calculation failed:', error);
      throw error;
    }
  }
}

// Usage
const analyzer = new BikeShareAnalyzer();

const coverage = await analyzer.analyzeStationCoverage(
  { lat: 29.7604, lng: -95.3698 },
  { lat: 29.7500, lng: -95.3600 }
);

const optimal = await analyzer.calculateOptimalRoute(
  { lat: 29.7604, lng: -95.3698 },
  { lat: 29.7500, lng: -95.3600 },
  { maxWalkDistance: 300, timeLimit: 1800 }
);
```

## 📊 Output Examples

### Transformed Route Response
```json
[
  {
    "transfers": 1,
    "generalized_cost": 1200,
    "start_time": 1619875200,
    "end_time": 1619876400,
    "travel_time": 1200,
    "sections": [
      {
        "type": "pedestrian",
        "travelSummary": {
          "duration": 180,
          "length": 150
        },
        "departure": {
          "time": 1619875200,
          "place": {
            "type": "place",
            "location": {"lat": 29.7604, "lng": -95.3698}
          }
        },
        "arrival": {
          "time": 1619875380,
          "place": {
            "type": "station",
            "name": "Main St Station",
            "location": {"lat": 29.7600, "lng": -95.3700}
          }
        }
      },
      {
        "type": "cycle",
        "travelSummary": {
          "duration": 480,
          "length": 1000
        },
        "transport": {
          "mode": "cycle",
          "agency": {"name": "Bcycle", "type": "1.0"}
        }
      },
      {
        "type": "pedestrian",
        "travelSummary": {
          "duration": 120,
          "length": 100
        }
      }
    ]
  }
]
```

### Station Coverage Analysis
```json
{
  "origin": {
    "coordinates": {"lat": 29.7604, "lng": -95.3698},
    "nearbyStations": 3,
    "stations": [
      {
        "name": "Main St Station",
        "distance": 145.2,
        "availableBikes": 8
      }
    ]
  },
  "destination": {
    "coordinates": {"lat": 29.7500, "lng": -95.3600},
    "nearbyStations": 2,
    "stations": [
      {
        "name": "Business District Station",
        "distance": 87.5,
        "availableDocks": 12
      }
    ]
  },
  "viability": {
    "bothEndsHaveStations": true,
    "totalPossiblePairs": 6,
    "recommendation": "Excellent bike share coverage - multiple station options available"
  }
}
```

## ⚠️ Important Notes

### Geospatial and Distance Calculations
- **Haversine Formula:** Precise geographic distance calculation using WGS84 Earth radius
- **MongoDB Geospatial:** Efficient station finding with $near operator and geospatial indexing
- **Coordinate Format:** GeoJSON standard [longitude, latitude] for MongoDB queries
- **Distance Precision:** Four decimal place precision for accurate routing

### Timing and Validation Logic
- **Three Timing Rules:** Walking speed baseline, buffer time allowance, and multiplier validation
- **Directional Processing:** Different time calculation logic for first-mile vs last-mile segments
- **Speed Assumptions:** 3 km/h walking, 10 km/h cycling for realistic time estimates
- **Feasibility Filtering:** Routes rejected if timing constraints not met

### Route Transformation Complexity
- **Section Reconstruction:** Complex logic to handle varying numbers of route segments
- **Station Pair Optimization:** Brute force comparison to find shortest combined distance
- **Time Synchronization:** Careful management of departure/arrival times across segments
- **Agency Integration:** Standardized Bcycle agency attribution for bike segments

### Performance and Scalability
- **Database Optimization:** Geospatial indexing for efficient station queries
- **Search Radius Limits:** Fixed 500m maximum to prevent excessive computation
- **Station Filtering:** Availability checks for bikes and docking spaces
- **Memory Management:** Deep cloning of route sections to prevent data corruption

## 🔗 Related File Links

- **GBFS Station Model:** `allrepo/connectsmart/tsp-api/src/models/GbfsStation.js`
- **Bike Stations Model:** `allrepo/connectsmart/tsp-api/src/models/bikeStations.js`
- **Route Planning Services:** Integration with route planning and transformation services

---
*This service provides comprehensive bike-sharing integration with sophisticated station pairing and route transformation for multi-modal transportation in the TSP platform.*