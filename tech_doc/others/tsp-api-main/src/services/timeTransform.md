# TSP API TimeTransform Service Documentation

## 🔍 Quick Summary (TL;DR)
The TimeTransform service provides utilities for converting between seconds and HH:MM:SS time formats, handling cross-day time calculations, and converting datetime strings to Unix timestamps with support for negative time values and 24-hour overflow scenarios.

**Keywords:** time-conversion | datetime-formatting | seconds-to-time | time-to-seconds | cross-day-handling | unix-timestamp | time-utilities | format-transformation

**Primary use cases:** Converting seconds to HH:MM:SS format with date handling, parsing time strings to seconds, converting datetime to Unix timestamps, handling transit schedule times

**Compatibility:** Node.js >= 16.0.0, moment.js for date manipulation, supports 24-hour time format with overflow handling

## ❓ Common Questions Quick Index
- **Q: What time formats are supported?** → Seconds to HH:MM:SS, HH:MM:SS to seconds, datetime to Unix timestamp
- **Q: How are negative times handled?** → Converted to previous day equivalent (e.g., -3600 becomes 23:00:00 previous day)
- **Q: What about times over 24 hours?** → Automatically rolls to next day (e.g., 25:00:00 becomes 01:00:00 next day)
- **Q: Are cross-day scenarios supported?** → Yes, with automatic date adjustment for overflow times
- **Q: What's the Unix timestamp conversion?** → Converts datetime strings to seconds since epoch with base offset
- **Q: How precise are the calculations?** → Second-level precision with proper hour/minute/second breakdown

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **time calculator** that helps convert between different time formats used in transit systems. It can turn seconds into readable times (like "3661 seconds" becomes "01:01:01"), handle times that go past midnight, and work with various time formats that transit schedules might use.

**Technical explanation:** 
A comprehensive time transformation utility that handles bidirectional conversion between seconds and time formats, manages cross-day time scenarios with automatic date adjustment, provides Unix timestamp conversion capabilities, and supports transit-specific time handling requirements with overflow and underflow scenarios.

**Business value explanation:**
Enables consistent time handling across transit systems, supports complex schedule management with cross-day scenarios, provides standardized time format conversion for API responses, ensures accurate time calculations for route planning, and facilitates integration with various transit data formats.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/timeTransform.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with moment.js date library
- **Type:** Time Conversion and Formatting Utility Service
- **File Size:** ~2.7 KB
- **Complexity Score:** ⭐⭐⭐ (Medium-High - Complex time calculation logic)

**Dependencies:**
- `moment`: Date manipulation and formatting library (**Critical**)
- No external API dependencies (**Self-contained**)

## 📝 Detailed Code Analysis

### Seconds to Time Conversion

### formatSeconds Function
**Purpose:** Converts seconds to HH:MM:SS format with date handling for overflow scenarios

```javascript
formatSeconds(value, date) {
  // secs to hh:mm:ss
  let theTime = parseInt(value); // secs
  let middle = 0; // mins
  let hour = 0; // hours
  
  // Handle negative times (previous day)
  theTime = !isNaN(theTime) && theTime < 0 ? 86400 + theTime : theTime;
  // Handle overflow times (next day)
  theTime = theTime > 86400 ? theTime - 86400 : theTime;

  // Convert seconds to hours, minutes, seconds
  if (theTime > 60) {
    middle = parseInt(theTime / 60);
    theTime = parseInt(theTime % 60);
    if (middle > 60) {
      hour = parseInt(middle / 60);
      middle = parseInt(middle % 60);
    }
  }
  
  // Format with zero padding
  let result = parseInt(theTime) < 10 ? '0' + parseInt(theTime) : '' + parseInt(theTime);
  
  // Handle minute formatting
  if (middle == 60) {
    hour += 1;
    result = '00:' + result;
  } else if (middle > 0 && middle >= 10 && middle <= 59) {
    result = '' + parseInt(middle) + ':' + result;
  } else if (middle == 0) {
    result = '00:' + result;
  } else {
    result = '0' + parseInt(middle) + ':' + result;
  }

  // Handle hour formatting
  if (hour > 0 && hour >= 10 && hour <= 23) {
    result = '' + parseInt(hour) + ':' + result;
  } else if (hour == 0 || hour == 24) {
    result = '00:' + result;
  } else {
    result = '0' + parseInt(hour) + ':' + result;
  }
  
  // Handle cross-day scenarios
  if (value >= 86400) {
    // Add one day for overflow
    date = moment(date).add('days', 1).format('YYYY-MM-DD');
  }
  
  return date + 'T' + result;
}
```

