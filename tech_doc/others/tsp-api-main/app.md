# TSP API CLI Entry Point

## 📋 Quick Summary
**Purpose:** Main CLI entry point for the TSP (Transportation Service Provider) API application - bootstraps the MaaS core system and provides command-line interface functionality.

**Keywords:** cli | entry-point | bootstrap | command-line | tsp-api | maas-core | application-launcher

## 🔧 Technical Specifications
- **File:** app.js (CLI executable)
- **Framework:** @maas/core CLI framework
- **Type:** Node.js CLI application entry point
- **Dependencies:** @maas/core (core MaaS framework), package.json (version info)
- **Executable:** Can be run directly via `./app.js` or `node app.js`

## 📝 Code Analysis
```javascript
#!/usr/bin/env node
require('@maas/core/bootstrap');  // Initialize MaaS core system
const { getProgram } = require('@maas/core');  // Get CLI program instance
const program = getProgram();  // Create CLI program
program.version(pjson.version);  // Set version from package.json
program.parse(process.argv);  // Parse command line arguments
```

**Execution Flow:**
1. Bootstrap MaaS core system (database connections, configs)
2. Create CLI program instance from @maas/core
3. Set application version from package.json
4. Parse and execute command line arguments

## 🚀 Usage Methods
```bash
# Direct execution
./app.js --help

# Via Node.js
node app.js --version

# Common commands (defined in @maas/core)
./app.js start    # Start the server
./app.js migrate  # Run database migrations
./app.js seed     # Run database seeds
```

## 📊 Output Examples
```bash
$ ./app.js --version
2.1.0

$ ./app.js --help
Usage: app [options] [command]
Options:
  -V, --version  output the version number
  -h, --help     display help for command
```

## ⚠️ Important Notes
- **Bootstrap Dependency:** Requires @maas/core/bootstrap to initialize the system
- **CLI Commands:** Actual commands are defined in @maas/core framework
- **Execution:** Must be run from TSP API directory for proper context
- **Permissions:** Requires executable permissions on Unix systems

## 🔗 Related Files
- `package.json` - Contains version information
- `@maas/core/bootstrap` - Core system initialization
- `@maas/core` - CLI framework and command definitions
- `src/index.js` - Main application server entry point

## 📈 Use Cases
- **Development:** Start development server, run migrations, seed data
- **Deployment:** Production server startup and maintenance tasks
- **CI/CD:** Automated deployment scripts and database operations
- **Administration:** Manual system maintenance and debugging

## 🏷️ Tags
**Keywords:** cli, entry-point, bootstrap, tsp-api, maas-core, command-line
**Category:** #cli #entry-point #bootstrap #infrastructure
**Difficulty:** ⭐ (Simple - basic CLI wrapper)
**Criticality:** High (Main application entry point)