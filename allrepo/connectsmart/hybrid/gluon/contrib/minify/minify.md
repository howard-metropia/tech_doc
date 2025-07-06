# Web2py Asset Minification Pipeline

🔍 **Quick Summary (TL;DR)**
Comprehensive web asset optimization system that concatenates, minifies, and optionally inlines CSS/JavaScript files with intelligent path handling and caching for web2py applications.

**Core functionality keywords**: asset-pipeline | concatenation | minification | css-optimization | js-optimization | web2py | performance | caching

**Primary use cases**: Production asset optimization, build pipeline integration, web performance enhancement

**Quick compatibility info**: Python 2.7+/3.x, integrates with web2py response system, supports file hashing for cache busting

📝 **Detailed Code Analysis**
- **Main function**: `minify(files, path_info, folder, optimize_css, optimize_js, ignore_concat=[], ignore_minify=[])`
- **Optimization modes**: concat|minify|inline for both CSS and JavaScript
- **File handling**: Automatic path resolution, hash-based naming, temporary file management

🚀 **Usage Methods**
```python
from gluon.contrib.minify.minify import minify

files = ['/static/css/style.css', '/static/js/app.js']
optimized = minify(
    files=files,
    path_info='/myapp/static/temp',
    folder='/path/to/app',
    optimize_css='concat|minify',
    optimize_js='concat|minify|inline'
)
# Returns optimized file list with combined/minified assets
```

📊 **Output Examples**
- CSS concatenation: Multiple files → single compressed_[hash].css
- JS inlining: Multiple files → ('js:inline', 'minified_content')
- Path fixing: Relative URLs adjusted for new locations

🏷️ **Document Tags**
- **Keywords**: asset-pipeline, concatenation, minification, web2py, performance, optimization
- **Difficulty level**: ⭐⭐⭐⭐ (4/5)
- **Business criticality**: Critical (essential for production performance)