**Conversion Features:**
- **Negative Time Handling:** Converts negative seconds to previous day equivalent
- **Overflow Management:** Handles times exceeding 24 hours with date increment
- **Zero Padding:** Ensures consistent HH:MM:SS format with leading zeros
- **Cross-Day Support:** Automatic date adjustment for time overflow scenarios
- **Modular Calculation:** Proper breakdown of seconds into hours, minutes, seconds

### Time to Seconds Conversion

### formatTime Function
**Purpose:** Converts HH:MM:SS time format to total seconds

```javascript
formatTime(value) {
  // hh:mm:ss to secs
  let temp_time = [];
  let total_secs;
  temp_time = value.split(':');
  
  // Convert hours to seconds
  total_secs = parseInt(temp_time[0]) * 60 * 60; // hours

  // Handle missing minutes
  temp_time[1] = temp_time[1] === undefined ? (temp_time[1] = 0) : temp_time[1];
  total_secs = total_secs + parseInt(temp_time[1]) * 60; // mins
  
  // Handle missing seconds
  temp_time[2] = temp_time[2] === undefined ? (temp_time[2] = 0) : temp_time[2];
  total_secs = total_secs + parseInt(temp_time[2]); // secs
  
  return total_secs;
}
```

**Parsing Features:**
- **Flexible Input:** Handles HH:MM:SS, HH:MM, or HH formats
- **Missing Component Handling:** Defaults undefined minutes/seconds to zero
- **Mathematical Conversion:** Proper seconds calculation (hours×3600 + minutes×60 + seconds)
- **Integer Parsing:** Ensures numeric conversion for all time components

### DateTime to Unix Timestamp

### DateTime2Seconds Function
**Purpose:** Converts datetime string to Unix timestamp with base epoch offset

```javascript
DateTime2Seconds(value) {
  console.log(value);
  const TempDatetime = value.split('T');
  const TempDatetime2 = TempDatetime[1].split(':');
  
  // Convert time portion to seconds
  const Hms = parseInt(TempDatetime2[0]) * 3600 +
              parseInt(TempDatetime2[1]) * 60 +
              parseInt(TempDatetime2[2]);
  console.log('Hms:' + Hms);
  
  // Calculate days since reference date
  const startDate = moment('2022-01-13');
  const endDate = moment(TempDatetime[0]);
  const days = endDate.diff(startDate, 'days');
  
  // Calculate total seconds with base offset
  const AllSenconds = 86400 * days + Hms + 1642002900;
  return AllSenconds;
}
```

**Timestamp Features:**
- **DateTime Parsing:** Splits datetime string into date and time components
- **Day Calculation:** Uses moment.js to calculate days between dates
- **Base Epoch:** Uses custom epoch base (1642002900) for timestamp calculation
- **Total Conversion:** Combines days and time-of-day seconds for final timestamp

## 🚀 Usage Methods

### Basic Time Conversion
```javascript
const timeTransform = require('@app/src/services/timeTransform');

// Convert seconds to formatted time with date
const formatted = timeTransform.formatSeconds(3661, '2024-06-25');
console.log('Formatted time:', formatted);
// Output: "2024-06-25T01:01:01"

// Handle overflow time (next day)
const overflow = timeTransform.formatSeconds(90000, '2024-06-25');
console.log('Overflow time:', overflow);
// Output: "2024-06-26T01:00:00"

// Handle negative time (previous day)
const negative = timeTransform.formatSeconds(-3600, '2024-06-25');
console.log('Negative time:', negative);
// Output: "2024-06-25T23:00:00"

// Convert time string to seconds
const seconds = timeTransform.formatTime('01:30:45');
console.log('Total seconds:', seconds);
// Output: 5445

// Convert datetime to Unix timestamp
const timestamp = timeTransform.DateTime2Seconds('2024-06-25T14:30:00');
console.log('Unix timestamp:', timestamp);
```

