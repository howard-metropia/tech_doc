# Knex Database Configuration

## 📋 Quick Summary
**Purpose:** Knex.js configuration file for database migrations and seeds - manages MySQL database connections and directory structure for TSP API.

**Keywords:** knex | database-config | mysql | migrations | seeds | objection-orm | database-setup

## 🔧 Technical Specifications
- **File:** knexfile.js (Knex configuration)
- **Database:** MySQL2 client
- **ORM:** Objection.js (Model global setup)
- **Dependencies:** dotenv, config, objection, mysql2
- **Config Source:** Uses config module for database connection details

## 📝 Code Analysis
```javascript
require('dotenv').config();  // Load environment variables
const config = require('config');  // Get configuration
const { Model } = require('objection');  // Objection ORM
global.Model = Model;  // Make Model globally available

module.exports = {
  client: 'mysql2',  // MySQL2 database client
  connection: config.get('database.mysql.portal'),  // Portal DB connection
  migrations: {
    directory: './database/migrations',  // Migration files location
  },
  seeds: {
    directory: './database/seeds',  // Seed files location
  },
};
```

**Configuration Details:**
- **Client:** MySQL2 for improved performance and features
- **Connection:** Portal database from config (host, user, password, database)
- **Migrations:** Located in `./database/migrations/`
- **Seeds:** Located in `./database/seeds/`

## 🚀 Usage Methods
```bash
# Run migrations
npx knex migrate:latest

# Rollback migrations
npx knex migrate:rollback

# Run seeds
npx knex seed:run

# Create new migration
npx knex migrate:make migration_name

# Create new seed
npx knex seed:make seed_name
```

## 📊 Output Examples
```bash
$ npx knex migrate:latest
Using environment: development
Batch 1 run: 3 migrations

$ npx knex seed:run
Using environment: development
Ran 2 seed files
```

## ⚠️ Important Notes
- **Global Model:** Makes Objection.js Model class globally available
- **Environment:** Uses config module for environment-specific settings
- **Portal Database:** Specifically configured for portal database connection
- **MySQL2:** Requires MySQL2 client for proper operation
- **Migration Order:** Migrations run in filename order (timestamp-based)

## 🔗 Related Files
- `config/default.js` - Database connection configuration
- `database/migrations/` - All migration files
- `database/seeds/` - All seed files
- `src/models/` - Objection.js model definitions
- `.env` - Environment variables for database credentials

## 📈 Use Cases
- **Development:** Local database setup and data seeding
- **Deployment:** Production database migrations
- **Testing:** Test database preparation
- **CI/CD:** Automated database schema updates

## 🏷️ Tags
**Keywords:** knex, database-config, mysql, migrations, seeds, objection-orm
**Category:** #database #configuration #migrations #infrastructure
**Difficulty:** ⭐⭐ (Configuration - requires database knowledge)
**Criticality:** High (Essential for database operations)