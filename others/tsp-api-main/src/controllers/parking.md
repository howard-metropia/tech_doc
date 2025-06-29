# Parking Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller provides a unified endpoint to search for both off-street (parking garages) and on-street (metered parking) parking availability. It acts as an aggregator and a complex data transformation layer, combining data from multiple third-party vendors (INRIX, Smarking) and an internal database (HAS for Houston airports) to present a single, coherent response to the client.

**Keywords:** parking | parking-availability | inrix | smarking | off-street-parking | on-street-parking | data-aggregation | tsp-api | real-time-data

**Primary use cases:** 
- Finding nearby parking lots based on a user's location or a bounding box.
- Displaying real-time availability for both parking garages and on-street meters.
- Providing detailed information for each parking lot, including pricing, hours, and contact info.
- Handling complex, region-specific business logic, such as merging multiple INRIX lots into one or overriding INRIX data with more accurate internal data for specific locations (e.g., Houston airports).

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x.

## ❓ Common Questions Quick Index
- **Q: How do I search for parking?** → [GET /parking](#get-parking)
- **Q: What's the difference between "off-street" and "on-street" parking?** → "Off-street" refers to parking garages and lots, while "on-street" refers to metered street parking.
- **Q: Where does the parking data come from?** → It's a combination of INRIX (global), Smarking (Houston on-street), and an internal HAS database (Houston airports).
- **Q: Why is there a `checkHasParkingLot` function?** → To override less accurate INRIX data with high-fidelity internal data for specific airport parking lots.
- **Q: What does the `statusIdentitfy` function do?** → It determines the current status of on-street parking meters based on complex time-based rules (day of the week, open hours, no-parking times).
- **Q: Is the data always real-time?** → The controller attempts to use real-time data but has checks (e.g., data timestamp validation) to ensure stale data isn't shown.
- **Q: What happens if the data from INRIX looks inaccurate?** → A data accuracy validation check runs, and if it fails, a warning is sent to a Slack channel.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a **master parking attendant for the entire city**. You tell the attendant where you are, and they instantly know about every available parking spot nearby.
- **For Parking Garages (Off-Street):** The attendant has a direct line to a global parking service called INRIX. However, for the major airports, the attendant trusts their own, more accurate "HAS" clipboard more, so they'll ignore the INRIX info for those specific lots and give you the info from their clipboard instead. They also know that three specific garages are actually part of one big complex, so they cleverly merge them into a single entry for you.
- **For Street Parking (On-Street):** The attendant also has a feed from "Smarking," which tracks all the metered spots in Houston. They look at the current time and day and consult a complex rulebook to tell you if a meter is currently active, free, or in a no-parking zone.
Finally, the attendant presents all this information to you in two neat lists: one for garages and one for street parking.

**Technical explanation:** 
A highly complex Koa.js controller that exposes a single `GET /parking` endpoint. This endpoint aggregates parking data from three different sources:
1.  **INRIX API**: Called via `ParkingService.inrix.getOffStreetParkingLot` to get a baseline of off-street parking lots.
2.  **Smarking API**: Called via `ParkingService.smarking.getOnStreetParkingLot` to get on-street parking data for Houston.
3.  **`HasParkingLot` MongoDB Model**: Used by the internal `checkHasParkingLot` function to query for and replace specific INRIX records with more accurate, internally managed data, primarily for Houston airports.

The controller's core logic involves fetching data from these sources and then performing extensive data transformation, filtering, and business rule application before sending the final response.

**Business value explanation:**
Reliable, real-time parking information is a high-value feature that directly addresses a major pain point for drivers. By aggregating multiple data sources into a single, user-friendly endpoint, this controller provides a superior user experience that would be impossible with a single data provider. The custom business logic (like overriding airport data) demonstrates a commitment to data accuracy, which builds user trust. This feature can significantly reduce driver frustration, save time, and decrease circling for parking, which in turn reduces traffic congestion and emissions.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/parking.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Aggregator/Controller
- **File Size:** ~14 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Due to the aggregation of multiple async data sources and extensive, complex data transformation and business logic.)

**Dependencies (Criticality Level):**
- `moment-timezone`: Date and time manipulation, critical for on-street parking rules (**Critical**).
- `@koa/router`: Core routing (**Critical**).
- `@app/src/middlewares/auth`: JWT authentication (**Critical**).
- `@app/src/services/parking`: The service layer containing the INRIX and Smarking API clients (**Critical**).
- `@app/src/models/HasParkingLot`: MongoDB model for internal airport parking data (**Critical**).
- `@app/src/services/dataAccuracySlackWarning`: For sending alerts on data quality issues (**High**).