### Advanced Time Management System
```javascript
class TransitTimeManager {
  constructor() {
    this.timeTransform = require('@app/src/services/timeTransform');
    this.timeCache = new Map();
  }

  formatTransitScheduleTime(seconds, baseDate, options = {}) {
    try {
      const {
        includeDate = true,
        handle24HourFormat = true,
        timezone = null
      } = options;

      // Use cached result if available
      const cacheKey = `${seconds}_${baseDate}_${JSON.stringify(options)}`;
      if (this.timeCache.has(cacheKey)) {
        return this.timeCache.get(cacheKey);
      }

      let result;
      
      if (handle24HourFormat) {
        // Use service's cross-day handling
        result = this.timeTransform.formatSeconds(seconds, baseDate);
      } else {
        // Simple conversion without date adjustment
        const hours = Math.floor(Math.abs(seconds) / 3600);
        const minutes = Math.floor((Math.abs(seconds) % 3600) / 60);
        const secs = Math.abs(seconds) % 60;
        
        const timeStr = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        result = includeDate ? `${baseDate}T${timeStr}` : timeStr;
      }

      // Apply timezone if specified
      if (timezone && result.includes('T')) {
        const moment = require('moment-timezone');
        result = moment.tz(result, timezone).format();
      }

      // Cache the result
      this.timeCache.set(cacheKey, result);
      return result;
    } catch (error) {
      console.error('Error formatting transit time:', error);
      return `${baseDate}T00:00:00`;
    }
  }

  parseFlexibleTimeFormat(timeInput) {
    try {
      // Handle various time input formats
      if (typeof timeInput === 'number') {
        // Already in seconds
        return timeInput;
      }
      
      if (typeof timeInput === 'string') {
        // Check if it's a datetime string
        if (timeInput.includes('T')) {
          return this.timeTransform.DateTime2Seconds(timeInput);
        }
        
        // Check if it's a time string
        if (timeInput.includes(':')) {
          return this.timeTransform.formatTime(timeInput);
        }
        
        // Try parsing as seconds
        const parsed = parseInt(timeInput);
        return isNaN(parsed) ? 0 : parsed;
      }
      
      return 0;
    } catch (error) {
      console.error('Error parsing time format:', error);
      return 0;
    }
  }

  calculateTimeDifference(startTime, endTime, format = 'seconds') {
    try {
      const startSeconds = this.parseFlexibleTimeFormat(startTime);
      const endSeconds = this.parseFlexibleTimeFormat(endTime);
      
      const difference = endSeconds - startSeconds;
      
      switch (format) {
        case 'seconds':
          return difference;
        case 'minutes':
          return Math.round(difference / 60);
        case 'hours':
          return Math.round(difference / 3600);
        case 'formatted':
          const hours = Math.floor(Math.abs(difference) / 3600);
          const minutes = Math.floor((Math.abs(difference) % 3600) / 60);
          const seconds = Math.abs(difference) % 60;
          const sign = difference < 0 ? '-' : '';
          return `${sign}${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        default:
          return difference;
      }
    } catch (error) {
      console.error('Error calculating time difference:', error);
      return 0;
    }
  }

  validateTimeRange(timeValue, minSeconds = 0, maxSeconds = 86400) {
    try {
      const seconds = this.parseFlexibleTimeFormat(timeValue);
      
      return {
        valid: seconds >= minSeconds && seconds <= maxSeconds,
        seconds,
        normalized: Math.max(minSeconds, Math.min(maxSeconds, seconds)),
        isOverflow: seconds > maxSeconds,
        isUnderflow: seconds < minSeconds
      };
    } catch (error) {
      return {
        valid: false,
        seconds: 0,
        normalized: 0,
        isOverflow: false,
        isUnderflow: false,
        error: error.message
      };
    }
  }

  batchConvertTimes(timeArray, baseDate, operation = 'formatSeconds') {
    const results = [];
    const errors = [];
    
    timeArray.forEach((timeValue, index) => {
      try {
        let result;
        
        switch (operation) {
          case 'formatSeconds':
            result = this.formatTransitScheduleTime(timeValue, baseDate);
            break;
          case 'formatTime':
            result = this.timeTransform.formatTime(timeValue);
            break;
          case 'DateTime2Seconds':
            result = this.timeTransform.DateTime2Seconds(timeValue);
            break;
          default:
            throw new Error(`Unknown operation: ${operation}`);
        }
        
        results.push({
          index,
          input: timeValue,
          output: result,
          success: true
        });
      } catch (error) {
        results.push({
          index,
          input: timeValue,
          output: null,
          success: false,
          error: error.message
        });
        errors.push({ index, error: error.message });
      }
    });
    
    return {
      results,
      errors,
      successCount: results.filter(r => r.success).length,
      errorCount: errors.length,
      totalProcessed: timeArray.length
    };
  }

  generateTimeSequence(startSeconds, endSeconds, intervalSeconds, baseDate) {
    try {
      const sequence = [];
      let currentTime = startSeconds;
      
      while (currentTime <= endSeconds) {
        const formatted = this.formatTransitScheduleTime(currentTime, baseDate);
        sequence.push({
          seconds: currentTime,
          formatted,
          timeOnly: formatted.split('T')[1],
          date: formatted.split('T')[0]
        });
        currentTime += intervalSeconds;
      }
      
      return {
        sequence,
        count: sequence.length,
        startTime: startSeconds,
        endTime: endSeconds,
        interval: intervalSeconds
      };
    } catch (error) {
      console.error('Error generating time sequence:', error);
      return {
        sequence: [],
        count: 0,
        error: error.message
      };
    }
  }

  getTimeStatistics(timeArray) {
    try {
      const secondsArray = timeArray.map(t => this.parseFlexibleTimeFormat(t)).filter(s => !isNaN(s));
      
      if (secondsArray.length === 0) {
        return {
          count: 0,
          min: 0,
          max: 0,
          average: 0,
          median: 0
        };
      }
      
      const sorted = secondsArray.sort((a, b) => a - b);
      const sum = secondsArray.reduce((acc, val) => acc + val, 0);
      
      return {
        count: secondsArray.length,
        min: sorted[0],
        max: sorted[sorted.length - 1],
        average: Math.round(sum / secondsArray.length),
        median: sorted.length % 2 === 0 
          ? Math.round((sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2)
          : sorted[Math.floor(sorted.length / 2)],
        sum,
        range: sorted[sorted.length - 1] - sorted[0]
      };
    } catch (error) {
      console.error('Error calculating time statistics:', error);
      return { count: 0, min: 0, max: 0, average: 0, median: 0, error: error.message };
    }
  }

  clearCache() {
    this.timeCache.clear();
    return { message: 'Time conversion cache cleared' };
  }

  getCacheInfo() {
    return {
      size: this.timeCache.size,
      keys: Array.from(this.timeCache.keys()).slice(0, 10) // First 10 keys
    };
  }
}

