# Report Mail Service

## Overview

The Report Mail Service is a comprehensive email reporting system that generates and sends personalized bi-weekly transportation reports to users. It includes sophisticated report generation with statistics, incentive data, weather alerts, construction information, and visual elements like charts and progress tracking.

## Service Information

- **Service Name**: Report Mail Service
- **File Path**: `/src/services/reportMail.js`
- **Type**: Email Reporting & Notification Service
- **Dependencies**: AWS SES, Canvas/WebP, MongoDB, MySQL, Incentive APIs

## Core Functions

### Token Management Functions

#### genToken(length = 64)
Generates secure random tokens for database record identification.

**Purpose**: Creates unique identifiers for mail list, batch, and status records
**Parameters**: 
- `length` (optional): Token length, defaults to 64 characters
**Returns**: Random alphanumeric string

**Example**:
```javascript
const token = genToken(32);
// Returns: "aB3dF9kL2mN8pQ1rS4tV7wX0yZ5cE6gH"
```

#### genMailListToken(), genMailBatchToken(), genMailStatusToken()
Generate unique tokens with database collision checking for specific record types.

**Purpose**: Ensures unique token generation with database validation
**Parameters**: None
**Returns**: Promise resolving to unique token string

### User Management Functions

#### addUsers(users = [])
Adds new users to the report mail list with unique token generation.

**Purpose**: Registers users for email reporting with unique identification
**Parameters**:
- `users`: Array of user objects with id and email properties
**Returns**: Promise (async function)

**Process Flow**:
1. Iterates through user array
2. Checks for existing email address
3. Generates unique token for new users
4. Inserts user record into RptMailList table
5. Logs successful additions

#### addMailList(userIds = [])
Synchronizes mail list with all eligible users from authentication system.

**Purpose**: Maintains current mail list by adding new users
**Parameters**: 
- `userIds` (optional): Specific user IDs to process
**Returns**: Promise (async function)

**Example**:
```javascript
await addMailList();
// Logs: "[addMailList] add user {user_id: 123, email: 'user@example.com', token: 'abc123'}"
```

### Batch Processing Functions

#### addMailBatch()
Creates new mail batch for bi-weekly report generation with user filtering.

**Purpose**: Initiates new reporting cycle with qualified user selection
**Parameters**: None
**Returns**: Promise (async function)

**Batch Creation Logic**:
1. Prevents duplicate batches within 10-day window
2. Generates descriptive batch title with environment prefix
3. Filters users created more than 14 days ago
4. Requires recent app activity (AppData within 14 days)
5. Creates batch record with user count and status

**User Qualification Criteria**:
- Account older than 14 days
- Recent app activity
- Email subscription status active
- No existing batch record

#### executeMailList(batches = [])
Processes mail batches and sends reports to qualified users.

**Purpose**: Executes email sending for active batches
**Parameters**:
- `batches` (optional): Specific batches to process, defaults to all active
**Returns**: Promise (async function)

**Process Flow**:
1. Retrieves active batches (status = 1)
2. Calculates 2-week reporting period
3. Processes each batch with user list
4. Updates batch status upon completion
5. Handles errors without stopping other batches

### Report Content Generation

#### getStats(user, start, end)
Generates comprehensive transportation statistics for user reporting period.

**Purpose**: Calculates CO2 savings, money saved, and trip counts
**Parameters**:
- `user`: User object with access token and creation date
- `start`: Report period start date
- `end`: Report period end date
**Returns**: Promise resolving to statistics object

**Statistics Calculated**:
```javascript
{
  co2_saved: "25.67",           // Pounds of CO2 saved
  money_saved: "45.23",         // Dollar amount saved  
  trip_number: 15,              // Total trips since registration
  weekly_trip_number: 3,        // Trips in report period
  co2_saved_weekly: "5.12",     // Weekly CO2 savings
  money_saved_weekly: "8.90",   // Weekly money savings
  tree: "base64ImageData",      // Tree progress image
  attachment: {...}             // Email attachment object
}
```

**CO2 Calculation Logic**:
- **Carpool Rider/Driver**: 0.5x driving emissions
- **Telework**: 2x driving emissions saved
- **Walking/Cycling**: Full driving emissions saved
- **Transit**: Reduced emissions vs driving
- **Ridehail**: Considers estimated fare vs driving cost

#### getRewards(user, start, end)
Calculates reward points and tokens earned during reporting period.

**Purpose**: Summarizes user reward activity and balances
**Parameters**:
- `user`: User object with ID
- `start`, `end`: Date range for reward calculation
**Returns**: Promise resolving to rewards object

