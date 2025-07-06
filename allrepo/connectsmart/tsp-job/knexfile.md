# TSP Job Service - Knex Configuration File

## Overview

The `knexfile.js` serves as the database configuration file for Knex.js, the SQL query builder used by the TSP Job service for MySQL database operations. This file defines database connection settings, migration configurations, and seed data management for the application's relational database needs.

## File Information

- **File Path**: `/knexfile.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: Knex.js database configuration and migration management
- **Dependencies**: dotenv, config module, Objection.js ORM

## Configuration Structure

### Environment and Dependencies
```javascript
require('dotenv').config();
const config = require('config');
const { Model } = require('objection');
global.Model = Model;
```

**Purpose**: 
- Loads environment variables from `.env` files
- Imports application configuration
- Sets up Objection.js ORM as a global reference

### Database Configuration Export
```javascript
module.exports = {
  client: 'mysql2',
  connection: JSON.parse(JSON.stringify(config.get('database.mysql.dataset'))),
  migrations: {
    directory: './database/migrations',
  },
  seeds: {
    directory: './database/seeds',
  },
};
```

## Configuration Components

### 1. Database Client
```javascript
client: 'mysql2'
```

**Purpose**: Specifies the database driver to use
- **mysql2**: Modern MySQL driver with improved performance
- Supports prepared statements and connection pooling
- Promise-based API for better async/await support
- Enhanced security with SQL injection protection

### 2. Connection Configuration
```javascript
connection: JSON.parse(JSON.stringify(config.get('database.mysql.dataset')))
```

**Purpose**: Deep clone of database connection settings
- Prevents configuration mutation during runtime
- Retrieves connection details from centralized config
- Supports environment-specific database configurations

**Expected Connection Structure**:
```javascript
{
  host: 'localhost',
  port: 3306,
  user: 'tsp_job_user',
  password: 'secure_password',
  database: 'tsp_job_db',
  charset: 'utf8mb4',
  timezone: 'UTC',
  ssl: {
    rejectUnauthorized: false
  },
  pool: {
    min: 2,
    max: 10,
    createTimeoutMillis: 3000,
    acquireTimeoutMillis: 30000,
    idleTimeoutMillis: 30000,
    reapIntervalMillis: 1000,
    createRetryIntervalMillis: 100
  }
}
```

### 3. Migration Configuration
```javascript
migrations: {
  directory: './database/migrations',
}
```

**Purpose**: Defines location of database migration files
- **Directory**: `./database/migrations/`
- Contains versioned schema changes
- Supports forward and backward migrations
- Enables database version control

### 4. Seed Configuration
```javascript
seeds: {
  directory: './database/seeds',
}
```

**Purpose**: Defines location of database seed files
- **Directory**: `./database/seeds/`
- Contains initial data population scripts
- Supports development and testing data
- Enables consistent data setup across environments

## Migration Management

### Available Migrations
The TSP Job service includes several migration files:

```javascript
// Example migrations in ./database/migrations/
const migrations = [
  '20250312063641_hntb_trip.js',           // HNTB trip data structure
  '20250313021039_hntb_rating.js',         // Rating system tables
  '20250313023754_hntb_bytemark_pass.js',  // Transit pass management
  '20250313032335_hntb_tow_and_go.js',     // Tow and Go service tables
  '20250313060040_hntb_school_zone.js',    // School zone definitions
  '20250317013526_hntb_pre_trip_alert.js', // Pre-trip alert system
  '20250317063457_hntb_saving_travel_time.js', // Travel time optimization
  '20250321064848_hntb_target_user.js',    // User targeting system
  '20250328021124_hntb_habitual_trip_origin.js', // Habitual trip analysis
  '20250331030708_quick_sight_table.js',   // Analytics tables
  '20250407031131_hntb_bytemark_order_payments.js', // Payment processing
  '20250425031207_MET-19138.js'            // Specific feature implementation
];
```

### Migration Commands
```bash
# Run all pending migrations
npx knex migrate:latest

# Rollback the last migration
npx knex migrate:rollback

# Check migration status
npx knex migrate:status

# Create new migration
npx knex migrate:make migration_name
```

## Database Schema Architecture

### Core Tables
The migrations create tables for various TSP Job service functions:

#### Trip Management Tables
- **hntb_trip**: Core trip data and metadata
- **hntb_habitual_trip_origin**: Habitual travel pattern analysis
- **hntb_saving_travel_time**: Travel time optimization data

#### Transit Integration Tables
- **hntb_bytemark_pass**: Digital transit pass management
- **hntb_bytemark_order_payments**: Transit payment processing
- **hntb_rating**: User rating and feedback system

#### Location Services Tables
- **hntb_school_zone**: School zone definitions and restrictions
- **hntb_tow_and_go**: Tow and go service locations and data

#### User Engagement Tables
- **hntb_target_user**: User targeting and segmentation
- **hntb_pre_trip_alert**: Pre-trip notification system

#### Analytics Tables
- **quick_sight_table**: Data warehouse integration for analytics

## Environment-Specific Configurations

### Development Environment
```javascript
// Development configuration example
module.exports = {
  development: {
    client: 'mysql2',
    connection: {
      host: 'localhost',
      port: 3306,
      user: 'dev_user',
      password: 'dev_password',
      database: 'tsp_job_dev',
      charset: 'utf8mb4'
    },
    migrations: {
      directory: './database/migrations'
    },
    seeds: {
      directory: './database/seeds'
    },
    debug: true
  }
};
```

### Production Environment
```javascript
// Production configuration example
module.exports = {
  production: {
    client: 'mysql2',
    connection: {
      host: process.env.DB_HOST,
      port: process.env.DB_PORT,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_DATABASE,
      ssl: { rejectUnauthorized: false },
      pool: {
        min: 5,
        max: 20
      }
    },
    migrations: {
      directory: './database/migrations'
    },
    acquireConnectionTimeout: 60000,
    asyncStackTraces: false
  }
};
```

## Objection.js Integration

### Model Binding
```javascript
const { Model } = require('objection');
global.Model = Model;
```

**Purpose**: Makes Objection.js Model class globally available
- Enables ORM functionality throughout the application
- Provides query builder interface
- Supports model relationships and validations

### Model Usage Example
```javascript
// Example model usage with Knex configuration
class Trip extends Model {
  static get tableName() {
    return 'hntb_trip';
  }
  
