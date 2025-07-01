# BytemarkFare Model Documentation

## 📋 Model Overview
- **Purpose:** Stores Bytemark transit fare product information and pricing details
- **Table/Collection:** bytemark_fare
- **Database Type:** MongoDB
- **Relationships:** Links to transit fare systems and product catalogs

## 🔧 Schema Definition
- **Field Name** | **Type** | **Required** | **Description**
- uuid | String | No | Unique identifier for the fare product
- entries | Mixed | No | Flexible entry data structure
- short_description | String | No | Brief product description
- base_product | Mixed | No | Base product reference data
- list_price | Number | No | Listed price of the product
- long_description | String | No | Detailed product description
- sale_price | Number | No | Discounted sale price
- organization | Mixed | No | Organization/provider information
- name | String | No | Product name
- legacy_product | Mixed | No | Legacy system product data
- cost_price | Number | No | Cost basis for the product
- list_priority | Number | No | Display priority in lists
- theme | Mixed | No | Visual theme configuration
- published | Boolean | No | Publication status
- requiresUserPhotoCheck | Boolean | No | Photo verification requirement
- product_image_path | String | No | Path to product image
- alert_message | String | No | Alert or warning message
- gtfs_fare_id | Mixed | No | GTFS fare system identifier
- shipping_enabled | Boolean | No | Physical shipping availability
- subscription | Mixed | No | Subscription-based pricing data
- input_field_required | Mixed | No | Required input field definitions
- type | String | No | Product category type
- sub_type | String | No | Product subcategory

## 🔑 Key Information
- **Primary Key:** _id (MongoDB default)
- **Indexes:** No custom indexes defined
- **Unique Constraints:** None explicitly defined
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Find published fare products
const publishedFares = await bytemarkFare.find({ published: true });

// Find fares by type
const transitFares = await bytemarkFare.find({ 
  type: 'transit_ticket',
  published: true 
});

// Find discounted products
const saleItems = await bytemarkFare.find({
  sale_price: { $lt: "$list_price" }
});
```

## 🔗 Related Models
- **Transit payment models** - Referenced through gtfs_fare_id
- **User purchase models** - Related to fare purchasing
- **Subscription models** - Linked through subscription field

## 📌 Important Notes
- Flexible schema with many Mixed type fields for extensibility
- Supports both one-time and subscription-based fare products
- Includes photo verification capability for certain fare types
- Connected to 'cache' MongoDB database for performance
- Manages pricing tiers (list_price, sale_price, cost_price)
- GTFS integration for standardized transit fare handling

## 🏷️ Tags
**Keywords:** bytemark, fare, transit, pricing, product, gtfs
**Category:** #model #database #mongodb #transit #fare