**Reward Metrics**:
```javascript
{
  weeklyPoints: "150.00",    // Points earned this period
  totalPoints: "1250.50",    // Total points balance
  weeklyTokens: "75.00",     // Tokens earned this period  
  totalTokens: "890.25",     // Total token balance
  raffleTickets: "12"        // Current raffle ticket count
}
```

### Alert & Information Systems

#### getUISInfo(user)
Retrieves construction and weather alerts for user's upcoming reservations.

**Purpose**: Provides location-based alerts for planned trips
**Parameters**:
- `user`: User object with ID
**Returns**: Promise resolving to alert information

**Alert Processing**:
1. Finds reservations in next 7 days
2. Retrieves polyline data for trip routes
3. Checks construction zones intersecting routes
4. Identifies weather alerts affecting trip areas
5. Generates AI-translated alert messages

#### getConstructions(user, reservationPolylines)
Identifies construction zones affecting user trip routes.

**Purpose**: Provides construction alert information for planned routes
**Parameters**:
- `user`: User object with timezone and language
- `reservationPolylines`: Array of trip polyline data
**Returns**: Promise resolving to construction messages array

**Construction Detection**:
- MongoDB geospatial intersection queries
- Time-based relevance categorization
- Multi-language AI message generation
- Route-specific impact assessment

#### getWeather(user, reservationPolylines)
Detects weather alerts affecting user trip routes.

**Purpose**: Provides weather-related travel warnings
**Parameters**:
- `user`: User object with device language
- `reservationPolylines`: Array of trip route data
**Returns**: Promise resolving to weather alert messages

### Incentive System Integration

#### getIncentives(user, start, end)
Retrieves comprehensive incentive data including badges, bingo cards, and tier status.

**Purpose**: Gathers gamification elements for user engagement
**Parameters**:
- `user`: User object with access token
- `start`, `end`: Date range for incentive calculation
**Returns**: Promise resolving to incentive data object

**Incentive Components**:
```javascript
{
  bingocard: {
    title: "Weekly Challenge",
    left: 3,                    // Squares remaining
    image: "data:image/png...", // Generated image
    attachment: {...}           // Email attachment
  },
  badge: {
    id: 1,
    name: "Trip Master",
    value: 75,                  // Current progress
    required_value: 100,        // Target value
    x: 25,                      // Remaining to achieve
    y: "trips"                  // Unit description
  },
  tier: {
    level: "bronze",
    required_points: 125,       // Points to next tier
    title: "Reach the Silver Tier!",
    body: "You are only 125 points away..."
  }
}
```

#### getBingocard(user, start, end)
Generates visual bingo card representation with progress tracking.

**Purpose**: Creates interactive bingo card image for email inclusion
**Parameters**:
- `user`: User object with access token
- `start`, `end`: Date range (not directly used)
**Returns**: Promise resolving to bingo card data or null

**Visual Generation**:
- Canvas-based image creation (576x576 pixels)
- Dynamic icon positioning based on grid size
- Progress calculation for completion tracking
- Base64 encoded image for email embedding

#### getBadge(user, start, end)
Creates visual badge progress representation with custom graphics.

**Purpose**: Shows badge advancement with progress bar visualization
**Parameters**:
- `user`: User object with access token
- `start`, `end`: Date range (not directly used)
**Returns**: Promise resolving to badge data object

**Badge Visualization**:
- 568x568 pixel canvas with progress graphics
- Dynamic progress bar based on achievement level
- Custom typography with Open Sans font family
- Gradient progress indicators
- Achievement milestone markers

#### getTier(user, start, end)
Generates tier status visualization with point progression.

**Purpose**: Displays tier advancement progress with visual feedback
**Parameters**:
- `user`: User object with ID
- `start`, `end`: Date range (not directly used)
**Returns**: Promise resolving to tier data or null for green tier

**Tier System**:
- **Bronze**: 500 points minimum
- **Silver**: 1,000 points minimum  
- **Gold**: 1,500 points minimum
- Visual progress bar with milestone markers
- Expiration warnings for current tier points

### Email Generation & Delivery

#### mailContent(user, token, start, end, list)
Generates complete HTML email content with all report components.

**Purpose**: Assembles comprehensive email report with all user data
**Parameters**:
- `user`: Complete user object with access token
- `token`: Unique mail status token
- `start`, `end`: Report date range
- `list`: Mail list record with unsubscribe token
**Returns**: Promise resolving to email content object

**Content Assembly**:
```javascript
{
  html: "<html>...</html>",        // Complete email HTML
  attachments: [...],              // Image attachments array
  unsubscribeUrl: "https://..."    // One-click unsubscribe link
}
```

**Template Data**:
- User statistics and achievements
- Reward summaries and balances
- Weather and construction alerts
- Incentive progress visualizations
- Personalized greetings and recommendations

