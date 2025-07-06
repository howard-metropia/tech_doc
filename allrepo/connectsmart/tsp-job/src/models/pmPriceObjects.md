# pmPriceObjects Model Documentation

## Overview
PmPriceObjects is a Mongoose-based model that manages comprehensive parking pricing data and time block information for ParkMobile integration. This model stores detailed pricing structures, time constraints, and zone-specific parking regulations.

## Schema Definition
```javascript
const { Schema } = require('mongoose');
const conn = require('@maas/core/mongo')('dataset');

const mongoSchema = new Schema({
  _id: { type: String },
  zone: { type: 'string' },
  paid: { type: 'boolean' },
  timeBlockUnit: { type: 'string' },
  timeBlockQuantity: { type: 'string' },
  timeBlockId: { type: 'string' },
  price: {
    parkingPrice: { type: 'number' },
  },
  parkingStartTimeLocal: { type: 'date' },
  parkingStopTimeLocal: { type: 'date' },
  isParkingAllowed: { type: 'boolean' },
  parkingNotAllowedReason: { type: 'string' },
  maxParkingTime: {
    hours: { type: 'number' },
    days: { type: 'number' },
    minutes: { type: 'number' },
    totalMinutes: { type: 'number' },
  },
  parkingStartTimeUtc: { type: 'date' },
  parkingStopTimeUtc: { type: 'date' },
  timeZoneStandardName: { type: 'string' },
  cultureCode: { type: 'string' },
  currency: { type: 'string' },
  currencySymbol: { type: 'string' },
}, { timestamps: true });
```

## Database Configuration
- **Database**: Dataset MongoDB (`dataset`)
- **Collection**: `pm_price_objects`
- **ORM**: Mongoose ODM
- **Connection**: Managed through @maas/core/mongo

## Schema Structure

### Core Pricing Fields
- **zone**: Parking zone identifier
- **paid**: Whether parking requires payment
- **price.parkingPrice**: Cost per time unit
- **currency**: Pricing currency code
- **currencySymbol**: Currency display symbol

### Time Management
- **timeBlockUnit**: Unit of time (minutes, hours)
- **timeBlockQuantity**: Quantity of time units
- **timeBlockId**: Unique time block identifier
- **maxParkingTime**: Maximum allowed parking duration

### Temporal Constraints
- **parkingStartTimeLocal**: Local start time for parking availability
- **parkingStopTimeLocal**: Local end time for parking availability
- **parkingStartTimeUtc**: UTC start time for standardization
- **parkingStopTimeUtc**: UTC end time for standardization
- **timeZoneStandardName**: Time zone identification

### Regulatory Information
- **isParkingAllowed**: Whether parking is currently permitted
- **parkingNotAllowedReason**: Explanation for parking restrictions
- **cultureCode**: Localization and language code

## Core Functionality

### Dynamic Pricing Management
- Real-time pricing calculation based on demand
- Time-based pricing variations (peak/off-peak)
- Zone-specific pricing structures
- Special event pricing adjustments

### Time Block Optimization
- Flexible time unit configuration
- Maximum duration enforcement
- Dynamic availability windows
- Time zone-aware scheduling

## Usage Patterns

### Pricing Queries
```javascript
const PmPriceObjects = require('./pmPriceObjects');

// Get pricing for specific zone
const zonePricing = await PmPriceObjects.findOne({ zone: zoneId });

// Calculate parking cost
const parkingCost = zonePricing.price.parkingPrice * duration;

// Check parking availability
const isAvailable = await PmPriceObjects.findOne({
  zone: zoneId,
  isParkingAllowed: true,
  parkingStartTimeLocal: { $lte: requestTime },
  parkingStopTimeLocal: { $gte: requestTime }
});

// Get pricing for time range
const availableSlots = await PmPriceObjects.find({
  zone: zoneId,
  parkingStartTimeUtc: { $gte: startTime },
  parkingStopTimeUtc: { $lte: endTime }
});
```

### Dynamic Pricing Calculation
- Real-time rate calculations
- Time-based pricing adjustments
- Zone-specific rate structures
- Currency conversion support

## Pricing Models

### Time-Based Pricing
- **Hourly Rates**: Standard hourly parking fees
- **Daily Maximums**: Daily rate caps
- **Minimum Charges**: Minimum parking fees
- **Fractional Pricing**: Partial hour calculations

### Zone-Based Pricing
- **Premium Zones**: High-demand area pricing
- **Standard Zones**: Regular parking rates
- **Discount Zones**: Reduced rate areas
- **Special Event Zones**: Dynamic event pricing

### Dynamic Pricing Factors
- **Demand-Based**: Real-time demand adjustments
- **Time-of-Day**: Peak and off-peak variations
- **Seasonal**: Holiday and seasonal rates
- **Event-Based**: Special event surcharges

## Time Management Features

### Availability Windows
- Operating hour management
- Day-of-week availability
- Holiday schedule adjustments
- Maintenance period handling

### Duration Limits
- Maximum parking time enforcement
- Minimum parking requirements
- Time extension capabilities
- Overstay penalty calculation

### Time Zone Handling
- Multi-time zone support
- Daylight saving time adjustments
- UTC standardization
- Local time display formatting

## Integration Points

### ParkMobile Platform
- **Rate Synchronization**: Real-time pricing updates
- **Zone Management**: Parking zone configuration
- **Time Block Coordination**: Available time slot management
- **Payment Integration**: Transaction amount calculation

### Internal Systems
- **Booking System**: Reservation pricing calculation
- **Mobile Applications**: Real-time rate display
- **Analytics**: Revenue and utilization analysis
- **Customer Service**: Pricing inquiry support

## Regulatory Compliance

### Municipal Integration
- City parking regulation compliance
- Rate structure alignment with local policies
- Enforcement period coordination
- Special permit pricing

### Accessibility Compliance
- ADA-compliant pricing structures
- Accessible parking spot pricing
- Special rate accommodations
- Compliance reporting

## Performance Optimization
- Efficient indexing on zone and time fields
- Caching of frequently accessed pricing data
- Optimized query patterns for real-time lookups
- Aggregation pipeline optimization

## Analytics Capabilities
- Pricing trend analysis
- Revenue optimization insights
- Demand pattern recognition
- Zone performance comparison

## Related Components
- **pmParkingEvent**: Event correlation with pricing
- **pmParkingEvents**: Event data caching
- **Booking System**: Reservation price calculation
- **Payment Processing**: Transaction amount validation

## Maintenance Operations
- Regular pricing data updates
- Zone configuration synchronization
- Time zone data maintenance
- Currency rate updates

## Future Enhancements
- Machine learning-based dynamic pricing
- Predictive demand pricing
- Advanced analytics integration
- Multi-currency automatic conversion
- Enhanced regulatory compliance features