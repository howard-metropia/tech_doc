# CSS Minifier - YUI Compressor Python Port

🔍 **Quick Summary (TL;DR)**
Python implementation of the YUI CSS compressor that removes comments, whitespace, and optimizes CSS syntax to reduce file size while maintaining functionality for web performance optimization.

**Core functionality keywords**: css | minifier | yui-compressor | optimization | compression | whitespace-removal | color-optimization | web-performance

**Primary use cases**: CSS file size reduction, web performance optimization, build pipeline integration, bandwidth savings

**Quick compatibility info**: Python 2.7+/3.x, processes standard CSS syntax, supports color and unit optimizations

📝 **Detailed Code Analysis**
- **Main functions**: `cssmin(css, wrap=None)` - Main minification function
- **Key optimizations**: Comment removal, whitespace compression, color hex shortening, zero unit condensing
- **Processing pipeline**: Comments → Whitespace → Semicolons → Colors → Units → Final cleanup

🚀 **Usage Methods**
```python
from gluon.contrib.minify.cssmin import cssmin

# Basic minification
minified = cssmin("body { color: #ffffff; margin: 0px; }")
# Result: "body{color:#fff;margin:0}"

# With line wrapping
minified = cssmin(css_content, wrap=80)  # Wrap at 80 characters
```

📊 **Output Examples**
- Input: `body { color: rgb(255,255,255); margin: 0px 0px 0px 0px; }`
- Output: `body{color:#fff;margin:0}`

🏷️ **Document Tags**
- **Keywords**: css, minifier, yui-compressor, optimization, compression, web-performance
- **Difficulty level**: ⭐⭐ (2/5)
- **Business criticality**: High (web performance essential)