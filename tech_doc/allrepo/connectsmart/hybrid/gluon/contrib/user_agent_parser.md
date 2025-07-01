# Gluon Contrib User Agent Parser Module

## Overview
User agent string parsing utilities for web2py applications. Provides functionality to parse and analyze HTTP User-Agent headers to extract browser, operating system, and device information.

## Module Information
- **Module**: `gluon.contrib.user_agent_parser`
- **Purpose**: User agent string analysis
- **Use Case**: Analytics, device detection, browser compatibility

## Key Features
- **Browser Detection**: Identify browser type and version
- **OS Detection**: Determine operating system
- **Device Detection**: Identify device types (mobile, tablet, desktop)
- **Bot Detection**: Identify web crawlers and bots
- **Analytics Support**: Provide data for web analytics

## Basic Usage

### User Agent Parsing
```python
from gluon.contrib.user_agent_parser import UserAgentParser

# Parse user agent
parser = UserAgentParser()
user_agent = request.env.http_user_agent

parsed = parser.parse(user_agent)

print(f"Browser: {parsed.browser.family} {parsed.browser.version}")
print(f"OS: {parsed.os.family} {parsed.os.version}")
print(f"Device: {parsed.device.family}")
```

### Analytics Integration
```python
def log_visitor_info():
    """Log visitor information for analytics"""
    
    parser = UserAgentParser()
    parsed = parser.parse(request.env.http_user_agent)
    
    # Store visitor information
    db.visitor_logs.insert(
        ip_address=request.env.remote_addr,
        user_agent=request.env.http_user_agent,
        browser_family=parsed.browser.family,
        browser_version=parsed.browser.version,
        os_family=parsed.os.family,
        os_version=parsed.os.version,
        device_family=parsed.device.family,
        is_mobile=parsed.is_mobile,
        is_tablet=parsed.is_tablet,
        is_bot=parsed.is_bot,
        visit_time=datetime.datetime.now(),
        page_url=request.url
    )
    db.commit()

def get_browser_stats():
    """Get browser usage statistics"""
    
    # Get browser statistics from logs
    browser_stats = db(db.visitor_logs).select(
        db.visitor_logs.browser_family,
        db.visitor_logs.id.count(),
        groupby=db.visitor_logs.browser_family,
        orderby=~db.visitor_logs.id.count()
    )
    
    return [
        {
            'browser': row.visitor_logs.browser_family,
            'count': row._extra[db.visitor_logs.id.count()]
        }
        for row in browser_stats
    ]
```

### Device-Specific Content
```python
def responsive_content():
    """Serve device-specific content"""
    
    parser = UserAgentParser()
    parsed = parser.parse(request.env.http_user_agent)
    
    if parsed.is_mobile:
        # Mobile-specific content
        response.view = 'mobile/index.html'
        return dict(device_type='mobile')
    
    elif parsed.is_tablet:
        # Tablet-specific content
        response.view = 'tablet/index.html'
        return dict(device_type='tablet')
    
    else:
        # Desktop content
        response.view = 'desktop/index.html'
        return dict(device_type='desktop')
```

This module provides essential user agent parsing capabilities for web2py applications, enabling device detection and analytics functionality.