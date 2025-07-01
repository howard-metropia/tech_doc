# autolinks.py

🔍 **Quick Summary (TL;DR)**
- Intelligent HTML content enhancement system that automatically converts URLs in text to embedded media, supporting images, videos, documents, and oEmbed services
- Core functionality: URL detection | media embedding | oEmbed integration | Google Docs viewer | automatic link conversion | HTML processing
- Primary use cases: Content management systems, blog posts, social media feeds, rich text processing, automatic media embedding
- Quick compatibility: Python 2.7+/3.x, BeautifulSoup for HTML parsing, Web2py framework, requires internet connectivity for oEmbed

❓ **Common Questions Quick Index**
- Q: What media types are auto-embedded? A: [Technical Specifications](#technical-specifications) - Images, videos, audio, documents, oEmbed services
- Q: Which services support oEmbed? A: [Detailed Code Analysis](#detailed-code-analysis) - YouTube, Vimeo, Flickr, SlideShare, etc.
- Q: How to process HTML content? A: [Usage Methods](#usage-methods) - Use expand_html() function
- Q: What document types are supported? A: [Output Examples](#output-examples) - PDF, DOC, PPT, XLS via Google Docs viewer
- Q: Is BeautifulSoup required? A: [Important Notes](#important-notes) - Yes, for HTML parsing and processing
- Q: How to handle email addresses? A: [Detailed Code Analysis](#detailed-code-analysis) - Automatically converts to mailto links
- Q: What if a service is down? A: [Important Notes](#important-notes) - Falls back to regular link
- Q: How to customize embedding? A: [Improvement Suggestions](#improvement-suggestions) - Extend EXTENSION_MAPS and EMBED_MAPS

📋 **Functionality Overview**
- **Non-technical explanation:** Like a smart assistant that reads through your web content and automatically turns plain text links into rich media - imagine posting a YouTube link and having it automatically become a playable video, or sharing a PDF link that becomes a viewable document. It recognizes different types of content and displays them in the best possible way.
- **Technical explanation:** Comprehensive URL detection and media embedding system that parses HTML content, identifies URLs, and replaces them with appropriate embedded media using oEmbed services, Google Docs viewer, or direct media embedding.
- Business value: Enhances user experience with rich media content, increases engagement through embedded media, reduces manual content formatting work
- Context: Content processing utility for Web2py applications requiring automatic media embedding and link enhancement

🔧 **Technical Specifications**
- File: autolinks.py, /gluon/contrib/, Python, Content processing utility, ~6KB, Medium complexity
- Dependencies: BeautifulSoup (HTML parsing), json (JSON handling), urllib (HTTP requests), re (regex), gluon._compat
- Compatibility: Python 2.7+/3.x, BeautifulSoup library, Web2py framework, internet connectivity for oEmbed
- Configuration: Predefined service mappings, customizable extension handlers, oEmbed endpoint definitions
- System requirements: BeautifulSoup installation, network access for external services
- Security: Safe HTML processing, external service dependency, URL validation through regex

📝 **Detailed Code Analysis**
```python
# Core media embedding functions
def image(url):
    return '<img src="%s" style="max-width:100%%"/>' % url

def video(url):
    return '<video controls="controls" style="max-width:100%%"><source src="%s" /></video>' % url

def googledoc_viewer(url):
    return '<iframe src="https://docs.google.com/viewer?url=%s&embedded=true" style="max-width:100%%"></iframe>' % urllib_quote(url)
```

**oEmbed Service Integration:**
```python
EMBED_MAPS = [
    (re.compile('http://\S*?flickr.com/\S*'),
     'http://www.flickr.com/services/oembed/'),
    (re.compile('http://\S*.youtu(\.be|be\.com)/watch\S*'),
     'http://www.youtube.com/oembed'),
    (re.compile('http://vimeo.com/\S*'),
     'http://vimeo.com/api/oembed.json'),
    # ... more services
]

def oembed(url):
    for pattern, endpoint in EMBED_MAPS:
        if pattern.match(url):
            oembed_url = endpoint + '?format=json&url=' + cgi.escape(url)
            try:
                data = urllib.urlopen(oembed_url).read()
                return loads(data)  # Parse JSON response
            except:
                pass
    return {}
```

**File Extension Mapping:**
```python
EXTENSION_MAPS = {
    'png': image, 'gif': image, 'jpg': image, 'jpeg': image,
    'wav': audio, 'ogg': audio, 'mp3': audio,
    'mov': video, 'mp4': video, 'mpeg': video,
    'pdf': googledoc_viewer, 'doc': googledoc_viewer,
    'ppt': googledoc_viewer, 'xls': googledoc_viewer,
    'load': web2py_component  # Web2py specific
}
```

**HTML Processing Engine:**
```python
def expand_html(html, cdict=None):
    if not have_soup:
        raise RuntimeError("Missing BeautifulSoup")
    
    soup = BeautifulSoup(html)
    # Remove HTML comments
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    [comment.extract() for comment in comments]
    
    # Process text nodes, avoiding already linked content
    for txt in soup.findAll(text=True):
        if not txt.parent.name in ('a', 'script', 'pre', 'code', 'embed', 'object', 'audio', 'video'):
            ntxt = regex_link.sub(
                lambda match: expand_one(match.group(0), cdict), txt)
            txt.replaceWith(BeautifulSoup(ntxt))
    
    return str(soup)
```

**Design Patterns:** Strategy pattern for different media types, Factory pattern for embed generation, Chain of responsibility for URL processing
**Performance:** Caching support via cdict parameter, regex-based URL detection, lazy loading of external services
**Error Handling:** Graceful fallback to regular links on service failures, exception handling for network issues

🚀 **Usage Methods**
```python
# Basic HTML expansion
from gluon.contrib.autolinks import expand_html

html_content = """
<p>Check out this video: http://www.youtube.com/watch?v=dQw4w9WgXcQ</p>
<p>And this image: http://example.com/image.jpg</p>
<p>Document: http://example.com/document.pdf</p>
"""

# Process and embed media
enhanced_html = expand_html(html_content)
print(enhanced_html)

# With caching for better performance
cache = {}
enhanced_html = expand_html(html_content, cdict=cache)

# Processing individual URLs
from gluon.contrib.autolinks import expand_one

# Embed a YouTube video
youtube_url = "http://www.youtube.com/watch?v=dQw4w9WgXcQ"
embedded = expand_one(youtube_url, {})

# Embed an image
image_url = "http://example.com/photo.jpg"
embedded_img = expand_one(image_url, {})

# Embed a PDF document
pdf_url = "http://example.com/document.pdf"
embedded_pdf = expand_one(pdf_url, {})
```

**Web2py Integration:**
```python
# In a Web2py controller
def process_content():
    user_content = request.vars.content
    enhanced_content = expand_html(user_content)
    return dict(content=enhanced_content)

# In a model for content processing
def enhance_post_content(post):
    if post.content:
        post.content = expand_html(post.content)
    return post
```

**Custom Extension Handling:**
```python
# Add custom media handler
def custom_handler(url):
    return f'<div class="custom-embed" data-url="{url}">Custom content</div>'

# Extend the extension map
EXTENSION_MAPS['xyz'] = custom_handler
```

📊 **Output Examples**
**YouTube Video Embedding:**
```html
<!-- Input -->
<p>http://www.youtube.com/watch?v=dQw4w9WgXcQ</p>

<!-- Output -->
<p><iframe width="480" height="270" src="http://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe></p>
```

**Image Embedding:**
```html
<!-- Input -->
<p>http://example.com/photo.jpg</p>

<!-- Output -->
<p><img src="http://example.com/photo.jpg" style="max-width:100%"/></p>
```

**PDF Document Embedding:**
```html
<!-- Input -->
<p>http://example.com/document.pdf</p>

<!-- Output -->
<p><iframe src="https://docs.google.com/viewer?url=http%3A//example.com/document.pdf&embedded=true" style="max-width:100%"></iframe></p>
```

**Email Address Conversion:**
```html
<!-- Input -->
<p>Contact us at support@example.com</p>

<!-- Output -->
<p>Contact us at <a href="mailto:support@example.com">support@example.com</a></p>
```

**Supported Document Types:**
- **Google Docs Viewer:** PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX, PAGES, AI, PSD, SVG, TTF, XPS
- **Direct Media:** PNG, GIF, JPG, JPEG, WAV, OGG, MP3, MOV, MP4, MPG, MPEG, WMV
- **oEmbed Services:** YouTube, Vimeo, Flickr, SlideShare, Hulu, WordPress.com

⚠️ **Important Notes**
- **BeautifulSoup Dependency:** Requires BeautifulSoup library installation for HTML processing
- **External Service Reliability:** Depends on external oEmbed services, may fail if services are down
- **Performance Impact:** External HTTP requests for oEmbed can slow down processing
- **Security Considerations:** Processes user-generated content, validate URLs before processing
- **Rate Limiting:** Some oEmbed services have rate limits, implement caching for production use
- **Content Security:** Embedded content may include scripts, consider CSP policies

**Common Troubleshooting:**
- BeautifulSoup not found → Install BeautifulSoup library (pip install beautifulsoup4)
- oEmbed service timeout → Implement timeout handling and fallback to regular links
- Malformed HTML → Validate HTML input before processing
- Missing media → Check URL accessibility and service availability
- Encoding issues → Ensure proper UTF-8 encoding for international content

🔗 **Related File Links**
- BeautifulSoup documentation for HTML parsing
- oEmbed specification and supported services
- Google Docs Viewer API documentation
- Web2py content management examples
- HTML sanitization and security best practices
- Performance optimization guides for content processing

📈 **Use Cases**
- **Content Management Systems:** Automatically embed media in blog posts and articles
- **Social Media Platforms:** Convert shared links to rich media previews
- **Forum Software:** Enhance user posts with embedded content
- **Email Processing:** Convert plain text emails to rich HTML with embedded media
- **Documentation Systems:** Embed documents and media in knowledge bases
- **News Aggregation:** Enhance news articles with embedded media content

🛠️ **Improvement Suggestions**
- **Async Processing:** Implement asynchronous oEmbed requests for better performance
- **Caching Layer:** Add persistent caching for oEmbed responses and media metadata
- **Service Management:** Implement fallback chains and service health monitoring
- **Security Enhancement:** Add URL validation and content sanitization
- **Mobile Optimization:** Add responsive embedding options for mobile devices
- **Analytics Integration:** Track embedded media engagement and performance
- **Custom Templates:** Allow custom embedding templates for different media types

🏷️ **Document Tags**
- Keywords: media embedding, oEmbed integration, URL detection, HTML processing, content enhancement, automatic linking, rich media, YouTube embedding, document viewer
- Technical tags: #media-embedding #oembed #html-processing #content-management #web2py-contrib #beautifulsoup
- Target roles: Frontend developers (intermediate), Content developers (basic), Full-stack developers (intermediate)
- Difficulty level: ⭐⭐⭐ - Requires understanding of HTML processing, HTTP requests, and media embedding
- Maintenance level: Medium - Requires updates for new oEmbed services and API changes
- Business criticality: Medium - Enhances user experience but not critical for core functionality
- Related topics: Content management, media embedding, HTML processing, oEmbed protocol, rich text editing