#### sendSESRawMail(mail, title, html, attachments, unsubscribeUrl)
Sends multi-part MIME email via Amazon SES with inline attachments.

**Purpose**: Delivers rich HTML emails with embedded images
**Parameters**:
- `mail`: Recipient email address
- `title`: Email subject line
- `html`: Complete HTML email content
- `attachments`: Array of image attachments
- `unsubscribeUrl`: Unsubscribe link URL
**Returns**: Promise resolving to SES Message ID

**MIME Structure**:
- Multipart/related content type
- Base64 encoded HTML content
- Inline image attachments with Content-ID headers
- List-Unsubscribe headers for compliance
- AWS SES configuration set integration

#### processMailList(list, id, title, reportStart, reportEnd)
Processes individual mail batch with comprehensive error handling.

**Purpose**: Sends emails to batch user list with status tracking
**Parameters**:
- `list`: Array of mail status records to process
- `id`: Mail batch ID
- `title`: Email subject line
- `reportStart`, `reportEnd`: Report date range
**Returns**: Promise resolving to array of Message IDs

**Processing Flow**:
1. Creates/validates user access tokens
2. Retrieves user and mail list data
3. Checks subscription status
4. Generates personalized email content
5. Sends email via AWS SES
6. Updates status with success/error codes
7. Continues processing despite individual failures

**Status Codes**:
- **1**: Successfully sent
- **2**: Access token creation failed
- **3**: User or list data not found
- **4**: User unsubscribed
- **5**: Unauthorized access
- **6**: General error

### Visual Asset Management

#### initResources()
Loads and caches WebP image resources for visual generation.

**Purpose**: Preloads image assets for efficient email generation
**Parameters**: None
**Returns**: Promise (async function)

**Resource Loading**:
- Star icon for completed activities
- 42 colored tile icons for different activities
- 42 grayscale versions for locked activities
- WebP format with canvas conversion
- Memory caching for performance

#### loadWebP(path)
Converts WebP images to Canvas Image objects for rendering.

**Purpose**: Handles WebP image format conversion
**Parameters**:
- `path`: Relative path to WebP image file
**Returns**: Promise resolving to Canvas Image object

**Conversion Process**:
1. Reads WebP file from filesystem
2. Decodes WebP data to ImageData
3. Creates Canvas context
4. Converts to Image object for drawing operations

### Calculation Utilities

#### calculateCO2(trips)
Calculates carbon dioxide savings based on trip mode and distance.

**Purpose**: Quantifies environmental impact of transportation choices
**Parameters**:
- `trips`: Array of trip objects with travel_mode and distance
**Returns**: Total CO2 saved in pounds

**Calculation Factors**:
- **Base driving emission**: 0.88 lbs CO2 per mile
- **Mile conversion**: distance * 0.00062 (meters to miles)
- **Mode multipliers**: carpool (0.5x), telework (2x), transit (0.64x)
- **Zero impact**: driving, intermodal, instant carpool

#### calculateSaving(trips)
Calculates monetary savings compared to driving costs.

**Purpose**: Quantifies financial benefits of alternative transportation
**Parameters**:
- `trips`: Array of trip objects with mode and distance data
**Returns**: Promise resolving to total dollar savings

**Saving Calculations**:
- **Base driving cost**: $0.58 per mile
- **Carpool**: Driving cost minus fare and premium
- **Transit**: Driving cost minus $1.25 average fare
- **Ridehail**: Driving cost minus estimated fare
- **Active modes**: Full driving cost savings

### Configuration & Environment

#### genMailTitle()
Generates environment-appropriate email subject line.

**Purpose**: Creates descriptive subject with environment indicators
**Parameters**: None
**Returns**: Formatted email subject string

**Environment Prefixes**:
- **Development**: "(DEV) Smart Moves: Last Week's Wins..."
- **Sandbox**: "(SB) Smart Moves: Last Week's Wins..."
- **Production**: "Smart Moves: Last Week's Wins..."

**API URL Generators**:
- `getIncentiveAPIURL()`: Returns environment-specific incentive API URL
- `getIncentiveHookURL()`: Returns environment-specific hook URL

## Data Sources

### MySQL Portal Database
- **AuthUser**: User authentication and profile data
- **Trip**: Transportation trip records
- **Reservation**: Trip reservation data
- **RptMail*** tables: Report mail management
- **PointsTransaction**: Reward point transactions
- **TokenTransaction**: Token reward transactions

### MongoDB Collections
- **WeatherCriticalAlert**: Weather alert data with geospatial indexing
- **ConstructionZone**: Construction zone data with temporal filtering
- **ReservationPolyline**: Trip route geometries
- **TripTrajectory**: GPS tracking data for trips

