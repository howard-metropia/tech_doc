# PimaUsers.js - TSP Job Model Documentation

## Quick Summary

The PimaUsers model represents Pima County employee users within the TSP Job scheduling system. This Objection.js ORM model provides database access to the `pima_users` table in the dataset database, storing verified Pima County government employees who are registered for the MaaS platform. The model is primarily used for analytics and data synchronization processes that track employee participation in transportation programs.

## Technical Analysis

### Code Structure
```javascript
const knex = require('@maas/core/mysql')('dataset');
class PimaUSers extends Model {
  static get tableName() {
    return 'pima_users';
  }
}
module.exports = PimaUSers.bindKnex(knex);
```

### Critical Bug Identified
The model contains a critical implementation error - it extends the `Model` class from Objection.js but fails to import it. The correct implementation should include:
```javascript
const { Model } = require('objection');
```

### Database Connection
- **Database**: `dataset` (MySQL connection via @maas/core)
- **Table**: `pima_users`
- **Connection Pattern**: Uses Knex.js query builder bound to the model
- **Multi-tenancy**: Separated from portal database for analytics isolation

### Data Schema Analysis
Based on the pima.js service implementation, the table stores:
- `user_id`: Primary identifier linking to auth_user table
- `UserID`: Hashed version of user_id for privacy
- `enterprise_email`: Pima County email address
- `email_token`: Email verification token
- `enterprise_domain`: Email domain (pima.gov, sc.pima.gov, etc.)
- `joined_group_date`: Enterprise group registration timestamp
- `verification_date`: Email verification completion timestamp
- `first_name`, `last_name`: User profile information
- `email_verify`: Verification status ('Verified'/'Not Verified')

## Usage/Integration

### Primary Integration Points

**Pima Data Synchronization Service** (`src/services/pima.js`):
- Used in `writeUsers()` function for bulk data operations
- Processes enterprise employee registration data from portal to dataset database
- Implements batch processing with 1000-record chunks for performance
- Excludes specific test users and domains for data quality

**Analytics and Reporting**:
- Foundation for Pima County employee transportation analytics
- Used by `writeReservations()` and `writeTrips()` to filter relevant user data
- Supports time-zone conversion from UTC to US/Mountain timezone
- Integrates with InfluxDB for scheduling job metrics

### Processing Workflow
1. **Data Extraction**: Portal database enterprise table queried for verified members
2. **User Filtering**: Excludes test accounts and specific domains
3. **Data Transformation**: User ID hashing and timezone conversion
4. **Batch Processing**: 1000-record batches to prevent memory issues
5. **Duplicate Prevention**: Checks existing records before insertion
6. **Metrics Recording**: Success metrics written to InfluxDB

## Dependencies

### Core Dependencies
- **@maas/core/mysql**: Database connection management for dataset database
- **objection**: ORM framework (missing import - requires fix)
- **knex**: SQL query builder (provided through @maas/core)
- **moment-timezone**: Date/time processing in US/Mountain timezone
- **@app/src/helpers/hashId**: User ID hashing for privacy protection
- **@app/src/helpers/influxDb**: Performance metrics logging

### Database Dependencies
- **dataset.pima_users**: Primary table for model operations
- **portal.enterprise**: Source data for synchronization
- **portal.auth_user**: User profile information source

### Security Considerations
- User ID hashing prevents direct user identification in analytics database
- Email domain validation ensures only legitimate Pima County employees
- Exclusion lists prevent test data contamination
- Separate dataset database provides analytics isolation

## Code Examples

### Basic Model Usage
```javascript
const PimaUsers = require('@app/src/models/PimaUsers');

// Query all Pima users
const allUsers = await PimaUsers.query();

// Find users by user_id
const specificUsers = await PimaUsers.query()
  .whereIn('user_id', [1001, 1002, 1003]);

// Get user count
const userCount = await PimaUsers.query().count();
```

### Batch Processing Pattern (from pima.js service)
```javascript
// Check for existing users before insertion
let existedUserIds = await PimaUsers.query()
  .select('user_id')
  .whereIn('user_id', memberIds);

// Batch insert new users
const finalData = processedUsers.filter(user => 
  !existedUserIds.includes(user.user_id)
);

if (finalData.length) {
  await datasetKnex(PimaUsers.tableName).insert(finalData);
}
```

### Integration with Other Models
```javascript
// Used in conjunction with PimaTrips and PimaReservations
const pimaUsers = await PimaUsers.query().select('user_id');
const pimaUserIds = pimaUsers.map(el => el.user_id);

// Filter trips for Pima users only
const pimaTrips = await PimaTrips.query()
  .whereIn('user_id', pimaUserIds);
```

### Data Transformation Example
```javascript
// Hash user ID for privacy (from pima.js)
row.UserID = hashid(row.user_id);

// Convert timezone for local reporting
row.joined_group_date = moment
  .utc(row.joined_group_date)
  .tz('US/Mountain')
  .format('YYYY-MM-DD HH:mm:ss');
```

This model serves as a critical component in the Pima County employee transportation analytics pipeline, enabling secure and efficient processing of employee mobility data while maintaining privacy through user ID hashing and database separation.