  static get jsonSchema() {
    return {
      type: 'object',
      required: ['origin', 'destination', 'userId'],
      properties: {
        id: { type: 'integer' },
        origin: { type: 'string' },
        destination: { type: 'string' },
        userId: { type: 'integer' },
        distance: { type: 'number' },
        duration: { type: 'number' },
        createdAt: { type: 'string', format: 'date-time' }
      }
    };
  }
  
  static get relationMappings() {
    return {
      user: {
        relation: Model.BelongsToOneRelation,
        modelClass: User,
        join: {
          from: 'hntb_trip.userId',
          to: 'users.id'
        }
      }
    };
  }
}
```

## Connection Pool Management

### Pool Configuration
```javascript
pool: {
  min: 2,                    // Minimum connections
  max: 10,                   // Maximum connections
  createTimeoutMillis: 3000, // Connection creation timeout
  acquireTimeoutMillis: 30000, // Connection acquisition timeout
  idleTimeoutMillis: 30000,  // Idle connection timeout
  reapIntervalMillis: 1000,  // Connection reaper interval
  createRetryIntervalMillis: 100 // Retry interval for failed connections
}
```

**Benefits**:
- Optimized database connection usage
- Prevents connection exhaustion
- Handles connection failures gracefully
- Improves application performance

## Security Considerations

### Connection Security
- SSL/TLS encryption for database connections
- Credential management through environment variables
- Connection timeout configurations to prevent hanging connections
- SQL injection protection through prepared statements

### Access Control
- Database user permissions restricted to necessary operations
- Separate credentials for different environments
- Regular credential rotation policies
- Audit logging for database operations

## Performance Optimization

### Query Optimization
```javascript
// Example optimized query patterns
const optimizedQuery = Trip.query()
  .select('id', 'origin', 'destination', 'duration')
  .where('userId', userId)
  .whereRaw('created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)')
  .orderBy('created_at', 'desc')
  .limit(100);
```

### Index Management
```javascript
// Example migration with proper indexing
exports.up = function(knex) {
  return knex.schema.createTable('hntb_trip', function(table) {
    table.increments('id').primary();
    table.integer('userId').unsigned().notNullable();
    table.string('origin').notNullable();
    table.string('destination').notNullable();
    table.decimal('distance', 10, 2);
    table.integer('duration');
    table.timestamps(true, true);
    
    // Indexes for performance
    table.index(['userId', 'created_at']);
    table.index('origin');
    table.index('destination');
    table.foreign('userId').references('users.id');
  });
};
```

## Testing and Development

### Test Database Configuration
```javascript
// Test environment configuration
test: {
  client: 'mysql2',
  connection: {
    host: 'localhost',
    user: 'test_user',
    password: 'test_password',
    database: 'tsp_job_test',
    charset: 'utf8mb4'
  },
  migrations: {
    directory: './database/migrations'
  },
  seeds: {
    directory: './database/seeds'
  }
}
```

### Migration Testing
```javascript
// Example migration test
describe('Database Migrations', () => {
  beforeEach(async () => {
    await knex.migrate.rollback();
    await knex.migrate.latest();
  });
  
  it('should create all required tables', async () => {
    const tables = await knex.raw('SHOW TABLES');
    expect(tables[0]).to.have.length.greaterThan(10);
  });
});
```

## Troubleshooting

### Common Issues
1. **Connection Timeout**: Increase `acquireTimeoutMillis` value
2. **Pool Exhaustion**: Increase `max` pool size or optimize query patterns
3. **Migration Failures**: Check database permissions and schema conflicts
4. **SSL Errors**: Verify SSL certificate configuration

### Debug Configuration
```javascript
// Enable debugging for development
debug: process.env.NODE_ENV === 'development',
log: {
  warn(message) {
    console.warn(message);
  },
  error(message) {
    console.error(message);
  },
  deprecate(message) {
    console.log(message);
  },
  debug(message) {
    console.debug(message);
  }
}
```

This Knex configuration file provides a robust foundation for database operations in the TSP Job service, supporting development, testing, and production environments with proper migration management and performance optimization.