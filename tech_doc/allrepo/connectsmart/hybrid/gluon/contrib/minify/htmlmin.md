# HTML Minifier

🔍 **Quick Summary (TL;DR)**
Lightweight HTML minification tool that removes unnecessary whitespace while preserving content within pre, textarea tags and HTML comments to maintain functionality.

**Core functionality keywords**: html | minifier | whitespace-removal | pre-tag-preservation | textarea-preservation | comment-preservation

**Primary use cases**: HTML file size reduction, web performance optimization, template optimization

**Quick compatibility info**: Python 2.7+/3.x, regex-based processing, preserves critical whitespace

📝 **Detailed Code Analysis**
- **Main function**: `minify(response)` - Minifies HTML while preserving important content
- **Preservation logic**: Maintains whitespace in `<pre>`, `<textarea>`, and HTML comments
- **Processing method**: Single regex substitution with intelligent content detection

🚀 **Usage Methods**
```python
from gluon.contrib.minify.htmlmin import minify

html = '''
<html>
  <body>
    <pre>  preserved  </pre>
    <p>   minified   </p>
  </body>
</html>
'''
minified = minify(html)
# Whitespace in <pre> preserved, other whitespace reduced
```

🏷️ **Document Tags**
- **Keywords**: html, minifier, whitespace-removal, web-performance, template-optimization
- **Difficulty level**: ⭐⭐ (2/5)
- **Business criticality**: Medium (useful for performance)