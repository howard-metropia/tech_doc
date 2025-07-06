# Streamer Module

## Overview
The streamer module provides efficient file streaming capabilities for web2py applications. It handles static file delivery with support for HTTP range requests, conditional responses (304 Not Modified), partial content delivery (206 Partial Content), compression, and browser caching. This module is essential for serving static assets, downloads, and media files efficiently.

## Core Functions

### streamer()
Generator function for streaming file content in chunks.

```python
def streamer(stream, chunk_size=DEFAULT_CHUNK_SIZE, 
             bytes=None, callback=None)
```

**Parameters:**
- `stream`: File-like object to read from
- `chunk_size`: Size of each chunk (default: 64KB)
- `bytes`: Total bytes to stream (None = all)
- `callback`: Function to call after streaming

**Features:**
- Memory-efficient streaming
- Automatic stream closure
- Progress tracking
- Callback support

**Example:**
```python
with open('large_file.zip', 'rb') as f:
    for chunk in streamer(f, chunk_size=8192):
        # Process chunk
        yield chunk
```

### stream_file_or_304_or_206()
Main function for serving static files with HTTP optimizations.

```python
def stream_file_or_304_or_206(static_file, chunk_size=DEFAULT_CHUNK_SIZE,
                              request=None, headers={}, status=200,
                              error_message=None)
```

**HTTP Features:**
- **304 Not Modified**: If-Modified-Since handling
- **206 Partial Content**: Range request support
- **Compression**: Gzip file serving
- **Caching**: Proper cache headers

## HTTP Response Types

### 304 Not Modified
Returned when file hasn't changed since last request.

```python
if request and request.env.http_if_modified_since == mtime:
    raise HTTP(304, **{"Content-Type": headers["Content-Type"]})
```

**Benefits:**
- Reduces bandwidth usage
- Improves loading performance
- Leverages browser caching

### 206 Partial Content
Supports HTTP range requests for resume capability.

```python
if request and request.env.http_range:
    start_items = regex_start_range.findall(request.env.http_range)
    stop_items = regex_stop_range.findall(request.env.http_range)
    
    part = (int(start_items[0]), int(stop_items[0]), fsize)
    bytes = part[1] - part[0] + 1
    
    headers["Content-Range"] = "bytes %i-%i/%i" % part
    headers["Content-Length"] = "%i" % bytes
    status = 206
```

**Use Cases:**
- Video/audio streaming
- Download resumption
- Progressive loading
- Mobile optimization

## Compression Support

### Gzip Handling
Automatic compressed file serving when available.

```python
if enc and "gzip" in enc and not "Content-Encoding" in headers:
    gzipped = static_file + ".gz"
    if os.path.isfile(gzipped) and os.path.getmtime(gzipped) >= modified:
        static_file = gzipped
        fsize = os.path.getsize(gzipped)
        headers["Content-Encoding"] = "gzip"
        headers["Vary"] = "Accept-Encoding"
```

**Requirements:**
- Pre-compressed .gz files
- Newer than original files
- Client accepts gzip encoding

## Configuration

### Default Settings
```python
DEFAULT_CHUNK_SIZE = 64 * 1024  # 64KB chunks

# Range parsing regex
regex_start_range = re.compile(r"\d+(?=\-)")
regex_stop_range = re.compile(r"(?<=\-)\d+")
```

### Headers Management
```python
# Default headers
headers.setdefault('Content-Type', contenttype(static_file))
headers.setdefault('Last-Modified', mtime)
headers.setdefault('Pragma', 'cache')
headers.setdefault('Cache-Control', 'private')
```

## Usage Examples

### Basic File Streaming
```python
def download():
    """Serve file downloads"""
    filename = request.args(0)
    file_path = os.path.join(request.folder, 'uploads', filename)
    
    try:
        stream_file_or_304_or_206(
            file_path,
            request=request,
            headers={'Content-Type': 'application/octet-stream'}
        )
    except HTTP as http_response:
        return http_response
```

### Video Streaming
```python
def video():
    """Stream video files with range support"""
    video_id = request.args(0)
    video_path = get_video_path(video_id)
    
    # Enable range requests for video
    response.headers['Accept-Ranges'] = 'bytes'
    
    try:
        stream_file_or_304_or_206(
            video_path,
            request=request,
            headers={'Content-Type': 'video/mp4'}
        )
    except HTTP as http_response:
        return http_response
```

### Custom Streaming with Callback
```python
def monitored_download():
    """Download with progress tracking"""
    file_path = get_file_path()
    
    def log_completion():
        # Log download completion
        db.downloads.insert(
            user_id=auth.user_id,
            file_path=file_path,
            completed_on=request.now
        )
    
    with open(file_path, 'rb') as f:
        for chunk in streamer(f, callback=log_completion):
            yield chunk
```

### Conditional Downloads
```python
def protected_download():
    """Download with access control"""
    if not auth.user:
        raise HTTP(401, "Authentication required")
    
    file_id = request.args(0)
    record = db.files(file_id)
    
    if not record or record.owner != auth.user_id:
        raise HTTP(403, "Access denied")
    
    file_path = os.path.join(request.folder, 'private', record.filename)
    
    try:
        stream_file_or_304_or_206(
            file_path,
            request=request,
            headers={
                'Content-Type': record.content_type,
                'Content-Disposition': 'attachment; filename="%s"' % record.original_name
            }
        )
    except HTTP as http_response:
        return http_response
```

## Error Handling

### File Access Errors
```python
try:
    fp = open(static_file, 'rb')
except IOError as e:
    if e.errno == errno.EISDIR:
        raise HTTP(403, error_message, web2py_error="file is a directory")
    elif e.errno == errno.EACCES:
        raise HTTP(403, error_message, web2py_error="inaccessible file")
    else:
        raise HTTP(404, error_message, web2py_error="invalid file")
```

