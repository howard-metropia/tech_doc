# test-uis-description-handler.js

## Overview
Comprehensive test suite for the Urban Information System (UIS) description handler in the TSP API. Tests Dynamic Message Sign (DMS) text processing, incident description formatting, and text-to-speech conversion for traffic information systems.

## File Location
`/test/test-uis-description-handler.js`

## Dependencies
- **chai**: BDD/TDD assertion library
- **sinon**: Test spies, stubs, and mocks
- **@maas/core/log**: Logging framework
- **Service**: uis/description-handler

## Functions Under Test
```javascript
const {
  highPriorityEventTypeMap,
  formatDescription,
  formatDmsSoundDescription,
  formatIncidentSoundDescription,
} = require('@app/src/services/uis/description-handler');
```

## Test Data

### DMS Message Test Cases
```javascript
const testCases = [
  {
    input: 'ROAD[nl]WORK[nl]AHEAD[np]REDUCED[nl]SPEED[nl]AHEAD',
    desc: 'ROAD\\nWORK\\nAHEAD\\fREDUCED\\nSPEED\\nAHEAD\\f',
    soundDesc: [
      { message: 'The traffic sign 2 miles down the route says', delay: 0.25 },
      { message: 'ROAD', delay: 0.25 },
      { message: 'WORK', delay: 0.25 },
      { message: 'AHEAD', delay: 0.5 },
      { message: 'REDUCED', delay: 0.25 },
      { message: 'SPEED', delay: 0.25 },
      { message: 'AHEAD', delay: 0.5 }
    ]
  }
];
```

## Test Suites

### 1. DMS (Dynamic Message Sign) Testing

#### Normal Processing
**Test Cases**: Standard DMS message formatting

**Input Format**:
- `[jp2]`: Page separator
- `[nl]`: New line marker
- `[np]`: New page marker

**Processing Flow**:
1. **formatDescription**: Convert DMS codes to display format
2. **formatDmsSoundDescription**: Convert to text-to-speech format

#### Complex DMS Messages
**Example**:
```javascript
input: '[jp2]IH 69 SOUTH[nl]AT SOUTH RICE[nl]MAJOR ACCIDENT[np]CENTER LN CLSD[nl]AT RICHMOND AVE[nl]STALLED TRUCK'
```

**Processed Output**:
```javascript
desc: 'IH 69 SOUTH\\nAT SOUTH RICE\\nMAJOR ACCIDENT\\fCENTER LN CLSD\\nAT RICHMOND AVE\\nSTALLED TRUCK\\f'
```

**Sound Description**:
```javascript
[
  { message: 'The traffic sign 2 miles down the route says', delay: 0.25 },
  { message: 'IH 69 SOUTH', delay: 0.25 },
  { message: 'AT SOUTH RICE', delay: 0.25 },
  { message: 'MAJOR ACCIDENT', delay: 0.5 },
  { message: 'CENTER LANE CLOSED', delay: 0.25 },
  { message: 'AT RICHMOND AVENUE', delay: 0.25 },
  { message: 'STALLED TRUCK', delay: 0.5 }
]
```

### 2. Edge Case Testing

#### Speed Notation Handling
**Input**: `'[jp2]LEFT SHOULDER[nl]100 M.P.H.[nl]RIGHT SHOULDER[nl]100 M.P.H.'`

**Expected Processing**:
- `M.P.H.` → `MILES PER HOUR`
- Proper text-to-speech conversion

#### Direction Abbreviations
**Input**: `'N ST[nl]S ST[nl]E ST[nl]W ST'`

**Expected Processing**:
- `N` → `NORTH`
- `S ST` → `S STREET` (partial abbreviation)
- `E ST` → `E STREET`
- `W ST` → `W STREET`

#### Interstate Notation
**Input**: `'[jp2]IH 69 SOUTH[nl]AT I'`

**Expected Processing**:
- `I` → `INTERSTATE`
- Proper context handling

### 3. Abbreviation Mapping

#### Transportation Terms
```javascript
// Lane and Traffic
'LN' → 'LANE'
'LNS' → 'LANES'
'CLSD' → 'CLOSED'
'TRAF' → 'TRAFFIC'

// Road Types
'AVE' → 'AVENUE'
'BLVD' → 'BOULEVARD'
'DR' → 'DRIVE'
'ST' → 'STREET'
'HWY' → 'HIGHWAY'

// Directions
'N' → 'NORTH'
'S' → 'SOUTH'
'E' → 'EAST'
'W' → 'WEST'
'LFT' → 'LEFT'
'RHT' → 'RIGHT'
```

#### Speed and Distance
```javascript
'MPH' → 'MILES PER HOUR'
'M.P.H.' → 'MILES PER HOUR'
'MI' → 'MILE(S)'
'FT' → 'FEET'
'SPD' → 'SPEED'
```

