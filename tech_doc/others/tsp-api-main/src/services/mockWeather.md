# `mockWeather.js`

## Overview

The `mockWeather.js` service is a testing and development utility for creating and managing mock weather data within the system. It allows developers to simulate various weather conditions, including forecasts and critical alerts, to test the application's response without needing a live weather data feed. It interacts with `WeatherCriticalAlert` and `WeatherForecastCurrent` models and uses a static weather definitions file for threshold values.

## Key Functions

### `checkEvent(forecastData)`

-   **Purpose:** Analyzes weather data to determine if it constitutes a significant weather event based on predefined thresholds.
-   **Logic:** Compares `windSpeed`, `windGust`, `rain`, `snow`, and temperature values against thresholds defined in `@app/src/static/defines`. It categorizes events as either "significant without driving impact" or "significant with driving impact".
-   **Parameters:** `forecastData` (Object): An object containing weather indicators.
-   **Returns:** (Object): An object with `categories` (an array of event types) and `indicators` (the specific values that triggered the event).

### `extractIndicators(weather)`

-   **Purpose:** A helper function to pull a standardized set of weather indicators from a larger weather data object.
-   **Parameters:** `weather` (Object): The source weather object.
-   **Returns:** (Object): A simplified object containing `highTemperature`, `lowTemperature`, `windSpeed`, `windGust`, `rain`, and `snow`.

### `updateForecast(mockData)`

-   **Purpose:** Updates an existing weather forecast record with new (potentially mock) data. It re-evaluates the forecast for significant events after the update.
-   **Parameters:** `mockData` (Object): An object containing the `id` of the forecast to update and optional `indicators`. If indicators are not provided, they are extracted from the existing forecast data.
-   **Returns:** (Promise<Object>): The updated weather forecast document from the database.

### `createAlert(mockData)`

-   **Purpose:** Creates and stores a new `WeatherCriticalAlert` document using mock data. The alert's geometry and properties are pulled from a static mock data file.
-   **Parameters:** `mockData` (Object): An object containing `startAt`, `endAt`, and `impactedArea` for the new alert.
-   **Returns:** (Promise<string>): The `alert_id` of the newly created alert.

### `getAlert(id)`

-   **Purpose:** Retrieves a specific weather alert by its `alert_id`.
-   **Parameters:** `id` (string): The ID of the alert to retrieve.
-   **Returns:** (Promise<Object|null>): The alert document or `null` if not found.

### `updateAlert(id, mockData)`

-   **Purpose:** Updates the start time, end time, and impacted area of an existing mock weather alert.
-   **Parameters:**
    -   `id` (string): The `alert_id` of the alert to update.
    -   `mockData` (Object): Data object with `startAt`, `endAt`, and `impactedArea`.
-   **Returns:** (Promise<Object>): The updated alert document.

### `getForecast(gridId)`

-   **Purpose:** Fetches all active and future weather forecasts for a specific grid ID.
-   **Parameters:** `gridId` (string): The grid ID to query for.
-   **Returns:** (Promise<Array>): An array of forecast documents.

### `deleteAlert(id)`

-   **Purpose:** Deletes a weather alert by its `alert_id`.
-   **Parameters:** `id` (string): The `alert_id` of the alert to delete.
-   **Returns:** (Promise<Object>): The result of the deletion operation from the database.

### `findGridByCoordinates(latitude, longitude)`

-   **Purpose:** Finds the corresponding weather grid for a given set of geographic coordinates.
-   **Logic:** Performs a geospatial query on the `WeatherGrids` collection to find a grid polygon that contains the provided latitude and longitude.
-   **Parameters:**
    -   `latitude` (Number): The latitude.
    -   `longitude` (Number): The longitude.
-   **Returns:** (Promise<Object|null>): The grid document or `null` if no grid contains the coordinates.

## Dependencies

-   **`moment`:** For handling date and time operations, particularly for setting start and end times.
-   **`@maas/core/log`:** For logging.
-   **Models:** `WeatherCriticalAlert`, `WeatherForecastCurrent`, `WeatherGrids`.
-   **Static Data:** `@app/src/static/defines`, `@app/src/static/mock-data/weather/criticalAlert`.
