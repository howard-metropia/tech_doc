# Database Mock Module for Testing

## Overview
A comprehensive mock implementation of database services designed for testing environments. This module provides Sinon-based stubs to replace actual database operations during test execution, ensuring tests run in isolation without requiring real database connections.

## File Purpose
- **Primary Function**: Mock database services for testing
- **Type**: Test utility module
- **Role**: Database service replacement during test execution

## Key Components

### Mock Models Object
Provides stubbed implementations of common database models:

```javascript
const mockModels = {
  Trip: {
    findByPk: sinon.stub().resolves({}),
    findAll: sinon.stub().resolves([])
  },
  DuoReservations: {
    findOne: sinon.stub().resolves({})
  },
  sequelize: {
    query: sinon.stub().resolves([[], null]),
    QueryTypes: { SELECT: 'SELECT' },
    Sequelize: {
      Op: { in: Symbol('in') }
    }
  }
};
```

### Mock MongoDB Integration
Provides stubbed implementations for MongoDB operations:

```javascript
const mockMongo = {
  db: {
    collection: sinon.stub().returns({
      find: sinon.stub().returns({
        toArray: sinon.stub().resolves([])
      }),
      findOne: sinon.stub().resolves(null)
    })
  }
};
```

## Functionality

### SQL Database Mocking
- **Trip Model**: Mocks trip-related database operations
- **DuoReservations Model**: Mocks reservation-related operations
- **Sequelize Integration**: Provides ORM-compatible interface
- **Query Operations**: Supports raw SQL query mocking

### MongoDB Mocking
- **Collection Access**: Mocks MongoDB collection operations
- **Find Operations**: Supports both single and multiple document queries
- **Promise-based API**: Maintains async/await compatibility

### Sinon Integration
- **Stub Creation**: Uses Sinon stubs for predictable test behavior
- **Return Value Control**: Pre-configured return values for common scenarios
- **Test Isolation**: Ensures tests don't interfere with each other

## Technical Specifications

### Sequelize Model Mocking

#### Trip Model Interface
- `findByPk()`: Returns empty object by default
- `findAll()`: Returns empty array by default
- Fully stubbed for test customization

#### DuoReservations Model Interface
- `findOne()`: Returns empty object by default
- Supports reservation-related test scenarios

#### Sequelize Core Mocking
- **Raw Queries**: `sequelize.query()` returns `[[], null]`
- **Query Types**: Provides `SELECT` query type constant
- **Operators**: Includes `Op.in` symbol for query building

### MongoDB Model Mocking

#### Collection Interface
- **Collection Access**: `db.collection()` returns mock collection
- **Find Operations**: Chainable find operations
- **Array Conversion**: `toArray()` resolves to empty array
- **Single Document**: `findOne()` resolves to null

## Usage Examples

### Basic Test Setup
```javascript
const mockDatabase = require('./mocks/database');

// Replace actual database with mocks
jest.mock('@maas/core/services/database', () => mockDatabase);
```

### Customizing Mock Behavior
```javascript
const { models } = require('./mocks/database');

// Customize Trip model behavior
models.Trip.findByPk.resolves({ id: 1, name: 'Test Trip' });
models.Trip.findAll.resolves([{ id: 1 }, { id: 2 }]);
```

### MongoDB Mock Customization
```javascript
const { mongo } = require('./mocks/database');

// Customize MongoDB behavior
mongo.db.collection.returns({
  find: sinon.stub().returns({
    toArray: sinon.stub().resolves([{ _id: '123', data: 'test' }])
  })
});
```

## Testing Patterns

### Model Testing
```javascript
describe('Trip Service', () => {
  beforeEach(() => {
    // Reset all stubs
    sinon.resetHistory();
  });

  it('should find trip by ID', async () => {
    models.Trip.findByPk.resolves({ id: 1, status: 'active' });
    
    const result = await tripService.getById(1);
    expect(models.Trip.findByPk).toHaveBeenCalledWith(1);
    expect(result.id).toBe(1);
  });
});
```

### MongoDB Testing
```javascript
describe('Reservation Service', () => {
  it('should query reservations', async () => {
    const mockResult = [{ _id: '123', userId: 456 }];
    mongo.db.collection().find().toArray.resolves(mockResult);
    
    const result = await reservationService.findAll();
    expect(result).toEqual(mockResult);
  });
});
```

## Integration with Test Frameworks

### Jest Integration
- Compatible with Jest mocking system
- Supports manual mocking with `jest.mock()`
- Works with Jest's beforeEach/afterEach hooks

### Mocha/Chai Integration
- Compatible with Mocha test structure
- Works with Chai assertions
- Supports Sinon's restore functionality

### Test Isolation
- Stubs can be reset between tests
- Consistent initial state for each test
- Prevents test interference

## Mock Configuration

### Default Behaviors
- Most operations return empty results
- Promises resolve successfully
- No error conditions by default

### Customization Options
- Override any stub behavior for specific tests
- Chain multiple stub configurations
- Support complex return value scenarios

## Dependencies

### External Dependencies
- `sinon`: Stub and mock functionality
- Relies on Sinon's stub API for behavior control

### Integration Dependencies
- Designed to replace `@maas/core/services/database`
- Compatible with Sequelize ORM patterns
- Supports MongoDB driver patterns

## Security Considerations

### Test Environment Safety
- No real database connections
- No sensitive data exposure
- Isolated from production systems

### Mock Data Management
- Test data doesn't persist
- No authentication required
- Simplified for testing scenarios

## Performance Benefits

### Test Execution Speed
- No database I/O operations
- Instant stub responses
- Parallel test execution support

### Resource Efficiency
- No database connection overhead
- Minimal memory usage
- Fast test suite execution

## Maintenance Notes

### Adding New Models
1. Add model stub to `mockModels` object
2. Include common methods with default returns
3. Document expected behavior patterns

### Mock Updates
- Keep mocks synchronized with actual model interfaces
- Update when database schema changes
- Maintain compatibility with ORM changes

### Testing Best Practices
- Reset stubs between tests
- Use specific stub configurations for each test case
- Avoid over-mocking - focus on units under test