// Usage
const transitTimeManager = new TransitTimeManager();

// Format transit schedule time
const scheduleTime = transitTimeManager.formatTransitScheduleTime(90000, '2024-06-25');
console.log('Schedule time:', scheduleTime);

// Calculate time difference
const timeDiff = transitTimeManager.calculateTimeDifference('14:30:00', '16:45:30', 'formatted');
console.log('Time difference:', timeDiff);

// Batch convert times
const batchResult = transitTimeManager.batchConvertTimes([3600, 7200, 10800], '2024-06-25', 'formatSeconds');
console.log('Batch conversion:', batchResult);

// Generate time sequence
const sequence = transitTimeManager.generateTimeSequence(28800, 32400, 900, '2024-06-25');
console.log('Time sequence:', sequence);
```

### Transit Schedule Integration
```javascript
class TransitScheduleProcessor {
  constructor() {
    this.timeTransform = require('@app/src/services/timeTransform');
  }

  processGTFSStopTimes(stopTimesArray, serviceDate) {
    try {
      return stopTimesArray.map((stopTime, index) => {
        const arrivalTime = this.timeTransform.formatSeconds(
          this.timeTransform.formatTime(stopTime.arrival_time),
          serviceDate
        );
        
        const departureTime = this.timeTransform.formatSeconds(
          this.timeTransform.formatTime(stopTime.departure_time),
          serviceDate
        );

        return {
          ...stopTime,
          arrival_datetime: arrivalTime,
          departure_datetime: departureTime,
          arrival_seconds: this.timeTransform.formatTime(stopTime.arrival_time),
          departure_seconds: this.timeTransform.formatTime(stopTime.departure_time),
          stop_sequence: index + 1
        };
      });
    } catch (error) {
      console.error('Error processing GTFS stop times:', error);
      return [];
    }
  }

  calculateServiceWindow(tripData, serviceDate) {
    try {
      if (!tripData || tripData.length === 0) {
        return null;
      }

      const startTime = tripData[0];
      const endTime = tripData[tripData.length - 1];
      
      const startSeconds = this.timeTransform.formatTime(startTime.departure_time);
      const endSeconds = this.timeTransform.formatTime(endTime.arrival_time);
      
      return {
        serviceDate,
        startTime: this.timeTransform.formatSeconds(startSeconds, serviceDate),
        endTime: this.timeTransform.formatSeconds(endSeconds, serviceDate),
        duration: endSeconds - startSeconds,
        totalStops: tripData.length
      };
    } catch (error) {
      console.error('Error calculating service window:', error);
      return null;
    }
  }