### Common Error Codes
- **403 Forbidden**: Directory access or permission denied
- **404 Not Found**: File doesn't exist
- **416 Range Not Satisfiable**: Invalid range request

## Performance Optimization

### Chunk Size Selection
```python
# Optimize chunk size based on use case
SMALL_FILES = 8 * 1024      # 8KB for small files
STANDARD_FILES = 64 * 1024  # 64KB default
LARGE_FILES = 1024 * 1024   # 1MB for large files

def optimal_chunk_size(file_size):
    if file_size < 100 * 1024:      # < 100KB
        return SMALL_FILES
    elif file_size < 10 * 1024 * 1024:  # < 10MB
        return STANDARD_FILES
    else:
        return LARGE_FILES
```

### Memory Management
```python
def memory_efficient_stream(file_path):
    """Stream without loading entire file"""
    file_size = os.path.getsize(file_path)
    chunk_size = optimal_chunk_size(file_size)
    
    with open(file_path, 'rb') as f:
        for chunk in streamer(f, chunk_size=chunk_size):
            yield chunk
```

### Caching Strategy
```python
def cached_file_info(file_path):
    """Cache file metadata"""
    cache_key = 'file_info_%s' % hash(file_path)
    
    info = cache.ram(cache_key, 
                     lambda: os.stat(file_path),
                     time_expire=300)  # 5 minutes
    return info
```

## Integration with Web2py

### Static File Handler
```python
# In routes.py or controller
def static_handler():
    """Enhanced static file serving"""
    filename = '/'.join(request.args)
    static_path = os.path.join(request.folder, 'static', filename)
    
    if not os.path.exists(static_path):
        raise HTTP(404)
    
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    
    stream_file_or_304_or_206(static_path, request=request)
```

### Upload Downloads
```python
def download():
    """Standard web2py download function with streaming"""
    filename = request.args(0)
    upload_path = os.path.join(request.folder, 'uploads', filename)
    
    # Validate filename
    if not filename or '..' in filename:
        raise HTTP(404)
    
    stream_file_or_304_or_206(upload_path, request=request)
```

## Security Considerations

### Path Validation
```python
def secure_path(filename):
    """Validate file path for security"""
    # Prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        raise HTTP(403, "Invalid path")
    
    # Validate allowed characters
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        raise HTTP(403, "Invalid filename")
    
    return True
```

### Access Control
```python
def check_download_permission(file_path, user):
    """Verify user can access file"""
    # Check file ownership
    file_record = db(db.files.path == file_path).select().first()
    
    if not file_record:
        raise HTTP(404)
    
    if file_record.private and file_record.owner != user.id:
        raise HTTP(403)
    
    return True
```

### Rate Limiting
```python
def rate_limited_download():
    """Implement download rate limiting"""
    user_ip = request.env.remote_addr
    cache_key = 'downloads_%s' % user_ip
    
    downloads = cache.ram(cache_key, lambda: 0, time_expire=3600)
    
    if downloads > 100:  # Max 100 downloads per hour
        raise HTTP(429, "Rate limit exceeded")
    
    cache.ram(cache_key, lambda: downloads + 1, time_expire=3600)
```

## Advanced Features

### Resume Support
```python
def resumable_download():
    """Support download resumption"""
    file_path = get_file_path()
    
    # Add resume headers
    response.headers['Accept-Ranges'] = 'bytes'
    response.headers['Content-Length'] = str(os.path.getsize(file_path))
    
    stream_file_or_304_or_206(file_path, request=request)
```

### Custom WSGI File Wrapper
```python
def wsgi_file_wrapper():
    """Use WSGI file wrapper when available"""
    if request.env.web2py_use_wsgi_file_wrapper:
        # Let WSGI server handle file streaming
        return request.env.wsgi_file_wrapper(stream, chunk_size)
    else:
        # Use Python streaming
        return streamer(stream, chunk_size=chunk_size)
```

## Monitoring and Logging

### Download Tracking
```python
def logged_download():
    """Track download statistics"""
    def completion_callback():
        db.download_stats.insert(
            file_path=file_path,
            user_id=auth.user_id,
            ip_address=request.env.remote_addr,
            user_agent=request.env.http_user_agent,
            downloaded_on=request.now
        )
    
    with open(file_path, 'rb') as f:
        for chunk in streamer(f, callback=completion_callback):
            yield chunk
```

### Performance Metrics
```python
def timed_stream():
    """Monitor streaming performance"""
    import time
    start_time = time.time()
    bytes_sent = 0
    
    def track_progress():
        nonlocal bytes_sent
        duration = time.time() - start_time
        speed = bytes_sent / duration if duration > 0 else 0
        logger.info("Stream completed: %d bytes in %.2fs (%.2f KB/s)",
                   bytes_sent, duration, speed / 1024)
    
    for chunk in streamer(stream, callback=track_progress):
        bytes_sent += len(chunk)
        yield chunk
```

## Best Practices

### File Serving
1. Use appropriate chunk sizes for file types
2. Implement proper error handling
3. Add security headers
4. Support range requests for media files
5. Enable compression when beneficial

### Performance
1. Pre-compress static files
2. Set appropriate cache headers
3. Use WSGI file wrapper when available
4. Monitor memory usage
5. Implement rate limiting

### Security
1. Validate all file paths
2. Implement access controls
3. Prevent directory traversal
4. Log download activities
5. Use HTTPS for sensitive files

## See Also
- HTTP/1.1 Range Requests specification
- WSGI file wrapper documentation
- Web2py upload/download guide
- Performance optimization techniques