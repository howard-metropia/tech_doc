# Markmin to HTML Converter

🔍 **Quick Summary (TL;DR)**
Comprehensive text markup processor that converts Markmin syntax to HTML, supporting tables, lists, code blocks, images, links, math formulas, and extensible custom formatting with performance optimization.

**Core functionality keywords**: markmin | markup | html | converter | text-processing | markdown-alternative | wiki | documentation | formatting | renderer

**Primary use cases**: Documentation generation, wiki content processing, scientific paper publishing, web content creation

**Quick compatibility info**: Python 2.7+/3.x, 30% faster than markdown for large texts, supports MathJax integration

❓ **Common Questions Quick Index**
- Q: How is Markmin different from Markdown? A: Designed for scientific papers, supports tables/math better, 30% faster
- Q: Can it handle math formulas? A: Yes, supports LaTeX math with $$formula$$ syntax and Google Charts rendering
- Q: How do I create tables? A: Use ---- delimiters with | separators, supports headers/footers/classes
- Q: Can I extend the markup? A: Yes, via 'extra' parameter for custom code block processing
- Q: Does it support HTML5 elements? A: Yes, video/audio tags with [[message link video/audio]] syntax
- Q: How do I escape special characters? A: Use backslash \ before markup characters or \\\\
- Q: Can I control CSS classes? A: Yes, via class_prefix parameter and :class[id] syntax
- Q: What about performance? A: 10x faster for small texts (~10K), 30% faster for large texts (~100K)

📋 **Functionality Overview**
**Non-technical explanation**: Like a smart translator that converts simple text with special formatting marks (like **bold** or [[links]]) into beautiful web pages, similar to how a publishing system converts a manuscript into a formatted book.

**Technical explanation**: Feature-rich markup language processor that parses Markmin syntax and generates semantic HTML with support for advanced features like nested lists, complex tables, mathematical formulas, and multimedia content.

**Business value**: Enables rapid creation of high-quality documentation and scientific publications with consistent formatting, reducing publishing time and maintaining professional appearance.

**Context within larger system**: Core component of web2py's documentation system, enabling wiki functionality and automatic book generation from markup sources.

🔧 **Technical Specifications**
- **File information**: markmin2html.py, 1565 lines, Python module, high complexity with regex-heavy processing
- **Dependencies**: re, sys, urllib, ast modules; optional MathJax for formula rendering
- **Compatibility matrix**: Python 2.7+ (uses PY2 compatibility layer), Python 3.x with urllib.parse
- **Configuration parameters**: extra={}, allowed={}, sep='p', class_prefix='', id_prefix='markmin_'
- **System requirements**: Standard Python installation, optional pdflatex for PDF generation
- **Security requirements**: Safe evaluation for code blocks, HTML escaping for user content

📝 **Detailed Code Analysis**
- **Main function signatures**: 
  - `render(text, extra={}, allowed={}, sep='p', ...)` - Core rendering engine
  - `markmin2html(text, extra={}, ...)` - Simplified interface
  - `markmin_escape(text)` - Escape markup characters
- **Execution flow**: Text preprocessing → Code block extraction → Link processing → Structure parsing → HTML generation
- **Important code snippets**:
```python
# Custom code block processing
extra = {'python': lambda code: highlight_python(code)}
html = markmin2html('``print("hello")``:python', extra=extra)

# Table with class and ID
text = '''
----
Name|Age|City
====
John|25|NYC
----:users[user_table]
'''
```
- **Design patterns**: State machine for parsing, factory pattern for content processors, decorator pattern for extensions
- **Error handling**: Safe evaluation with AST parsing, graceful degradation for malformed syntax
- **Memory usage**: Efficient regex processing, temporary segments storage during parsing

