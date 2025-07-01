# twTransitFares.js Documentation

## 🔍 Quick Summary (TL;DR)

Service for calculating Taiwan public transit fares including TRA (Taiwan Railways), HSR (High-Speed Rail), MRT (Metro), city buses, and highway buses.

**Keywords:** Taiwan transit fares | TRA pricing | HSR fare | MRT fare | bus fare | public transport pricing | 台鐵票價 | 高鐵票價 | 捷運票價 | fare calculation

**Primary Use Cases:**
- Multi-modal route fare calculation
- Transit trip cost estimation
- Public transport fare aggregation

**Compatibility:** Node.js 14+, MongoDB models

## ❓ Common Questions Quick Index

- [How to calculate TRA train fares?](#usage-methods)
- [What transit types are supported?](#technical-specifications)
- [How are multi-leg fares calculated?](#detailed-code-analysis)
- [Why is fare showing as 0?](#important-notes)
- [How to get HSR standard fares?](#output-examples)
- [How to handle MRT transfer pricing?](#detailed-code-analysis)
- [What fare types are supported?](#functionality-overview)
- [How to troubleshoot missing fares?](#important-notes)

## 📋 Functionality Overview

**Non-technical explanation:** This service is like a fare calculator for Taiwan's public transportation system. Just as a ticket agent would calculate your total fare for a journey involving multiple trains or buses, this service automatically determines the cost for each segment of your trip across different transit systems.

**Technical explanation:** A fare calculation service that queries MongoDB collections for Taiwan transit fare data and applies appropriate pricing based on transit type, route, and ticket class, supporting TRA, HSR, MRT, city buses, and highway buses.

**Business value:** Enables accurate fare estimation for multi-modal trips, supporting transparent pricing and trip planning features for users navigating Taiwan's public transit network.

**System context:** Integrated with the intermodal routing service to provide complete trip cost calculations for routes involving multiple transit types.

## 🔧 Technical Specifications

- **File:** twTransitFares.js
- **Path:** /src/services/twTransitFares.js
- **Type:** Service class
- **Size:** ~7KB
- **Complexity:** Medium

**Dependencies:**
- `@app/src/models/TwTraFares` - Taiwan Railway fare data
- `@app/src/models/TwMrtFares` - MRT fare data
- `@app/src/models/TwHsrFares` - High-Speed Rail fare data
- `@app/src/models/TwHighwayBusFares` - Highway bus fare data

**MongoDB Collections:**
- TwTraFares - TRA fare matrix
- TwMrtFares - MRT station-to-station fares
- TwHsrFares - HSR fare tables
- TwHighwayBusFares - Highway bus route fares

## 📝 Detailed Code Analysis

**Main Methods:**

1. **getTraFares(index, index2, name, id)**
   - Calculates Taiwan Railway fares based on train type
   - Train types: 普悠瑪/太魯閣/自強 (index 0), 莒光 (index 5), 復興 (index 10), 普通 (index 15)

2. **getHsrFares(index, index2, oStation, dStation)**
   - Retrieves HSR fares for standard adult tickets
   - Filters: TicketType=1, FareClass=1, CabinClass=1

3. **getMrtFares(index, index2, oStation, dStation)**
   - Calculates MRT fares between stations
   - Returns adult fare (TicketType=1, FareClass=1)

4. **getCityBusFares(index, index2, totalStops)**
   - Fixed fare structure based on stop count:
     - 1-10 stops: NT$18
     - 11-20 stops: NT$36
     - 21+ stops: NT$54

5. **getHighwayBusFares(index, index2, routeName)**
   - Returns maximum fare for highway bus routes

**Route Processing:**
- **parseRoutes(data)** - Adds fare information to route segments
- **parseRoutesTwFare(data)** - Consolidates fares and calculates totals

## 🚀 Usage Methods

**Basic Fare Calculation:**
```javascript
const twTransitFares = require('./services/twTransitFares');

// Process routes with fare calculation
const routeData = {
  routes: [{
    sections: [{
      type: 'transit',
      transport: { mode: 'TRA', name: '自強號' },
      departure: { place: { stop_id: '1000' }},
      arrival: { place: { stop_id: '1020' }}
    }]
  }]
};

const faresData = await twTransitFares.parseRoutes(routeData);
```

**Multi-Modal Trip:**
```javascript
// Route with TRA + MRT segments
const multiModalRoute = {
  routes: [{
    sections: [
      // TRA segment
      {
        type: 'transit',
        transport: { mode: 'TRA', name: '莒光號' },
        departure: { place: { stop_id: '1000_1020' }}
      },
      // MRT segment
      {
        type: 'transit',
        transport: { type: 'MRT' },
        departure: { place: { name: '台北車站' }},
        arrival: { place: { name: '忠孝復興' }}
      }
    ]
  }]
};

const result = await twTransitFares.parseRoutes(multiModalRoute);
const totalFare = await twTransitFares.parseRoutesTwFare(result);
```

## 📊 Output Examples

**TRA Fare Response:**
```javascript
// Taipei to Taichung (自強號)
[0, 0, 375] // [routeIndex, sectionIndex, fare]
```

**HSR Fare Response:**
```javascript
// Taipei to Kaohsiung (Standard)
[0, 1, 1490] // NT$1,490
```

**Complete Route with Fares:**
```javascript
{
  routes: [{
    total_price: 445, // Total trip cost
    sections: [
      {
        transport: { 
          mode: 'TRA',
          fare: 375 // Individual segment fare
        }
      },
      {
        transport: {
          type: 'MRT',
          fare: 70
        }
      }
    ]
  }]
}
```

## ⚠️ Important Notes

**Data Dependencies:**
- Requires up-to-date fare data in MongoDB
- Missing fare data returns 0
- Station names must match database entries exactly

**Common Issues:**
1. **Zero fares:** Check if station IDs exist in database
2. **Wrong train type:** Verify train name matching logic
3. **MRT transfers:** Complex logic for multi-segment MRT trips

**Performance Considerations:**
- Batch database queries when possible
- Cache frequently requested fares
- Consider fare data update frequency

## 🔗 Related File Links

**Models:**
- `/models/TwTraFares.js` - TRA fare schema
- `/models/TwMrtFares.js` - MRT fare schema
- `/models/TwHsrFares.js` - HSR fare schema
- `/models/TwHighwayBusFares.js` - Bus fare schema

**Used By:**
- `/controllers/intermodal.js` - Multi-modal routing
- `/services/trip.js` - Trip planning service

## 📈 Use Cases

**Trip Planning:**
- Cost estimation before booking
- Budget-based route selection
- Fare comparison between options

**Analytics:**
- Transit cost analysis
- Route pricing optimization
- Fare subsidy calculations

**User Features:**
- Real-time fare display
- Multi-modal trip budgeting
- Corporate travel expense calculation

## 🛠️ Improvement Suggestions

**Code Optimization:**
- Implement fare caching layer
- Add input validation for station names
- Refactor repetitive fare lookup logic

**Feature Expansion:**
- Support discount tickets (student, senior)
- Add time-based fare variations
- Include seat class options for all transit types

**Data Management:**
- Automated fare data updates
- Fare history tracking
- API fallback for missing data

## 🏷️ Document Tags

**Keywords:** Taiwan transit | fare calculation | TRA | HSR | MRT | bus fare | public transport | pricing | 台鐵 | 高鐵 | 捷運 | 票價計算 | multi-modal | transit pricing

**Technical Tags:** #service #fare-calculation #transit #mongodb #taiwan-transit

**Target Roles:** Backend Developer (Mid-level), Transit Integration Engineer

**Difficulty Level:** ⭐⭐⭐ (Complex fare logic and data dependencies)

**Maintenance Level:** High (fare data updates required)

**Business Criticality:** High (affects trip cost accuracy)

**Related Topics:** Transit systems, Fare integration, Multi-modal routing, Taiwan public transport