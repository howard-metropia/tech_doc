# RoutesHistorys Model

## Overview
MongoDB-based route history tracking model for the TSP Job system. Stores comprehensive trip routing history, travel patterns, and journey analytics data for users across the MaaS platform.

## Model Definition
```javascript
const { Schema } = require('mongoose');
const conn = require('@maas/core/mongo')('cache');

const historyObj = {
  // 轉乘次數 (Transfer count)
  transfers: { type: Number },
  // 引擎演算法使用 (Engine algorithm usage)
  generalized_cost: { type: Number },
  sections: { type: Array },
  total_travel_meters: { type: Number },
  // 總票價 (Total fare)
  total_price: { type: Number },
  travel_mode: { type: String },
  trip_detail_uuid: { type: String },
  // UTC time format is "2022-04-28T12:11:59+00:00"
  started_on: { type: String },
  ended_on: { type: String },
  // 單位是秒 (Unit is seconds)
  total_travel_time: { type: Number },
};

const mogonSchema = new Schema(
  {
    id: { type: 'string', columnName: '_id' },
    user_id: { type: 'string' },
    history: [historyObj],
  },
  { versionKey: false },
);

const routesHistory = conn.model('routes_history', mogonSchema);
module.exports = routesHistory;
```

## Database Configuration
- **Database**: Cache MongoDB instance
- **Collection**: `routes_history`
- **ODM**: Mongoose with schema validation
- **Connection**: Managed by @maas/core MongoDB connection pool

## Purpose
- Historical route and trip data storage
- Travel pattern analysis and insights
- Journey optimization algorithm input
- User travel behavior tracking

## Key Features
- Document-based flexible data storage
- Nested history object arrays for multiple trips
- Real-time route performance tracking
- Multi-modal transportation support
- Comprehensive trip metadata storage

## Technical Analysis
The RoutesHistorys model utilizes MongoDB's document-oriented storage to maintain flexible, scalable route history data. Each document represents a user's complete routing history with an embedded array of individual trip records.

The model uses Mongoose ODM for schema definition and data validation, connecting to the cache MongoDB instance through @maas/core connection management. The nested historyObj structure allows for efficient storage of multiple trip records per user while maintaining query performance.

## History Object Structure
Each history entry contains:
- **transfers**: Number of transportation mode changes during trip
- **generalized_cost**: Algorithm-calculated trip cost for optimization
- **sections**: Array of trip segments with detailed routing information
- **total_travel_meters**: Total distance traveled in meters
- **total_price**: Complete trip cost including all fees
- **travel_mode**: Primary transportation mode used
- **trip_detail_uuid**: Unique identifier linking to detailed trip information
- **started_on**: Trip start timestamp in UTC ISO format
- **ended_on**: Trip completion timestamp in UTC ISO format
- **total_travel_time**: Complete journey duration in seconds

## Data Analytics Applications
- **Travel Pattern Recognition**: Identifying user commute patterns
- **Route Optimization**: Algorithm improvement through historical data
- **Performance Metrics**: Service quality and efficiency measurement
- **Cost Analysis**: Fare optimization and pricing strategy
- **Modal Split Analysis**: Transportation mode usage patterns
- **Temporal Analysis**: Peak usage times and seasonal variations

## Integration Points
- **TripDetail**: Detailed trip information linking
- **TripRecords**: Trip processing and validation
- **AuthUsers**: User identification and personalization
- **RidehailTrips**: Ridehail-specific journey data
- **TransitAlert**: Impact analysis of service disruptions

## Usage Context
Used extensively for:
- Historical journey analysis and reporting
- Machine learning algorithm training data
- User travel behavior insights
- Route recommendation improvements
- Service performance evaluation

## Travel Mode Support
- **Public Transit**: Bus, rail, subway routing history
- **Ridehail**: Uber, Lyft, and other on-demand services
- **Active Transportation**: Walking, cycling route tracking
- **Multi-Modal**: Combined transportation mode journeys
- **Micro-Mobility**: Scooter, bike-share integration

## Performance Considerations
- MongoDB document structure optimized for user-based queries
- Indexed fields for efficient user_id and temporal queries
- Embedded arrays reduce join operations
- Connection pooling through @maas/core reduces overhead
- Horizontal scaling capabilities through MongoDB sharding

## Section Data Structure
The sections array contains detailed segment information:
- **Segment Identification**: Route identifiers, stop information
- **Transportation Details**: Vehicle type, provider information
- **Timing Information**: Segment start/end times, delays
- **Geographic Data**: Waypoints, path coordinates
- **Cost Breakdown**: Segment-specific fare information
- **Quality Metrics**: On-time performance, comfort ratings

## Query Patterns
- **User History Retrieval**: Complete routing history for specific users
- **Temporal Queries**: Trip data within date ranges
- **Route Analysis**: Specific route performance metrics
- **Modal Analysis**: Transportation mode usage patterns
- **Geographic Queries**: Route data for specific areas or corridors

## Security Features
- User data privacy protection through secure connection
- Data anonymization capabilities for analytics
- Access control through connection management
- Audit trail capabilities for data access
- Secure data transmission and storage

## Algorithm Integration
- **Route Optimization**: Generalized cost calculation input
- **Machine Learning**: Training data for prediction models
- **Recommendation Engine**: Historical preference analysis
- **Performance Optimization**: Service improvement insights
- **Predictive Analytics**: Travel pattern forecasting

## API Integration
- Historical data retrieval endpoints
- Analytics and reporting interfaces
- Route performance monitoring
- User travel pattern analysis
- Transportation planning support

## Related Models
- TripDetail: Comprehensive trip information
- TripRecords: Trip processing status
- AuthUsers: User identification
- RidehailTrips: Ridehail service data
- Reservations: Trip booking information

## Data Retention
- **Historical Preservation**: Long-term journey data storage
- **Performance Optimization**: Efficient storage of large datasets
- **Data Archival**: Automated archival of old records
- **Privacy Compliance**: Data retention policy adherence
- **Analytics Support**: Historical trend analysis capabilities

## Quality Assurance
- **Data Validation**: Schema-enforced data integrity
- **Completeness Checks**: Required field validation
- **Consistency Verification**: Cross-reference validation with other models
- **Performance Monitoring**: Query performance optimization
- **Error Handling**: Robust error detection and correction

## Development Notes
- Flexible schema supports evolving routing requirements
- Efficient storage for high-volume historical data
- Optimized for analytical query patterns
- Compatible with existing MongoDB infrastructure
- Supports real-time and batch data processing

## Scalability Features
- MongoDB horizontal scaling through sharding
- Efficient indexing for high-volume queries
- Connection pooling reduces resource overhead
- Document-based storage supports flexible data structures
- Analytics-optimized data organization