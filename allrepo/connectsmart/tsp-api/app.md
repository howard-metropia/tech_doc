# TSP API Application Entry Point

## Overview
The main entry point for the TSP (Transportation Service Provider) API application. This file serves as the CLI bootstrapper and command-line interface for the TSP API service.

## File Purpose
- **Primary Function**: Application entry point and CLI command handler
- **Type**: Executable Node.js script
- **Role**: Bootstraps the TSP API service and processes command-line arguments

## Key Components

### Dependencies
- `@maas/core/bootstrap`: Core MaaS platform bootstrapping functionality
- `@maas/core`: Core MaaS platform utilities and program management
- `package.json`: Application metadata and version information

### Main Functionality

#### CLI Program Setup
```javascript
const { getProgram } = require('@maas/core');
const program = getProgram();
program.version(pjson.version);
program.parse(process.argv);
```

**Key Features:**
- Initializes the MaaS core platform
- Sets up command-line argument parsing
- Configures version information from package.json
- Processes CLI arguments for service execution

## Architecture Integration

### Bootstrapping Process
1. **Core Bootstrap**: Initializes `@maas/core/bootstrap` for platform setup
2. **Program Configuration**: Sets up CLI program with version and argument parsing
3. **Service Launch**: Processes command-line arguments to start appropriate services

### CLI Command Structure
The application supports various CLI commands managed by the MaaS core platform:
- Service startup commands
- Database migration commands
- Scheduled job execution
- Development and production mode switches

## Usage Examples

### Development Mode
```bash
./app.js dev
```

### Production Mode
```bash
./app.js prod
```

### Scheduler Jobs
```bash
./app.js schedule
```

## Technical Details

### Executable Configuration
- **Shebang**: `#!/usr/bin/env node` - Makes file executable as Node.js script
- **Version Management**: Dynamically loads version from package.json
- **Command Processing**: Delegates to MaaS core program handler

### Error Handling
- Relies on MaaS core platform for error handling and logging
- Command-line argument validation handled by core program

## Dependencies
- **@maas/core**: Core MaaS platform functionality
- **package.json**: Application metadata

## Integration Points
- Entry point for all TSP API operations
- Integrates with MaaS core platform services
- Connects to database, scheduling, and service management systems

## Security Considerations
- Executable permissions required for CLI operation
- Environment variable dependencies managed through MaaS core
- Authentication and authorization handled by downstream services

## Maintenance Notes
- Version updates automatically reflected from package.json
- Command-line interface extensions should be added through MaaS core
- Bootstrap configuration changes require coordination with core platform