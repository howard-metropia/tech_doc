# Create Toll Data Import

## 📋 Job Overview
- **Purpose:** Imports toll road data from CSV/JSON files into MongoDB collections for toll calculation
- **Type:** One-time migration / Data import job
- **Schedule:** Manual execution with file path parameter
- **Impact:** MongoDB collections - populates toll_zones, toll_zone_pairs, and toll_rates

## 🔧 Technical Details
- **Dependencies:** TollModels (TollRate, TollZonePairs, TollZones), Turf.js, Google Polyline, CSV parser
- **Database Operations:** Bulk upsert operations with batch processing (100 records per batch)
- **Key Operations:** CSV parsing, geospatial polygon creation, JSON toll rate processing

## 📝 Code Summary
```javascript
const fetchFromCSV = async (filePath, tableName) => {
  const csvContent = await readCSV(filePath, offset, columnList);
  await table.bulkWrite(writeData.map(el => ({
    updateOne: { filter: {...}, update: { $set: el }, upsert: true }
  })));
};

// For toll zones - creates circular geopolygons
const geoPolygon = turf.circle(center, radius, { steps: 16, units: 'meters' });
```

## ⚠️ Important Notes
- Supports both CSV (toll zones/pairs) and JSON (toll rates) file formats
- Creates 5-meter radius circular polygons for toll zone locations
- Uses batch processing to handle large datasets efficiently
- Removes older data after successful import using timestamp comparison
- Exits process after completion (process.exit(0))

## 📊 Example Output
```
Insert Total: 1500 rows into toll_zones
Insert Total: 850 rows into toll_zone_pairs
Write 12000 HoustonTollRate records
There are 36000 HoustonTollRate records have been imported
```

## 🏷️ Tags
**Keywords:** toll-data, csv-import, geospatial, houston-toll, data-migration
**Category:** #job #data-import #toll-system #geospatial #batch-processing