## 📝 Detailed Code Analysis

### `GET /parking`
This is the sole, highly complex endpoint.
**Execution Flow:**
1.  **Validation**: Ensures `lat`, `lng`, `bounding_box`, `radius`, and `userId` are present.
2.  **Off-Street Data Fetching & Processing**:
    - Calls the INRIX service to get a list of parking lots.
    - Iterates through the INRIX results using `Promise.all` for parallel processing.
    - For each INRIX lot, it performs significant data mapping to transform the INRIX object structure into the desired API response structure.
    - **Crucially**, it calls `await checkHasParkingLot(inrixData)`. This helper function checks if the INRIX lot ID is on a predefined list of airport lots. If it is, and fresh data exists in the `HasParkingLot` MongoDB collection, it completely replaces the INRIX data with the internal data. This function also handles a special case where one INRIX ID maps to two internal lots.
    - It implements logic to merge three specific INRIX lots (`'85290', '99544', '187831'`) into a single entry.
    - The processed lots are pushed to the `offStreet` array.
3.  **Data Accuracy Check**: After processing all off-street lots, it calls `dataAccuracyValidation(offStreet)` to check for data quality issues. If the check fails, it triggers a Slack alert.
4.  **On-Street Data Fetching & Processing**:
    - Calls the Smarking service to get Houston-specific on-street parking data.
    - Iterates through the Smarking results.
    - For each result, it determines the current day of the week and calls `statusIdentitfy`. This massive helper function takes the various open/closed/no-parking time ranges and the current time and returns the meter's current operational status.
    - It determines a `color` for the parking icon based on availability (`getVacancyRateColor`).
    - The processed on-street spots are pushed to the `onStreet` array.
5.  **Final Response**: It filters out any temporarily closed lots (using a separate service call) and returns a final object containing the `offStreet` and `onStreet` arrays.

### Helper Functions
This controller relies heavily on local helper functions to encapsulate complex logic:
- `checkHasParkingLot`: The INRIX data override logic.
- `statusIdentitfy`: The core of the on-street parking rule engine.
- `getSpaceType`, `getOpenStatus`: Simple data mapping functions.
- `getHourMinuteFromString`, `noPakringWording`: Time parsing and formatting utilities.
- `getVacancyRateColor`: Maps an availability rate to a color code.
- `dataAccuracyValidation`: Checks for anomalies in the final data set.

## 🚀 Usage Methods

### Get Parking Near a Location
```bash
curl -X GET "https://api.tsp.example.com/api/v2/parking?lat=29.7604&lng=-95.3698&radius=1000&bounding_box=29.75,-95.38,29.77,-95.36" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123"
```

## 📊 Output Example

```json
{
  "result": "success",
  "data": {
    "offStreet": [
      {
        "parkinglot_uid": "209674",
        "name": "IAH Terminal C Garage",
        "address": "...",
        "total_lots": 2500,
        "available_lots": 875,
        "status": 1, // 1 = Open
        "lat": 29.987,
        "lng": -95.337,
        "rate": 35, // 35% available
        // ... and many more fields
      }
    ],
    "onStreet": [
      {
        "station_id": "HOU-1234",
        "address": "1000 Main St",
        "rate": 80, // 80% available
        "color": "green",
        "status": 1, // 1 = Available and payable
        // ... and more fields
      }
    ]
  }
}
```

## ⚠️ Important Notes
- **Brittle Business Logic**: The controller contains a lot of hard-coded IDs (e.g., the `hasParkingLots` array, the `needToMerge` array). This makes the code brittle; if these IDs change in the source systems, this controller will break.
- **Data Source Dependency**: The application's parking feature is critically dependent on the availability and correctness of the INRIX, Smarking, and internal HAS data sources.
- **Timezone Sensitivity**: The on-street parking logic is highly sensitive to the timezone (`moment.tz('US/Central')`). Any errors in timezone handling would lead to incorrect status reporting.

## 🔗 Related File Links
- **Parking API Clients:** `allrepo/connectsmart/tsp-api/src/services/parking/index.js`
- **Internal Parking DB Model:** `allrepo/connectsmart/tsp-api/src/models/HasParkingLot.js`
- **Road Closure Filtering:** `allrepo/connectsmart/tsp-api/src/services/parking/roadTemporaryClosure.js`
- **Slack Alerter:** `allrepo/connectsmart/tsp-api/src/services/dataAccuracySlackWarning.js`

---
*This documentation was regenerated to detail the complex data aggregation and business logic required to provide a unified parking data feed.*