#### Time and Days
```javascript
'MIN' → 'MINUTE(S)'
'MON' → 'MONDAY'
'TUES' → 'TUESDAY'
'WED' → 'WEDNESDAY'
'THURS' → 'THURSDAY'
'FRI' → 'FRIDAY'
'SAT' → 'SATURDAY'
'SUN' → 'SUNDAY'
```

#### Emergency and Construction
```javascript
'EMER' → 'EMERGENCY'
'HAZMAT' → 'HAZARDOUS MATERIAL'
'HAZ' → 'HAZARDOUS'
'CONST' → 'CONSTRUCTION'
'RDWK' → 'ROADWORK'
'MAINT' → 'MAINTENANCE'
```

### 4. Error Handling

#### Invalid Input Types
**Test**: Non-string input to DMS formatter

**Input**: `123` (number instead of string)

**Expected Behavior**:
- Returns empty array `[]`
- Logs error twice (once for each validation step)
- Graceful degradation without crashes

### 5. Incident Sound Description

#### High Priority Events
**Function**: `formatIncidentSoundDescription(eventType, location)`

**High Priority Event Types**:
- Events defined in `highPriorityEventTypeMap`
- Return structured sound description
- Include 0.5 delay for emphasis

**Test Logic**:
```javascript
const highPriorityEvents = Array.from(highPriorityEventTypeMap.keys());
highPriorityEvents.forEach((event) => {
  const result = formatIncidentSoundDescription(event, 'Los Angeles');
  expect(result.message).not.eq('');
  expect(result.delay).equal(0.5);
});
```

#### Empty Input Handling
**Test Cases**:
1. **Empty Type and Location**:
   ```javascript
   formatIncidentSoundDescription('', '')
   // Returns: { message: '', delay: 0 }
   ```

2. **Non-High Priority Events**:
   ```javascript
   formatIncidentSoundDescription('Traffic jam', 'IH-69')
   // Returns: { message: '', delay: 0 }
   ```

#### Error Conditions
**Test**: Invalid location type (number instead of string)

**Input**: `formatIncidentSoundDescription('Crash', 456)`

**Expected Behavior**:
- Returns empty object `{}`
- Logs error for type validation

## Sound Description Structure

### Message Format
```javascript
{
  message: string,    // Text-to-speech content
  delay: number      // Pause duration in seconds
}
```

### Delay Patterns
- **0.25 seconds**: Standard word separation
- **0.5 seconds**: End of phrase/sentence
- **0 seconds**: No delay (error cases)

### Introduction Message
- **Standard Prefix**: "The traffic sign 2 miles down the route says"
- **Consistent Timing**: 0.25 second delay after introduction

## DMS Code Translation

### Control Codes
- **[jp2]**: Page separator (removed in processing)
- **[nl]**: New line → `\n`
- **[np]**: New page → `\f` (form feed)

### Text Processing
1. **Code Removal**: Strip DMS control codes
2. **Line Breaks**: Convert to display format
3. **Abbreviation Expansion**: Full word conversion
4. **Sound Timing**: Add appropriate delays

## Business Logic

### Traffic Information System
- **Real-time Messages**: Dynamic highway sign content
- **Voice Announcements**: Text-to-speech for driver safety
- **Accessibility**: Audio descriptions for visual content

### Transportation Context
- **Highway Alerts**: Construction, accidents, closures
- **Speed Information**: Speed limits and advisories
- **Navigation Aid**: Route-specific information
- **Emergency Notifications**: High-priority incident alerts

## Testing Strategy

### Comprehensive Coverage
- **Normal Cases**: Standard DMS message processing
- **Edge Cases**: Special characters and abbreviations
- **Error Handling**: Invalid inputs and type checking
- **Abbreviation Testing**: Complete abbreviation dictionary

### Real-world Data
- **Actual DMS Messages**: Houston area traffic signs
- **Complex Scenarios**: Multi-page messages with mixed content
- **Emergency Situations**: High-priority incident processing

### Error Resilience
- **Type Validation**: Handle non-string inputs
- **Graceful Degradation**: Continue operation despite errors
- **Logging**: Track processing errors for debugging

## Integration Points

### Urban Information Systems
- **DMS Integration**: Dynamic Message Sign data processing
- **Incident Management**: Traffic incident description formatting
- **Voice Systems**: Text-to-speech audio generation

### User Experience
- **Driver Safety**: Audio announcements while driving
- **Accessibility**: Vision-impaired user support
- **Multilingual**: Consistent abbreviation handling

This test suite ensures the UIS description handler accurately processes dynamic message sign content, properly formats incident descriptions, and provides reliable text-to-speech conversion for the TSP API's traffic information and accessibility features.