🚀 **Usage Methods**
- **Basic usage**:
```python
from gluon.contrib.markmin.markmin2html import markmin2html
html = markmin2html("**Hello** ''world''")  # <p><strong>Hello</strong> <em>world</em></p>
```
- **Advanced configuration**:
```python
# Custom code highlighting
extra = {
    'python': lambda code: syntax_highlight(code, 'python'),
    'latex': lambda code: render_math(code)
}
html = markmin2html(text, extra=extra, class_prefix='docs_', pretty_print=True)
```
- **Table creation**:
```python
table_text = '''
---------
**Name**|**Score**
=========
Alice|95
Bob|87
---------:results[scores]
'''
```
- **Media embedding**:
```python
# Images with positioning
"[[Alt text [title] http://example.com/image.jpg center 200px]]"
# Video embedding  
"[[Video description http://example.com/video.mp4 video]]"
```

📊 **Output Examples**
- **Basic formatting**: 
  - Input: `**bold** ''italic''` 
  - Output: `<p><strong>bold</strong> <em>italic</em></p>`
- **Complex table**:
  - Input: Table with headers/footers
  - Output: Semantic HTML table with proper thead/tbody/tfoot structure
- **Math formulas**:
  - Input: `$$\int_a^b f(x)dx$$`
  - Output: `<img src="http://chart.apis.google.com/chart?cht=tx&chl=..." />`
- **Performance benchmarks**: ~100ms for 10K text, ~300ms for 100K text
- **Error handling**: Malformed links return `[[original text]]`, invalid code blocks show escaped content

⚠️ **Important Notes**
- **Security considerations**: Safe AST evaluation prevents code injection, HTML escaping prevents XSS attacks
- **Permission requirements**: File system access for image path processing
- **Common troubleshooting**: 
  - Links not working → Check [[text link]] format
  - Tables malformed → Verify ---- delimiters and | separators
  - Math not rendering → Check $$formula$$ syntax and MathJax setup
- **Performance gotchas**: Large nested lists can slow processing, use simple structures when possible
- **Breaking changes**: Syntax changes between versions may affect existing content
- **Rate limiting**: Consider caching for high-volume document processing

🔗 **Related File Links**
- **Project structure**: Part of gluon/contrib/markmin/ package
- **Related files**: 
  - markmin2latex.py (LaTeX output)
  - markmin2pdf.py (PDF generation)
  - Used by web2py wiki system
- **Configuration files**: No specific config files, uses runtime parameters
- **Test files**: Extensive doctests within module (run with `python markmin2html.py`)
- **API documentation**: Comprehensive docstring with examples and syntax reference

📈 **Use Cases**
- **Documentation systems**: Technical documentation, API docs, user manuals
- **Scientific publishing**: Academic papers, research reports with math formulas
- **Wiki systems**: Collaborative content creation, knowledge bases
- **Content management**: Blog posts, articles with rich formatting
- **E-learning platforms**: Course materials with multimedia content
- **Anti-patterns**: Avoid for simple text (overkill), complex nested structures (performance impact)

🛠️ **Improvement Suggestions**
- **Code optimization**: Cache compiled regex patterns, optimize nested list parsing for better performance
- **Feature expansion**: CommonMark compatibility mode, improved math rendering with MathJax 3.x
- **Technical debt**: Refactor large render() function into smaller components
- **Maintenance recommendations**: Update regex patterns for edge cases, improve error messages
- **Monitoring improvements**: Add processing time metrics, content complexity analysis
- **Documentation enhancements**: Interactive syntax playground, more real-world examples

🏷️ **Document Tags**
- **Keywords**: markmin, markup, html, converter, text-processing, documentation, wiki, markdown-alternative, scientific-publishing, web2py, formatting, renderer, tables, math, latex
- **Technical tags**: #markup #html #text-processing #documentation #wiki #python #regex #parsing
- **Target roles**: Technical writers, web developers, content creators, documentation specialists, scientific publishers
- **Difficulty level**: ⭐⭐⭐ (3/5 - requires understanding of markup syntax and HTML)
- **Maintenance level**: Medium (occasional syntax updates and performance improvements)
- **Business criticality**: High (core documentation infrastructure component)
- **Related topics**: Markup languages, document generation, content management, scientific publishing, web development