# Google Place Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller acts as a secure proxy and wrapper for specific Google Places API functionalities. It allows authenticated clients to fetch photos for a place and retrieve address details for a given Place ID, without exposing API keys to the client.

**Keywords:** google-places | api-proxy | google-maps | place-photo | place-details | geocoding | poi | tsp-api | wrapper-api

**Primary use cases:** 
- Fetching a URL for a Google Place photo based on its `photo_reference`.
- Batch fetching multiple photo URLs in a single request.
- Retrieving the formatted address and coordinates for a Google `place_id`.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x.

## ❓ Common Questions Quick Index
- **Q: How do I get a single photo for a place?** → [GET /google/place/photo](#get-googleplacephoto)
- **Q: How do I get multiple photos at once?** → [POST /google/place/photo/batch](#post-googleplacephotobatch)
- **Q: How do I get the address for a Place ID?** → [GET /google/place/poi_address/:place_id](#get-googleplacepoi_addressplace_id)
- **Q: Why use this API instead of calling Google directly?** → To protect the Google API key by keeping it on the server-side.
- **Q: What parameters are needed for a photo?** → `photo_reference` is required; `maxwidth` and `maxheight` are optional.
- **Q: What does the batch photo endpoint return?** → An array of objects, each containing an `id` you provided and the fetched `url`.
- **Q: What happens if the Google API call fails?** → The controller returns a generic `ERROR_THIRD_PARTY_FAILED` error.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a **personal shopper for Google Maps information**. Instead of giving you the company credit card (the API key) to go shopping on Google's website yourself, you give your shopping list to the personal shopper. If you need a picture of a restaurant (`GET /photo`), you give the shopper the photo's reference number, and they come back with a direct link to the photo. If you need pictures of ten different places (`POST /photo/batch`), you give them the whole list, and they return with all the photo links. If you need the street address for a specific store (`GET /poi_address`), you give them the store's unique ID, and they bring back the formatted address and map coordinates. This keeps the company credit card safe and sound.

**Technical explanation:** 
A Koa.js controller that securely wraps three functionalities of the Google Places API.
1.  `GET /google/place/photo`: Proxies a request to the Google Places Photo API for a single image.
2.  `POST /google/place/photo/batch`: Provides a batch-processing endpoint that iterates through an array of photo requests and calls the underlying `fetchGooglePlacePhoto` service for each, returning an aggregated result.
3.  `GET /google/place/poi_address/:place_id`: Proxies a request to the Google Places Details API, specifically to fetch address and geometry information for a given `place_id`.
All endpoints are authenticated and use a shared input validator. This controller's primary architectural purpose is to abstract the Google API calls and protect the server's API key.

**Business value explanation:**
This controller is essential for securely integrating rich, third-party location data from Google into the application. By proxying the API calls, it prevents the Google API key from being exposed in client-side code, which is a critical security best practice to avoid unauthorized use and billing. It also provides a centralized point for managing and potentially caching Google API requests, which can help control costs and improve performance. The batch endpoint offers an efficiency gain for clients that need to display multiple place photos simultaneously.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/googlePlace.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Proxy/Wrapper
- **File Size:** ~4 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - Involves batch processing with `Promise.all` and data transformation.)

**Dependencies (Criticality Level):**
- `@koa/router`, `koa-bodyparser`: Core routing and body parsing (**Critical**).
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**).
- `@app/src/services/response`: Standardized success response formatter (**High**).
- `@app/src/services/googleApis`: The service layer containing the actual Google API call logic (**Critical**).
- `@app/src/schemas/google-place`: Joi schemas for input validation (**Critical**).
- `@app/src/static/error-code`: Static error code definitions (**High**).

## 📝 Detailed Code Analysis

### `GET /google/place/photo`
- **Purpose**: Get a URL for a single Google Place photo.
- **Logic**: A simple wrapper. It validates the query parameters (`photo_reference`, `maxwidth`, `maxheight`), calls the `fetchGooglePlacePhoto` service, and returns the resulting URL in a standard success response.

### `POST /google/place/photo/batch`
- **Purpose**: Get URLs for multiple photos in one API call.
- **Logic**:
    1. It validates the request body, expecting an array of `photos`, where each object has a `photo_reference` and an `id`.
    2. It uses `map` to create an array of promises. For each photo object in the input, it calls `fetchGooglePlacePhoto`.
    3. It wraps these promises in `Promise.all()` to execute them concurrently.
    4. It constructs a response that maps the original `id` provided by the client to the fetched `url`. This allows the client to easily correlate results with its requests.
    5. Includes a `try...catch` block to handle errors from the Google API and wrap them in a standard `MaasError`.

### `GET /google/place/poi_address/:place_id`
- **Purpose**: Get address details for a Google Place ID.
- **Logic**:
    1. Validates the `place_id` from the URL path.
    2. Calls the `fetchGooglePlaceAddress` service.
    3. Transforms the detailed result from the Google API into a simpler, standardized `pObj` (place object) containing only `poi_name`, `poi_address`, `lat`, and `lng`.
    4. Includes a default/empty object structure in case the Google API returns no results, preventing downstream errors.
    5. Wraps the result in a standard success response.

## 🚀 Usage Methods

**Base URL:** `https://api.tsp.example.com/api/v2`
**Headers (for all requests):**
- `Authorization`: `Bearer <YOUR_JWT_TOKEN>`
- `Content-Type`: `application/json` (for POST)

### Get a Single Photo
```bash
curl -X GET "https://api.tsp.example.com/api/v2/google/place/photo?photo_reference=CmRaAAA...&maxwidth=400" \
  -H "Authorization: Bearer <TOKEN>"
```

### Get a Batch of Photos
```bash
curl -X POST "https://api.tsp.example.com/api/v2/google/place/photo/batch" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "photos": [
      { "id": "place1", "photo_reference": "CmRaAAA...1", "maxwidth": 100 },
      { "id": "place2", "photo_reference": "CmRaAAA...2", "maxwidth": 100 }
    ]
  }'
```

### Get Place Address Details
```bash
curl -X GET "https://api.tsp.example.com/api/v2/google/place/poi_address/ChIJN1t_tDeuEmsRUsoyG83frY4" \
  -H "Authorization: Bearer <TOKEN>"
```

## 📊 Output Examples

### Single Photo Response
```json
{
  "result": "success",
  "data": {
    "url": "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=CmRaAAA...&key=..."
  }
}
```

### Batch Photo Response
```json
{
  "result": "success",
  "data": {
    "result": [
      { "url": "https://maps.googleapis.com/...", "id": "place1" },
      { "url": "https://maps.googleapis.com/...", "id": "place2" }
    ]
  }
}
```

### Place Address Response
```json
{
  "result": "success",
  "data": {
    "poi_name": "",
    "poi_address": "48 Pirrama Rd, Pyrmont NSW 2009, Australia",
    "lat": -33.866611,
    "lng": 151.195832
  }
}
```

## ⚠️ Important Notes
- **Security**: The primary purpose of this controller is to avoid exposing the Google API key on the client side. This is a critical security measure.
- **Error Abstraction**: The controller catches specific errors from the service layer but also has a fallback to a generic `ERROR_THIRD_PARTY_FAILED`. This abstracts the details of the third-party API failure from the client.
- **Data Transformation**: The `poi_address` endpoint intentionally simplifies the rich data from the Google Places API into a lean, consistent object for client-side use.

## 🔗 Related File Links
- **Google API Logic:** `allrepo/connectsmart/tsp-api/src/services/googleApis.js`
- **Input Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/google-place.js`
- **Standard Response:** `@app/src/services/response` (likely a core or shared service)
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This documentation was regenerated to provide a clearer, more structured explanation of how this controller securely wraps and utilizes the Google Places API.* 