### External APIs
- **Incentive API**: Badge, bingo card, and tier data
- **Incentive Hook API**: Tier status and point calculations
- **Portal API**: Statistics and raffle ticket information
- **AWS SES**: Email delivery service
- **AWS S3**: Static asset storage

## Integration Points

### Used By
- **Scheduled Jobs**: Bi-weekly report generation
- **Admin Commands**: Manual report triggering
- **Batch Processing**: Large-scale email campaigns
- **User Engagement**: Retention and motivation

### External Dependencies
- **Canvas/WebP**: Image generation and processing
- **AWS SES**: Email delivery infrastructure
- **JWT Helper**: Access token management
- **EJS Templates**: HTML email template rendering
- **Moment.js**: Date/time manipulation with timezone support

## Email Template System

### Template Structure
- **biweeklyReport3.ejs**: Main email template file
- **Dynamic Content**: Stats, rewards, alerts, incentives
- **Responsive Design**: Mobile and desktop compatible
- **Image Integration**: Inline attachments with CID references

### Personalization Features
- **User Name**: Personalized greeting
- **Date Range**: Formatted report period
- **Statistics**: Individual user metrics
- **Recommendations**: Based on user activity patterns
- **Unsubscribe**: One-click unsubscribe compliance

## Error Handling & Resilience

### Database Resilience
- **Connection pooling**: Efficient resource management
- **Transaction safety**: Atomic operations where needed
- **Graceful degradation**: Continues despite partial failures
- **Comprehensive logging**: Detailed error tracking

### Email Delivery
- **AWS SES integration**: Reliable delivery infrastructure
- **Bounce handling**: SES feedback processing
- **Rate limiting**: Respects SES sending limits
- **Retry logic**: Built into batch processing

### Visual Generation
- **Resource caching**: Prevents repeated file loading
- **Error isolation**: Individual image failures don't stop batch
- **Memory management**: Efficient canvas operations
- **Format validation**: Ensures proper image encoding

## Performance Considerations

### Batch Processing Optimization
- **Parallel Operations**: Multiple database queries
- **Efficient Queries**: Optimized joins and indexes
- **Memory Management**: Streams large datasets
- **Resource Pooling**: Reuses connections and resources

### Image Generation Performance
- **Canvas Optimization**: Efficient drawing operations
- **WebP Compression**: Smaller file sizes
- **Caching Strategy**: Reuses loaded resources
- **Parallel Processing**: Independent image generation

### Email Delivery Optimization
- **SES Raw Email**: Efficient multi-part MIME
- **Attachment Optimization**: Base64 encoding efficiency
- **Batch Status Tracking**: Prevents duplicate sends
- **Error Recovery**: Continues processing after failures

## Security Considerations

### Email Security
- **List-Unsubscribe**: RFC-compliant unsubscribe headers
- **Content Validation**: Sanitized user data
- **Token Security**: Unique tokens prevent unauthorized access
- **Access Control**: JWT-based API authentication

### Data Protection
- **Personal Data**: Limited to necessary fields
- **Token Rotation**: Prevents long-term token abuse
- **Secure Storage**: Encrypted database connections
- **Audit Logging**: Complete operation tracking

## Compliance Features

### Email Compliance
- **CAN-SPAM**: Required headers and unsubscribe
- **GDPR**: Data minimization and user consent
- **List Management**: Subscription status tracking
- **Delivery Reporting**: SES feedback integration

### Data Retention
- **Mail Status**: Tracks delivery attempts
- **Error Logging**: Debugging and compliance
- **User Preferences**: Respects subscription choices
- **Cleanup Jobs**: Removes old batch data

## Usage Guidelines

### Report Generation
1. **Scheduling**: Run addMailBatch weekly
2. **Processing**: Execute batch processing daily
3. **Monitoring**: Check batch completion status
4. **Error Handling**: Review failed deliveries

### Visual Content
1. **Resource Management**: Initialize resources before batch processing
2. **Canvas Operations**: Efficient image generation
3. **Memory Usage**: Monitor for memory leaks
4. **File Storage**: Clean up temporary files

### Email Delivery
1. **SES Limits**: Respect sending quotas
2. **Bounce Handling**: Process delivery notifications
3. **List Hygiene**: Remove invalid addresses
4. **Personalization**: Ensure data accuracy

## Dependencies

- **moment-timezone**: Date manipulation with timezone support
- **ejs**: Email template rendering
- **superagent**: HTTP client for API calls
- **canvas**: Server-side image generation
- **@cwasm/webp**: WebP image processing
- **aws-sdk**: Amazon Web Services integration
- **@maas/core**: Database and logging utilities
- **Various Models**: Database ORM models for data access