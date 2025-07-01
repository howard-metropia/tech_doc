# Gluon Contrib RSS2 Module

## Overview
PyRSS2Gen library for generating RSS 2.0 feeds in web2py applications. Provides a Python interface for creating standards-compliant RSS feeds with support for all RSS 2.0 elements and extensions.

## Module Information
- **Module**: `gluon.contrib.rss2`
- **Original**: PyRSS2Gen by Andrew Dalke
- **License**: BSD License
- **Version**: 1.1.0
- **Purpose**: RSS 2.0 feed generation

## Key Features
- **RSS 2.0 Compliance**: Full RSS 2.0 specification support
- **Easy Generation**: Simple Python API for feed creation
- **Extensible**: Support for RSS extensions and custom elements
- **Web2py Integration**: Seamless integration with web2py applications
- **Unicode Support**: Proper handling of international content

## Main Classes

### RSS2
Main RSS feed class representing the complete RSS document.

### RSSItem
Individual RSS feed item/entry class.

## Basic Usage

### Simple Feed Generation
```python
from gluon.contrib.rss2 import RSS2, RSSItem
import datetime

# Create RSS feed
rss = RSS2(
    title="My Blog",
    link="http://example.com/blog",
    description="Latest posts from my blog",
    lastBuildDate=datetime.datetime.now()
)

# Add items
item1 = RSSItem(
    title="First Post",
    link="http://example.com/blog/post1",
    description="This is my first blog post",
    pubDate=datetime.datetime.now()
)

item2 = RSSItem(
    title="Second Post", 
    link="http://example.com/blog/post2",
    description="This is my second blog post",
    pubDate=datetime.datetime.now()
)

rss.items = [item1, item2]

# Generate XML
rss_xml = rss.to_xml()
```

### Web2py Controller Integration
```python
def rss():
    """Generate RSS feed for blog posts"""
    from gluon.contrib.rss2 import RSS2, RSSItem
    
    # Get recent posts
    posts = db(db.posts.published==True).select(
        orderby=~db.posts.created_on,
        limitby=(0, 20)
    )
    
    # Create RSS feed
    rss = RSS2(
        title="%s Blog" % request.application,
        link=URL('default', 'index', scheme=True),
        description="Latest blog posts",
        lastBuildDate=datetime.datetime.now(),
        generator="web2py RSS generator"
    )
    
    # Add items
    items = []
    for post in posts:
        item = RSSItem(
            title=post.title,
            link=URL('default', 'post', args=[post.id], scheme=True),
            description=post.summary or post.content[:200] + "...",
            pubDate=post.created_on,
            guid=URL('default', 'post', args=[post.id], scheme=True)
        )
        items.append(item)
    
    rss.items = items
    
    # Set proper content type
    response.headers['Content-Type'] = 'application/rss+xml'
    
    return rss.to_xml()
```

### Advanced Feed Features
```python
def advanced_rss():
    """RSS feed with advanced features"""
    
    # Create feed with full metadata
    rss = RSS2(
        title="Tech News",
        link="http://example.com",
        description="Latest technology news and updates",
        language="en-us",
        copyright="Copyright 2023 Tech News",
        managingEditor="editor@example.com",
        webMaster="webmaster@example.com",
        category="Technology",
        ttl=60,  # Time to live in minutes
        image=RSSImage(
            url="http://example.com/logo.png",
            title="Tech News",
            link="http://example.com"
        )
    )
    
    # Add items with extended metadata
    posts = db(db.posts).select(limitby=(0, 10))
    items = []
    
    for post in posts:
        item = RSSItem(
            title=post.title,
            link=URL('post', args=[post.slug], scheme=True),
            description=post.summary,
            author=post.author_email,
            category=post.category,
            pubDate=post.published_on,
            guid=URL('post', args=[post.slug], scheme=True),
            # Add enclosure for podcasts/media
            enclosure=post.audio_file and RSSEnclosure(
                url=URL('download', args=[post.audio_file], scheme=True),
                length=post.audio_size,
                type="audio/mpeg"
            )
        )
        items.append(item)
    
    rss.items = items
    return rss.to_xml()
```

## Feed Validation and Optimization

### RSS Validation
```python
def validate_rss_content(content):
    """Validate RSS content before publishing"""
    try:
        # Basic XML validation
        import xml.etree.ElementTree as ET
        ET.fromstring(content)
        
        # Check required elements
        required_elements = ['title', 'link', 'description']
        for element in required_elements:
            if f'<{element}>' not in content:
                return False, f"Missing required element: {element}"
        
        return True, "RSS feed is valid"
    
    except ET.ParseError as e:
        return False, f"XML parsing error: {str(e)}"
```

### Performance Optimization
```python
@cache.action(time_expire=3600)  # Cache for 1 hour
def cached_rss():
    """Cached RSS feed for better performance"""
    return generate_rss_feed()

def generate_rss_feed():
    """Generate RSS feed with optimized queries"""
    
    # Optimized database query
    posts = db(db.posts.published==True).select(
        db.posts.title,
        db.posts.slug,
        db.posts.summary,
        db.posts.published_on,
        db.posts.author_name,
        orderby=~db.posts.published_on,
        limitby=(0, 20),
        cacheable=True
    )
    
    # Generate feed
    rss = RSS2(
        title="Cached Blog Feed",
        link=URL('index', scheme=True),
        description="Efficiently generated RSS feed"
    )
    
    # Add items efficiently
    rss.items = [
        RSSItem(
            title=post.title,
            link=URL('post', args=[post.slug], scheme=True),
            description=post.summary,
            pubDate=post.published_on
        ) for post in posts
    ]
    
    return rss.to_xml()
```

This module enables web2py applications to generate standards-compliant RSS feeds for content syndication, supporting all RSS 2.0 features and providing easy integration with web2py's MVC architecture.