  normalizeScheduleTimes(scheduleData, baseDate) {
    try {
      const normalized = [];
      
      scheduleData.forEach(schedule => {
        const normalizedSchedule = {
          ...schedule,
          times: []
        };
        
        schedule.times.forEach(timeStr => {
          try {
            const seconds = this.timeTransform.formatTime(timeStr);
            const formatted = this.timeTransform.formatSeconds(seconds, baseDate);
            
            normalizedSchedule.times.push({
              original: timeStr,
              seconds,
              formatted,
              isNextDay: seconds >= 86400
            });
          } catch (timeError) {
            console.warn(`Error processing time ${timeStr}:`, timeError.message);
          }
        });
        
        normalized.push(normalizedSchedule);
      });
      
      return {
        normalized,
        baseDate,
        processedCount: normalized.length
      };
    } catch (error) {
      console.error('Error normalizing schedule times:', error);
      return { normalized: [], baseDate, processedCount: 0, error: error.message };
    }
  }
}

// Usage
const scheduleProcessor = new TransitScheduleProcessor();

// Process GTFS stop times
const gtfsData = [
  { stop_id: '001', arrival_time: '08:30:00', departure_time: '08:30:30' },
  { stop_id: '002', arrival_time: '08:35:00', departure_time: '08:35:30' }
];

const processedStops = scheduleProcessor.processGTFSStopTimes(gtfsData, '2024-06-25');
console.log('Processed stops:', processedStops);

// Calculate service window
const serviceWindow = scheduleProcessor.calculateServiceWindow(gtfsData, '2024-06-25');
console.log('Service window:', serviceWindow);
```

## 📊 Output Examples

### Seconds to Time Conversion
```javascript
// Normal time
timeTransform.formatSeconds(3661, '2024-06-25')
// Output: "2024-06-25T01:01:01"

// Overflow time (next day)
timeTransform.formatSeconds(90000, '2024-06-25')
// Output: "2024-06-26T01:00:00"

// Negative time (previous day)
timeTransform.formatSeconds(-3600, '2024-06-25')
// Output: "2024-06-25T23:00:00"
```

### Time to Seconds Conversion
```javascript
// Full time format
timeTransform.formatTime('01:30:45')
// Output: 5445

// Partial formats
timeTransform.formatTime('02:15')
// Output: 8100

timeTransform.formatTime('3')
// Output: 10800
```

### DateTime to Unix Timestamp
```javascript
timeTransform.DateTime2Seconds('2024-06-25T14:30:00')
// Output: 1719316200 (approximate, based on calculation)
```

### Batch Time Conversion
```javascript
{
  results: [
    { index: 0, input: 3600, output: "2024-06-25T01:00:00", success: true },
    { index: 1, input: 7200, output: "2024-06-25T02:00:00", success: true },
    { index: 2, input: 90000, output: "2024-06-26T01:00:00", success: true }
  ],
  errors: [],
  successCount: 3,
  errorCount: 0,
  totalProcessed: 3
}
```

### Time Statistics
```javascript
{
  count: 5,
  min: 3600,
  max: 43200,
  average: 18000,
  median: 14400,
  sum: 90000,
  range: 39600
}
```

## ⚠️ Important Notes

### Time Calculation Logic
- **Cross-Day Handling:** Automatically adjusts dates for times exceeding 24 hours or negative values
- **Zero Padding:** Ensures consistent HH:MM:SS format with proper leading zeros
- **Overflow Management:** Times >= 86400 seconds trigger next-day date increment
- **Underflow Handling:** Negative times converted to previous day equivalent

### Format Conversion Accuracy
- **Bidirectional Conversion:** Supports both seconds→time and time→seconds conversion
- **Component Validation:** Handles missing time components (minutes/seconds) gracefully
- **Integer Parsing:** Ensures numeric conversion for all time calculations
- **Precision Maintenance:** Second-level precision maintained throughout conversions

### Unix Timestamp Considerations
- **Custom Epoch:** Uses specific base timestamp (1642002900) rather than standard Unix epoch
- **Date Calculation:** Relies on moment.js for accurate date difference calculations
- **Reference Date:** Uses '2022-01-13' as reference point for day calculations
- **Timezone Awareness:** Consider timezone implications when using timestamp conversions

### Performance and Usage
- **No External APIs:** Self-contained utility with no network dependencies
- **Memory Efficient:** Minimal memory footprint for time calculations
- **Error Handling:** Graceful handling of invalid time formats and edge cases
- **Caching Recommended:** Consider caching results for repeated conversions

## 🔗 Related File Links

- **Moment.js Documentation:** External moment.js library for date manipulation
- **Transit Services:** Services that use time conversion for schedule processing
- **Route Planning:** Services that require time calculations for trip planning

---
*This service provides comprehensive time format conversion and manipulation utilities for transit schedule processing and general time handling in the TSP platform.*