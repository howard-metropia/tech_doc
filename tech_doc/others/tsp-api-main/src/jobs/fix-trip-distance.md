# Fix Trip Distance Calculation

## 📋 Job Overview
- **Purpose:** Recalculates and fixes missing or incorrect trip distances using routing APIs
- **Type:** One-time migration / Data correction job
- **Schedule:** On-demand execution with configurable start date parameter
- **Impact:** Telework_log and trips tables - updates distance values for accuracy

## 🔧 Technical Details
- **Dependencies:** HERE Maps API, Google Maps API, Teleworks/TeleworkLogs/Trips models
- **Database Operations:** Updates distance fields in telework_log and trips tables
- **Key Operations:** Calculates route distances using HERE routing (primary) and Google routing (fallback)

## 📝 Code Summary
```javascript
const fixTripDistance = async (originLat, originLon, destinationLat, destinationLon, travelMode) => {
  let distance = calcDistance(originLon, originLat, destinationLon, destinationLat);
  if (distance > MIN_DISTANCE) {
    // Try HERE API first, then Google API if HERE fails
    const { routes: hereRoutes } = await hereRouting(routeMode, origin, destination);
    if (!hereRoutes.length) {
      const { routes: googleRoutes } = await fetchGoogleRoute(googleInput);
      distance = googleRoutes[0].legs[0].distance.value;
    }
  }
  return distance;
};
```

## ⚠️ Important Notes
- Requires startDate parameter to limit scope of data processing
- Uses HERE API as primary source, Google API as fallback
- Only processes records with distance = 0 or negative distances
- May incur API costs due to external routing service calls
- Updates both telework logs and associated trip records

## 📊 Example Output
```
Fetch data from 2024-01-01 length: 1250
The distance from Here: 5420
The distance from Google: 5380
Updated telework count: 845 ids: [123,456,789...]
Updated trips count: 234 ids: [321,654,987...]
```

## 🏷️ Tags
**Keywords:** distance-calculation, data-correction, routing-api, telework, trip-validation
**Category:** #job #data-correction #routing #distance-calculation #api-integration