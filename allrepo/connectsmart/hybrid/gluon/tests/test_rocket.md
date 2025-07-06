# test_rocket.py

## Overview
This file is a placeholder for future Rocket web server tests, containing only TODO comments about testing strategy.

## Current Status
The file contains no actual test code, only planning notes for future implementation.

## Proposed Testing Approach

### Tool Recommendation
The TODO suggests using **pathoc** (from the pathod project) for testing Rocket.

### What is pathoc?
- Part of the pathod testing framework
- A flexible HTTP/HTTPS client
- Designed for testing HTTP servers
- Can craft arbitrary HTTP requests
- Useful for edge cases and malformed requests

### Integration Plan
The comment suggests:
1. Continue using pathoc for Rocket testing
2. Integrate pathoc calls into the gluon/tests suite
3. Enable automatic test execution
4. Avoid reimplementing existing test functionality

## Reference
Links to a Google Groups discussion about Web2py developers' testing strategies:
- URL: https://groups.google.com/d/msg/web2py-developers/Cjye8_hXZk8/AXbftS3sCgAJ
- Likely contains discussion about testing approaches for Rocket

## Rocket Web Server Context

### What is Rocket?
- Pure Python web server included with Web2py
- Lightweight WSGI server
- No external dependencies
- Supports SSL/HTTPS
- Multi-threaded

### Why Test Rocket?
Important areas for testing include:
- HTTP protocol compliance
- Request parsing
- Response generation
- Error handling
- Performance under load
- SSL/TLS functionality
- Threading behavior

## Potential Test Coverage

### Basic HTTP Tests
- GET, POST, PUT, DELETE methods
- Header parsing
- Content encoding
- Keep-alive connections
- Chunked transfers

### Security Tests
- SSL certificate handling
- Protocol negotiation
- Malformed request handling
- DoS protection

### Performance Tests
- Concurrent connections
- Request throughput
- Memory usage
- Thread pool management

### Edge Cases
- Large payloads
- Slow clients
- Aborted connections
- Protocol violations

## Benefits of pathoc

### Request Crafting
```python
# Example pathoc usage (not in file)
# Send custom malformed request
pathoc.Pathoc("localhost", 8000).request("get:/foo:h'Invalid-Header'=value")
```

### Test Scenarios
- Invalid HTTP syntax
- Header injection
- Protocol fuzzing
- Timing attacks

## Integration Considerations

### Automated Testing
- Should run as part of test suite
- No manual intervention required
- Clear pass/fail criteria
- Performance benchmarks

### Test Isolation
- Start/stop Rocket for each test
- Clean state between tests
- Port management
- Process cleanup

## Notes
- This placeholder indicates testing infrastructure is planned but not implemented
- The reference to external discussion shows collaborative development approach
- Using established tools (pathoc) rather than reinventing testing
- Focus on integration with existing test framework