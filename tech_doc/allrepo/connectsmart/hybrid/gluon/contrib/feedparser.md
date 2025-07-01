# Gluon Contrib Feedparser Module

## Overview
Universal feed parser for RSS and Atom feeds. This module handles RSS 0.9x, RSS 1.0, RSS 2.0, CDF, Atom 0.3, and Atom 1.0 feeds with comprehensive parsing capabilities and error handling.

## Module Information
- **Module**: `gluon.contrib.feedparser`
- **Version**: 5.2.1
- **Author**: Mark Pilgrim
- **License**: BSD-style license
- **Dependencies**: None (pure Python)

## Key Features
- **Multi-format Support**: Handles multiple RSS and Atom feed formats
- **HTTP Support**: Built-in HTTP client with headers and caching
- **Error Handling**: Robust parsing with bozo detection for malformed feeds
- **Encoding Detection**: Automatic character encoding detection
- **Sanitization**: Optional HTML content sanitization
- **Geospatial Support**: Geographic data parsing for location-aware feeds
- **Python 2/3 Compatible**: Works with both Python versions

## Configuration Constants

### Global Settings
```python
USER_AGENT = "UniversalFeedParser/5.2.1 +https://code.google.com/p/feedparser/"
ACCEPT_HEADER = "application/atom+xml,application/rdf+xml,application/rss+xml,..."
PREFERRED_XML_PARSERS = ["drv_libxml2"]
RESOLVE_RELATIVE_URIS = 1
SANITIZE_HTML = 1
```

## Main Functions

### parse()
Primary feed parsing function that accepts various input sources.

**Signature:**
```python
def parse(url_file_stream_or_string, etag=None, modified=None, agent=None, 
          referrer=None, handlers=None, request_headers=None, response_headers=None)
```

**Parameters:**
- `url_file_stream_or_string`: Feed source (URL, file path, stream, or string)
- `etag`: HTTP ETag for conditional requests
- `modified`: Last-Modified header for conditional requests
- `agent`: Custom User-Agent string
- `referrer`: HTTP Referrer header
- `handlers`: Custom URL handlers
- `request_headers`: Additional HTTP request headers
- `response_headers`: Override response headers

**Returns:**
`FeedParserDict` containing:
- `feed`: Feed metadata
- `entries`: List of feed entries
- `bozo`: Error flag (1 if malformed)
- `bozo_exception`: Exception details if errors occurred
- `headers`: HTTP response headers

## Core Classes

### FeedParserDict
Enhanced dictionary class for feed data with attribute access.

**Key Features:**
- Attribute-style access (`feed.title` instead of `feed['title']`)
- Nested structure support
- Unicode handling
- Backward compatibility

### _FeedParserMixin
Base parser class containing XML parsing logic and feed-specific handlers.

**Key Methods:**
- `_start_*()`: Element start handlers
- `_end_*()`: Element end handlers
- `_mapToStandardPrefix()`: Namespace mapping
- `_save()`: Data preservation during parsing

## Feed Format Support

### RSS Formats
- **RSS 0.90**: Basic RSS support
- **RSS 0.91**: Netscape RSS format
- **RSS 0.92**: UserLand RSS format
- **RSS 0.93**: UserLand RSS format
- **RSS 0.94**: UserLand RSS format
- **RSS 1.0**: RDF Site Summary
- **RSS 2.0**: Really Simple Syndication

### Atom Formats
- **Atom 0.3**: Early Atom specification
- **Atom 1.0**: Current Atom specification

### Other Formats
- **CDF**: Channel Definition Format
- **RDF**: Resource Description Framework

## Content Processing

### HTML Sanitization
When `SANITIZE_HTML = 1`:
- Removes potentially dangerous HTML tags
- Filters JavaScript and other executable content
- Preserves safe formatting tags
- Handles entity encoding

### Encoding Detection
Automatic detection of:
- XML encoding declarations
- HTTP Content-Type headers
- Byte Order Marks (BOM)
- Heuristic encoding detection

### Relative URI Resolution
When `RESOLVE_RELATIVE_URIS = 1`:
- Converts relative URLs to absolute URLs
- Uses feed base URI or document URL
- Handles complex URI resolution cases

## Geospatial Support

### Supported Formats
- **GeoRSS Simple**: Basic geographic data
- **GeoRSS GML**: Geography Markup Language
- **W3C Geo**: Simple latitude/longitude

### Geographic Elements
- Point locations
- Bounding boxes
- Complex geometries
- Coordinate systems

## Error Handling

### Bozo Detection
Identifies and flags malformed feeds:
- XML parsing errors
- Invalid feed structure
- Missing required elements
- Encoding problems

### Exception Types
- `SAXParseException`: XML parsing errors
- `UnicodeError`: Character encoding issues
- `URLError`: Network/HTTP errors
- Custom feedparser exceptions

## HTTP Features

### Conditional Requests
- ETag support for caching
- Last-Modified headers
- HTTP 304 Not Modified handling

### Custom Headers
- User-Agent customization
- Accept header configuration
- Custom request headers
- Referrer support

### Authentication
- Basic HTTP authentication
- Custom authentication handlers
- Proxy support

## Performance Considerations

### Memory Usage
- Streaming parser design
- Minimal memory footprint
- Efficient string handling
- Optional content filtering

### Speed Optimization
- Preferred XML parser selection
- Namespace optimization
- Selective parsing options
- Caching mechanisms

## Usage Examples

### Basic Usage
```python
import feedparser

# Parse from URL
d = feedparser.parse('http://example.com/feed.xml')

# Access feed data
print(d.feed.title)
print(d.feed.description)

# Access entries
for entry in d.entries:
    print(entry.title)
    print(entry.link)
    print(entry.published)
```

### Advanced Usage
```python
# With custom headers
headers = {'User-Agent': 'MyApp/1.0'}
d = feedparser.parse('http://example.com/feed.xml', 
                    request_headers=headers)

# With caching
d = feedparser.parse('http://example.com/feed.xml',
                    etag=previous_etag,
                    modified=previous_modified)

# From file
d = feedparser.parse('/path/to/feed.xml')

# From string
feed_data = open('feed.xml').read()
d = feedparser.parse(feed_data)
```

### Error Handling
```python
d = feedparser.parse('http://example.com/feed.xml')

if d.bozo:
    print("Feed has errors:", d.bozo_exception)
else:
    print("Feed parsed successfully")
    
# Check for specific content
if hasattr(d.feed, 'title'):
    print("Feed title:", d.feed.title)
```

## Integration Notes

### Web2py Integration
- Used for RSS/Atom feed processing in web applications
- Integrates with web2py's HTTP client features
- Supports web2py's caching mechanisms
- Compatible with web2py's Unicode handling

### Security Considerations
- HTML content sanitization enabled by default
- Safe handling of external URLs
- Protection against XML external entity attacks
- Secure parsing of untrusted feed content

### Customization Options
- Parser preference configuration
- Content filtering rules
- Namespace handling
- Output format customization

## Dependencies
- **Standard Library**: xml.sax, urllib, re, time
- **Optional**: chardet (for better encoding detection)
- **Recommended**: iconv_codec (for character encoding)

This module provides comprehensive feed parsing capabilities for web2py applications, handling the complexity of various feed formats while maintaining security and performance.