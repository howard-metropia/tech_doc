# BytemarkFare Model

## Overview
MongoDB model for storing Bytemark transit fare products and pricing information.

## File Location
`/src/models/BytemarkFare.js`

## Database Configuration
- **Connection**: MongoDB cache database
- **Collection**: `bytemark_fare`
- **Framework**: Mongoose ODM

## Schema Definition

```javascript
const mogonSchema = new Schema({
  uuid: { type: String },                    // Unique identifier
  entries: { type: Schema.Types.Mixed },     // Fare entries/rules
  short_description: { type: String },       // Brief description
  base_product: { type: Schema.Types.Mixed }, // Base product info
  list_price: { type: Number },             // Listed price
  long_description: { type: String },        // Detailed description
  sale_price: { type: Number },             // Sale/discounted price
  organization: { type: Schema.Types.Mixed }, // Transit organization
  name: { type: String },                   // Product name
  legacy_product: { type: Schema.Types.Mixed }, // Legacy product data
  cost_price: { type: Number },             // Cost price
  list_priority: { type: Number },          // Display priority
  theme: { type: Schema.Types.Mixed },      // UI theme settings
  published: { type: Boolean },             // Publication status
  requiresUserPhotoCheck: { type: Boolean }, // Photo verification required
  product_image_path: { type: String },     // Image URL
  alert_message: { type: String },          // Alert/warning message
  gtfs_fare_id: { type: Schema.Types.Mixed }, // GTFS fare identifier
  shipping_enabled: { type: Boolean },      // Physical shipping option
  subscription: { type: Schema.Types.Mixed }, // Subscription details
  input_field_required: { type: Schema.Types.Mixed }, // Required input fields
  type: { type: String },                   // Product type
  sub_type: { type: String }                // Product sub-type
});
```

## Key Fields

### Identification
- **uuid**: Unique Bytemark product identifier
- **name**: Human-readable product name
- **type/sub_type**: Product categorization

### Pricing
- **list_price**: Standard retail price
- **sale_price**: Discounted price (if applicable)
- **cost_price**: Internal cost price

### Product Information
- **short_description**: Brief product summary
- **long_description**: Detailed product information
- **product_image_path**: Visual representation

### Business Rules
- **entries**: Complex fare rules and conditions
- **base_product**: Foundation product reference
- **legacy_product**: Historical product mapping

### Integration
- **organization**: Transit agency details
- **gtfs_fare_id**: GTFS feed integration
- **subscription**: Recurring payment options

### Configuration
- **published**: Availability status
- **list_priority**: Display ordering
- **theme**: UI appearance settings
- **requiresUserPhotoCheck**: Verification requirements
- **shipping_enabled**: Physical delivery option
- **input_field_required**: Custom form fields
- **alert_message**: Important notifications

## Usage Context
- **Transit Ticketing**: Manage fare products for Bytemark integration
- **Price Management**: Store current and promotional pricing
- **Product Catalog**: Display available transit options
- **Integration**: Connect with Bytemark API and GTFS systems

## Export Structure
```javascript
module.exports = {
  bytemarkFare,
};
```

## Related Components
- Bytemark API integration
- Transit ticketing system
- GTFS fare management
- Transit payment processing
- Product catalog displays

## Performance Considerations
- Indexed on uuid for fast lookups
- Cached pricing data for quick access
- Mixed type fields for flexible data storage
- Optimized for read-heavy operations