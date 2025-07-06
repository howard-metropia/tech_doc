# Google Place Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates Google Places API requests for photos and place details
- **Validation Library:** Joi
- **Related Controller:** Google Place controller for Maps API integration

## 🔧 Schema Structure
```javascript
// Photo parameters schema
{
  photo_reference: Joi.string().required(),
  maxwidth: Joi.number(),
  maxheight: Joi.number(),
}.or('maxwidth', 'maxheight')

// Batch photo parameters schema
Joi.array().items({
  id: Joi.string().required(),
  photo_reference: Joi.string().required(),
  maxwidth: Joi.number(),
  maxheight: Joi.number(),
}).min(1).required()

// Place address schema
{
  place_id: Joi.string().required(),
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| photo_reference | string | Yes | Any string | Google photo reference ID |
| maxwidth | number | Conditional | Positive number | Maximum photo width in pixels |
| maxheight | number | Conditional | Positive number | Maximum photo height in pixels |
| id | string | Yes (batch) | Any string | Unique identifier for batch requests |
| place_id | string | Yes | Any string | Google Places place ID |

## 💡 Usage Example
```javascript
// Single photo request
{
  "photo_reference": "CmRaAAAAmS_7Yb...",
  "maxwidth": 400
}

// Batch photo request
[
  {
    "id": "photo1",
    "photo_reference": "CmRaAAAAmS_7Yb...",
    "maxwidth": 400
  },
  {
    "id": "photo2", 
    "photo_reference": "CmRaAAAAnX_8Zc...",
    "maxheight": 300
  }
]

// Place address request
{
  "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"
}

// Request that fails validation
{
  "photo_reference": "CmRaAAAAmS_7Yb..."
  // Error: must specify either maxwidth or maxheight
}
```

## ⚠️ Important Validations
- Photo requests require either maxwidth OR maxheight (not both optional)
- Batch requests must contain at least one item
- Each batch item needs unique ID for response mapping
- Place ID is required for address lookup requests

## 🏷️ Tags
**Keywords:** google-places, photo-api, place-details, maps-integration
**Category:** #schema #validation #joi #google-place